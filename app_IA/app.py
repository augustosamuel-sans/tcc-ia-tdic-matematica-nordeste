from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Dict, List

import streamlit as st

from core import (
    checklist_validacao_manual_10_passos,
    discover_paths,
    load_base_rows,
    load_vinculos_rows,
    prepare_base,
    build_notebooklm_prompts,
    list_available_ufs,
    normalize_doc_id,
    read_csv_rows,
    save_outputs,
)


VALIDATED_STATUSES = {"VALIDADO", "AJUSTADO"}
STATUS_OPTIONS = ["PENDENTE", "VALIDADO", "AJUSTADO"]

RESP1_KEY = "resp_prompt_1_input"
RESP2_KEY = "resp_prompt_2_input"
RESP3_KEY = "resp_prompt_3_input"
REVISOR_KEY = "revisor_humano_input"
STATUS_KEY = "status_validacao_input"
OBS_KEY = "obs_validacao_input"
DOC_TOKEN_KEY = "active_doc_token"
CLEAR_FORM_NEXT_RUN_KEY = "clear_form_next_run"


def clear_form_inputs() -> None:
    st.session_state[RESP1_KEY] = ""
    st.session_state[RESP2_KEY] = ""
    st.session_state[RESP3_KEY] = ""
    st.session_state[REVISOR_KEY] = ""
    st.session_state[STATUS_KEY] = "PENDENTE"
    st.session_state[OBS_KEY] = ""


def request_clear_form_on_next_run() -> None:
    st.session_state[CLEAR_FORM_NEXT_RUN_KEY] = True


def apply_pending_form_clear() -> None:
    if st.session_state.pop(CLEAR_FORM_NEXT_RUN_KEY, False):
        clear_form_inputs()


def row_analysis_key(row: Dict[str, str]) -> str:
    uf = (row.get("UF", "") or "").upper().strip()
    doc_id = normalize_doc_id(row.get("DOC_ID", ""))
    filename = (row.get("NOME_ARQUIVO_LOCAL", "") or "").strip().lower()
    return f"{uf}|{doc_id}|{filename}"


def row_ui_token(row: Dict[str, str]) -> str:
    key = row_analysis_key(row)
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def build_status_map(paths, uf: str) -> Dict[str, str]:
    rows = read_csv_rows(paths.respostas_consolidadas_csv)
    output: Dict[str, str] = {}

    for row in rows:
        if row.get("UF", "").upper() != uf.upper():
            continue

        doc_id = normalize_doc_id(row.get("DOC_ID", ""))
        filename = (row.get("NOME_ARQUIVO_LOCAL", "") or "").strip()
        if not doc_id or not filename:
            continue

        output[row_analysis_key(row)] = (row.get("STATUS_VALIDACAO_HUMANA", "") or "PENDENTE").upper()

    return output


def first_pending_index(rows_uf_sorted: List[Dict[str, str]], status_map: Dict[str, str]) -> int:
    for index, row in enumerate(rows_uf_sorted):
        if status_map.get(row_analysis_key(row), "PENDENTE") not in VALIDATED_STATUSES:
            return index
    return 0


def validated_count(rows_uf_sorted: List[Dict[str, str]], status_map: Dict[str, str]) -> int:
    count = 0
    for row in rows_uf_sorted:
        if status_map.get(row_analysis_key(row), "PENDENTE") in VALIDATED_STATUSES:
            count += 1
    return count


st.set_page_config(
    page_title="Automacao NotebookLM - Analise Qualitativa",
    layout="wide",
)

app_root = Path(__file__).resolve().parent
paths = discover_paths(app_root)

# Ensure output roots exist to avoid runtime write errors.
paths.texto_root.mkdir(parents=True, exist_ok=True)
paths.resposta_root.mkdir(parents=True, exist_ok=True)
paths.validacao_root.mkdir(parents=True, exist_ok=True)

# Streamlit does not allow changing widget-backed session keys after widget instantiation.
# Apply pending clears early in the script, before response widgets are created.
apply_pending_form_clear()

st.title("Automacao NotebookLM para Codificacao Qualitativa")
st.caption(
    "Fluxo: preparar base PDF x campus, gerar prompts, colar respostas do NotebookLM e salvar MD + CSV + validacao manual."
)

with st.expander("1) Preparar base (recomendado antes de codificar)", expanded=True):
    ufs_disponiveis = list_available_ufs(paths.pdf_root)
    default_ufs = ["AL"] if "AL" in ufs_disponiveis else (ufs_disponiveis[:1] if ufs_disponiveis else [])

    ufs_base = st.multiselect(
        "UFs para preparar/atualizar base",
        options=ufs_disponiveis,
        default=default_ufs,
        help="A base une PDFs baixados com o mapeamento de campus/polos por UF.",
    )

    if st.button("Preparar/Atualizar base agora", type="primary"):
        if not ufs_base:
            st.warning("Selecione ao menos uma UF.")
        else:
            try:
                resultado_base = prepare_base(paths, ufs_base)
                st.success(
                    f"Base atualizada. Documentos: {resultado_base['base_total']} | Vinculos: {resultado_base['vinculos_total']}"
                )
                st.dataframe(resultado_base["resumo_ufs"], use_container_width=True)
            except Exception as exc:
                st.error(f"Falha ao preparar base: {exc}")

base_rows = load_base_rows(paths)
if not base_rows:
    st.info("A base ainda esta vazia. Clique em 'Preparar/Atualizar base agora'.")
    st.stop()

ufs_na_base = sorted({row.get("UF", "") for row in base_rows if row.get("UF", "")})

col_a, col_b = st.columns(2)
default_uf_index = ufs_na_base.index("AL") if "AL" in ufs_na_base else 0

with col_a:
    uf_selecionada = st.selectbox("2) UF do documento", options=ufs_na_base, index=default_uf_index)
    lote_mode = st.toggle(
        "Modo lote sequencial (validacao obrigatoria para avancar)",
        value=True,
        help="No lote, o botao Proximo so funciona quando o documento atual esta VALIDADO ou AJUSTADO.",
    )

status_map = build_status_map(paths, uf_selecionada)

rows_uf = [row for row in base_rows if row.get("UF", "") == uf_selecionada]
rows_uf_sorted = sorted(rows_uf, key=lambda item: (item.get("DOC_ID", ""), item.get("NOME_ARQUIVO_LOCAL", "")))

if not rows_uf_sorted:
    st.warning("Nao ha documentos para a UF selecionada.")
    st.stop()

labels = [f"{row.get('DOC_ID', '')} | {row.get('NOME_ARQUIVO_LOCAL', '')}" for row in rows_uf_sorted]
label_to_row = {label: row for label, row in zip(labels, rows_uf_sorted)}

idx_key = f"lote_idx_{uf_selecionada}"
if idx_key not in st.session_state:
    st.session_state[idx_key] = first_pending_index(rows_uf_sorted, status_map)

st.session_state[idx_key] = max(0, min(st.session_state[idx_key], len(labels) - 1))
current_idx = st.session_state[idx_key]

if lote_mode:
    doc_label = labels[current_idx]
    with col_b:
        st.selectbox(
            "3) Documento (automatico no lote)",
            options=labels,
            index=current_idx,
            disabled=True,
        )
    selected_idx = current_idx
else:
    with col_b:
        doc_label = st.selectbox("3) Documento", options=labels)
    selected_idx = labels.index(doc_label)
    st.session_state[idx_key] = selected_idx

doc_row = label_to_row[doc_label]
doc_id = normalize_doc_id(doc_row.get("DOC_ID", ""))
doc_key = row_analysis_key(doc_row)
doc_ui_token = row_ui_token(doc_row)
vinculos = load_vinculos_rows(
    paths,
    uf=uf_selecionada,
    doc_id=doc_id,
    pdf_filename=doc_row.get("NOME_ARQUIVO_LOCAL", ""),
)

total_docs = len(rows_uf_sorted)
done_docs = validated_count(rows_uf_sorted, status_map)
progress_ratio = done_docs / total_docs if total_docs else 0

progress_col_1, progress_col_2, progress_col_3 = st.columns(3)
with progress_col_1:
    st.metric("Documentos validados/ajustados", f"{done_docs}/{total_docs}")
with progress_col_2:
    st.metric("Percentual concluido", f"{progress_ratio * 100:.0f}%")
with progress_col_3:
    st.metric("Documento atual", f"{selected_idx + 1}/{total_docs}")

st.progress(progress_ratio)

doc_status_atual = status_map.get(doc_key, "SEM_REGISTRO")
st.info(
    f"Status atual no consolidado para {doc_id} | {doc_row.get('NOME_ARQUIVO_LOCAL', '')}: {doc_status_atual}"
)

if lote_mode:
    st.subheader("Navegacao de lote")
    nav_col_1, nav_col_2, nav_col_3 = st.columns(3)

    with nav_col_1:
        if st.button("Anterior", use_container_width=True):
            if selected_idx > 0:
                st.session_state[idx_key] = selected_idx - 1
                request_clear_form_on_next_run()
                st.rerun()

    with nav_col_2:
        if st.button("Proximo (requer validado/ajustado)", use_container_width=True):
            if doc_status_atual not in VALIDATED_STATUSES:
                st.warning(
                    "Para avancar, salve este documento com status VALIDADO ou AJUSTADO."
                )
            elif selected_idx >= len(rows_uf_sorted) - 1:
                st.info("Voce ja esta no ultimo documento do lote.")
            else:
                st.session_state[idx_key] = selected_idx + 1
                request_clear_form_on_next_run()
                st.rerun()

    with nav_col_3:
        if st.button("Ir para primeiro pendente", use_container_width=True):
            st.session_state[idx_key] = first_pending_index(rows_uf_sorted, status_map)
            request_clear_form_on_next_run()
            st.rerun()

st.subheader("Metadados do documento")
st.dataframe([doc_row], use_container_width=True)

st.subheader("Vinculos de campus/polo para comparacao")
if vinculos:
    st.dataframe(vinculos, use_container_width=True)

    inconsistencias_ies = [row for row in vinculos if row.get("CONSISTENCIA_IES_0_1", "") == "0"]
    if inconsistencias_ies:
        st.warning(
            "Foram encontrados vinculos com baixa consistencia de IES. Revise com cuidado antes da decisao final."
        )
else:
    st.warning("Nenhum vinculo encontrado no banco para este PDF. O app ainda vai salvar, mas marque para revisao.")

prompts = build_notebooklm_prompts(doc_row, vinculos)

st.subheader("Prompts prontos para copiar no NotebookLM")
prompt_col_1, prompt_col_2, prompt_col_3 = st.columns(3)
with prompt_col_1:
    st.text_area("Prompt 1", prompts["prompt_1"], height=430, key=f"prompt1_{doc_ui_token}")
with prompt_col_2:
    st.text_area("Prompt 2", prompts["prompt_2"], height=430, key=f"prompt2_{doc_ui_token}")
with prompt_col_3:
    st.text_area("Prompt 3", prompts["prompt_3"], height=430, key=f"prompt3_{doc_ui_token}")

doc_token = doc_key
if st.session_state.get(DOC_TOKEN_KEY) != doc_token:
    clear_form_inputs()
    st.session_state[DOC_TOKEN_KEY] = doc_token

st.subheader("Colar respostas do NotebookLM")
resposta_prompt_1 = st.text_area(
    "Resposta Prompt 1 (Resumo + Evidencias + Comparacao base)",
    height=260,
    key=RESP1_KEY,
)
resposta_prompt_2 = st.text_area(
    "Resposta Prompt 2 (CSV: cabecalho + 1 linha)",
    height=200,
    key=RESP2_KEY,
)
resposta_prompt_3 = st.text_area(
    "Resposta Prompt 3 (Auditoria critica)",
    height=260,
    key=RESP3_KEY,
)

meta_col_1, meta_col_2 = st.columns(2)
with meta_col_1:
    revisor_humano = st.text_input("Revisor humano", key=REVISOR_KEY)
with meta_col_2:
    status_validacao = st.selectbox(
        "Status validacao humana",
        options=STATUS_OPTIONS,
        key=STATUS_KEY,
    )

obs_validacao = st.text_area("Observacoes da validacao humana", height=100, key=OBS_KEY)

save_col_1, save_col_2 = st.columns(2)
salvar_clicked = save_col_1.button("Salvar respostas e atualizar arquivos", type="primary", use_container_width=True)
salvar_avancar_clicked = False

if lote_mode:
    salvar_avancar_clicked = save_col_2.button(
        "Salvar e avancar no lote",
        use_container_width=True,
    )

if salvar_clicked or salvar_avancar_clicked:
    try:
        resultado_save = save_outputs(
            paths=paths,
            doc_row=doc_row,
            vinculos_rows=vinculos,
            resposta_prompt_1=resposta_prompt_1,
            resposta_prompt_2=resposta_prompt_2,
            resposta_prompt_3=resposta_prompt_3,
            revisor_humano=revisor_humano,
            status_validacao_humana=status_validacao,
            obs_validacao_humana=obs_validacao,
        )
        st.success("Arquivos atualizados com sucesso.")

        st.write("Texto qualitativo:", str(resultado_save["texto_path"]))
        st.write("Validacao manual:", str(resultado_save["validacao_path"]))
        st.write("CSV por UF:", str(resultado_save["resposta_uf_csv"]))
        st.write("CSV consolidado:", str(resultado_save["resposta_consolidada_csv"]))
        st.write("Controle de validacao:", str(resultado_save["validacao_controle_csv"]))

        st.subheader("Linha parseada da matriz")
        st.dataframe([resultado_save["parsed_matrix"]], use_container_width=True)

        status_salvo = (status_validacao or "PENDENTE").upper()
        status_map[doc_key] = status_salvo

        if salvar_avancar_clicked:
            if status_salvo not in VALIDATED_STATUSES:
                st.warning(
                    "Documento salvo, mas nao foi possivel avancar: use status VALIDADO ou AJUSTADO."
                )
            elif selected_idx >= len(rows_uf_sorted) - 1:
                st.info("Documento salvo. Voce concluiu o ultimo item do lote.")
            else:
                st.session_state[idx_key] = selected_idx + 1
                request_clear_form_on_next_run()
                st.rerun()
    except Exception as exc:
        st.error(f"Falha ao salvar: {exc}")

with st.expander("Checklist de validacao manual (10 passos)", expanded=False):
    for idx, item in enumerate(checklist_validacao_manual_10_passos(), start=1):
        st.markdown(f"{idx}. {item}")

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

ROOT_DEFAULT = Path(r"C:\Users\augus\Music\TCC\Data\new_date")
CSV_REL = Path("output_csv") / "mapeamento_ppc_polos.csv"
PDF_ROOT_REL = Path("pdfs_baixados")
LOG_REL = Path("output_csv") / "logs" / "app_triagem_modificacoes.csv"

SKIP_STATUSES = {"OK_PDF", "OK_PDF_MANUAL", "NAO_ENCONTRADO"}
TARGET_STATUSES = {"HTML_INTERMEDIARIO", "404", "BLOQUEADO", ""}

DOC_ID_RE = re.compile(r"DOC\s*0*(\d{1,6})", re.IGNORECASE)


@dataclass
class AppPaths:
    root: Path
    csv_path: Path
    pdf_root: Path
    log_path: Path


def remove_accents(text: str) -> str:
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def sanitize(text: str, max_len: int = 64) -> str:
    text = remove_accents((text or "").strip())
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    if not text:
        return "NA"
    return text[:max_len]


def clean(value: str) -> str:
    return str(value or "").strip()


def clean_url(url: str) -> str:
    value = str(url or "").strip().strip('"').strip("'")
    value = re.sub(r"\s*\[(web|page):\d+\]\s*$", "", value, flags=re.IGNORECASE)
    if value.upper() in {"", "NAO_ENCONTRADO", "SEM_LINK", "N/A", "NONE"}:
        return ""
    if not value.lower().startswith(("http://", "https://")):
        return ""
    if "..." in value:
        return ""
    return value


def pick_best_source_url(row: pd.Series) -> str:
    for col in ["URL_DOWNLOAD_PDF", "URL_FONTE"]:
        url = clean_url(row.get(col, ""))
        if url:
            return url
    return ""


def normalize_doc_id(value: str) -> str:
    text = str(value or "").strip().upper()
    match = DOC_ID_RE.search(text)
    if not match:
        return ""
    number = int(match.group(1))
    width = max(4, len(match.group(1)))
    return f"DOC{number:0{width}d}"


def extract_doc_id_from_text(value: str) -> str:
    return normalize_doc_id(value)


def discover_paths() -> AppPaths:
    root = ROOT_DEFAULT
    csv_path = root / CSV_REL
    pdf_root = root / PDF_ROOT_REL
    log_path = root / LOG_REL
    return AppPaths(root=root, csv_path=csv_path, pdf_root=pdf_root, log_path=log_path)


def load_mapping(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV nao encontrado: {csv_path}")
    df = pd.read_csv(csv_path, dtype=str, encoding="utf-8-sig").fillna("")
    for col in [
        "STATUS_LINK",
        "URL_FONTE",
        "URL_DOWNLOAD_PDF",
        "URL_DOWNLOAD_PDF_LIMPA",
        "CAMINHO_ARQUIVO_LOCAL",
        "NOME_ARQUIVO_LOCAL",
        "UF",
        "INSTITUICAO",
        "MODALIDADE",
        "NOME_POLO_OU_CAMPUS",
        "MUNICIPIO_POLO",
        "CURSO",
        "DOC_ID",
        "ACAO_RECOMENDADA",
        "LOCALIDADE_DOCUMENTO",
        "HASH_OU_ID_PDF_CANONICO",
        "PPC_COMPARTILHADO",
        "ANO_PPC",
    ]:
        if col not in df.columns:
            df[col] = ""
    return df


def row_needs_manual_download(row: pd.Series) -> bool:
    status = (row.get("STATUS_LINK", "") or "").strip().upper()
    path = (row.get("CAMINHO_ARQUIVO_LOCAL", "") or "").strip()

    if status in SKIP_STATUSES:
        return False

    if path and Path(path).exists():
        return False

    # Keep only statuses that still have realistic chance of manual recovery.
    return status in TARGET_STATUSES


def has_valid_download_source(row: pd.Series) -> bool:
    if pick_best_source_url(row):
        return True
    raw_path = str(row.get("CAMINHO_ARQUIVO_LOCAL", "") or "").strip()
    return bool(raw_path and raw_path.lower().startswith(("c:\\", "d:\\")))


def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_of_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def build_localidade(row: pd.Series) -> str:
    modalidade = (row.get("MODALIDADE", "") or "").lower()
    polo = sanitize(row.get("NOME_POLO_OU_CAMPUS", ""))
    municipio = sanitize(row.get("MUNICIPIO_POLO", ""))
    if "dist" in modalidade:
        return f"POLO__{polo}__{municipio}"
    return f"POLO__{polo}__{municipio}"


def next_doc_id_for_uf(df: pd.DataFrame, uf: str) -> str:
    max_id = 0

    uf_rows = df[df["UF"].str.upper() == uf.upper()]
    for _, row in uf_rows.iterrows():
        values = [row.get("DOC_ID", ""), row.get("NOME_ARQUIVO_LOCAL", ""), row.get("CAMINHO_ARQUIVO_LOCAL", "")]
        for value in values:
            doc_id = extract_doc_id_from_text(str(value))
            if doc_id:
                max_id = max(max_id, int(doc_id.replace("DOC", "")))
    return f"DOC{max_id + 1:04d}"


def guess_file_name(row: pd.Series, doc_id: str) -> str:
    uf = sanitize(row.get("UF", ""), 8)
    inst = sanitize(row.get("INSTITUICAO", ""))
    modalidade = (row.get("MODALIDADE", "") or "").lower()
    tipo = "EAD" if "dist" in modalidade else "PRESENCIAL"
    localidade = build_localidade(row)
    ano = sanitize(row.get("ANO_PPC", "") or "MANUAL", 40)
    return f"{uf}__{inst}__{tipo}__{localidade}__{ano}__{doc_id}.pdf"


def enforce_doc_id_in_filename(file_name: str, doc_id: str) -> str:
    if not file_name:
        return f"{doc_id}.pdf"

    p = Path(file_name)
    suffix = p.suffix if p.suffix else ".pdf"
    stem = p.stem

    current = extract_doc_id_from_text(file_name)
    if current and current != doc_id:
        stem = re.sub(r"DOC\s*0*\d{1,6}", doc_id, stem, flags=re.IGNORECASE)
    elif not current:
        stem = f"{stem}__{doc_id}"

    return f"{stem}{suffix}"


def existing_pdf_by_hash(pdf_root: Path, target_hash: str) -> Optional[Path]:
    if not pdf_root.exists():
        return None
    for pdf in pdf_root.rglob("*.pdf"):
        try:
            file_hash = hashlib.sha256(pdf.read_bytes()).hexdigest().upper()
            if file_hash == target_hash:
                return pdf
        except Exception:
            continue
    return None


def save_mapping(df: pd.DataFrame, csv_path: Path, expected_rows: int) -> None:
    if len(df) != expected_rows:
        raise RuntimeError(
            f"Bloqueado: o app nao pode inserir/remover linhas. Esperado={expected_rows}, atual={len(df)}."
        )
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")


def append_audit_log(paths: AppPaths, payload: dict) -> None:
    log_path = paths.log_path
    log_path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "TS": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ACAO": "",
        "IDX_MAIN": "",
        "UF": "",
        "INSTITUICAO": "",
        "NOME_POLO_OU_CAMPUS": "",
        "MUNICIPIO_POLO": "",
        "CURSO": "",
        "STATUS_ANTES": "",
        "STATUS_DEPOIS": "",
        "DOC_ID": "",
        "HASH": "",
        "NOME_ARQUIVO_LOCAL": "",
        "CAMINHO_ARQUIVO_LOCAL": "",
        "FONTE_UTIL": "",
        "LINHAS_ATUALIZADAS": "",
        "LINHAS_RELACIONADAS": "",
        "OBS": "",
    }
    for k, v in payload.items():
        record[k] = "" if v is None else str(v)

    out_df = pd.DataFrame([record], columns=list(record.keys()))
    out_df.to_csv(
        log_path,
        mode="a",
        header=not log_path.exists(),
        index=False,
        encoding="utf-8-sig",
    )


def update_row_as_ok(df: pd.DataFrame, idx: int, row: pd.Series, path: Path, file_hash: str, status: str = "OK_PDF_MANUAL") -> None:
    df.at[idx, "STATUS_LINK"] = status
    df.at[idx, "URL_DOWNLOAD_PDF_LIMPA"] = clean_url(row.get("URL_DOWNLOAD_PDF", ""))
    df.at[idx, "NOME_ARQUIVO_LOCAL"] = path.name
    df.at[idx, "CAMINHO_ARQUIVO_LOCAL"] = str(path)
    df.at[idx, "HASH_OU_ID_PDF_CANONICO"] = file_hash
    df.at[idx, "LOCALIDADE_DOCUMENTO"] = build_localidade(row)
    if (df.at[idx, "ACAO_RECOMENDADA"] or "").strip().upper() in {"", "NOVA_BUSCA", "VALIDACAO_MANUAL"}:
        df.at[idx, "ACAO_RECOMENDADA"] = "OK"


def update_row_as_failed(df: pd.DataFrame, idx: int) -> None:
    df.at[idx, "STATUS_LINK"] = "NAO_ENCONTRADO"
    if (df.at[idx, "ACAO_RECOMENDADA"] or "").strip().upper() in {"", "NOVA_BUSCA", "VALIDACAO_MANUAL"}:
        df.at[idx, "ACAO_RECOMENDADA"] = "VALIDACAO_MANUAL"


def canonical_info_for_doc_id(df: pd.DataFrame, uf: str, doc_id: str) -> tuple[set[str], str, Optional[Path]]:
    if not doc_id:
        return set(), "", None

    mask = (
        df["UF"].fillna("").str.strip().str.upper().eq(uf.upper())
        & df["DOC_ID"].fillna("").apply(normalize_doc_id).eq(doc_id)
    )
    subset = df[mask]

    hashes = set(
        h.strip().upper()
        for h in subset["HASH_OU_ID_PDF_CANONICO"].astype(str).tolist()
        if h.strip()
    )

    canonical_name = ""
    for name in subset["NOME_ARQUIVO_LOCAL"].astype(str).tolist():
        if name.strip():
            canonical_name = name.strip()
            break

    canonical_path = None
    first_non_empty = None
    for path_text in subset["CAMINHO_ARQUIVO_LOCAL"].astype(str).tolist():
        if not path_text.strip():
            continue
        candidate = Path(path_text.strip())
        if first_non_empty is None:
            first_non_empty = candidate
        if candidate.exists():
            canonical_path = candidate
            break
    if canonical_path is None:
        canonical_path = first_non_empty

    return hashes, canonical_name, canonical_path


def build_source_series(df: pd.DataFrame) -> pd.Series:
    return df.apply(pick_best_source_url, axis=1)


def assign_doc_id_to_related_rows(
    df: pd.DataFrame,
    idx_selected: int,
    row: pd.Series,
    doc_id: str,
    source_url: str,
    force_selected_only: bool = False,
) -> int:
    changed = set()

    df.at[idx_selected, "DOC_ID"] = doc_id
    changed.add(idx_selected)

    if force_selected_only:
        return len(changed)

    shared = str(row.get("PPC_COMPARTILHADO", "") or "").strip().upper() == "SIM"
    if not shared:
        return len(changed)

    uf = str(row.get("UF", "") or "").strip().upper()
    inst = str(row.get("INSTITUICAO", "") or "").strip().upper()
    modalidade = str(row.get("MODALIDADE", "") or "").strip().upper()
    curso = str(row.get("CURSO", "") or "").strip().upper()

    mask = (
        df["UF"].fillna("").str.strip().str.upper().eq(uf)
        & df["INSTITUICAO"].fillna("").str.strip().str.upper().eq(inst)
        & df["MODALIDADE"].fillna("").str.strip().str.upper().eq(modalidade)
        & df["CURSO"].fillna("").str.strip().str.upper().eq(curso)
    )

    if source_url:
        source_series = build_source_series(df)
        mask = mask & source_series.eq(source_url)

    missing_doc = df["DOC_ID"].fillna("").str.strip().eq("")
    for idx in df[mask & missing_doc].index.tolist():
        df.at[idx, "DOC_ID"] = doc_id
        changed.add(idx)

    return len(changed)


def update_rows_for_doc_id(df: pd.DataFrame, uf: str, doc_id: str, path: Path, file_hash: str) -> int:
    mask = (
        df["UF"].fillna("").str.strip().str.upper().eq(uf.upper())
        & df["DOC_ID"].fillna("").apply(normalize_doc_id).eq(doc_id)
    )
    targets = df[mask].index.tolist()

    updated = 0
    for idx in targets:
        row = df.loc[idx].copy()
        status_atual = str(df.at[idx, "STATUS_LINK"] or "").strip().upper()
        new_status = "OK_PDF" if status_atual == "OK_PDF" else "OK_PDF_MANUAL"
        update_row_as_ok(df, idx, row, path, file_hash, status=new_status)
        updated += 1
    return updated


def join_preview(values: list[str], limit: int = 4) -> str:
    cleaned = [v for v in values if v]
    if not cleaned:
        return ""
    if len(cleaned) <= limit:
        return " | ".join(cleaned)
    return " | ".join(cleaned[:limit]) + f" | ... (+{len(cleaned) - limit})"


def build_audit_tables(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    tmp = df.fillna("").copy()
    tmp["HASH_NORM"] = tmp["HASH_OU_ID_PDF_CANONICO"].astype(str).str.strip().str.upper()
    tmp["DOC_NORM"] = tmp["DOC_ID"].astype(str).apply(normalize_doc_id)
    tmp["NAME_NORM"] = tmp["NOME_ARQUIVO_LOCAL"].astype(str).str.strip()

    hash_name_rows = tmp[(tmp["HASH_NORM"] != "") & (tmp["NAME_NORM"] != "")]
    hash_name = (
        hash_name_rows.groupby("HASH_NORM")["NAME_NORM"]
        .agg(lambda s: sorted(set(s)))
        .reset_index()
    )
    hash_name["QTD_NOMES"] = hash_name["NAME_NORM"].apply(len)
    hash_name = hash_name[hash_name["QTD_NOMES"] > 1].copy()
    if not hash_name.empty:
        hash_name["NOMES"] = hash_name["NAME_NORM"].apply(join_preview)
        hash_name = hash_name.rename(columns={"HASH_NORM": "HASH"})[["HASH", "QTD_NOMES", "NOMES"]]
    else:
        hash_name = pd.DataFrame(columns=["HASH", "QTD_NOMES", "NOMES"])

    doc_hash_rows = tmp[(tmp["DOC_NORM"] != "") & (tmp["HASH_NORM"] != "")]
    doc_hash = (
        doc_hash_rows.groupby(["UF", "DOC_NORM"])["HASH_NORM"]
        .agg(lambda s: sorted(set(s)))
        .reset_index()
    )
    doc_hash["QTD_HASHES"] = doc_hash["HASH_NORM"].apply(len)
    doc_hash = doc_hash[doc_hash["QTD_HASHES"] > 1].copy()
    if not doc_hash.empty:
        doc_hash["HASHES"] = doc_hash["HASH_NORM"].apply(lambda values: join_preview(values, limit=3))
        doc_hash = doc_hash.rename(columns={"DOC_NORM": "DOC_ID"})[["UF", "DOC_ID", "QTD_HASHES", "HASHES"]]
    else:
        doc_hash = pd.DataFrame(columns=["UF", "DOC_ID", "QTD_HASHES", "HASHES"])

    hash_doc_rows = tmp[(tmp["HASH_NORM"] != "") & (tmp["DOC_NORM"] != "")]
    hash_doc = (
        hash_doc_rows.groupby("HASH_NORM")["DOC_NORM"]
        .agg(lambda s: sorted(set(s)))
        .reset_index()
    )
    hash_doc["QTD_DOC_IDS"] = hash_doc["DOC_NORM"].apply(len)
    hash_doc = hash_doc[hash_doc["QTD_DOC_IDS"] > 1].copy()
    if not hash_doc.empty:
        hash_doc["DOC_IDS"] = hash_doc["DOC_NORM"].apply(join_preview)
        hash_doc = hash_doc.rename(columns={"HASH_NORM": "HASH"})[["HASH", "QTD_DOC_IDS", "DOC_IDS"]]
    else:
        hash_doc = pd.DataFrame(columns=["HASH", "QTD_DOC_IDS", "DOC_IDS"])

    return hash_name, doc_hash, hash_doc


def schedule_next_item(idx_selected: int, current_pos: int) -> None:
    st.session_state["processed_idx"] = idx_selected
    st.session_state["processed_pos"] = current_pos
    st.session_state["uploader_nonce"] = st.session_state.get("uploader_nonce", 0) + 1


st.set_page_config(page_title="Triagem de Download Manual PPC", layout="wide")
st.title("Triagem de Download Manual de PPCs")
st.caption("Fluxo: abrir fonte, baixar manualmente, arrastar PDF, salvar sem criar linhas novas no CSV")

paths = discover_paths()

try:
    df = load_mapping(paths.csv_path)
except Exception as exc:
    st.error(str(exc))
    st.stop()

expected_rows = len(df)

if "cursor_pos" not in st.session_state:
    st.session_state["cursor_pos"] = 0
if "uploader_nonce" not in st.session_state:
    st.session_state["uploader_nonce"] = 0

c1, c2, c3 = st.columns(3)
with c1:
    uf_options = sorted([u for u in df["UF"].dropna().unique().tolist() if u])
    uf_sel = st.selectbox("UF", options=["TODAS"] + uf_options, index=0)
with c2:
    only_downloadable = st.toggle("Somente com fonte para tentar baixar (URL_DOWNLOAD_PDF ou URL_FONTE)", value=False)
with c3:
    only_pending = st.toggle("Somente pendentes de triagem manual", value=True)

work = df.copy()
if uf_sel != "TODAS":
    work = work[work["UF"].str.upper() == uf_sel.upper()]

if only_pending:
    work = work[work.apply(row_needs_manual_download, axis=1)]

if only_downloadable:
    work = work[work.apply(has_valid_download_source, axis=1)]

work = work.copy()
work["FONTE_UTIL"] = work.apply(pick_best_source_url, axis=1)
work["ROW_LABEL"] = (
    work["UF"]
    + " | "
    + work["INSTITUICAO"]
    + " | "
    + work["MODALIDADE"]
    + " | "
    + work["NOME_POLO_OU_CAMPUS"]
    + " | "
    + work["MUNICIPIO_POLO"]
    + " | status="
    + work["STATUS_LINK"]
)

st.subheader("Resumo")
r1, r2, r3 = st.columns(3)
r1.metric("Linhas no CSV (base fixa)", len(df))
r2.metric("Pendentes no filtro", len(work))
existing_pdfs = len(list(paths.pdf_root.rglob("*.pdf"))) if paths.pdf_root.exists() else 0
r3.metric("PDFs atualmente no acervo", existing_pdfs)

with st.expander("Auditoria de consistencia (DOC_ID, hash e nomes)"):
    hash_name_df, doc_hash_df, hash_doc_df = build_audit_tables(df)

    a1, a2, a3 = st.columns(3)
    a1.metric("Mesmo hash com nomes diferentes", len(hash_name_df))
    a2.metric("Mesmo DOC_ID com hashes diferentes", len(doc_hash_df))
    a3.metric("Mesmo hash ligado a DOC_IDs diferentes", len(hash_doc_df))

    if not hash_name_df.empty:
        st.markdown("Hashes iguais com nomes diferentes")
        st.dataframe(hash_name_df, width="stretch", height=180)
    if not doc_hash_df.empty:
        st.markdown("DOC_IDs com conflito de hash")
        st.dataframe(doc_hash_df, width="stretch", height=180)
    if not hash_doc_df.empty:
        st.markdown("Hash reaproveitado em mais de um DOC_ID")
        st.dataframe(hash_doc_df, width="stretch", height=180)
    if hash_name_df.empty and doc_hash_df.empty and hash_doc_df.empty:
        st.info("Sem conflitos detectados nos campos de hash/DOC_ID/nome.")

if work.empty:
    st.info("Sem itens pendentes para o filtro atual.")
    st.stop()

show_cols = [
    "UF",
    "INSTITUICAO",
    "MODALIDADE",
    "NOME_POLO_OU_CAMPUS",
    "MUNICIPIO_POLO",
    "CURSO",
    "STATUS_LINK",
    "URL_DOWNLOAD_PDF",
    "URL_FONTE",
    "DOC_ID",
    "NOME_ARQUIVO_LOCAL",
]
st.dataframe(work[show_cols], width="stretch", height=280)

idx_options = work.index.tolist()
processed_idx = st.session_state.pop("processed_idx", None)
processed_pos = st.session_state.pop("processed_pos", None)

if processed_pos is not None:
    if processed_idx in idx_options:
        st.session_state["cursor_pos"] = min(processed_pos + 1, len(idx_options) - 1)
    else:
        st.session_state["cursor_pos"] = min(processed_pos, len(idx_options) - 1)

st.session_state["cursor_pos"] = max(0, min(st.session_state["cursor_pos"], len(idx_options) - 1))

idx_selected = st.selectbox(
    "Selecione a linha para processar",
    options=idx_options,
    index=st.session_state["cursor_pos"],
    format_func=lambda i: work.at[i, "ROW_LABEL"],
)
current_pos = idx_options.index(idx_selected)
st.session_state["cursor_pos"] = current_pos

row = df.loc[idx_selected].copy()
source_url = pick_best_source_url(row)
st.markdown("### Item selecionado")
left, right = st.columns(2)
with left:
    st.write({
        "UF": row.get("UF", ""),
        "INSTITUICAO": row.get("INSTITUICAO", ""),
        "MODALIDADE": row.get("MODALIDADE", ""),
        "NOME_POLO_OU_CAMPUS": row.get("NOME_POLO_OU_CAMPUS", ""),
        "MUNICIPIO_POLO": row.get("MUNICIPIO_POLO", ""),
        "CURSO": row.get("CURSO", ""),
        "STATUS_LINK": row.get("STATUS_LINK", ""),
        "DOC_ID": normalize_doc_id(row.get("DOC_ID", "")),
        "PPC_COMPARTILHADO": row.get("PPC_COMPARTILHADO", ""),
    })
with right:
    raw_download = (row.get("URL_DOWNLOAD_PDF", "") or "").strip()
    raw_source = (row.get("URL_FONTE", "") or "").strip()
    clean_download = clean_url(raw_download)
    clean_source = clean_url(raw_source)

    st.text_input("URL_DOWNLOAD_PDF (bruto)", value=raw_download, disabled=True)
    st.text_input("URL_FONTE (bruto)", value=raw_source, disabled=True)
    st.text_input("Fonte util (limpa)", value=source_url, disabled=True)

    if clean_download:
        st.link_button("Abrir URL_DOWNLOAD_PDF", clean_download)
    if clean_source and clean_source != clean_download:
        st.link_button("Abrir URL_FONTE", clean_source)

st.markdown("### Upload do PDF baixado")
uploaded = st.file_uploader(
    "Arraste o PDF aqui",
    type=["pdf"],
    key=f"pdf_upload_{idx_selected}_{st.session_state['uploader_nonce']}",
)

col_save, col_fail = st.columns(2)

with col_fail:
    if st.button("Nao consegui baixar este item", width="stretch"):
        status_before = clean(row.get("STATUS_LINK", "")).upper()
        update_row_as_failed(df, idx_selected)
        status_after = clean(df.at[idx_selected, "STATUS_LINK"]).upper()
        save_mapping(df, paths.csv_path, expected_rows)
        append_audit_log(
            paths,
            {
                "ACAO": "NAO_CONSEGUI_BAIXAR",
                "IDX_MAIN": idx_selected,
                "UF": row.get("UF", ""),
                "INSTITUICAO": row.get("INSTITUICAO", ""),
                "NOME_POLO_OU_CAMPUS": row.get("NOME_POLO_OU_CAMPUS", ""),
                "MUNICIPIO_POLO": row.get("MUNICIPIO_POLO", ""),
                "CURSO": row.get("CURSO", ""),
                "STATUS_ANTES": status_before,
                "STATUS_DEPOIS": status_after,
                "DOC_ID": normalize_doc_id(df.at[idx_selected, "DOC_ID"]),
                "FONTE_UTIL": source_url,
                "OBS": "Marcado como NAO_ENCONTRADO/VALIDACAO_MANUAL.",
            },
        )
        schedule_next_item(idx_selected, current_pos)
        st.rerun()

with col_save:
    if st.button("Salvar PDF neste item", type="primary", width="stretch"):
        if uploaded is None:
            st.error("Envie um PDF antes de salvar.")
        else:
            data = uploaded.getvalue()
            if not data.startswith(b"%PDF-"):
                st.error("Arquivo enviado nao parece ser um PDF valido.")
            else:
                uf = sanitize(row.get("UF", ""), 8)
                if not uf or uf == "NA":
                    st.error("UF invalida na linha selecionada.")
                else:
                    file_hash = compute_sha256(data)
                    duplicate_path = existing_pdf_by_hash(paths.pdf_root, file_hash)

                    doc_id = normalize_doc_id(row.get("DOC_ID", ""))
                    if not doc_id and duplicate_path is not None:
                        doc_id = extract_doc_id_from_text(duplicate_path.name)
                    if not doc_id:
                        doc_id = next_doc_id_for_uf(df, uf)

                    related_doc_rows = assign_doc_id_to_related_rows(df, idx_selected, row, doc_id, source_url)

                    known_hashes, canonical_name, canonical_path = canonical_info_for_doc_id(df, uf, doc_id)
                    if duplicate_path is None and known_hashes and file_hash not in known_hashes:
                        # Prevent two different PDFs from sharing the same DOC_ID.
                        old_doc_id = doc_id
                        doc_id = next_doc_id_for_uf(df, uf)
                        related_doc_rows = assign_doc_id_to_related_rows(
                            df,
                            idx_selected,
                            row,
                            doc_id,
                            source_url,
                            force_selected_only=False,
                        )
                        st.info(
                            f"Conflito detectado no {old_doc_id}: hash diferente. "
                            f"Reatribuido automaticamente para {doc_id}."
                        )
                        known_hashes, canonical_name, canonical_path = canonical_info_for_doc_id(df, uf, doc_id)

                    if duplicate_path is not None:
                        target_path = duplicate_path
                    else:
                        uf_dir = paths.pdf_root / uf
                        uf_dir.mkdir(parents=True, exist_ok=True)

                        current_name = (row.get("NOME_ARQUIVO_LOCAL", "") or "").strip()
                        base_name = canonical_name or current_name or guess_file_name(row, doc_id)
                        target_name = enforce_doc_id_in_filename(base_name, doc_id)
                        target_path = uf_dir / target_name

                        if target_path.exists():
                            existing_hash = sha256_of_file(target_path)
                            if existing_hash != file_hash:
                                suffix = 1
                                while target_path.exists():
                                    candidate = uf_dir / f"{target_path.stem}__dup{suffix}{target_path.suffix}"
                                    if not candidate.exists():
                                        target_path = candidate
                                        break
                                    suffix += 1
                            # If same hash, keep existing file and do not rewrite.
                        if not target_path.exists():
                            target_path.write_bytes(data)

                    updated_rows = update_rows_for_doc_id(df, uf, doc_id, target_path, file_hash)
                    if updated_rows == 0:
                        # Safety fallback: update selected row even if DOC_ID matching failed.
                        df.at[idx_selected, "DOC_ID"] = doc_id
                        update_row_as_ok(df, idx_selected, row, target_path, file_hash, status="OK_PDF_MANUAL")
                        updated_rows = 1

                    save_mapping(df, paths.csv_path, expected_rows)
                    append_audit_log(
                        paths,
                        {
                            "ACAO": "SALVAR_PDF",
                            "IDX_MAIN": idx_selected,
                            "UF": row.get("UF", ""),
                            "INSTITUICAO": row.get("INSTITUICAO", ""),
                            "NOME_POLO_OU_CAMPUS": row.get("NOME_POLO_OU_CAMPUS", ""),
                            "MUNICIPIO_POLO": row.get("MUNICIPIO_POLO", ""),
                            "CURSO": row.get("CURSO", ""),
                            "STATUS_ANTES": clean(row.get("STATUS_LINK", "")).upper(),
                            "STATUS_DEPOIS": clean(df.at[idx_selected, "STATUS_LINK"]).upper(),
                            "DOC_ID": doc_id,
                            "HASH": file_hash,
                            "NOME_ARQUIVO_LOCAL": target_path.name,
                            "CAMINHO_ARQUIVO_LOCAL": str(target_path),
                            "FONTE_UTIL": source_url,
                            "LINHAS_ATUALIZADAS": updated_rows,
                            "LINHAS_RELACIONADAS": related_doc_rows,
                            "OBS": "Persistido via app triagem manual.",
                        },
                    )
                    schedule_next_item(idx_selected, current_pos)
                    st.success(
                        f"PDF vinculado com sucesso. DOC_ID={doc_id} | "
                        f"linhas atualizadas={updated_rows} | linhas relacionadas={related_doc_rows}"
                    )
                    st.rerun()

st.markdown("### Regras aplicadas")
st.write(
    {
        "base_fixa": "o app bloqueia qualquer insercao/remocao de linhas no CSV",
        "ignorar_status": sorted(SKIP_STATUSES),
        "incluir_status_alvo": sorted(list(TARGET_STATUSES)),
        "filtro_fonte": "considera URL_DOWNLOAD_PDF e URL_FONTE",
        "deduplicacao": "por hash SHA256 no acervo inteiro",
        "propagacao_por_doc_id": "ao salvar, atualiza polos do mesmo DOC_ID",
        "conflito_doc_id": "se hash novo conflitar com DOC_ID existente, cria novo DOC_ID automaticamente",
        "nao_sobrescrever": "se arquivo alvo existir, cria sufixo __dupN",
        "auto_fluxo": "apos salvar/falhar, avanca para o proximo e limpa uploader",
        "marcar_falha_manual": "STATUS_LINK=NAO_ENCONTRADO, ACAO_RECOMENDADA=VALIDACAO_MANUAL",
    }
)

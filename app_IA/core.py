from __future__ import annotations

import csv
import hashlib
import io
import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

BASE_MATRIX_COLUMNS = [
    "PRESENCA_TDIC_0_1",
    "PRESENCA_IA_0_1",
    "NIVEL_INTEGRACAO_0_1_2_3",
    "FINALIDADE_PEDAGOGICA",
    "COMPETENCIAS_DOCENTES",
    "DIMENSAO_ETICA_IA_0_1",
    "ASPECTO_ETICO",
    "ESTRATEGIAS_METODOLOGICAS",
    "EVIDENCIA_LITERAL",
    "LOCALIZACAO_SECAO_PAGINA",
    "NIVEL_CONFIANCA_CODIFICADOR_1_2_3",
]

COMPARISON_COLUMNS = [
    "CAMPUS_IDENTIFICADOS_NO_PDF",
    "CAMPUS_BASE_CONFIRMADOS",
    "CAMPUS_BASE_NAO_CONFIRMADOS",
    "CAMPUS_NOVOS_NAO_BASE",
    "STATUS_COMPARACAO_BASE",
]

ALL_MATRIX_COLUMNS = BASE_MATRIX_COLUMNS + COMPARISON_COLUMNS

RESULT_METADATA_COLUMNS = [
    "UF",
    "DOC_ID",
    "NOME_ARQUIVO_LOCAL",
    "PDF_PATH",
    "IES_PDF",
    "MODALIDADE_PDF",
    "QTD_VINCULOS_BASE",
    "DATA_REGISTRO_UTC",
    "REVISOR_HUMANO",
    "STATUS_VALIDACAO_HUMANA",
    "OBS_VALIDACAO_HUMANA",
]

RESULT_COLUMNS = RESULT_METADATA_COLUMNS + ALL_MATRIX_COLUMNS

VALIDACAO_COLUMNS = [
    "UF",
    "DOC_ID",
    "NOME_ARQUIVO_LOCAL",
    "DATA_REGISTRO_UTC",
    "REVISOR_HUMANO",
    "STATUS_VALIDACAO_HUMANA",
    "OBS_VALIDACAO_HUMANA",
]

BASE_DOC_COLUMNS = [
    "UF",
    "DOC_ID",
    "NOME_ARQUIVO_LOCAL",
    "PDF_PATH",
    "IES_PDF",
    "MODALIDADE_PDF",
    "TAG_LOCALIDADE_PDF",
    "ANO_FONTE_TAG",
    "QTD_VINCULOS_ENCONTRADOS",
    "CAMPUS_SUGERIDOS",
    "METODO_VINCULO",
    "OBS_BASE",
]

VINCULO_COLUMNS = [
    "UF",
    "DOC_ID",
    "NOME_ARQUIVO_LOCAL",
    "PDF_PATH",
    "IES_PDF",
    "INSTITUICAO_BANCO",
    "MODALIDADE_BANCO",
    "NOME_POLO_OU_CAMPUS",
    "MUNICIPIO_POLO",
    "CURSO",
    "TIPO_VINCULO",
    "PPC_COMPARTILHADO",
    "QTD_POLOS_NO_GRUPO",
    "HASH_OU_ID_PDF_CANONICO",
    "ANO_PPC",
    "METODO_VINCULO",
    "CONSISTENCIA_IES_0_1",
    "CONSISTENCIA_UF_0_1",
]

DOC_ID_PATTERN = re.compile(r"DOC\s*0*(\d{1,6})", re.IGNORECASE)
FENCED_BLOCK_PATTERN = re.compile(r"```(?:csv|text)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


@dataclass
class AppPaths:
    app_root: Path
    analyse_root: Path
    pdf_root: Path
    mapeamento_csv: Path
    texto_root: Path
    resposta_root: Path
    validacao_root: Path
    data_root: Path
    base_docs_csv: Path
    vinculos_csv: Path
    respostas_consolidadas_csv: Path
    validacao_controle_csv: Path


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_text(value: str) -> str:
    if value is None:
        return ""
    decomposed = unicodedata.normalize("NFKD", str(value))
    ascii_text = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    lowered = ascii_text.lower()
    return re.sub(r"[^a-z0-9]+", " ", lowered).strip()


def slug_text(value: str) -> str:
    return normalize_text(value).replace(" ", "_")


def normalize_doc_id(value: str) -> str:
    if not value:
        return ""

    match = DOC_ID_PATTERN.search(str(value))
    if match:
        return f"DOC{int(match.group(1)):04d}"

    digits = re.sub(r"\D", "", str(value))
    if digits:
        return f"DOC{int(digits):04d}"

    return str(value).strip().upper()


def extract_doc_id_from_filename(filename: str) -> str:
    return normalize_doc_id(filename)


def normalize_filename(value: str) -> str:
    return normalize_text(Path(value or "").name)


def build_analysis_uid(uf: str, doc_id: str, nome_arquivo_local: str) -> str:
    uf_norm = (uf or "").upper().strip()
    doc_norm = normalize_doc_id(doc_id)
    filename_norm = normalize_filename(nome_arquivo_local)

    raw = f"{uf_norm}|{doc_norm}|{filename_norm}"
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]
    return f"{uf_norm}_{doc_norm}_{digest}"


def find_directory_by_slug(parent: Path, slug: str, default_name: str) -> Path:
    for child in parent.iterdir():
        if child.is_dir() and slug_text(child.name) == slug:
            return child
    return parent / default_name


def discover_paths(app_root: Path) -> AppPaths:
    app_root = app_root.resolve()
    analyse_root = app_root.parent
    new_date_root = analyse_root.parent

    texto_root = find_directory_by_slug(analyse_root, "texto_qualitativo", "Texto_Qualitativo")
    resposta_root = find_directory_by_slug(analyse_root, "resposta_csv", "Resposta_csv")
    validacao_root = find_directory_by_slug(analyse_root, "validacao_manual", "Validacao_Manual")

    data_root = app_root / "data"
    data_root.mkdir(parents=True, exist_ok=True)

    respostas_consolidadas_csv = resposta_root / "analise_notebooklm_consolidado.csv"
    validacao_controle_csv = validacao_root / "validacao_controle.csv"

    return AppPaths(
        app_root=app_root,
        analyse_root=analyse_root,
        pdf_root=new_date_root / "pdfs_baixados",
        mapeamento_csv=new_date_root / "output_csv" / "mapeamento_ppc_polos.csv",
        texto_root=texto_root,
        resposta_root=resposta_root,
        validacao_root=validacao_root,
        data_root=data_root,
        base_docs_csv=data_root / "base_documentos.csv",
        vinculos_csv=data_root / "vinculos_pdf_campus.csv",
        respostas_consolidadas_csv=respostas_consolidadas_csv,
        validacao_controle_csv=validacao_controle_csv,
    )


def read_csv_rows(csv_path: Path) -> List[Dict[str, str]]:
    if not csv_path.exists():
        return []

    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def write_csv_rows(csv_path: Path, rows: Sequence[Dict[str, str]], columns: Sequence[str]) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            out_row = {column: row.get(column, "") for column in columns}
            writer.writerow(out_row)


def upsert_rows(
    current_rows: Sequence[Dict[str, str]],
    new_rows: Sequence[Dict[str, str]],
    key_fields: Sequence[str],
) -> List[Dict[str, str]]:
    merged: Dict[Tuple[str, ...], Dict[str, str]] = {}

    for row in current_rows:
        key = tuple(row.get(field, "") for field in key_fields)
        merged[key] = dict(row)

    for row in new_rows:
        key = tuple(row.get(field, "") for field in key_fields)
        merged[key] = dict(row)

    return list(merged.values())


def replace_rows_for_ufs(
    current_rows: Sequence[Dict[str, str]],
    new_rows: Sequence[Dict[str, str]],
    target_ufs: Sequence[str],
    key_fields: Sequence[str],
) -> List[Dict[str, str]]:
    target_set = {uf.upper() for uf in target_ufs}
    kept_rows = [row for row in current_rows if row.get("UF", "").upper() not in target_set]
    return upsert_rows(kept_rows, new_rows, key_fields)


def parse_pdf_metadata(pdf_path: Path) -> Dict[str, str]:
    stem = pdf_path.stem
    parts = stem.split("__")

    doc_id = extract_doc_id_from_filename(pdf_path.name)
    uf = parts[0].upper() if len(parts) > 0 else ""
    ies_pdf = parts[1].upper() if len(parts) > 1 else ""
    modalidade_pdf = parts[2].upper() if len(parts) > 2 else ""

    ano_tag = ""
    for part in parts:
        if re.search(r"\d{4}", part):
            ano_tag = part
            break

    localidade_tag = ""
    if len(parts) >= 6:
        localidade_tag = parts[4]

    return {
        "UF": uf,
        "DOC_ID": doc_id,
        "NOME_ARQUIVO_LOCAL": pdf_path.name,
        "PDF_PATH": str(pdf_path.resolve()),
        "IES_PDF": ies_pdf,
        "MODALIDADE_PDF": modalidade_pdf,
        "TAG_LOCALIDADE_PDF": localidade_tag,
        "ANO_FONTE_TAG": ano_tag,
    }


def match_mapeamento_rows(
    mapeamento_rows: Sequence[Dict[str, str]],
    uf: str,
    pdf_filename: str,
    doc_id: str,
) -> Tuple[List[Dict[str, str]], str]:
    uf_rows = [row for row in mapeamento_rows if row.get("UF", "").upper() == uf.upper()]
    normalized_pdf_name = normalize_text(pdf_filename)

    exact_name = [
        row
        for row in uf_rows
        if normalize_text(row.get("NOME_ARQUIVO_LOCAL", "")) == normalized_pdf_name
    ]
    if exact_name:
        return exact_name, "EXATO_NOME_ARQUIVO"

    by_doc = []
    for row in uf_rows:
        name_doc = extract_doc_id_from_filename(row.get("NOME_ARQUIVO_LOCAL", ""))
        path_doc = extract_doc_id_from_filename(row.get("CAMINHO_ARQUIVO_LOCAL", ""))
        if doc_id and (name_doc == doc_id or path_doc == doc_id):
            by_doc.append(row)

    if by_doc:
        return by_doc, "MATCH_POR_DOC_ID"

    partial_name = []
    for row in uf_rows:
        row_name = normalize_text(row.get("NOME_ARQUIVO_LOCAL", ""))
        if normalized_pdf_name and row_name and (row_name in normalized_pdf_name or normalized_pdf_name in row_name):
            partial_name.append(row)

    if partial_name:
        return partial_name, "PARCIAL_NOME_ARQUIVO"

    return [], "SEM_MATCH"


def ies_consistency(ies_pdf: str, instituicao_banco: str) -> str:
    ies_pdf_norm = normalize_text(ies_pdf)
    inst_norm = normalize_text(instituicao_banco)

    if not ies_pdf_norm or not inst_norm:
        return "0"

    if ies_pdf_norm in inst_norm or inst_norm in ies_pdf_norm:
        return "1"

    return "0"


def prepare_base(paths: AppPaths, ufs: Sequence[str]) -> Dict[str, object]:
    if not paths.mapeamento_csv.exists():
        raise FileNotFoundError(f"Arquivo de mapeamento nao encontrado: {paths.mapeamento_csv}")

    mapeamento_rows = read_csv_rows(paths.mapeamento_csv)
    existing_base = read_csv_rows(paths.base_docs_csv)
    existing_vinculos = read_csv_rows(paths.vinculos_csv)

    base_new: List[Dict[str, str]] = []
    vinculos_new: List[Dict[str, str]] = []
    resumo_ufs: List[Dict[str, str]] = []

    for uf in sorted({value.upper() for value in ufs}):
        uf_folder = paths.pdf_root / uf
        pdf_files = sorted(uf_folder.glob("*.pdf")) if uf_folder.exists() else []

        for pdf_file in pdf_files:
            meta = parse_pdf_metadata(pdf_file)
            matches, metodo = match_mapeamento_rows(
                mapeamento_rows,
                uf=meta["UF"],
                pdf_filename=meta["NOME_ARQUIVO_LOCAL"],
                doc_id=meta["DOC_ID"],
            )

            campus_unicos = sorted(
                {
                    row.get("NOME_POLO_OU_CAMPUS", "").strip()
                    for row in matches
                    if row.get("NOME_POLO_OU_CAMPUS", "").strip()
                }
            )

            base_row = {
                **meta,
                "QTD_VINCULOS_ENCONTRADOS": str(len(matches)),
                "CAMPUS_SUGERIDOS": " | ".join(campus_unicos) if campus_unicos else "SEM_VINCULO",
                "METODO_VINCULO": metodo,
                "OBS_BASE": "OK" if matches else "SEM_VINCULO_NO_MAPEAMENTO",
            }
            base_new.append(base_row)

            for row in matches:
                vinculos_new.append(
                    {
                        "UF": meta["UF"],
                        "DOC_ID": meta["DOC_ID"],
                        "NOME_ARQUIVO_LOCAL": meta["NOME_ARQUIVO_LOCAL"],
                        "PDF_PATH": meta["PDF_PATH"],
                        "IES_PDF": meta["IES_PDF"],
                        "INSTITUICAO_BANCO": row.get("INSTITUICAO", ""),
                        "MODALIDADE_BANCO": row.get("MODALIDADE", ""),
                        "NOME_POLO_OU_CAMPUS": row.get("NOME_POLO_OU_CAMPUS", ""),
                        "MUNICIPIO_POLO": row.get("MUNICIPIO_POLO", ""),
                        "CURSO": row.get("CURSO", ""),
                        "TIPO_VINCULO": row.get("TIPO_VINCULO", ""),
                        "PPC_COMPARTILHADO": row.get("PPC_COMPARTILHADO", ""),
                        "QTD_POLOS_NO_GRUPO": row.get("QTD_POLOS_NO_GRUPO", ""),
                        "HASH_OU_ID_PDF_CANONICO": row.get("HASH_OU_ID_PDF_CANONICO", ""),
                        "ANO_PPC": row.get("ANO_PPC", ""),
                        "METODO_VINCULO": metodo,
                        "CONSISTENCIA_IES_0_1": ies_consistency(meta["IES_PDF"], row.get("INSTITUICAO", "")),
                        "CONSISTENCIA_UF_0_1": "1" if meta["UF"] == row.get("UF", "").upper() else "0",
                    }
                )

        resumo_ufs.append(
            {
                "UF": uf,
                "QTD_PDFS": str(len(pdf_files)),
                "QTD_VINCULOS_TOTAL": "0",
            }
        )

    merged_base = replace_rows_for_ufs(
        existing_base,
        base_new,
        target_ufs=ufs,
        key_fields=("UF", "DOC_ID", "NOME_ARQUIVO_LOCAL"),
    )

    merged_vinculos = replace_rows_for_ufs(
        existing_vinculos,
        vinculos_new,
        target_ufs=ufs,
        key_fields=(
            "UF",
            "DOC_ID",
            "NOME_ARQUIVO_LOCAL",
            "NOME_POLO_OU_CAMPUS",
            "MUNICIPIO_POLO",
            "INSTITUICAO_BANCO",
            "HASH_OU_ID_PDF_CANONICO",
        ),
    )

    write_csv_rows(paths.base_docs_csv, merged_base, BASE_DOC_COLUMNS)
    write_csv_rows(paths.vinculos_csv, merged_vinculos, VINCULO_COLUMNS)

    resumo_ufs_final: List[Dict[str, str]] = []
    for item in resumo_ufs:
        uf = item.get("UF", "").upper()
        pdf_count = len([row for row in merged_base if row.get("UF", "").upper() == uf])
        vinc_count = len([row for row in merged_vinculos if row.get("UF", "").upper() == uf])
        resumo_ufs_final.append(
            {
                "UF": uf,
                "QTD_PDFS": str(pdf_count),
                "QTD_VINCULOS_TOTAL": str(vinc_count),
            }
        )

    return {
        "base_total": len(merged_base),
        "vinculos_total": len(merged_vinculos),
        "resumo_ufs": resumo_ufs_final,
    }


def list_available_ufs(pdf_root: Path) -> List[str]:
    if not pdf_root.exists():
        return []
    return sorted([folder.name.upper() for folder in pdf_root.iterdir() if folder.is_dir()])


def load_base_rows(paths: AppPaths, uf: str | None = None) -> List[Dict[str, str]]:
    rows = read_csv_rows(paths.base_docs_csv)
    if uf:
        return [row for row in rows if row.get("UF", "").upper() == uf.upper()]
    return rows


def load_vinculos_rows(
    paths: AppPaths,
    uf: str,
    doc_id: str,
    pdf_filename: str = "",
) -> List[Dict[str, str]]:
    target_doc_id = normalize_doc_id(doc_id)
    target_filename = normalize_filename(pdf_filename)
    rows = read_csv_rows(paths.vinculos_csv)

    matches_by_doc = [
        row
        for row in rows
        if row.get("UF", "").upper() == uf.upper() and normalize_doc_id(row.get("DOC_ID", "")) == target_doc_id
    ]

    if not target_filename:
        return matches_by_doc

    matches_exact_filename = [
        row
        for row in matches_by_doc
        if normalize_filename(row.get("NOME_ARQUIVO_LOCAL", "")) == target_filename
    ]

    if matches_exact_filename:
        return matches_exact_filename

    return matches_by_doc


def _split_vinculos_context_lines(vinculos_rows: Sequence[Dict[str, str]]) -> Tuple[List[str], List[str]]:
    if not vinculos_rows:
        return ["- SEM_VINCULO_ALTA_CONFIANCA"], ["- SEM_VINCULO_BAIXA_CONFIANCA"]

    seen = set()
    high_conf_lines: List[str] = []
    low_conf_lines: List[str] = []

    for row in vinculos_rows:
        campus = row.get("NOME_POLO_OU_CAMPUS", "").strip() or "SEM_NOME_CAMPUS"
        municipio = row.get("MUNICIPIO_POLO", "").strip() or "SEM_MUNICIPIO"
        instituicao = row.get("INSTITUICAO_BANCO", "").strip() or "SEM_INSTITUICAO"
        consistencia = (row.get("CONSISTENCIA_IES_0_1", "") or "").strip()

        key = (campus, municipio, instituicao)
        if key in seen:
            continue
        seen.add(key)

        line = (
            f"- CAMPUS_BASE: {campus} | MUNICIPIO: {municipio} | "
            f"INSTITUICAO_BANCO: {instituicao} | CONSISTENCIA_IES_0_1: {consistencia or 'NA'}"
        )

        if consistencia == "1":
            high_conf_lines.append(line)
        else:
            low_conf_lines.append(line)

    if not high_conf_lines:
        high_conf_lines = ["- SEM_VINCULO_ALTA_CONFIANCA"]
    if not low_conf_lines:
        low_conf_lines = ["- SEM_VINCULO_BAIXA_CONFIANCA"]

    return high_conf_lines, low_conf_lines


def build_notebooklm_prompts(
    doc_row: Dict[str, str],
    vinculos_rows: Sequence[Dict[str, str]],
) -> Dict[str, str]:
    uf = doc_row.get("UF", "")
    doc_id = normalize_doc_id(doc_row.get("DOC_ID", ""))
    nome_arquivo = doc_row.get("NOME_ARQUIVO_LOCAL", "")
    ies_pdf = doc_row.get("IES_PDF", "")
    modalidade_pdf = doc_row.get("MODALIDADE_PDF", "")

    contexto_linhas_alta, contexto_linhas_baixa = _split_vinculos_context_lines(vinculos_rows)
    contexto_base_alta = "\n".join(contexto_linhas_alta)
    contexto_base_baixa = "\n".join(contexto_linhas_baixa)

    contexto_comum = f"""
METADADOS_DO_DOCUMENTO:
- UF: {uf}
- DOC_ID: {doc_id}
- NOME_ARQUIVO_LOCAL: {nome_arquivo}
- IES_DO_NOME_ARQUIVO: {ies_pdf}
- MODALIDADE_DO_NOME_ARQUIVO: {modalidade_pdf}

BASE_LOCAL_ALTA_CONFIANCA_PARA_COMPARACAO_DE_CAMPUS:
{contexto_base_alta}

BASE_LOCAL_BAIXA_CONFIANCA_APENAS_COMO_ALERTA:
{contexto_base_baixa}

REGRAS_GERAIS:
- Use apenas evidencias do PDF analisado.
- Sempre cite trecho literal entre aspas e indique secao/pagina.
- Se nao houver evidencia explicita, use AUSENTE.
- Priorize vinculos da base de alta confianca (CONSISTENCIA_IES_0_1=1).
- Nao trate vinculos de baixa confianca como verdade sem evidencia no PDF.
- Se PRESENCA_IA_0_1=0 (IA ausente), NIVEL_INTEGRACAO_0_1_2_3 nao pode ser 3.
- Ao comparar com a base local, diferencie: confirmado, nao confirmado e novo.
""".strip()

    prompt_1 = f"""
{contexto_comum}

TAREFA_PROMPT_1_RESUMO_EVIDENCIAS:
Produza um resumo analitico com foco em:
1) presenca de TDIC
2) presenca de IA
3) nivel de integracao curricular
4) competencias digitais docentes
5) dimensao etica/critica da IA
6) relacao entre IES do PDF e campi/polos mencionados no texto

FORMATO_OBRIGATORIO:
BLOCO_A_RESUMO
- TDIC:
- IA:
- Integracao Curricular:
- Competencias Docentes:
- Dimensao Etica/Critica:

BLOCO_B_EVIDENCIAS
- TDIC | "trecho literal" | secao/pagina
- IA | "trecho literal" | secao/pagina
- Integracao Curricular | "trecho literal" | secao/pagina
- Competencias Docentes | "trecho literal" | secao/pagina
- Dimensao Etica/Critica | "trecho literal" | secao/pagina

BLOCO_C_COMPARACAO_BASE
- CAMPUS_IDENTIFICADOS_NO_PDF:
- CAMPUS_BASE_CONFIRMADOS:
- CAMPUS_BASE_NAO_CONFIRMADOS:
- CAMPUS_NOVOS_NAO_BASE:
- STATUS_COMPARACAO_BASE: COERENTE ou PARCIAL ou DIVERGENTE ou SEM_EVIDENCIA
""".strip()

    csv_header = ",".join(ALL_MATRIX_COLUMNS)
    prompt_2 = f"""
{contexto_comum}

TAREFA_PROMPT_2_MATRIZ_CSV:
Aplique a matriz de codificacao e responda em CSV.

Rubrica NIVEL_INTEGRACAO_0_1_2_3:
- 0: ausente
- 1: mencao superficial, sem estrategia curricular clara
- 2: uso aplicado/instrumental com estrategia didatica
- 3: integracao curricular estruturante, explicita e sustentada por evidencias multiplas, com mencao explicita de IA no documento

Rubrica NIVEL_CONFIANCA_CODIFICADOR_1_2_3:
- 1: baixa
- 2: media
- 3: alta

REGRAS DE SAIDA:
- Retorne somente 2 linhas: cabecalho CSV e uma unica linha CSV.
- Nao escreva explicacoes fora do CSV.
- Se houver virgula em campos textuais, use aspas.
- Se PRESENCA_IA_0_1=0, NIVEL_INTEGRACAO_0_1_2_3 deve ser no maximo 2.
- Sem evidencia literal + localizacao, nao use nivel 3.

CABECALHO_EXATO:
{csv_header}
""".strip()

    prompt_3 = f"""
{contexto_comum}

TAREFA_PROMPT_3_AUDITORIA_CRITICA:
Revise sua propria codificacao e sinalize:
1) campos com baixa confianca
2) ambiguidades de interpretacao
3) risco de superestimacao de integracao curricular
4) risco de erro no vinculo entre IES e campus/polo

REGRA CENTRAL:
Sem evidencia literal + localizacao, ou sem mencao de IA no documento, nao classificar integracao como nivel 3.

FORMATO_OBRIGATORIO:
BLOCO_A_ALERTAS
- Campo: [nome] | Problema: [descricao] | Risco: [baixo/medio/alto]

BLOCO_B_PONTOS_A_REVISAR_PELO_HUMANO
- Item 1:
- Item 2:
- Item 3:

BLOCO_C_DECISAO_SOBRE_INTEGRACAO
- Nivel inicialmente atribuido:
- Nivel recomendado apos revisao:
- Justificativa com evidencia literal:

BLOCO_D_DECISAO_SOBRE_VINCULO_IES_CAMPUS
- Status: COERENTE ou PARCIAL ou DIVERGENTE ou INCONCLUSIVO
- Justificativa:
""".strip()

    return {
        "prompt_1": prompt_1,
        "prompt_2": prompt_2,
        "prompt_3": prompt_3,
    }


def clean_csv_text(raw_text: str) -> str:
    text = (raw_text or "").strip()
    if not text:
        return ""

    fence_match = FENCED_BLOCK_PATTERN.search(text)
    if fence_match:
        text = fence_match.group(1).strip()

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def _read_csv_rows_from_text(text: str) -> List[List[str]]:
    handle = io.StringIO(text)
    reader = csv.reader(handle)
    rows = []
    for row in reader:
        if not row:
            continue
        if not any(cell.strip() for cell in row):
            continue
        rows.append([cell.strip() for cell in row])
    return rows


def _mapped_value(mapped_row: Dict[str, str], key: str) -> str:
    target = normalize_text(key)
    for row_key, value in mapped_row.items():
        if normalize_text(row_key) == target:
            return (value or "").strip()
    return ""


def parse_prompt2_csv(raw_text: str) -> Dict[str, str]:
    cleaned = clean_csv_text(raw_text)
    if not cleaned:
        raise ValueError("Resposta do Prompt 2 vazia. Cole o CSV retornado pelo NotebookLM.")

    rows = _read_csv_rows_from_text(cleaned)
    if not rows:
        raise ValueError("Nao foi possivel ler o CSV do Prompt 2.")

    mapped_row: Dict[str, str]

    first_row_normalized = [normalize_text(cell) for cell in rows[0]]
    header_is_present = normalize_text("PRESENCA_TDIC_0_1") in first_row_normalized

    if header_is_present:
        if len(rows) < 2:
            raise ValueError("CSV com cabecalho, mas sem linha de dados.")

        header = rows[0]
        values = rows[1]
        if len(values) < len(header):
            values = values + [""] * (len(header) - len(values))

        mapped_row = {header[index]: values[index] for index in range(len(header))}
    else:
        values = rows[0]
        if len(values) < len(BASE_MATRIX_COLUMNS):
            raise ValueError(
                "Linha CSV sem cabecalho tem menos colunas que o minimo esperado da matriz base."
            )

        mapped_row = {}
        for index, column in enumerate(BASE_MATRIX_COLUMNS):
            mapped_row[column] = values[index] if index < len(values) else ""

        for offset, column in enumerate(COMPARISON_COLUMNS, start=len(BASE_MATRIX_COLUMNS)):
            mapped_row[column] = values[offset] if offset < len(values) else ""

    parsed = {column: _mapped_value(mapped_row, column) for column in ALL_MATRIX_COLUMNS}
    return parsed


def _markdown_header_section(doc_row: Dict[str, str], vinculos_rows: Sequence[Dict[str, str]]) -> str:
    analysis_uid = build_analysis_uid(
        doc_row.get("UF", ""),
        doc_row.get("DOC_ID", ""),
        doc_row.get("NOME_ARQUIVO_LOCAL", ""),
    )

    return "\n".join(
        [
            f"- UF: {doc_row.get('UF', '')}",
            f"- DOC_ID: {normalize_doc_id(doc_row.get('DOC_ID', ''))}",
            f"- NOME_ARQUIVO_LOCAL: {doc_row.get('NOME_ARQUIVO_LOCAL', '')}",
            f"- ANALISE_UID: {analysis_uid}",
            f"- PDF_PATH: {doc_row.get('PDF_PATH', '')}",
            f"- IES_PDF: {doc_row.get('IES_PDF', '')}",
            f"- MODALIDADE_PDF: {doc_row.get('MODALIDADE_PDF', '')}",
            f"- QTD_VINCULOS_BASE: {len(vinculos_rows)}",
        ]
    )


def enforce_integration_rule_requires_ia(parsed_matrix: Dict[str, str]) -> Tuple[Dict[str, str], str]:
    ia_raw = (parsed_matrix.get("PRESENCA_IA_0_1", "") or "").strip()
    nivel_raw = (parsed_matrix.get("NIVEL_INTEGRACAO_0_1_2_3", "") or "").strip()

    if nivel_raw == "3" and ia_raw != "1":
        parsed_matrix["NIVEL_INTEGRACAO_0_1_2_3"] = "2"
        return (
            parsed_matrix,
            "AJUSTE_HUMANO_APLICADO: NIVEL_INTEGRACAO reduzido de 3 para 2 porque PRESENCA_IA_0_1=0.",
        )

    return parsed_matrix, ""


def save_outputs(
    paths: AppPaths,
    doc_row: Dict[str, str],
    vinculos_rows: Sequence[Dict[str, str]],
    resposta_prompt_1: str,
    resposta_prompt_2: str,
    resposta_prompt_3: str,
    revisor_humano: str,
    status_validacao_humana: str,
    obs_validacao_humana: str,
) -> Dict[str, object]:
    uf = doc_row.get("UF", "").upper()
    doc_id = normalize_doc_id(doc_row.get("DOC_ID", ""))
    pdf_filename = (doc_row.get("NOME_ARQUIVO_LOCAL", "") or "").strip()
    if not uf or not doc_id or not pdf_filename:
        raise ValueError("UF, DOC_ID e NOME_ARQUIVO_LOCAL sao obrigatorios para salvar as respostas.")

    analysis_uid = build_analysis_uid(uf, doc_id, pdf_filename)

    parsed_matrix = parse_prompt2_csv(resposta_prompt_2)
    parsed_matrix, adjustment_note = enforce_integration_rule_requires_ia(parsed_matrix)
    timestamp = now_utc_iso()

    status_validacao_final = (status_validacao_humana or "").strip() or "PENDENTE"
    obs_validacao_final = (obs_validacao_humana or "").strip()

    if adjustment_note:
        if obs_validacao_final:
            obs_validacao_final = f"{obs_validacao_final} | {adjustment_note}"
        else:
            obs_validacao_final = adjustment_note

        if status_validacao_final == "VALIDADO":
            status_validacao_final = "AJUSTADO"

    texto_folder = paths.texto_root / uf
    validacao_folder = paths.validacao_root / uf
    resposta_uf_folder = paths.resposta_root / uf

    texto_folder.mkdir(parents=True, exist_ok=True)
    validacao_folder.mkdir(parents=True, exist_ok=True)
    resposta_uf_folder.mkdir(parents=True, exist_ok=True)

    texto_path = texto_folder / f"{analysis_uid}.md"
    validacao_path = validacao_folder / f"{analysis_uid}.md"
    resposta_uf_csv = resposta_uf_folder / f"analise_notebooklm_{uf}.csv"

    metadata_md = _markdown_header_section(doc_row, vinculos_rows)

    texto_md = "\n".join(
        [
            f"# TEXTO_QUALITATIVO_{analysis_uid}",
            "",
            "## METADADOS",
            metadata_md,
            "",
            "## RESPOSTA_PROMPT_1",
            (resposta_prompt_1 or "").strip() or "AUSENTE",
            "",
            "## LOG",
            f"- DATA_REGISTRO_UTC: {timestamp}",
        ]
    )

    validacao_md = "\n".join(
        [
            f"# VALIDACAO_MANUAL_{analysis_uid}",
            "",
            "## METADADOS",
            metadata_md,
            "",
            "## RESPOSTA_PROMPT_3",
            (resposta_prompt_3 or "").strip() or "AUSENTE",
            "",
            "## CAMPOS_DE_VALIDACAO_HUMANA",
            f"- REVISOR_HUMANO: {revisor_humano or 'NAO_INFORMADO'}",
            f"- STATUS_VALIDACAO_HUMANA: {status_validacao_final}",
            f"- OBS_VALIDACAO_HUMANA: {obs_validacao_final or 'SEM_OBS'}",
            "",
            "## CHECKLIST_RAPIDO",
            "- [ ] Evidencia literal existe para todos os campos essenciais",
            "- [ ] Localizacao secao/pagina esta informada",
            "- [ ] Nivel de integracao revisado sem inflacao",
            "- [ ] Vinculo IES x campus revisado com base local",
            "- [ ] Decisao final registrada",
            "",
            "## LOG",
            f"- DATA_REGISTRO_UTC: {timestamp}",
        ]
    )

    texto_path.write_text(texto_md, encoding="utf-8")
    validacao_path.write_text(validacao_md, encoding="utf-8")

    result_row = {
        "UF": uf,
        "DOC_ID": doc_id,
        "NOME_ARQUIVO_LOCAL": pdf_filename,
        "PDF_PATH": doc_row.get("PDF_PATH", ""),
        "IES_PDF": doc_row.get("IES_PDF", ""),
        "MODALIDADE_PDF": doc_row.get("MODALIDADE_PDF", ""),
        "QTD_VINCULOS_BASE": str(len(vinculos_rows)),
        "DATA_REGISTRO_UTC": timestamp,
        "REVISOR_HUMANO": (revisor_humano or "").strip(),
        "STATUS_VALIDACAO_HUMANA": status_validacao_final,
        "OBS_VALIDACAO_HUMANA": obs_validacao_final,
    }
    result_row.update(parsed_matrix)

    consolidated_rows = read_csv_rows(paths.respostas_consolidadas_csv)
    consolidated_rows = upsert_rows(
        consolidated_rows,
        [result_row],
        key_fields=("UF", "DOC_ID", "NOME_ARQUIVO_LOCAL"),
    )
    write_csv_rows(paths.respostas_consolidadas_csv, consolidated_rows, RESULT_COLUMNS)

    uf_rows = read_csv_rows(resposta_uf_csv)
    uf_rows = upsert_rows(
        uf_rows,
        [result_row],
        key_fields=("UF", "DOC_ID", "NOME_ARQUIVO_LOCAL"),
    )
    write_csv_rows(resposta_uf_csv, uf_rows, RESULT_COLUMNS)

    validacao_row = {
        "UF": uf,
        "DOC_ID": doc_id,
        "NOME_ARQUIVO_LOCAL": pdf_filename,
        "DATA_REGISTRO_UTC": timestamp,
        "REVISOR_HUMANO": (revisor_humano or "").strip(),
        "STATUS_VALIDACAO_HUMANA": status_validacao_final,
        "OBS_VALIDACAO_HUMANA": obs_validacao_final,
    }

    validacao_rows = read_csv_rows(paths.validacao_controle_csv)
    validacao_rows = upsert_rows(
        validacao_rows,
        [validacao_row],
        key_fields=("UF", "DOC_ID", "NOME_ARQUIVO_LOCAL"),
    )
    write_csv_rows(paths.validacao_controle_csv, validacao_rows, VALIDACAO_COLUMNS)

    return {
        "texto_path": texto_path,
        "validacao_path": validacao_path,
        "resposta_uf_csv": resposta_uf_csv,
        "resposta_consolidada_csv": paths.respostas_consolidadas_csv,
        "validacao_controle_csv": paths.validacao_controle_csv,
        "parsed_matrix": parsed_matrix,
    }


def checklist_validacao_manual_10_passos() -> List[str]:
    return [
        "Definir lote do dia e registrar IDs dos documentos.",
        "Rodar Prompt 1 no NotebookLM para cada documento.",
        "Verificar citacao literal e localizacao dos 5 eixos.",
        "Rodar Prompt 2 e colar o CSV no app.",
        "Rodar Prompt 3 e registrar alertas.",
        "Revisar manualmente trechos ambiguos.",
        "Reavaliar nivel de integracao se evidencia for fraca.",
        "Comparar 20% do lote com segundo codificador (NotebookLM nova rodada ou outro modelo).",
        "Registrar divergencias e decisao final humana.",
        "Fechar lote com status VALIDADO, AJUSTADO ou PENDENTE.",
    ]

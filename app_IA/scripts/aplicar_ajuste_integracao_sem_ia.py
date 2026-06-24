from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

ADJUST_NOTE = "AJUSTE_HUMANO_APLICADO: NIVEL_INTEGRACAO reduzido de 3 para 2 porque PRESENCA_IA_0_1=0."


def read_rows(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    if not path.exists():
        return [], []

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def write_rows(path: Path, fieldnames: Sequence[str], rows: Sequence[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            out = {name: row.get(name, "") for name in fieldnames}
            writer.writerow(out)


def normalize_doc_id(value: str) -> str:
    text = (value or "").strip().upper()
    if text.startswith("DOC"):
        digits = "".join(ch for ch in text if ch.isdigit())
        if digits:
            return f"DOC{int(digits):04d}"
    return text


def normalize_filename(value: str) -> str:
    return (value or "").strip().lower()


def build_analysis_token(doc_id: str, nome_arquivo_local: str) -> str:
    doc_norm = normalize_doc_id(doc_id)
    filename_norm = normalize_filename(nome_arquivo_local)
    if doc_norm and filename_norm:
        return f"{doc_norm}||{filename_norm}"
    return doc_norm or filename_norm


def format_analysis_token(token: str) -> str:
    if "||" not in token:
        return token
    doc_id, filename_norm = token.split("||", 1)
    if doc_id and filename_norm:
        return f"{doc_id} | {filename_norm}"
    return token


def append_note(obs: str) -> str:
    base = (obs or "").strip()
    if ADJUST_NOTE in base:
        return base
    if not base:
        return ADJUST_NOTE
    return f"{base} | {ADJUST_NOTE}"


def apply_adjustment_to_analysis_rows(rows: List[Dict[str, str]], uf: str) -> Tuple[List[Dict[str, str]], List[str]]:
    uf = uf.upper()
    adjusted_tokens: List[str] = []

    for row in rows:
        row_uf = (row.get("UF", "") or "").upper().strip()
        if row_uf != uf:
            continue

        ia = (row.get("PRESENCA_IA_0_1", "") or "").strip()
        nivel = (row.get("NIVEL_INTEGRACAO_0_1_2_3", "") or "").strip()

        if ia != "1" and nivel == "3":
            row["NIVEL_INTEGRACAO_0_1_2_3"] = "2"

            status = (row.get("STATUS_VALIDACAO_HUMANA", "") or "").strip().upper()
            if status == "VALIDADO":
                row["STATUS_VALIDACAO_HUMANA"] = "AJUSTADO"

            row["OBS_VALIDACAO_HUMANA"] = append_note(row.get("OBS_VALIDACAO_HUMANA", ""))

            token = build_analysis_token(row.get("DOC_ID", ""), row.get("NOME_ARQUIVO_LOCAL", ""))
            if token:
                adjusted_tokens.append(token)

    return rows, sorted(set(adjusted_tokens))


def apply_adjustment_to_validation_rows(
    rows: List[Dict[str, str]],
    uf: str,
    adjusted_tokens: Sequence[str],
) -> List[Dict[str, str]]:
    uf = uf.upper()
    adjusted_set = set(adjusted_tokens)

    for row in rows:
        row_uf = (row.get("UF", "") or "").upper().strip()
        token = build_analysis_token(row.get("DOC_ID", ""), row.get("NOME_ARQUIVO_LOCAL", ""))

        if row_uf != uf or token not in adjusted_set:
            continue

        status = (row.get("STATUS_VALIDACAO_HUMANA", "") or "").strip().upper()
        if status == "VALIDADO":
            row["STATUS_VALIDACAO_HUMANA"] = "AJUSTADO"

        row["OBS_VALIDACAO_HUMANA"] = append_note(row.get("OBS_VALIDACAO_HUMANA", ""))

    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Aplica ajuste humano de integracao: se IA=0, nivel 3 vira 2.")
    parser.add_argument("--uf", required=True, help="UF alvo (ex.: AL)")
    parser.add_argument(
        "--data-root",
        default=r"c:\Users\augus\Music\TCC\Data",
        help="Raiz do workspace Data",
    )
    args = parser.parse_args()

    uf = args.uf.upper()
    data_root = Path(args.data_root)

    consolidated_path = data_root / "new_date" / "Analyse_IA" / "Resposta_csv" / "analise_notebooklm_consolidado.csv"
    uf_path = data_root / "new_date" / "Analyse_IA" / "Resposta_csv" / uf / f"analise_notebooklm_{uf}.csv"
    validacao_path = data_root / "new_date" / "Analyse_IA" / "Validação_Manual" / "validacao_controle.csv"

    cons_fields, cons_rows = read_rows(consolidated_path)
    uf_fields, uf_rows = read_rows(uf_path)
    val_fields, val_rows = read_rows(validacao_path)

    if not cons_rows:
        print(f"Arquivo consolidado vazio ou ausente: {consolidated_path}")
        return 1

    cons_rows, adjusted_tokens_cons = apply_adjustment_to_analysis_rows(cons_rows, uf)
    uf_rows, adjusted_tokens_uf = apply_adjustment_to_analysis_rows(uf_rows, uf)

    adjusted_tokens = sorted(set(adjusted_tokens_cons) | set(adjusted_tokens_uf))

    if val_rows and adjusted_tokens:
        val_rows = apply_adjustment_to_validation_rows(val_rows, uf, adjusted_tokens)

    write_rows(consolidated_path, cons_fields, cons_rows)
    if uf_fields and uf_rows:
        write_rows(uf_path, uf_fields, uf_rows)
    if val_fields and val_rows:
        write_rows(validacao_path, val_fields, val_rows)

    print(f"UF processada: {uf}")
    print(f"Registros (PDFs) ajustados: {len(adjusted_tokens)}")
    if adjusted_tokens:
        print("Registros ajustados: " + ", ".join(format_analysis_token(token) for token in adjusted_tokens))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

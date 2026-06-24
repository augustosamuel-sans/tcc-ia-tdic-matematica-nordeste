from __future__ import annotations

import argparse
import hashlib
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import pandas as pd


KEY_COLS = [
    "UF",
    "INSTITUICAO",
    "MODALIDADE",
    "NOME_POLO_OU_CAMPUS",
    "MUNICIPIO_POLO",
    "CURSO",
]

OK_STATUSES = {"OK_PDF", "OK_PDF_MANUAL"}
PLACEHOLDERS = {"", "NAO_ENCONTRADO", "SEM_LINK", "NONE", "N/A", "NULL"}
URL_COLS = {"URL_FONTE", "URL_DOWNLOAD_PDF", "URL_DOWNLOAD_PDF_LIMPA"}
TEXT_PREF_LONGER_COLS = {"EVIDENCIA_MINIMA", "OBS"}
FILE_COLS = {"NOME_ARQUIVO_LOCAL", "CAMINHO_ARQUIVO_LOCAL", "HASH_OU_ID_PDF_CANONICO", "DOC_ID"}
IMMUTABLE_IDENTITY_COLS = set(KEY_COLS)

DOC_ID_RE = re.compile(r"DOC\s*0*(\d{1,6})", re.IGNORECASE)

STATUS_RANK = {
    "": 0,
    "BLOQUEADO": 1,
    "404": 2,
    "NAO_ENCONTRADO": 3,
    "HTML_INTERMEDIARIO": 4,
    "OK_PDF_MANUAL": 5,
    "OK_PDF": 6,
}


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def normalize_text(value: str) -> str:
    txt = str(value or "").strip().upper()
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(ch for ch in txt if not unicodedata.combining(ch))
    txt = re.sub(r"\s+", " ", txt)
    return txt


def norm_key_token(value: str) -> str:
    txt = normalize_text(value)
    txt = txt.replace("´", "'")
    return txt


def build_key_from_row(row: pd.Series) -> str:
    return "||".join(norm_key_token(row.get(col, "")) for col in KEY_COLS)


def build_key_columns(df: pd.DataFrame) -> pd.Series:
    return df.apply(build_key_from_row, axis=1)


def clean(value: str) -> str:
    return str(value or "").strip()


def is_placeholder(value: str) -> bool:
    return clean(value).upper() in PLACEHOLDERS


def has_http(value: str) -> bool:
    v = clean(value).lower()
    return v.startswith("http://") or v.startswith("https://")


def status_rank(status: str) -> int:
    return STATUS_RANK.get(clean(status).upper(), 0)


def normalize_doc_id(value: str) -> str:
    txt = clean(value).upper()
    m = DOC_ID_RE.search(txt)
    if not m:
        return ""
    number = int(m.group(1))
    width = max(4, len(m.group(1)))
    return f"DOC{number:0{width}d}"


def extract_doc_id_from_values(values: Iterable[str]) -> str:
    for value in values:
        doc = normalize_doc_id(value)
        if doc:
            return doc
    return ""


def replace_doc_id_in_filename(file_name: str, new_doc_id: str) -> str:
    name = clean(file_name)
    if not name:
        return f"{new_doc_id}.pdf"
    p = Path(name)
    suffix = p.suffix if p.suffix else ".pdf"
    stem = p.stem
    if DOC_ID_RE.search(stem):
        stem = DOC_ID_RE.sub(new_doc_id, stem)
    else:
        stem = f"{stem}__{new_doc_id}"
    return f"{stem}{suffix}"


def build_max_doc_by_uf(df: pd.DataFrame) -> Dict[str, int]:
    max_by_uf: Dict[str, int] = defaultdict(int)
    for idx in df.index.tolist():
        uf = normalize_text(df.at[idx, "UF"])
        if not uf:
            continue
        doc = extract_doc_id_from_values(
            [
                clean(df.at[idx, "DOC_ID"]),
                clean(df.at[idx, "NOME_ARQUIVO_LOCAL"]),
                clean(df.at[idx, "CAMINHO_ARQUIVO_LOCAL"]),
            ]
        )
        if not doc:
            continue
        try:
            number = int(doc.replace("DOC", ""))
        except Exception:
            continue
        if number > max_by_uf[uf]:
            max_by_uf[uf] = number
    return max_by_uf


def alloc_next_doc_id(max_by_uf: Dict[str, int], uf: str) -> str:
    current = max_by_uf.get(uf, 0)
    current += 1
    max_by_uf[uf] = current
    return f"DOC{current:04d}"


def score_state_row(row: pd.Series) -> int:
    score = 0
    status = clean(row.get("STATUS_LINK", "")).upper()
    score += status_rank(status) * 3
    if has_http(row.get("URL_DOWNLOAD_PDF", "")):
        score += 4
    if has_http(row.get("URL_FONTE", "")):
        score += 2
    if clean(row.get("HASH_OU_ID_PDF_CANONICO", "")):
        score += 3
    if clean(row.get("CAMINHO_ARQUIVO_LOCAL", "")):
        score += 2
    if clean(row.get("NOME_ARQUIVO_LOCAL", "")):
        score += 1
    if clean(row.get("EVIDENCIA_MINIMA", "")):
        score += 1
    if clean(row.get("OBS", "")):
        score += 1
    return score


def choose_best_state_row(group: pd.DataFrame) -> pd.Series:
    if len(group) == 1:
        return group.iloc[0]
    scored = group.copy()
    scored["__SCORE"] = scored.apply(score_state_row, axis=1)
    scored = scored.sort_values(by=["__SCORE"], ascending=False)
    return scored.iloc[0]


def should_take_state_value(col: str, old: str, new: str) -> bool:
    old = clean(old)
    new = clean(new)

    if not new:
        return False

    if col in URL_COLS:
        if is_placeholder(old) and not is_placeholder(new):
            return True
        if not has_http(old) and has_http(new):
            return True
        return False

    if col == "STATUS_LINK":
        old_s = clean(old).upper()
        new_s = clean(new).upper()
        if old_s in OK_STATUSES:
            return False
        if old_s == "HTML_INTERMEDIARIO" and new_s == "NAO_ENCONTRADO":
            return False
        return status_rank(new_s) > status_rank(old_s)

    if col in TEXT_PREF_LONGER_COLS:
        if is_placeholder(old) and not is_placeholder(new):
            return True
        return len(new) > len(old) and len(new) >= 60

    if col in FILE_COLS:
        return not old and bool(new)

    if is_placeholder(old) and not is_placeholder(new):
        return True

    return False


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def choose_status_for_existing_file(current_status: str) -> str:
    status = clean(current_status).upper()
    if status in OK_STATUSES:
        return status
    return "OK_PDF_MANUAL"


def ensure_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df


def build_pdf_indexes(pdf_root: Path) -> Tuple[Dict[str, str], Dict[str, List[Path]], Dict[Tuple[str, str], List[Path]]]:
    path_hash_cache: Dict[str, str] = {}
    hash_to_paths: Dict[str, List[Path]] = defaultdict(list)
    uf_name_to_paths: Dict[Tuple[str, str], List[Path]] = defaultdict(list)

    for pdf in sorted(pdf_root.rglob("*.pdf")):
        try:
            file_hash = sha256_file(pdf)
        except Exception:
            continue
        path_hash_cache[str(pdf)] = file_hash
        hash_to_paths[file_hash].append(pdf)
        uf = normalize_text(pdf.parent.name)
        uf_name_to_paths[(uf, normalize_text(pdf.name))].append(pdf)

    return path_hash_cache, hash_to_paths, uf_name_to_paths


def reconcile_main(args: argparse.Namespace) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    root = Path(args.root)
    main_path = root / "output_csv" / "mapeamento_ppc_polos.csv"
    per_state_dir = root / "output_csv" / "por_estado"
    pdf_root = root / "pdfs_baixados"

    if not main_path.exists():
        raise FileNotFoundError(f"CSV principal nao encontrado: {main_path}")
    if not per_state_dir.exists():
        raise FileNotFoundError(f"Diretorio por_estado nao encontrado: {per_state_dir}")

    main = pd.read_csv(main_path, dtype=str, encoding="utf-8-sig").fillna("")
    original_columns = list(main.columns)
    main = ensure_columns(main, original_columns)

    state_files = sorted(per_state_dir.glob("mapeamento_ppc_polos_*.csv"))
    if not state_files:
        raise RuntimeError("Nenhum CSV por estado encontrado.")

    state_frames: List[pd.DataFrame] = []
    for file in state_files:
        df = pd.read_csv(file, dtype=str, encoding="utf-8-sig").fillna("")
        df = ensure_columns(df, original_columns)
        df["__SRC_FILE"] = file.name
        state_frames.append(df)

    states = pd.concat(state_frames, ignore_index=True)

    main["__KEY"] = build_key_columns(main)
    states["__KEY"] = build_key_columns(states)

    # Choose one best row per key from per-state source.
    state_by_key: Dict[str, pd.Series] = {}
    for key, group in states.groupby("__KEY", dropna=False):
        best = choose_best_state_row(group)
        state_by_key[str(key)] = best

    changes: List[dict] = []
    conflicts: List[dict] = []

    # Merge non-destructively: preserve main and use per-state to fill or improve.
    for idx in main.index.tolist():
        key = main.at[idx, "__KEY"]
        state_row = state_by_key.get(str(key))
        if state_row is None:
            continue

        src_file = clean(state_row.get("__SRC_FILE", ""))
        for col in original_columns:
            if col in IMMUTABLE_IDENTITY_COLS:
                continue
            if col == "DOC_ID":
                # DOC_ID is maintained by principal/app/pdf reconciliation, not by per-state.
                continue

            old_value = clean(main.at[idx, col])
            new_value = clean(state_row.get(col, ""))

            if should_take_state_value(col, old_value, new_value):
                main.at[idx, col] = new_value
                changes.append(
                    {
                        "ORIGEM": "POR_ESTADO",
                        "IDX_MAIN": idx,
                        "CHAVE": key,
                        "COLUNA": col,
                        "VALOR_ANTIGO": old_value,
                        "VALOR_NOVO": new_value,
                        "ARQUIVO_ORIGEM": src_file,
                    }
                )

    # Build PDF indexes.
    path_hash_cache, hash_to_paths, uf_name_to_paths = build_pdf_indexes(pdf_root)

    # Reconcile file path/name/hash/doc with existing acervo.
    for idx in main.index.tolist():
        uf = normalize_text(main.at[idx, "UF"])
        path_txt = clean(main.at[idx, "CAMINHO_ARQUIVO_LOCAL"])
        name_txt = clean(main.at[idx, "NOME_ARQUIVO_LOCAL"])
        hash_txt = clean(main.at[idx, "HASH_OU_ID_PDF_CANONICO"]).upper()

        resolved_path: Path | None = None

        if path_txt and Path(path_txt).exists():
            resolved_path = Path(path_txt)
        elif uf and name_txt:
            candidates = uf_name_to_paths.get((uf, normalize_text(name_txt)), [])
            if candidates:
                resolved_path = sorted(candidates, key=lambda p: str(p))[0]
        elif hash_txt and hash_txt in hash_to_paths:
            resolved_path = sorted(hash_to_paths[hash_txt], key=lambda p: str(p))[0]

        if resolved_path is not None:
            resolved_path_txt = str(resolved_path)
            resolved_name = resolved_path.name
            resolved_hash = path_hash_cache.get(str(resolved_path), "")

            if path_txt != resolved_path_txt:
                changes.append(
                    {
                        "ORIGEM": "PDF_ACERVO",
                        "IDX_MAIN": idx,
                        "CHAVE": main.at[idx, "__KEY"],
                        "COLUNA": "CAMINHO_ARQUIVO_LOCAL",
                        "VALOR_ANTIGO": path_txt,
                        "VALOR_NOVO": resolved_path_txt,
                        "ARQUIVO_ORIGEM": "pdfs_baixados",
                    }
                )
                main.at[idx, "CAMINHO_ARQUIVO_LOCAL"] = resolved_path_txt

            if name_txt != resolved_name:
                changes.append(
                    {
                        "ORIGEM": "PDF_ACERVO",
                        "IDX_MAIN": idx,
                        "CHAVE": main.at[idx, "__KEY"],
                        "COLUNA": "NOME_ARQUIVO_LOCAL",
                        "VALOR_ANTIGO": name_txt,
                        "VALOR_NOVO": resolved_name,
                        "ARQUIVO_ORIGEM": "pdfs_baixados",
                    }
                )
                main.at[idx, "NOME_ARQUIVO_LOCAL"] = resolved_name

            if resolved_hash and hash_txt != resolved_hash:
                changes.append(
                    {
                        "ORIGEM": "PDF_ACERVO",
                        "IDX_MAIN": idx,
                        "CHAVE": main.at[idx, "__KEY"],
                        "COLUNA": "HASH_OU_ID_PDF_CANONICO",
                        "VALOR_ANTIGO": hash_txt,
                        "VALOR_NOVO": resolved_hash,
                        "ARQUIVO_ORIGEM": "pdfs_baixados",
                    }
                )
                main.at[idx, "HASH_OU_ID_PDF_CANONICO"] = resolved_hash

            status_old = clean(main.at[idx, "STATUS_LINK"]).upper()
            status_new = choose_status_for_existing_file(status_old)
            if status_old != status_new:
                changes.append(
                    {
                        "ORIGEM": "PDF_ACERVO",
                        "IDX_MAIN": idx,
                        "CHAVE": main.at[idx, "__KEY"],
                        "COLUNA": "STATUS_LINK",
                        "VALOR_ANTIGO": status_old,
                        "VALOR_NOVO": status_new,
                        "ARQUIVO_ORIGEM": "pdfs_baixados",
                    }
                )
                main.at[idx, "STATUS_LINK"] = status_new

        # Normalize DOC_ID using available hints.
        doc_old = clean(main.at[idx, "DOC_ID"])
        doc_new = extract_doc_id_from_values(
            [
                doc_old,
                clean(main.at[idx, "NOME_ARQUIVO_LOCAL"]),
                clean(main.at[idx, "CAMINHO_ARQUIVO_LOCAL"]),
            ]
        )
        if doc_new and normalize_doc_id(doc_old) != doc_new:
            changes.append(
                {
                    "ORIGEM": "DOC_ID_NORMALIZACAO",
                    "IDX_MAIN": idx,
                    "CHAVE": main.at[idx, "__KEY"],
                    "COLUNA": "DOC_ID",
                    "VALOR_ANTIGO": doc_old,
                    "VALOR_NOVO": doc_new,
                    "ARQUIVO_ORIGEM": "main+arquivo",
                }
            )
            main.at[idx, "DOC_ID"] = doc_new

    # Force same DOC_ID for same hash within same UF.
    grouped_hash = defaultdict(list)
    for idx in main.index.tolist():
        uf = normalize_text(main.at[idx, "UF"])
        hash_value = clean(main.at[idx, "HASH_OU_ID_PDF_CANONICO"]).upper()
        if uf and hash_value:
            grouped_hash[(uf, hash_value)].append(idx)

    for (uf, hash_value), indices in grouped_hash.items():
        docs = [normalize_doc_id(main.at[i, "DOC_ID"]) for i in indices if normalize_doc_id(main.at[i, "DOC_ID"])]
        if docs:
            canonical_doc = Counter(docs).most_common(1)[0][0]
        else:
            inferred = []
            for i in indices:
                inferred_doc = extract_doc_id_from_values(
                    [
                        clean(main.at[i, "NOME_ARQUIVO_LOCAL"]),
                        clean(main.at[i, "CAMINHO_ARQUIVO_LOCAL"]),
                    ]
                )
                if inferred_doc:
                    inferred.append(inferred_doc)
            canonical_doc = Counter(inferred).most_common(1)[0][0] if inferred else ""

        if not canonical_doc:
            continue

        for i in indices:
            current_doc = normalize_doc_id(main.at[i, "DOC_ID"])
            if current_doc != canonical_doc:
                changes.append(
                    {
                        "ORIGEM": "DOC_ID_POR_HASH",
                        "IDX_MAIN": i,
                        "CHAVE": main.at[i, "__KEY"],
                        "COLUNA": "DOC_ID",
                        "VALOR_ANTIGO": clean(main.at[i, "DOC_ID"]),
                        "VALOR_NOVO": canonical_doc,
                        "ARQUIVO_ORIGEM": "grupo_hash",
                    }
                )
                main.at[i, "DOC_ID"] = canonical_doc

    # Resolve conflicts: same UF+DOC_ID tied to multiple hashes.
    if args.resolve_doc_conflicts:
        max_doc_by_uf = build_max_doc_by_uf(main)
        grouped_doc_hash = defaultdict(lambda: defaultdict(list))

        for idx in main.index.tolist():
            uf = normalize_text(main.at[idx, "UF"])
            doc = normalize_doc_id(main.at[idx, "DOC_ID"])
            hash_value = clean(main.at[idx, "HASH_OU_ID_PDF_CANONICO"]).upper()
            if uf and doc and hash_value:
                grouped_doc_hash[(uf, doc)][hash_value].append(idx)

        for (uf, doc), hash_map in sorted(grouped_doc_hash.items()):
            if len(hash_map) <= 1:
                continue

            ordered_hash_groups = sorted(hash_map.items(), key=lambda kv: (-len(kv[1]), kv[0]))
            # Keep current DOC_ID in the largest group and split the remaining groups.
            for hash_value, idx_list in ordered_hash_groups[1:]:
                new_doc = alloc_next_doc_id(max_doc_by_uf, uf)

                for i in idx_list:
                    old_doc_value = clean(main.at[i, "DOC_ID"])
                    if normalize_doc_id(old_doc_value) != new_doc:
                        main.at[i, "DOC_ID"] = new_doc
                        changes.append(
                            {
                                "ORIGEM": "DOC_ID_SPLIT_HASH",
                                "IDX_MAIN": i,
                                "CHAVE": main.at[i, "__KEY"],
                                "COLUNA": "DOC_ID",
                                "VALOR_ANTIGO": old_doc_value,
                                "VALOR_NOVO": new_doc,
                                "ARQUIVO_ORIGEM": f"UF={uf}|DOC={doc}|HASH={hash_value}",
                            }
                        )

                unique_paths = sorted(
                    {
                        clean(main.at[i, "CAMINHO_ARQUIVO_LOCAL"])
                        for i in idx_list
                        if clean(main.at[i, "CAMINHO_ARQUIVO_LOCAL"])
                    }
                )

                for old_path_txt in unique_paths:
                    old_path = Path(old_path_txt)
                    if not old_path.exists():
                        continue

                    proposed_name = replace_doc_id_in_filename(old_path.name, new_doc)
                    new_path = old_path.with_name(proposed_name)

                    if str(new_path) != str(old_path) and new_path.exists():
                        counter = 1
                        while True:
                            candidate_name = f"{new_path.stem}__docfix{counter}{new_path.suffix}"
                            candidate_path = new_path.with_name(candidate_name)
                            if not candidate_path.exists():
                                new_path = candidate_path
                                break
                            counter += 1

                    if str(new_path) != str(old_path):
                        old_path.rename(new_path)

                        affected_indices = [
                            j
                            for j in main.index.tolist()
                            if clean(main.at[j, "CAMINHO_ARQUIVO_LOCAL"]) == old_path_txt
                        ]
                        for j in affected_indices:
                            old_path_value = clean(main.at[j, "CAMINHO_ARQUIVO_LOCAL"])
                            old_name_value = clean(main.at[j, "NOME_ARQUIVO_LOCAL"])

                            main.at[j, "CAMINHO_ARQUIVO_LOCAL"] = str(new_path)
                            main.at[j, "NOME_ARQUIVO_LOCAL"] = new_path.name

                            if old_path_value != str(new_path):
                                changes.append(
                                    {
                                        "ORIGEM": "FILE_RENAME_DOC_ID",
                                        "IDX_MAIN": j,
                                        "CHAVE": main.at[j, "__KEY"],
                                        "COLUNA": "CAMINHO_ARQUIVO_LOCAL",
                                        "VALOR_ANTIGO": old_path_value,
                                        "VALOR_NOVO": str(new_path),
                                        "ARQUIVO_ORIGEM": "rename_by_doc_split",
                                    }
                                )

                            if old_name_value != new_path.name:
                                changes.append(
                                    {
                                        "ORIGEM": "FILE_RENAME_DOC_ID",
                                        "IDX_MAIN": j,
                                        "CHAVE": main.at[j, "__KEY"],
                                        "COLUNA": "NOME_ARQUIVO_LOCAL",
                                        "VALOR_ANTIGO": old_name_value,
                                        "VALOR_NOVO": new_path.name,
                                        "ARQUIVO_ORIGEM": "rename_by_doc_split",
                                    }
                                )

                for i in idx_list:
                    current_name = clean(main.at[i, "NOME_ARQUIVO_LOCAL"])
                    if not current_name:
                        continue
                    normalized_name_doc = normalize_doc_id(current_name)
                    if normalized_name_doc and normalized_name_doc != new_doc:
                        new_name_value = replace_doc_id_in_filename(current_name, new_doc)
                        if new_name_value != current_name:
                            main.at[i, "NOME_ARQUIVO_LOCAL"] = new_name_value
                            changes.append(
                                {
                                    "ORIGEM": "DOC_ID_SPLIT_HASH",
                                    "IDX_MAIN": i,
                                    "CHAVE": main.at[i, "__KEY"],
                                    "COLUNA": "NOME_ARQUIVO_LOCAL",
                                    "VALOR_ANTIGO": current_name,
                                    "VALOR_NOVO": new_name_value,
                                    "ARQUIVO_ORIGEM": f"UF={uf}|DOC={doc}|HASH={hash_value}",
                                }
                            )

    # Final pass: ensure no invalid path remains when it can be resolved by hash/name.
    path_hash_cache, hash_to_paths, uf_name_to_paths = build_pdf_indexes(pdf_root)

    for idx in main.index.tolist():
        uf = normalize_text(main.at[idx, "UF"])
        path_txt = clean(main.at[idx, "CAMINHO_ARQUIVO_LOCAL"])
        name_txt = clean(main.at[idx, "NOME_ARQUIVO_LOCAL"])
        hash_txt = clean(main.at[idx, "HASH_OU_ID_PDF_CANONICO"]).upper()

        if path_txt and Path(path_txt).exists():
            continue

        resolved_path: Path | None = None

        if hash_txt and hash_txt in hash_to_paths:
            candidates = hash_to_paths[hash_txt]
            if uf:
                by_uf = [p for p in candidates if normalize_text(p.parent.name) == uf]
                if by_uf:
                    candidates = by_uf
            resolved_path = sorted(candidates, key=lambda p: str(p))[0]
        elif uf and name_txt:
            candidates = uf_name_to_paths.get((uf, normalize_text(name_txt)), [])
            if candidates:
                resolved_path = sorted(candidates, key=lambda p: str(p))[0]

        if resolved_path is not None:
            resolved_path_txt = str(resolved_path)
            resolved_name = resolved_path.name
            resolved_hash = path_hash_cache.get(resolved_path_txt, "")

            if path_txt != resolved_path_txt:
                main.at[idx, "CAMINHO_ARQUIVO_LOCAL"] = resolved_path_txt
                changes.append(
                    {
                        "ORIGEM": "POST_RESOLVE_PATH",
                        "IDX_MAIN": idx,
                        "CHAVE": main.at[idx, "__KEY"],
                        "COLUNA": "CAMINHO_ARQUIVO_LOCAL",
                        "VALOR_ANTIGO": path_txt,
                        "VALOR_NOVO": resolved_path_txt,
                        "ARQUIVO_ORIGEM": "pdfs_baixados",
                    }
                )

            if name_txt != resolved_name:
                main.at[idx, "NOME_ARQUIVO_LOCAL"] = resolved_name
                changes.append(
                    {
                        "ORIGEM": "POST_RESOLVE_PATH",
                        "IDX_MAIN": idx,
                        "CHAVE": main.at[idx, "__KEY"],
                        "COLUNA": "NOME_ARQUIVO_LOCAL",
                        "VALOR_ANTIGO": name_txt,
                        "VALOR_NOVO": resolved_name,
                        "ARQUIVO_ORIGEM": "pdfs_baixados",
                    }
                )

            if resolved_hash and hash_txt != resolved_hash:
                main.at[idx, "HASH_OU_ID_PDF_CANONICO"] = resolved_hash
                changes.append(
                    {
                        "ORIGEM": "POST_RESOLVE_PATH",
                        "IDX_MAIN": idx,
                        "CHAVE": main.at[idx, "__KEY"],
                        "COLUNA": "HASH_OU_ID_PDF_CANONICO",
                        "VALOR_ANTIGO": hash_txt,
                        "VALOR_NOVO": resolved_hash,
                        "ARQUIVO_ORIGEM": "pdfs_baixados",
                    }
                )
        elif path_txt:
            main.at[idx, "CAMINHO_ARQUIVO_LOCAL"] = ""
            changes.append(
                {
                    "ORIGEM": "POST_RESOLVE_PATH",
                    "IDX_MAIN": idx,
                    "CHAVE": main.at[idx, "__KEY"],
                    "COLUNA": "CAMINHO_ARQUIVO_LOCAL",
                    "VALOR_ANTIGO": path_txt,
                    "VALOR_NOVO": "",
                    "ARQUIVO_ORIGEM": "path_invalido_limpo",
                }
            )

    # Build conflict report: same UF+DOC_ID with multiple hashes.
    grouped_doc = defaultdict(set)
    for idx in main.index.tolist():
        uf = normalize_text(main.at[idx, "UF"])
        doc = normalize_doc_id(main.at[idx, "DOC_ID"])
        h = clean(main.at[idx, "HASH_OU_ID_PDF_CANONICO"]).upper()
        if uf and doc and h:
            grouped_doc[(uf, doc)].add(h)

    for (uf, doc), hashes in sorted(grouped_doc.items()):
        if len(hashes) > 1:
            conflicts.append(
                {
                    "TIPO": "DOC_ID_COM_MULTIPLOS_HASHES",
                    "UF": uf,
                    "DOC_ID": doc,
                    "QTD_HASHES": len(hashes),
                    "HASHES": " | ".join(sorted(hashes)),
                }
            )

    # Build conflict report: same hash with multiple file names.
    grouped_name = defaultdict(set)
    for idx in main.index.tolist():
        h = clean(main.at[idx, "HASH_OU_ID_PDF_CANONICO"]).upper()
        n = clean(main.at[idx, "NOME_ARQUIVO_LOCAL"])
        if h and n:
            grouped_name[h].add(n)

    for h, names in sorted(grouped_name.items()):
        if len(names) > 1:
            conflicts.append(
                {
                    "TIPO": "HASH_COM_MULTIPLOS_NOMES",
                    "UF": "",
                    "DOC_ID": "",
                    "QTD_HASHES": 1,
                    "HASHES": h,
                    "DETALHE": " | ".join(sorted(names)),
                }
            )

    # Keep original column order only.
    main = main[original_columns]

    changes_df = pd.DataFrame(changes)
    conflicts_df = pd.DataFrame(conflicts)

    return main, changes_df, conflicts_df


def main_cli() -> int:
    parser = argparse.ArgumentParser(description="Reconciliar mapeamento principal com por_estado e acervo de PDFs.")
    parser.add_argument(
        "--root",
        default=r"C:\Users\augus\Music\TCC\Data\new_date",
        help="Raiz new_date",
    )
    parser.add_argument(
        "--no-resolve-doc-conflicts",
        action="store_true",
        help="Nao separar DOC_ID com hashes diferentes.",
    )
    parser.add_argument("--apply", action="store_true", help="Aplicar alteracoes no CSV principal")
    args = parser.parse_args()
    args.resolve_doc_conflicts = not args.no_resolve_doc_conflicts

    root = Path(args.root)
    out_dir = root / "output_csv" / "reconcile_logs"
    out_dir.mkdir(parents=True, exist_ok=True)

    main_path = root / "output_csv" / "mapeamento_ppc_polos.csv"
    before = pd.read_csv(main_path, dtype=str, encoding="utf-8-sig").fillna("")
    before_rows = len(before)

    reconciled, changes_df, conflicts_df = reconcile_main(args)

    if len(reconciled) != before_rows:
        raise RuntimeError(
            f"Seguranca: quantidade de linhas alterou indevidamente ({before_rows} -> {len(reconciled)})."
        )

    ts = now_stamp()
    preview_path = out_dir / f"mapeamento_ppc_polos_PREVIEW_{ts}.csv"
    changes_path = out_dir / f"reconcile_changes_{ts}.csv"
    conflicts_path = out_dir / f"reconcile_conflicts_{ts}.csv"

    reconciled.to_csv(preview_path, index=False, encoding="utf-8-sig")
    changes_df.to_csv(changes_path, index=False, encoding="utf-8-sig")
    conflicts_df.to_csv(conflicts_path, index=False, encoding="utf-8-sig")

    print(f"PREVIEW_GERADO={preview_path}")
    print(f"CHANGES_GERADO={changes_path}")
    print(f"CONFLICTS_GERADO={conflicts_path}")
    print(f"MAIN_ROWS={before_rows}")
    print(f"CHANGED_CELLS={len(changes_df)}")
    print(f"CONFLICT_ITEMS={len(conflicts_df)}")

    if args.apply:
        backup_path = root / "output_csv" / f"mapeamento_ppc_polos_PRE_RECONCILE_{ts}.csv"
        before.to_csv(backup_path, index=False, encoding="utf-8-sig")
        reconciled.to_csv(main_path, index=False, encoding="utf-8-sig")
        print(f"BACKUP_GERADO={backup_path}")
        print(f"MAIN_ATUALIZADO={main_path}")
    else:
        print("MODO_DRY_RUN=1")

    return 0


if __name__ == "__main__":
    raise SystemExit(main_cli())

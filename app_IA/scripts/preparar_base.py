from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
APP_ROOT = SCRIPT_PATH.parent.parent

if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from core import discover_paths, list_available_ufs, prepare_base  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepara base de documentos PDF e vinculos de campus para o app NotebookLM."
    )
    parser.add_argument(
        "--ufs",
        nargs="+",
        default=None,
        help="Lista de UFs para preparar (exemplo: --ufs AL BA PI). Se vazio, usa todas disponiveis.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = discover_paths(APP_ROOT)

    available = list_available_ufs(paths.pdf_root)
    if not available:
        print("Nenhuma UF encontrada em pdfs_baixados.")
        return 1

    if args.ufs:
        requested = [uf.upper() for uf in args.ufs]
        missing = [uf for uf in requested if uf not in available]
        if missing:
            print(f"UFs sem pasta em pdfs_baixados: {', '.join(missing)}")
        target = [uf for uf in requested if uf in available]
    else:
        target = available

    if not target:
        print("Nenhuma UF valida para processar.")
        return 1

    result = prepare_base(paths, target)
    print("Base preparada com sucesso.")
    print(f"Total documentos: {result['base_total']}")
    print(f"Total vinculos: {result['vinculos_total']}")
    for row in result["resumo_ufs"]:
        print(f"UF={row['UF']} PDFs={row['QTD_PDFS']} Vinculos={row['QTD_VINCULOS_TOTAL']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

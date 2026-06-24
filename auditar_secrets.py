#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script utilitário para Auditoria e Higienização de Repositório (Open Science)
Busca por chaves de API, senhas, tokens e credenciais confidenciais.
"""

import os
import re
import sys

# Diretórios a ignorar completamente durante a varredura
IGNORE_DIRS = {
    '.git',
    '.venv',
    '.venv-1',
    'venv',
    '__pycache__',
    '.vscode',
    '.idea',
    '.ipynb_checkpoints',
    'BACKUPS',
    'arquivo_morto',
    'pdfs_baixados'
}

# Extensões de arquivos binários ou grandes a ignorar
IGNORE_EXTS = {
    '.zip', '.rar', '.7z', '.pdf', '.docx', '.xlsx', '.pptx', '.png', 
    '.jpg', '.jpeg', '.gif', '.mp3', '.mp4', '.avi', '.pyc', '.pyd'
}

# Expressões regulares para busca de segredos
SECRET_PATTERNS = {
    "Perplexity API Key": re.compile(r'\bpplx-[a-zA-Z0-9]{48,}\b'),
    "OpenAI API Key": re.compile(r'\bsk-[a-zA-Z0-9]{48,}\b'),
    "OpenAI Project API Key": re.compile(r'\bsk-proj-[a-zA-Z0-9]{48,}\b'),
    "Generic Private Key / Token": re.compile(r'\b(?:key|token|secret|password|passwd|senha)\s*=\s*[\'"][a-zA-Z0-9_\-\.\@\#\$\%\&\*]{16,}[\'"]', re.IGNORECASE),
    "Slack Webhook": re.compile(r'https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+'),
    "GitHub Token": re.compile(r'\bgh[hsro]_[a-zA-Z0-9]{36,}\b'),
    "AWS Access Key": re.compile(r'\bAKIA[0-9A-Z]{16}\b'),
}

def scan_file(file_path):
    """Varre um arquivo individual linha por linha procurando credenciais."""
    findings = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_idx, line in enumerate(f, 1):
                clean_line = line.strip()
                # Pula linhas vazias ou comentários óbvios que não contenham chaves
                if not clean_line or clean_line.startswith('#') and 'key' not in clean_line.lower():
                    continue
                
                for pattern_name, regex in SECRET_PATTERNS.items():
                    matches = regex.findall(clean_line)
                    for match in matches:
                        # Ofuscar a chave no terminal por segurança
                        ofuscado = match[:10] + "..." + match[-6:] if len(match) > 16 else "***"
                        findings.append({
                            "line": line_idx,
                            "type": pattern_name,
                            "value": ofuscado,
                            "raw_line": clean_line[:120] + ("..." if len(clean_line) > 120 else "")
                        })
    except Exception as e:
        print(f"Erro ao ler {file_path}: {e}", file=sys.stderr)
    return findings

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print("=" * 80)
    print(f"Iniciando auditoria preventiva de segredos em: {root_dir}")
    print(f"Diretórios ignorados: {', '.join(IGNORE_DIRS)}")
    print(f"Extensões ignoradas: {', '.join(IGNORE_EXTS)}")
    print("=" * 80)
    
    total_files_scanned = 0
    total_findings = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modifica dirnames in-place para que o os.walk não entre em diretórios ignorados
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in IGNORE_EXTS:
                continue
            
            # Não varrer o próprio script de auditoria para evitar falsos positivos
            if filename == os.path.basename(__file__):
                continue
                
            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, root_dir)
            
            findings = scan_file(file_path)
            total_files_scanned += 1
            
            if findings:
                print(f"\n[ALERTA] Suspeita de segredo em: {rel_path}")
                for find in findings:
                    print(f"  └─ Linha {find['line']} | Tipo: {find['type']} | Valor: {find['value']}")
                    print(f"     Trecho: {find['raw_line']}")
                    total_findings += 1

    print("\n" + "=" * 80)
    print("AUDITORIA CONCLUÍDA")
    print(f"Total de arquivos texto varridos: {total_files_scanned}")
    if total_findings == 0:
        print("\033[92m[SUCESSO] Nenhum segredo óbvio ou chave de API foi encontrado! O projeto parece seguro para publicação.\033[0m")
        sys.exit(0)
    else:
        print(f"\033[91m[ATENÇÃO] Foram encontrados {total_findings} potenciais vazamentos de credenciais!\033[0m")
        print("Revise as linhas listadas acima antes de realizar qualquer commit público.")
        sys.exit(1)

if __name__ == "__main__":
    main()

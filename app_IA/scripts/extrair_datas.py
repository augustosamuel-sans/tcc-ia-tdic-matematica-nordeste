import pandas as pd
import fitz  # PyMuPDF
import re
from pathlib import Path
from collections import Counter

base_dir = Path('C:/Users/augus/Music/TCC/Data')
analyse_dir = base_dir / 'new_date' / 'Analyse_IA'
pdf_folder = base_dir / 'new_date' / 'pdfs_baixados'

csv_path = analyse_dir / 'Resposta_csv' / 'analise_notebooklm_consolidado.csv'
out_path = analyse_dir / 'Relatorios' / 'RELATORIO_TEMPORAL_CRUZADO.csv'

df = pd.read_csv(csv_path)
df = df[df['UF'] != 'UF'].copy() # limpar cabeçalhos

def extract_year_from_pdf(filepath):
    """Lê as 3 primeiras páginas e tenta achar o ano de aprovação."""
    if not Path(filepath).exists():
        return 'ARQUIVO_FALTANDO'
        
    try:
        doc = fitz.open(filepath)
        text = ""
        # Ler apenas as primeiras 4 páginas
        for page in doc.pages(0, min(4, len(doc))):
            text += page.get_text("text") + " "
            
        doc.close()
        
        # Estratégia 1: Regex buscando 20XX ou 19XX na capa
        years_found = re.findall(r'\b(199[0-9]|200[0-9]|201[0-9]|202[0-6])\b', text)
        if years_found:
            # Pega o ano que mais repete nas primeiras páginas (geralmente o correto)
            most_common = Counter(years_found).most_common(1)[0][0]
            return most_common
            
        return 'SEM_ANO_TEXTUAL'
        
    except Exception as e:
        return 'ERRO_LEITURA'

print('⏳ Extraindo anos dos 96 PDFs... Isso pode levar alguns segundos.')
extracted_years = []

for _, row in df.iterrows():
    pdf_filename = row['NOME_ARQUIVO_LOCAL']
    uf = row['UF']
    full_path = pdf_folder / uf / pdf_filename
    year = extract_year_from_pdf(full_path)
    extracted_years.append(year)

df['ANO_EXTRAIDO'] = extracted_years

# Garantir conversão das colunas chaves
df['NIVEL_TDIC'] = pd.to_numeric(df['NIVEL_INTEGRACAO_0_1_2_3'], errors='coerce')
df['TEM_IA'] = pd.to_numeric(df['PRESENCA_IA_0_1'], errors='coerce')

# Salvar
cols = ['UF', 'DOC_ID', 'ANO_EXTRAIDO', 'MODALIDADE_PDF', 'NIVEL_TDIC', 'TEM_IA', 'IES_PDF']
df[cols].to_csv(out_path, index=False, encoding='utf-8-sig')

print(f'✅ Extração concluída! Salvo em: {out_path}')

# Gerar insight rápido
print('\n=== LINHA DO TEMPO DA PRESENÇA DE IA ===')
df_ia = df[df['TEM_IA'] == 1]
for _, r in df_ia.iterrows():
    print(f"{r['ANO_EXTRAIDO']} - [Nível {r['NIVEL_TDIC']}] {r['IES_PDF']} ({r['UF']})")

print('\n=== DECADÊNCIA NO EAD (EaD com nível 0) ===')
df_ead0 = df[(df['NIVEL_TDIC'] == 0) & (df['MODALIDADE_PDF'].str.upper() == 'EAD')]
for _, r in df_ead0.iterrows():
    print(f"De {r['ANO_EXTRAIDO']} -> {r['IES_PDF']} ({r['UF']})")

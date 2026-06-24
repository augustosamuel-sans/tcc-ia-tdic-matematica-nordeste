import pandas as pd
from pathlib import Path
from datetime import datetime

base_dir = Path('C:/Users/augus/Music/TCC/Data/new_date/Analyse_IA')
df = pd.read_csv(base_dir / 'Resposta_csv/analise_notebooklm_consolidado.csv')
df = df[df['UF'] != 'UF'] # remove duplicated headers

report_path = base_dir / 'Relatorios/RELATORIO_CONSOLIDADO_FINAL.md'
report_path.parent.mkdir(exist_ok=True, parents=True)

with open(report_path, 'w', encoding='utf-8') as f:
    f.write('# Relatório Consolidado de Análise - Projetos Pedagógicos de Curso (PPC)\n\n')
    
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    f.write(f'*Gerado em: {current_time}*\n\n')
    
    total_docs = len(df)
    f.write('## 1. Visão Geral\n')
    f.write(f'- **Total de Documentos Analisados:** {total_docs}\n')
    
    uf_counts = df['UF'].value_counts()
    f.write('- **Distribuição por Estado:**\n')
    for uf, count in uf_counts.items():
        f.write(f'  - **{uf}**: {count} documentos\n')
    f.write('\n')
    
    f.write('## 2. Presença de TDIC e IA\n')
    tdic_count = pd.to_numeric(df['PRESENCA_TDIC_0_1'], errors='coerce').sum()
    ia_count = pd.to_numeric(df['PRESENCA_IA_0_1'], errors='coerce').sum()
    etica_count = pd.to_numeric(df['DIMENSAO_ETICA_IA_0_1'], errors='coerce').sum()
    
    total_docs_valid = df['PRESENCA_TDIC_0_1'].replace('PRESENCA_TDIC_0_1', pd.NA).dropna().shape[0]
    
    f.write(f'- **PPCs com menção a TDIC:** {tdic_count:.0f} ({(tdic_count/total_docs_valid*100):.1f}%)\n')
    f.write(f'- **PPCs com menção a Inteligência Artificial (IA):** {ia_count:.0f} ({(ia_count/total_docs_valid*100):.1f}%)\n')
    f.write(f'- **PPCs com Dimensão Ética da IA:** {etica_count:.0f} ({(etica_count/total_docs_valid*100):.1f}%)\n\n')
    
    f.write('## 3. Nível de Integração\n')
    nivel_counts = pd.to_numeric(df['NIVEL_INTEGRACAO_0_1_2_3'], errors='coerce').value_counts().sort_index()
    desc_niveis = {0: "0 - Nenhuma", 1: "1 - Básica/Instrumental", 2: "2 - Intermediária/Metodológica", 3: "3 - Avançada/Transformadora"}
    for nivel, count in nivel_counts.items():
        desc = desc_niveis.get(nivel, str(nivel))
        f.write(f'- **{desc}**: {count} documentos ({(count/total_docs_valid*100):.1f}%)\n')
    f.write('\n')

    f.write('## 4. Validação Humana\n')
    val_counts = df['STATUS_VALIDACAO_HUMANA'].value_counts()
    for status, count in val_counts.items():
        f.write(f'- **{status}**: {count} documentos\n')
    f.write('\n')
    
    f.write('## 5. Exemplos de Finalidade Pedagógica\n')
    sample_finalidade = df[df['FINALIDADE_PEDAGOGICA'].notna() & (df['FINALIDADE_PEDAGOGICA'] != '')]['FINALIDADE_PEDAGOGICA'].head(10)
    for fin in sample_finalidade:
        f.write(f'- {fin}\n')
    f.write('\n')

print("Relatorio gerado com sucesso em", report_path)
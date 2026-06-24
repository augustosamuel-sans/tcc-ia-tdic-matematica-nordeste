import pandas as pd
from pathlib import Path

base_dir = Path('C:/Users/augus/Music/TCC/Data/new_date/Analyse_IA')
df = pd.read_csv(base_dir / 'Resposta_csv/analise_notebooklm_consolidado.csv')

# Buscar os 2 PDFs com IA
ia_mask = pd.to_numeric(df['PRESENCA_IA_0_1'], errors='coerce') == 1
df_ia = df[ia_mask]

print('=' * 50)
print(f'ENCONTRADOS {len(df_ia)} DOCUMENTOS COM MENCÃO A IA')
print('=' * 50)
for _, row in df_ia.iterrows():
    print(f"ESTADO: {row['UF']}")
    print(f"DOC_ID: {row['DOC_ID']}")
    print(f"IES:    {row['IES_PDF']}")
    print(f"EVIDÊNCIA: {row['EVIDENCIA_LITERAL']}")
    print("-" * 50)

# Gerar relatórios detalhados por estado
for uf in df['UF'].dropna().unique():
    if uf == 'UF': continue # Ignorar cabeçalho duplicado
    
    df_uf = df[df['UF'] == uf]
    
    report_path = base_dir / f'Relatorios/RELATORIO_DETALHADO_{uf}.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f'# Relatório Detalhado de Análise PPC - Estado: {uf}\n\n')
        f.write(f'**Total de Documentos Analisados no {uf}:** {len(df_uf)}\n\n')
        
        # Estatísticas do estado
        tdic_count = pd.to_numeric(df_uf['PRESENCA_TDIC_0_1'], errors='coerce').sum()
        ia_count = pd.to_numeric(df_uf['PRESENCA_IA_0_1'], errors='coerce').sum()
        
        f.write('## 1. Estatísticas Rápidas\n')
        f.write(f'- PPCs com TDIC: {tdic_count:.0f}\n')
        f.write(f'- PPCs com IA: {ia_count:.0f}\n\n')
        
        f.write('## 2. Detalhamento por Documento\n\n')
        
        for index, row in df_uf.iterrows():
            f.write(f'### {row["DOC_ID"]} - {row.get("IES_PDF", "N/A")}\n')
            
            # Validação
            f.write(f'- **Status de Validação:** {row.get("STATUS_VALIDACAO_HUMANA", "N/A")}\n')
            
            # Nível
            nivel = str(row.get("NIVEL_INTEGRACAO_0_1_2_3", "N/A"))
            f.write(f'- **Nível de Integração:** {nivel}\n')
            
            # Finalidade Pedagógica
            fin = str(row.get("FINALIDADE_PEDAGOGICA", ""))
            if fin and fin.lower() != 'nan':
                f.write(f'- **Finalidade Pedagógica:** {fin}\n')
                
            # Estratégias Metodológicas
            est = str(row.get("ESTRATEGIAS_METODOLOGICAS", ""))
            if est and est.lower() != 'nan':
                f.write(f'- **Estratégias Metodológicas:** {est}\n')
                
            # Evidência Literal
            evi = str(row.get("EVIDENCIA_LITERAL", ""))
            if evi and evi.lower() != 'nan':
                f.write(f'> **Evidência Extraída:** "{evi[:500]}..."\n')
                
            f.write('\n---\n\n')
            
print("Relatórios detalhados gerados com sucesso na pasta Relatorios!")
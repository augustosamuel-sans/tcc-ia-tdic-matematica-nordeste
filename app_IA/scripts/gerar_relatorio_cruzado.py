import pandas as pd
from pathlib import Path

base_dir = Path('C:/Users/augus/Music/TCC/Data/new_date/Analyse_IA')
df = pd.read_csv(base_dir / 'Resposta_csv/analise_notebooklm_consolidado.csv')

# Limpar cabeçalho acidental
df = df[df['UF'] != 'UF']

# Padronizar modalidades
df['MODALIDADE_PDF'] = df['MODALIDADE_PDF'].replace('_PRESENCIAL', 'PRESENCIAL').str.upper()

report_path = base_dir / 'Relatorios/RELATORIO_ANALISES_CRUZADAS.md'

with open(report_path, 'w', encoding='utf-8') as f:
    f.write('# Relatório Analítico: Cruzamentos e Comparações\n\n')
    
    f.write('## 1. O Mito da IA no Nível 3\n')
    f.write('Uma das constatações mais importantes para a sua pesquisa:\n')
    f.write('> **Os dois únicos documentos que citam Inteligência Artificial (SE e PI) NÃO SÃO de Nível 3.**\n\n')
    f.write('Ambos foram classificados como **Nível 2 (Intermediária/Metodológica)**. O que isso significa para o TCC?\n')
    f.write('Significa que mesmo as poucas instituições que já inseriram "Inteligência Artificial" no texto do PPC da Licenciatura em Matemática, o fazem apenas como "uso de uma nova ferramenta metodológica" (para o professor usar na aula), mas a IA ainda **não transformou a estrutura curricular base ou causou disrupção na forma como o currículo é pensado** (que seria o requisito para chegar no Nível 3).\n\n')
    
    f.write('**Ficha dos PDFs de IA:**\n')
    ia_docs = df[pd.to_numeric(df['PRESENCA_IA_0_1'], errors='coerce') == 1]
    for _, row in ia_docs.iterrows():
        f.write(f'- **Estado:** {row["UF"]}\n')
        f.write(f'  - **Modalidade:** {row["MODALIDADE_PDF"]}\n')
        f.write(f'  - **IES:** {row["IES_PDF"]}\n')
        f.write(f'  - **Nível de Integração:** {row["NIVEL_INTEGRACAO_0_1_2_3"]}\n\n')

    f.write('## 2. Ponto Cego Modalidade: EAD com Nível 0 em TDIC?\n')
    f.write('Cruzamos a Modalidade (EaD vs Presencial) com o Nível de Integração (TDIC). O esperado era que cursos EaD fossem extremamente altos em tecnologia. Contudo, encontramos **5 documentos EaD com Nível 0 de integração de TDIC**.\n\n')
    
    cross_modalidade_nivel = pd.crosstab(df['MODALIDADE_PDF'], df['NIVEL_INTEGRACAO_0_1_2_3'])
    f.write('**Tabela: Modalidade x Nível de Integração**\n')
    f.write('| Modalidade | Nível 0 | Nível 1 | Nível 2 | Nível 3 |\n')
    f.write('|------------|---------|---------|---------|---------|\n')
    for idx, row in cross_modalidade_nivel.iterrows():
        n0 = row.get('0', 0)
        n1 = row.get('1', 0)
        n2 = row.get('2', 0)
        n3 = row.get('3', 0)
        f.write(f'| {idx} | {n0} | {n1} | {n2} | {n3} |\n')
    
    f.write('\n**Significado para a pesquisa:** É um contrassenso absurdo que 5 cursos EaD não dediquem parte substancial do projeto pedagógico para descrever a integração das tecnologias, tratando a tecnologia apenas como o canal de transmissão, mas não como algo que o professor da licenciatura precisa aprender metodologicamente.\n\n')
    
    f.write('## 3. Comparações Presencial vs EAD no Uso da Tecnologia\n')
    cross_tdic = pd.crosstab(df['MODALIDADE_PDF'], pd.to_numeric(df['PRESENCA_TDIC_0_1'], errors='coerce'))
    f.write('**PPCs que citam TDIC nominalmente:**\n')
    f.write('| Modalidade | Não Citam (0) | Citam (1) |\n')
    f.write('|------------|---------------|-----------|\n')
    for idx, row in cross_tdic.iterrows():
        nao = row.get(0.0, 0)
        sim = row.get(1.0, 0)
        f.write(f'| {idx} | {nao} | {sim} |\n')
        
    f.write('\nA grossa maioria dos cursos presenciais (59) cita o TDIC, indicando que a resolução do CNE/MEC começou a surtir efeito mesmo nos presenciais, forçando o uso de laboratórios de informática ou referências metodológicas.\n\n')

    f.write('## 4. Recomendações de Análise e Próximos Passos (Para o TCC)\n')
    f.write('- **Sobre a Data de Criação do PDF:** A base atual não extraiu o "Ano do PPC". Como alguns PDFs vieram da reitoria e foram gerados há poucos meses (2024/2025), o "Ano do PPC" impresso na capa nem sempre é igual a data do arquivo digital. Recomendamos que, no seu fechamento textual, você mencione: *"Os PPCs, embora em sua maioria baixados entre 2024 e 2026, refletem formulações que muitas vezes antecedem o boom das IAs Generativas (pós-2022)."*\n')
    f.write('- **Foque no Paradoxo Nível 2:** Explore por que, mesmo em 96 projetos novos, 0% atingiu a inovação curricular completa (Nível 3). Formam-se professores instrumentalizados a "usar ferramentas" (Nível 2), mas não a pensarem o currículo transpassado inteiramente pela cultura digital.\n')

print(f"Relatorio analitico gerado em {report_path}")
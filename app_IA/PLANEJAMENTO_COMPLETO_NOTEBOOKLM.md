# Planejamento Completo - App NotebookLM

## 1. Objetivo real do sistema

Criar um fluxo operacional confiavel para muitos PDFs, sem perder rastreabilidade:
1. Preparar base de documentos por UF com DOC_ID padronizado.
2. Relacionar cada PDF aos campus/polos do banco local.
3. Gerar prompts robustos para NotebookLM com contexto do banco.
4. Salvar respostas em formatos de trabalho academico:
   - leitura qualitativa (md)
   - matriz consolidada (csv)
   - validacao manual (md + controle csv)

## 2. Variaveis criticas do processo

Variaveis de identificacao:
- UF
- DOC_ID (padrao DOC0001)
- NOME_ARQUIVO_LOCAL
- PDF_PATH

Variaveis de comparacao PDF x banco:
- IES_PDF (extraido do nome do arquivo)
- INSTITUICAO_BANCO
- NOME_POLO_OU_CAMPUS
- MUNICIPIO_POLO
- CONSISTENCIA_IES_0_1
- CONSISTENCIA_UF_0_1

Variaveis de codificacao qualitativa:
- PRESENCA_TDIC_0_1
- PRESENCA_IA_0_1
- NIVEL_INTEGRACAO_0_1_2_3
- FINALIDADE_PEDAGOGICA
- COMPETENCIAS_DOCENTES
- DIMENSAO_ETICA_IA_0_1
- ASPECTO_ETICO
- ESTRATEGIAS_METODOLOGICAS
- EVIDENCIA_LITERAL
- LOCALIZACAO_SECAO_PAGINA
- NIVEL_CONFIANCA_CODIFICADOR_1_2_3

Variaveis de reconciliacao com base:
- CAMPUS_IDENTIFICADOS_NO_PDF
- CAMPUS_BASE_CONFIRMADOS
- CAMPUS_BASE_NAO_CONFIRMADOS
- CAMPUS_NOVOS_NAO_BASE
- STATUS_COMPARACAO_BASE

Variaveis de controle humano:
- REVISOR_HUMANO
- STATUS_VALIDACAO_HUMANA (PENDENTE, VALIDADO, AJUSTADO)
- OBS_VALIDACAO_HUMANA

## 3. Fluxo operacional recomendado

Etapa A - Preparacao de base:
1. Rodar preparacao para UF alvo.
2. Conferir se QTD_PDFS bate com pasta de PDFs.
3. Revisar vinculos com CONSISTENCIA_IES_0_1 = 0.

Etapa B - Codificacao NotebookLM:
1. Selecionar documento no app.
2. Copiar Prompt 1, Prompt 2 e Prompt 3 gerados.
3. Colar no NotebookLM com PDF correspondente.
4. Colar respostas de volta no app.

Etapa C - Registro e auditoria:
1. Salvar no app.
2. Conferir se gerou:
   - Texto_Qualitativo/<UF>/<DOC_ID>.md
   - Resposta_csv/<UF>/analise_notebooklm_<UF>.csv
   - Resposta_csv/analise_notebooklm_consolidado.csv
   - Validacao_Manual/<UF>/<DOC_ID>.md
   - Validacao_Manual/validacao_controle.csv

Etapa D - Validacao humana:
1. Revisar casos de risco alto no Prompt 3.
2. Rebaixar nivel de integracao se faltar evidencia forte.
3. Fechar status final por documento.

## 4. Regras de qualidade (nao negociaveis)

1. Sem evidencia literal + localizacao, nao classificar integracao como nivel 3.
2. Campo textual sem citação literal vira AUSENTE ou baixa confianca.
3. Vinculo IES x campus com conflito vai para PARCIAL ou DIVERGENTE ate revisao.
4. Decisao final sempre humana, mesmo com resposta "boa" da IA.

## 5. Decisao sobre "mandar o banco para o NotebookLM"

Resposta: sim, vale muito a pena.

Motivo:
- O NotebookLM melhora quando recebe contexto estruturado de comparacao.
- Reduz erro de associacao de campus por inferencia livre.
- Ajuda a apontar divergencias entre PDF e banco local.

Como fazer no app:
- O app injeta no prompt os campus/polos da base local para o DOC_ID.
- O modelo retorna confirmados, nao confirmados e novos.

## 6. Riscos e mitigacoes

Risco 1: vinculo errado por dado historico ruidoso no banco.
- Mitigacao: mostrar consistencia de IES e exigir validacao humana.

Risco 2: CSV mal formatado pelo NotebookLM.
- Mitigacao: parser tolerante no app + erro explicito para nova colagem.

Risco 3: nome de DOC_ID inconsistente (DOC004 vs DOC0004).
- Mitigacao: normalizacao automatica para DOC0004.

Risco 4: inflacao de interpretacao qualitativa.
- Mitigacao: Prompt 3 obrigatorio + checklist de revisao.

## 7. Plano para AL (estado inicial)

- PDFs detectados: 6
- DOC_IDs: DOC0001 a DOC0006
- Base inicial preparada e pronta para uso no app
- Recomendacao: processar lote AL completo, depois repetir UF por UF

## 8. Meta de produtividade com qualidade

Meta diaria sugerida:
1. 6 a 10 documentos/dia com qualidade alta.
2. Validacao manual de 20% a 30% do lote no mesmo dia.
3. Fechamento de pendencias no dia seguinte.

Indicadores de controle:
- % documentos com STATUS_VALIDACAO_HUMANA = VALIDADO
- % documentos com STATUS_COMPARACAO_BASE = DIVERGENTE
- % documentos com NIVEL_CONFIANCA_CODIFICADOR_1_2_3 = 1

## 9. Checklist de inicio rapido (hoje)

1. Executar run_app.bat.
2. Atualizar base para AL.
3. Selecionar DOC0001.
4. Rodar 3 prompts no NotebookLM e colar respostas.
5. Salvar e conferir geracao dos 5 arquivos de saida.
6. Repetir para DOC0002...DOC0006.

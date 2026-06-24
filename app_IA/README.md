# App IA - Automacao NotebookLM

Aplicacao local para acelerar a codificacao qualitativa com NotebookLM, com foco em:
- gerar prompts por documento PDF
- incluir contexto de comparacao com a base de campus/polos
- salvar automaticamente as 3 saidas:
  - Texto_Qualitativo (md)
  - Resposta_csv (csv atualizado)
  - Validacao_Manual (md + csv de controle)

## Estrutura de arquivos

- app principal: app.py
- funcoes de negocio: core.py
- script de preparo de base: scripts/preparar_base.py
- base interna gerada:
  - data/base_documentos.csv
  - data/vinculos_pdf_campus.csv

Saidas geradas pelo app:
- ../Texto_Qualitativo/<UF>/<DOC_ID>.md
- ../Resposta_csv/<UF>/analise_notebooklm_<UF>.csv
- ../Resposta_csv/analise_notebooklm_consolidado.csv
- ../Validacao_Manual/<UF>/<DOC_ID>.md
- ../Validacao_Manual/validacao_controle.csv

## Como usar

1. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

2. Abrir o app:

```powershell
streamlit run app.py
```

3. No app, clique em "Preparar/Atualizar base agora" e selecione a UF (exemplo: AL).

4. Escolha o documento (DOC_ID) e copie os 3 prompts para o NotebookLM.

5. Cole as 3 respostas do NotebookLM nos campos do app e clique em "Salvar respostas e atualizar arquivos".

## Modo lote sequencial (novo)

O app agora possui um modo de lote para percorrer documentos em sequencia (ex.: AL DOC0001 ate DOC0006).

Recursos:
- botao Anterior
- botao Proximo com validacao obrigatoria
- botao Ir para primeiro pendente
- botao Salvar e avancar no lote

Regra de avancar:
- para ir ao proximo documento, o item atual precisa estar com status VALIDADO ou AJUSTADO
- se estiver PENDENTE, o app bloqueia o avancar e mostra aviso

Indicadores visiveis no app:
- validados/ajustados por UF
- percentual concluido
- posicao atual no lote

## O que o app resolve

- Padroniza DOC_ID (ex.: doc0004 -> DOC0004).
- Cruza PDFs com mapeamento_ppc_polos.csv.
- Mostra vinculos de campus/polo para comparacao durante a leitura.
- Registra inconsistencias de IES para validacao humana.
- Mantem CSV consolidado sempre atualizado por UF e geral.

## Sobre a comparacao no NotebookLM

Sim, vale a pena mandar para o NotebookLM a lista de campus/polos da base local para comparar com o PDF.

Por isso os prompts gerados pelo app ja incluem:
- metadados do PDF
- lista de campus/polos sugeridos pela base com separacao entre alta e baixa confianca
- campos de saida para confirmar, negar ou apontar campus novos

## Recomendacoes metodologicas

- Trate NotebookLM como codificador assistente, nao como decisor final.
- Use a validacao manual para fechar divergencias.
- Nao usar nivel de integracao 3 sem evidencia literal + localizacao.
- Em caso de vinculo IES x campus duvidoso, manter status PARCIAL ou DIVERGENTE ate revisao humana.

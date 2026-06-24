# Planejamento Completo - App de Triagem e Upload Manual de PDFs

## Objetivo
Criar uma aplicacao para operar em cima de:
- C:\Users\augus\Music\TCC\Data\new_date\output_csv\mapeamento_ppc_polos.csv

Fluxo esperado:
1. Exibir apenas itens que ainda valem tentativa de download manual.
2. Mostrar link de download para voce abrir.
3. Permitir arrastar e soltar o PDF baixado.
4. Organizar automaticamente em:
   - C:\Users\augus\Music\TCC\Data\new_date\pdfs_baixados\<UF>
5. Evitar duplicacao:
   - Se PDF ja existe (mesmo hash), manter arquivo existente.
   - Se nome colidir, gerar sufixo __dupN sem sobrescrever.
6. Atualizar o CSV com status e caminho final.

## Escopo funcional implementado
- Leitura do mapeamento (UTF-8-SIG).
- Filtro padrao para triagem manual:
  - Inclui: HTML_INTERMEDIARIO, 404, BLOQUEADO, vazio.
  - Ignora: OK_PDF, OK_PDF_MANUAL, NAO_ENCONTRADO.
- Toggle para:
  - filtrar por UF
  - exibir somente itens com fonte de download
  - exibir somente pendentes
- Exibicao de link bruto e link limpo.
- Botao para abrir link no navegador.
- Upload de PDF por arrastar.
- Acao de falha manual:
  - STATUS_LINK = NAO_ENCONTRADO
  - ACAO_RECOMENDADA = VALIDACAO_MANUAL
- Salvar upload com:
  - validacao de cabecalho PDF (%PDF-)
  - hash SHA256
  - deduplicacao global por hash
  - escrita em pasta por UF
  - atualizacao das colunas-chave no CSV

## Arquivo da aplicacao
- c:\Users\augus\Music\TCC\Data\new_date\script\app_triagem_download_manual.py

## Campos do CSV atualizados pelo app
- STATUS_LINK
- URL_DOWNLOAD_PDF_LIMPA
- NOME_ARQUIVO_LOCAL
- CAMINHO_ARQUIVO_LOCAL
- HASH_OU_ID_PDF_CANONICO
- LOCALIDADE_DOCUMENTO
- ACAO_RECOMENDADA
- DOC_ID (quando vazio, gera proximo DOC para a UF)

## Regras de nomeacao
- Se NOME_ARQUIVO_LOCAL ja existe na linha, ele e reutilizado.
- Se nao existir, o app gera nome padrao:
  - UF__INSTITUICAO__TIPO__LOCALIDADE__ANO__DOCXXXX.pdf

## Regras de deduplicacao
1. Calcula SHA256 do arquivo enviado.
2. Procura o mesmo hash em toda arvore pdfs_baixados.
3. Se encontrar:
   - nao copia
   - vincula a linha ao arquivo existente
4. Se nao encontrar:
   - grava no diretorio da UF
   - sem sobrescrever; em colisao de nome usa __dupN

## Execucao
No PowerShell:

```powershell
c:/Users/augus/Music/TCC/Data/.venv-1/Scripts/python.exe -m streamlit run C:/Users/augus/Music/TCC/Data/new_date/script/app_triagem_download_manual.py
```

## Roteiro rapido de teste
1. Abrir o app.
2. Filtrar UF (opcional).
3. Escolher uma linha com HTML_INTERMEDIARIO ou 404.
4. Clicar em Abrir link para download.
5. Baixar manualmente o arquivo.
6. Arrastar PDF para o app.
7. Clicar em Salvar PDF neste item.
8. Validar no CSV e na pasta da UF.

## Criterios de aceite
- Nao sobrescrever arquivos existentes.
- Nao gerar duplicata fisica para mesmo hash.
- Atualizar CSV de forma consistente e imediata.
- Remover da fila itens salvos (status OK_PDF_MANUAL).
- Permitir marcar itens como nao encontrados sem travar o fluxo.

## Observacoes
- O app foi pensado para fluxo manual assistido, mantendo compatibilidade com os scripts oficiais de pipeline.
- Para grande volume, voce pode usar filtros por UF para reduzir a lista e acelerar a triagem.

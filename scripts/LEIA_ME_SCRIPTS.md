# Scripts PS1 - Guia Rapido

## O que e um arquivo .ps1
Arquivo .ps1 e um script do PowerShell (shell do Windows).
Ele automatiza tarefas repetitivas com comandos salvos em arquivo.

## Scripts desta pasta

### 1) util_validar_coleta.ps1
Valida os arquivos de resposta da coleta de um estado.
Verifica se tem YAML preenchido, template ou sem YAML.

### 2) util_consolidar_yaml_csv.ps1
Lê respostas da coleta e consolida no CSV principal.
Agora faz merge inteligente (preserva dados existentes e incorpora melhorias).
Tambem cria checkpoint automatico do CSV antes da consolidacao.

### 3) util_baixar_pdfs_atualizar_planilha.ps1
Tenta baixar os PDFs a partir das URLs do CSV.
Atualiza status, caminho local do arquivo, hash e metadados.

### 4) util_deduplicar_pdfs_planilha.ps1
Remove duplicacoes de PDF no disco e ajusta referencias no CSV.
Mantem consistencia entre planilha e pasta de PDFs.

### 5) util_atualizar_relatorios_qualidade.ps1
Gera artefatos de qualidade automaticamente:
- CSV por estado
- seguranca PDF x polos (global e por estado)
- resumo de seguranca por UF

### 6) util_processar_uf.ps1
Orquestra o pipeline completo por estado:
1. validacao da coleta
2. consolidacao no CSV
3. download/atualizacao de PDFs
4. deduplicacao
5. atualizacao dos relatorios de qualidade

## Observacao importante
Os scripts oficiais ficam apenas nesta pasta `script` para manter o projeto organizado.

Execucao recomendada do pipeline por estado:
```powershell
& "C:\Users\augus\Music\TCC\Data\new_date\script\util_processar_uf.ps1" -UF BA
```

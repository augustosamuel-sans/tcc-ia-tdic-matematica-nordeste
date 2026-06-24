param (
    [string]$CsvPath = ".\output_csv\mapeamento_ppc_polos.csv",
    [string]$PromptsRoot = ".\prompts_individuais_7em7",
    [int]$ChunkSize = 7,
    [string[]]$UFs = @("BA", "PI")
)

$ErrorActionPreference = "Stop"

function Clean-Field([string]$Value) {
    if ([string]::IsNullOrWhiteSpace($Value)) { return "" }
    return (($Value -replace "[\r\n]+", " ").Trim())
}

function Status-Priority([string]$Status) {
    switch ($Status) {
        "HTML_INTERMEDIARIO" { return 1 }
        "404" { return 2 }
        "BLOQUEADO" { return 3 }
        "NAO_ENCONTRADO" { return 4 }
        default { return 9 }
    }
}

function Build-PromptHeader([string]$UF, [int]$BlockNumber, [int]$TotalBlocks) {
    return @"
# Prompt de Repesquisa - $UF - Bloco $BlockNumber/$TotalBlocks

Objetivo: converter casos NAO_OK para OK_PDF com fonte oficial verificavel e evidencia literal.

Regras obrigatorias:
1. Somente fonte oficial verificavel.
2. Sem evidencia literal + URL => retornar NAO_ENCONTRADO.
3. Nao inventar ano, link, status do PPC ou resumo.
4. Se o mesmo PDF atender varios polos, marcar PPC_COMPARTILHADO=SIM.

Formato de saida: YAML por item.

~~~yaml
estado: "$UF"
instituicao: "..."
modalidade: "..."
nome_polo_ou_campus: "..."
municipio_polo: "..."
curso: "Licenciatura em Matematica"
ano_ppc: "..."
url_fonte: "..."
url_download_pdf: "..."
status_link: "OK_PDF|HTML_INTERMEDIARIO|404|BLOQUEADO|NAO_ENCONTRADO"
ppc_compartilhado: "SIM|NAO"
polos_relacionados:
  - "..."
evidencia_minima: "..."
obs: "..."
confianca: "alta|media|baixa"
acao_recomendada: "OK|NOVA_BUSCA|VALIDACAO_MANUAL"
fontes:
  - url: "..."
    evidencia_literal: "..."
~~~

## Itens (maximo 7)

"@
}

function Build-PromptItem([psobject]$Row, [int]$Number) {
    $curso = Clean-Field([string]$Row.CURSO)
    if ([string]::IsNullOrWhiteSpace($curso)) { $curso = "Licenciatura em Matematica" }

    $status = Clean-Field([string]$Row.STATUS_LINK)
    if ([string]::IsNullOrWhiteSpace($status)) { $status = "NAO_ENCONTRADO" }

    $urlFonte = Clean-Field([string]$Row.URL_FONTE)
    if ([string]::IsNullOrWhiteSpace($urlFonte)) { $urlFonte = "NAO_ENCONTRADO" }

    $urlDownload = Clean-Field([string]$Row.URL_DOWNLOAD_PDF)
    if ([string]::IsNullOrWhiteSpace($urlDownload)) { $urlDownload = "NAO_ENCONTRADO" }

    return @"
### Item $Number
- estado: $(Clean-Field([string]$Row.UF))
- instituicao_bruta: $(Clean-Field([string]$Row.INSTITUICAO))
- modalidade_bruta: $(Clean-Field([string]$Row.MODALIDADE))
- nome_polo_ou_campus_bruto: $(Clean-Field([string]$Row.NOME_POLO_OU_CAMPUS))
- municipio_polo_bruto: $(Clean-Field([string]$Row.MUNICIPIO_POLO))
- curso_alvo: $curso
- status_anterior: $status
- url_fonte_anterior: $urlFonte
- url_download_anterior: $urlDownload
- precisa_ano_ppc: sim
- precisa_url_fonte: sim
- precisa_url_download_pdf: sim
- precisa_status_link: sim
- precisa_ppc_compartilhado: sim
- precisa_polos_relacionados: sim
- precisa_evidencia_minima: sim
- precisa_obs: sim
- precisa_acao_recomendada: sim

"@
}

function Write-Index([string]$UF, [string]$StateRoot, [int]$BlockCount) {
    $indexPath = Join-Path $StateRoot ("INDICE_{0}_ATIVOS.md" -f $UF)
    $content = @()
    $content += ("# INDICE {0} - PROMPTS ATIVOS" -f $UF)
    $content += ""
    $content += ("Use estes prompts para pesquisa do estado {0}." -f $UF)
    $content += ""
    $content += "Arquivos:"

    for ($i = 1; $i -le $BlockCount; $i++) {
        $fileName = ("PROMPT_{0}_ATIVO_BLOCO_{1}.md" -f $UF, $i.ToString("00"))
        $content += ("- [01_prompts_ativos/{0}](./01_prompts_ativos/{0})" -f $fileName)
    }

    $content -join "`r`n" | Set-Content -Path $indexPath -Encoding UTF8
}

if (-not (Test-Path $CsvPath)) {
    throw "CSV nao encontrado: $CsvPath"
}

$data = @(Import-Csv $CsvPath -Encoding UTF8)

foreach ($uf in $UFs) {
    $ufData = @(
        $data |
            Where-Object {
                $_.UF -eq $uf -and
                -not [string]::IsNullOrWhiteSpace($_.STATUS_LINK) -and
                $_.STATUS_LINK -ne "OK_PDF"
            } |
            Sort-Object @{ Expression = { Status-Priority([string]$_.STATUS_LINK) } }, INSTITUICAO, MUNICIPIO_POLO, NOME_POLO_OU_CAMPUS
    )

    $total = $ufData.Count
    $stateRoot = Join-Path $PromptsRoot $uf
    $activeDir = Join-Path $stateRoot "01_prompts_ativos"
    $historyRoot = Join-Path $stateRoot "02_historico_rodadas"
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupDir = Join-Path $historyRoot ("backup_ativos_{0}" -f $timestamp)

    New-Item -ItemType Directory -Path $activeDir -Force | Out-Null
    New-Item -ItemType Directory -Path $historyRoot -Force | Out-Null

    $oldPromptFiles = Get-ChildItem -Path $activeDir -Filter ("PROMPT_{0}_ATIVO_BLOCO_*.md" -f $uf) -File -ErrorAction SilentlyContinue
    if ($oldPromptFiles.Count -gt 0) {
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        foreach ($f in $oldPromptFiles) {
            Move-Item -Path $f.FullName -Destination (Join-Path $backupDir $f.Name) -Force
        }
    }

    if ($total -eq 0) {
        Write-Index -UF $uf -StateRoot $stateRoot -BlockCount 0
        Write-Host "[$uf] Nenhum item NAO_OK encontrado." -ForegroundColor Yellow
        continue
    }

    $blockCount = [int][Math]::Ceiling($total / [double]$ChunkSize)

    for ($block = 0; $block -lt $blockCount; $block++) {
        $start = $block * $ChunkSize
        $end = [Math]::Min($start + $ChunkSize - 1, $total - 1)
        $slice = @($ufData[$start..$end])

        $parts = @()
        $parts += Build-PromptHeader -UF $uf -BlockNumber ($block + 1) -TotalBlocks $blockCount

        $itemNumber = 1
        foreach ($row in $slice) {
            $parts += Build-PromptItem -Row $row -Number $itemNumber
            $itemNumber++
        }

        $fileName = ("PROMPT_{0}_ATIVO_BLOCO_{1}.md" -f $uf, ($block + 1).ToString("00"))
        $filePath = Join-Path $activeDir $fileName
        ($parts -join "`r`n") | Set-Content -Path $filePath -Encoding UTF8
    }

    Write-Index -UF $uf -StateRoot $stateRoot -BlockCount $blockCount
    Write-Host ("[{0}] Prompts ativos gerados: {1} itens em {2} blocos." -f $uf, $total, $blockCount) -ForegroundColor Green
}

Write-Host "Geracao concluida no formato antigo (.md por bloco)." -ForegroundColor Cyan

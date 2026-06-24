param(
    [string]$UF = "AL",
    [string]$RootPath = "c:\Users\augus\Music\TCC\Data\new_date",
    [switch]$IncludeIncomplete
)

$ErrorActionPreference = "Stop"

$inputDir = Join-Path $RootPath ("coleta_md_por_estado\" + $UF)
$inputDirAtual = Join-Path $inputDir "atual"
$csvPath = Join-Path $RootPath "output_csv\mapeamento_ppc_polos.csv"
$checkpointDir = Join-Path $RootPath "output_csv\checkpoints"

if (!(Test-Path $inputDir)) {
    Write-Error "Pasta nao encontrada: $inputDir"
}
if (!(Test-Path $csvPath)) {
    Write-Error "CSV nao encontrado: $csvPath"
}

if (!(Test-Path $checkpointDir)) {
    New-Item -ItemType Directory -Path $checkpointDir | Out-Null
}

$checkpointStamp = Get-Date -Format "yyyyMMdd_HHmmss_fff"
$checkpointPath = Join-Path $checkpointDir ("mapeamento_ppc_polos__PRE_CONSOLIDACAO__" + $UF + "__" + $checkpointStamp + ".csv")
Copy-Item -LiteralPath $csvPath -Destination $checkpointPath -Force
Write-Output ("Checkpoint criado: " + $checkpointPath)

function Get-YamlBlocks([string]$text) {
    $matches = [regex]::Matches($text, '```yaml\s*([\s\S]*?)\s*```', [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
    $blocks = @()
    foreach ($m in $matches) {
        $blocks += $m.Groups[1].Value
    }
    # Fallback: accept plain YAML documents (without fenced ```yaml```).
    if ($blocks.Count -eq 0 -and $text -match '(?m)^\s*(-\s*)?estado\s*:\s*(".*"|\S.+)$') {
        $blocks += $text
    }
    return $blocks
}

function Normalize-Text([string]$text) {
    if ([string]::IsNullOrWhiteSpace($text)) { return "" }
    return (($text.Trim().ToLowerInvariant()) -replace '\s+', ' ')
}

function Is-Meaningful([string]$text) {
    if ([string]::IsNullOrWhiteSpace($text)) { return $false }
    $t = $text.Trim()
    if ($t -eq "...") { return $false }
    if ($t -eq "NAO_ENCONTRADO") { return $false }
    return $true
}

function Get-StatusRank([string]$status) {
    switch ($status) {
        "OK_PDF" { return 5 }
        "HTML_INTERMEDIARIO" { return 4 }
        "404" { return 3 }
        "BLOQUEADO" { return 2 }
        "NAO_ENCONTRADO" { return 1 }
        default { return 0 }
    }
}

function Build-RowKey($row) {
    $uf = Normalize-Text([string]$row.UF)
    $inst = Normalize-Text([string]$row.INSTITUICAO)
    $nome = Normalize-Text([string]$row.NOME_POLO_OU_CAMPUS)
    $mun = Normalize-Text([string]$row.MUNICIPIO_POLO)
    $mod = Normalize-Text([string]$row.MODALIDADE)
    $curso = Normalize-Text([string]$row.CURSO)

    # Do not merge rows that do not have minimally reliable identity fields.
    if ([string]::IsNullOrWhiteSpace($uf) -or [string]::IsNullOrWhiteSpace($inst) -or [string]::IsNullOrWhiteSpace($nome) -or [string]::IsNullOrWhiteSpace($mun)) {
        return ""
    }

    $parts = @(
        $uf,
        $inst,
        $mod,
        $nome,
        $mun,
        $curso
    )
    return ($parts -join "||")
}

function Merge-PreferValue([string]$current, [string]$incoming) {
    if (-not (Is-Meaningful $current) -and (Is-Meaningful $incoming)) { return $incoming }
    return $current
}

function Merge-Text([string]$current, [string]$incoming, [int]$currentStatusRank, [int]$incomingStatusRank) {
    if (-not (Is-Meaningful $incoming)) { return $current }
    if (-not (Is-Meaningful $current)) { return $incoming }
    if ($incomingStatusRank -ge $currentStatusRank -and $incoming.Length -gt $current.Length) {
        return $incoming
    }
    return $current
}

function Merge-Row($current, $incoming) {
    $cRank = Get-StatusRank([string]$current.STATUS_LINK)
    $iRank = Get-StatusRank([string]$incoming.STATUS_LINK)

    # Identity and stable fields: fill only when missing.
    foreach ($idField in @("UF","INSTITUICAO","MODALIDADE","NOME_POLO_OU_CAMPUS","MUNICIPIO_POLO","CURSO")) {
        $current.$idField = Merge-PreferValue ([string]$current.$idField) ([string]$incoming.$idField)
    }

    # Keep best status (never regress).
    if ($iRank -gt $cRank) {
        $current.STATUS_LINK = $incoming.STATUS_LINK
    }

    # URLs and source fields: update when incoming is meaningful and status is not worse.
    if (Is-Meaningful([string]$incoming.URL_FONTE)) {
        if (-not (Is-Meaningful([string]$current.URL_FONTE)) -or $iRank -ge $cRank) {
            $current.URL_FONTE = $incoming.URL_FONTE
        }
    }
    if (Is-Meaningful([string]$incoming.URL_DOWNLOAD_PDF)) {
        if (-not (Is-Meaningful([string]$current.URL_DOWNLOAD_PDF)) -or $iRank -ge $cRank) {
            $current.URL_DOWNLOAD_PDF = $incoming.URL_DOWNLOAD_PDF
        }
    }

    # Shared document semantics.
    if (([string]$incoming.PPC_COMPARTILHADO) -eq "SIM" -or ([string]$current.PPC_COMPARTILHADO) -eq "SIM") {
        $current.PPC_COMPARTILHADO = "SIM"
    } elseif (-not (Is-Meaningful([string]$current.PPC_COMPARTILHADO))) {
        $current.PPC_COMPARTILHADO = $incoming.PPC_COMPARTILHADO
    }

    # Derived/group fields: keep existing unless missing.
    foreach ($f in @("GRUPO_COMPARTILHAMENTO_ID","TIPO_VINCULO","URL_DOWNLOAD_PDF_LIMPA","LOCALIDADE_DOCUMENTO","NOME_ARQUIVO_LOCAL","CAMINHO_ARQUIVO_LOCAL","HASH_OU_ID_PDF_CANONICO")) {
        $current.$f = Merge-PreferValue ([string]$current.$f) ([string]$incoming.$f)
    }

    # Quantities: keep max.
    $cQtd = 0
    $iQtd = 0
    [void][int]::TryParse(([string]$current.QTD_POLOS_NO_GRUPO), [ref]$cQtd)
    [void][int]::TryParse(([string]$incoming.QTD_POLOS_NO_GRUPO), [ref]$iQtd)
    if ($iQtd -gt $cQtd) {
        $current.QTD_POLOS_NO_GRUPO = [string]$iQtd
    } elseif (-not (Is-Meaningful([string]$current.QTD_POLOS_NO_GRUPO)) -and $iQtd -gt 0) {
        $current.QTD_POLOS_NO_GRUPO = [string]$iQtd
    }

    # Content fields: preserve and only improve with better/equal status.
    $current.ANO_PPC = Merge-Text ([string]$current.ANO_PPC) ([string]$incoming.ANO_PPC) $cRank $iRank
    $current.EVIDENCIA_MINIMA = Merge-Text ([string]$current.EVIDENCIA_MINIMA) ([string]$incoming.EVIDENCIA_MINIMA) $cRank $iRank
    $current.OBS = Merge-Text ([string]$current.OBS) ([string]$incoming.OBS) $cRank $iRank

    # Action recommendation: OK has precedence, otherwise preserve existing meaningful value.
    if (([string]$incoming.ACAO_RECOMENDADA) -eq "OK" -or ([string]$current.ACAO_RECOMENDADA) -eq "OK") {
        $current.ACAO_RECOMENDADA = "OK"
    } else {
        $current.ACAO_RECOMENDADA = Merge-PreferValue ([string]$current.ACAO_RECOMENDADA) ([string]$incoming.ACAO_RECOMENDADA)
    }

    return $current
}

function Ensure-Columns($rows, [string[]]$cols) {
    foreach ($r in $rows) {
        foreach ($c in $cols) {
            if (-not ($r.PSObject.Properties.Name -contains $c)) {
                Add-Member -InputObject $r -MemberType NoteProperty -Name $c -Value ""
            }
        }
    }
}

function New-RowObject($row) {
    return [pscustomobject]@{
        UF = [string]$row.UF
        INSTITUICAO = [string]$row.INSTITUICAO
        MODALIDADE = [string]$row.MODALIDADE
        NOME_POLO_OU_CAMPUS = [string]$row.NOME_POLO_OU_CAMPUS
        MUNICIPIO_POLO = [string]$row.MUNICIPIO_POLO
        CURSO = [string]$row.CURSO
        URL_FONTE = [string]$row.URL_FONTE
        URL_DOWNLOAD_PDF = [string]$row.URL_DOWNLOAD_PDF
        URL_DOWNLOAD_PDF_LIMPA = [string]$row.URL_DOWNLOAD_PDF_LIMPA
        STATUS_LINK = [string]$row.STATUS_LINK
        HASH_OU_ID_PDF_CANONICO = [string]$row.HASH_OU_ID_PDF_CANONICO
        PPC_COMPARTILHADO = [string]$row.PPC_COMPARTILHADO
        GRUPO_COMPARTILHAMENTO_ID = [string]$row.GRUPO_COMPARTILHAMENTO_ID
        QTD_POLOS_NO_GRUPO = [string]$row.QTD_POLOS_NO_GRUPO
        TIPO_VINCULO = [string]$row.TIPO_VINCULO
        ANO_PPC = [string]$row.ANO_PPC
        LOCALIDADE_DOCUMENTO = [string]$row.LOCALIDADE_DOCUMENTO
        NOME_ARQUIVO_LOCAL = [string]$row.NOME_ARQUIVO_LOCAL
        CAMINHO_ARQUIVO_LOCAL = [string]$row.CAMINHO_ARQUIVO_LOCAL
        EVIDENCIA_MINIMA = [string]$row.EVIDENCIA_MINIMA
        OBS = [string]$row.OBS
        ACAO_RECOMENDADA = [string]$row.ACAO_RECOMENDADA
    }
}

function Split-YamlDocuments([string]$yamlBlock) {
    # Support multi-document YAML inside one fenced block.
    if ([string]::IsNullOrWhiteSpace($yamlBlock)) { return @() }
    $docs = $yamlBlock -split '(?m)^\s*---\s*$'
    return $docs | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
}

function Parse-YamlFlat([string]$yaml) {
    $obj = @{}
    $currentList = ""
    foreach ($line in ($yaml -split '\r?\n')) {
        $trim = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trim)) { continue }

        if ($trim -match '^[-\s]*([A-Za-z0-9_]+):\s*"(.*)"\s*$') {
            $key = $matches[1]
            $val = $matches[2]
            $obj[$key] = $val
            $currentList = ""
            continue
        }

        if ($trim -match '^[-\s]*([A-Za-z0-9_]+):\s*(.+)\s*$') {
            $key = $matches[1]
            $val = $matches[2].Trim()
            # Ignore markdown content/citations while still accepting scalar key-value pairs.
            if (-not ($key -match '^[A-Za-z0-9_]+$')) { continue }
            if ($val -match '^\[\^\d+\]:') { continue }
            if ($val -match '^\*\*') { continue }
            $obj[$key] = $val
            $currentList = ""
            continue
        }

        if ($trim -match '^[-\s]*([A-Za-z0-9_]+):\s*$') {
            $currentList = $matches[1]
            if (-not $obj.ContainsKey($currentList)) {
                $obj[$currentList] = @()
            }
            continue
        }

        if ($trim -match '^[-\u00A0\s]*"(.*)"\s*$' -and $currentList -ne "") {
            if ($obj[$currentList] -isnot [System.Collections.IList]) {
                $obj[$currentList] = @($obj[$currentList])
            }
            $obj[$currentList] += $matches[1]
            continue
        }
    }
    return $obj
}

function Is-Incomplete($obj) {
    $required = @("instituicao", "modalidade", "nome_polo_ou_campus", "municipio_polo", "url_fonte", "status_link")
    foreach ($k in $required) {
        if (-not $obj.ContainsKey($k)) { return $true }
        $v = [string]$obj[$k]
        if ([string]::IsNullOrWhiteSpace($v)) { return $true }
        if ($v -eq "...") { return $true }
    }
    if ($obj.ContainsKey("url_download_pdf") -and ([string]$obj["url_download_pdf"]).Trim() -eq "...") { return $true }
    if ($obj.ContainsKey("evidencia_minima") -and ([string]$obj["evidencia_minima"]).Trim() -eq "...") { return $true }
    return $false
}

$fileCandidates = @()
$fileCandidates += (Get-ChildItem -Path $inputDir -File -Filter "*.md" -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '^LEIA_ME' })
$fileCandidates += (Get-ChildItem -Path $inputDirAtual -File -Filter "*.md" -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '^LEIA_ME' })
$files = $fileCandidates | Sort-Object FullName -Unique
$parsed = @()

foreach ($f in $files) {
    $content = Get-Content -Path $f.FullName -Raw -Encoding UTF8
    $blocks = Get-YamlBlocks $content
    foreach ($b in $blocks) {
        $docs = Split-YamlDocuments $b
        foreach ($d in $docs) {
            $obj = Parse-YamlFlat $d
            if ((Is-Incomplete $obj) -and -not $IncludeIncomplete) { continue }

            $polosRelacionados = ""
            if ($obj.ContainsKey("polos_relacionados")) {
                if ($obj["polos_relacionados"] -is [System.Collections.IList]) {
                    $polosRelacionados = (($obj["polos_relacionados"] | Where-Object { $_ -and $_ -ne "..." -and $_ -ne "NAO_ENCONTRADO" }) -join " | ")
                } else {
                    $polosRelacionados = [string]$obj["polos_relacionados"]
                }
            }

            $parsed += [pscustomobject]@{
                UF = if ($obj.ContainsKey("estado")) { $obj["estado"] } else { $UF }
                INSTITUICAO = if ($obj.ContainsKey("instituicao")) { $obj["instituicao"] } else { "" }
                MODALIDADE = if ($obj.ContainsKey("modalidade")) { $obj["modalidade"] } else { "" }
                NOME_POLO_OU_CAMPUS = if ($obj.ContainsKey("nome_polo_ou_campus")) { $obj["nome_polo_ou_campus"] } else { "" }
                MUNICIPIO_POLO = if ($obj.ContainsKey("municipio_polo")) { $obj["municipio_polo"] } else { "" }
                CURSO = if ($obj.ContainsKey("curso")) { $obj["curso"] } else { "Licenciatura em Matematica" }
                URL_FONTE = if ($obj.ContainsKey("url_fonte")) { $obj["url_fonte"] } else { "" }
                URL_DOWNLOAD_PDF = if ($obj.ContainsKey("url_download_pdf")) { $obj["url_download_pdf"] } else { "" }
                URL_DOWNLOAD_PDF_LIMPA = ""
                STATUS_LINK = if ($obj.ContainsKey("status_link")) { $obj["status_link"] } else { "NAO_ENCONTRADO" }
                HASH_OU_ID_PDF_CANONICO = ""
                PPC_COMPARTILHADO = if ($obj.ContainsKey("ppc_compartilhado")) { $obj["ppc_compartilhado"] } else { "NAO" }
                GRUPO_COMPARTILHAMENTO_ID = ""
                QTD_POLOS_NO_GRUPO = if ($polosRelacionados -ne "") { [string](($polosRelacionados -split '\s*\|\s*').Count) } else { "" }
                TIPO_VINCULO = if ($polosRelacionados -ne "") { "INSTITUCIONAL_COMPARTILHADO" } else { "POLO_ESPECIFICO" }
                ANO_PPC = if ($obj.ContainsKey("ano_ppc")) { $obj["ano_ppc"] } else { "" }
                LOCALIDADE_DOCUMENTO = ""
                NOME_ARQUIVO_LOCAL = ""
                CAMINHO_ARQUIVO_LOCAL = ""
                EVIDENCIA_MINIMA = if ($obj.ContainsKey("evidencia_minima")) { $obj["evidencia_minima"] } else { "" }
                OBS = if ($obj.ContainsKey("obs")) { $obj["obs"] } else { "" }
                ACAO_RECOMENDADA = if ($obj.ContainsKey("acao_recomendada")) { $obj["acao_recomendada"] } else { "NOVA_BUSCA" }
            }
        }
    }
}

if ($parsed.Count -eq 0) {
    Write-Output "Nenhum YAML preenchido encontrado para consolidar em $inputDir ou $inputDirAtual"
    exit 0
}

$existing = Import-Csv -Path $csvPath
$requiredCols = @(
    "UF","INSTITUICAO","MODALIDADE","NOME_POLO_OU_CAMPUS","MUNICIPIO_POLO","CURSO",
    "URL_FONTE","URL_DOWNLOAD_PDF","URL_DOWNLOAD_PDF_LIMPA","STATUS_LINK","HASH_OU_ID_PDF_CANONICO",
    "PPC_COMPARTILHADO","GRUPO_COMPARTILHAMENTO_ID","QTD_POLOS_NO_GRUPO","TIPO_VINCULO","ANO_PPC",
    "LOCALIDADE_DOCUMENTO","NOME_ARQUIVO_LOCAL","CAMINHO_ARQUIVO_LOCAL",
    "EVIDENCIA_MINIMA","OBS","ACAO_RECOMENDADA"
)

Ensure-Columns $existing $requiredCols
Ensure-Columns $parsed $requiredCols

$existingUF = @($existing | Where-Object { $_.UF -eq $UF })
$otherUFs = @($existing | Where-Object { $_.UF -ne $UF })

# First, consolidate any existing duplicates in target UF.
$index = @{}
$fallbackKeyCounter = 0
foreach ($r in $existingUF) {
    $obj = New-RowObject $r
    $k = Build-RowKey $obj
    if ([string]::IsNullOrWhiteSpace($k)) {
        $fallbackKeyCounter++
        $k = "__ROW__EXISTING__" + $fallbackKeyCounter
    }
    if ($index.ContainsKey($k)) {
        $index[$k] = Merge-Row $index[$k] $obj
    } else {
        $index[$k] = $obj
    }
}

# Then upsert parsed rows intelligently.
foreach ($p in $parsed) {
    $objP = New-RowObject $p
    $k = Build-RowKey $objP
    if ([string]::IsNullOrWhiteSpace($k)) {
        $fallbackKeyCounter++
        $k = "__ROW__PARSED__" + $fallbackKeyCounter
    }
    if ($index.ContainsKey($k)) {
        $index[$k] = Merge-Row $index[$k] $objP
    } else {
        $index[$k] = $objP
    }
}

$finalUF = @($index.Values)
$finalAll = @()
$finalAll += $otherUFs
$finalAll += $finalUF

Ensure-Columns $finalAll $requiredCols

$finalAll |
    Select-Object $requiredCols |
    Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8

Write-Output ("Consolidado com sucesso. Registros novos lidos: " + $parsed.Count)
Write-Output ("Total atual no CSV: " + ((Import-Csv -Path $csvPath).Count))

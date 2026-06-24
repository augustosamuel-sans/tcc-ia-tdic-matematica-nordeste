param (
    [string]$RefDir = ".\dados_iniciais_ref\data_2_estrutura",
    [string]$SourceCsvPath = ".\output_csv\mapeamento_ppc_polos_ANTIGO_BKP.csv",
    [string]$OutCanonical = ".\output_csv\mapeamento_ppc_polos_CANONICO.csv",
    [string]$OutQuarantine = ".\output_csv\mapeamento_ppc_polos_QUARENTENA.csv",
    [switch]$SetAsMain
)

$ErrorActionPreference = "Stop"

$ExpectedColumns = @(
    "UF",
    "INSTITUICAO",
    "MODALIDADE",
    "NOME_POLO_OU_CAMPUS",
    "MUNICIPIO_POLO",
    "CURSO",
    "URL_FONTE",
    "URL_DOWNLOAD_PDF",
    "URL_DOWNLOAD_PDF_LIMPA",
    "STATUS_LINK",
    "HASH_OU_ID_PDF_CANONICO",
    "PPC_COMPARTILHADO",
    "GRUPO_COMPARTILHAMENTO_ID",
    "QTD_POLOS_NO_GRUPO",
    "TIPO_VINCULO",
    "ANO_PPC",
    "LOCALIDADE_DOCUMENTO",
    "NOME_ARQUIVO_LOCAL",
    "CAMINHO_ARQUIVO_LOCAL",
    "EVIDENCIA_MINIMA",
    "OBS",
    "ACAO_RECOMENDADA"
)

Write-Host "Iniciando reconciliacao canonica (schema completo)..." -ForegroundColor Cyan

function Normalize-String([string]$Text) {
    if ([string]::IsNullOrWhiteSpace($Text)) { return "" }
    $normalized = $Text.Normalize([System.Text.NormalizationForm]::FormD)
    $regex = [regex]"\p{M}"
    $noDiacritics = $regex.Replace($normalized, "").ToLowerInvariant()
    return ($noDiacritics -replace "[^a-z0-9]", "")
}

function Build-KeyStrict([string]$uf, [string]$inst, [string]$mod, [string]$nome, [string]$mun) {
    return @(
        Normalize-String $uf,
        Normalize-String $inst,
        Normalize-String $mod,
        Normalize-String $nome,
        Normalize-String $mun
    ) -join "|"
}

function Build-KeyInstMunMod([string]$uf, [string]$inst, [string]$mod, [string]$mun) {
    return @(
        Normalize-String $uf,
        Normalize-String $inst,
        Normalize-String $mod,
        Normalize-String $mun
    ) -join "|"
}

function Build-KeyInstMun([string]$uf, [string]$inst, [string]$mun) {
    return @(
        Normalize-String $uf,
        Normalize-String $inst,
        Normalize-String $mun
    ) -join "|"
}

function Build-KeyNomeMun([string]$uf, [string]$nome, [string]$mun) {
    return @(
        Normalize-String $uf,
        Normalize-String $nome,
        Normalize-String $mun
    ) -join "|"
}

function Ensure-Columns([object[]]$Rows, [string[]]$Columns) {
    foreach ($row in $Rows) {
        foreach ($col in $Columns) {
            if (-not $row.PSObject.Properties[$col]) {
                $row | Add-Member -NotePropertyName $col -NotePropertyValue "" -Force
            }
        }
    }
}

function Resolve-Status([string]$Status) {
    if ([string]::IsNullOrWhiteSpace($Status)) { return "NAO_ENCONTRADO" }
    if ($Status -eq "PENDENTE_PESQUISA") { return "NAO_ENCONTRADO" }
    return $Status
}

function Resolve-DefaultAcao([string]$Status) {
    if ($Status -eq "OK_PDF") { return "OK" }
    return "NOVA_BUSCA"
}

function Find-UnusedMatch(
    [object[]]$Rows,
    [string]$K1,
    [string]$K2,
    [string]$K3,
    [string]$K4
) {
    $m1 = $Rows | Where-Object { -not $_._Used -and $_._K1 -eq $K1 } | Select-Object -First 1
    if ($m1) { return [pscustomobject]@{ Row = $m1; Nivel = "L1_STRICT" } }

    $m2 = $Rows | Where-Object { -not $_._Used -and $_._K2 -eq $K2 } | Select-Object -First 1
    if ($m2) { return [pscustomobject]@{ Row = $m2; Nivel = "L2_INST_MUN_MOD" } }

    $m3 = $Rows | Where-Object { -not $_._Used -and $_._K3 -eq $K3 } | Select-Object -First 1
    if ($m3) { return [pscustomobject]@{ Row = $m3; Nivel = "L3_INST_MUN" } }

    $m4 = $Rows | Where-Object { -not $_._Used -and $_._K4 -eq $K4 } | Select-Object -First 1
    if ($m4) { return [pscustomobject]@{ Row = $m4; Nivel = "L4_NOME_MUN" } }

    return $null
}

if (-not (Test-Path $RefDir)) {
    throw "Diretorio de referencia nao encontrado: $RefDir"
}
if (-not (Test-Path $SourceCsvPath)) {
    throw "CSV de origem nao encontrado: $SourceCsvPath"
}

$refFiles = Get-ChildItem -Path $RefDir -Filter "Pesquisa_*.csv" -File | Sort-Object Name
$referenceRows = @()

foreach ($f in $refFiles) {
    $uf = ($f.BaseName -replace "^Pesquisa_", "").ToUpperInvariant()
    $lines = Get-Content -Path $f.FullName -Encoding UTF8 | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
    $parsed = $lines | ConvertFrom-Csv -Header "INSTITUICAO","MODALIDADE","NOME_POLO_OU_CAMPUS","MUNICIPIO_POLO"

    foreach ($r in $parsed) {
        if ((Normalize-String ([string]$r.INSTITUICAO)) -eq "instituicao") { continue }
        $referenceRows += [pscustomobject]@{
            UF = [string]$uf
            INSTITUICAO = [string]$r.INSTITUICAO
            MODALIDADE = [string]$r.MODALIDADE
            NOME_POLO_OU_CAMPUS = [string]$r.NOME_POLO_OU_CAMPUS
            MUNICIPIO_POLO = [string]$r.MUNICIPIO_POLO
        }
    }
}

Write-Host "Total de linhas na referencia canonica: $($referenceRows.Count)" -ForegroundColor Green

$sourceRows = @(Import-Csv -Path $SourceCsvPath -Encoding UTF8)
Write-Host "Total de linhas no consolidado de origem: $($sourceRows.Count)" -ForegroundColor Yellow

Ensure-Columns -Rows $sourceRows -Columns $ExpectedColumns

for ($i = 0; $i -lt $sourceRows.Count; $i++) {
    $row = $sourceRows[$i]
    $row | Add-Member -NotePropertyName _Index -NotePropertyValue $i -Force
    $row | Add-Member -NotePropertyName _Used -NotePropertyValue $false -Force
    $row | Add-Member -NotePropertyName _K1 -NotePropertyValue (Build-KeyStrict $row.UF $row.INSTITUICAO $row.MODALIDADE $row.NOME_POLO_OU_CAMPUS $row.MUNICIPIO_POLO) -Force
    $row | Add-Member -NotePropertyName _K2 -NotePropertyValue (Build-KeyInstMunMod $row.UF $row.INSTITUICAO $row.MODALIDADE $row.MUNICIPIO_POLO) -Force
    $row | Add-Member -NotePropertyName _K3 -NotePropertyValue (Build-KeyInstMun $row.UF $row.INSTITUICAO $row.MUNICIPIO_POLO) -Force
    $row | Add-Member -NotePropertyName _K4 -NotePropertyValue (Build-KeyNomeMun $row.UF $row.NOME_POLO_OU_CAMPUS $row.MUNICIPIO_POLO) -Force
}

$canonicalRows = @()
$matchStats = @{}

foreach ($ref in $referenceRows) {
    $refK1 = Build-KeyStrict $ref.UF $ref.INSTITUICAO $ref.MODALIDADE $ref.NOME_POLO_OU_CAMPUS $ref.MUNICIPIO_POLO
    $refK2 = Build-KeyInstMunMod $ref.UF $ref.INSTITUICAO $ref.MODALIDADE $ref.MUNICIPIO_POLO
    $refK3 = Build-KeyInstMun $ref.UF $ref.INSTITUICAO $ref.MUNICIPIO_POLO
    $refK4 = Build-KeyNomeMun $ref.UF $ref.NOME_POLO_OU_CAMPUS $ref.MUNICIPIO_POLO

    $found = Find-UnusedMatch -Rows $sourceRows -K1 $refK1 -K2 $refK2 -K3 $refK3 -K4 $refK4

    if ($found) {
        $m = $found.Row
        $m._Used = $true

        $nivel = $found.Nivel
        if (-not $matchStats.ContainsKey($nivel)) { $matchStats[$nivel] = 0 }
        $matchStats[$nivel]++

        $status = Resolve-Status ([string]$m.STATUS_LINK)
        $acao = [string]$m.ACAO_RECOMENDADA
        if ([string]::IsNullOrWhiteSpace($acao)) { $acao = Resolve-DefaultAcao $status }

        $curso = [string]$m.CURSO
        if ([string]::IsNullOrWhiteSpace($curso)) { $curso = "Licenciatura em Matematica" }

        $ppcCompartilhado = [string]$m.PPC_COMPARTILHADO
        if ([string]::IsNullOrWhiteSpace($ppcCompartilhado)) { $ppcCompartilhado = "NAO" }

        $tipoVinculo = [string]$m.TIPO_VINCULO
        if ([string]::IsNullOrWhiteSpace($tipoVinculo)) { $tipoVinculo = "POLO_ESPECIFICO" }

        $evidencia = [string]$m.EVIDENCIA_MINIMA
        if ([string]::IsNullOrWhiteSpace($evidencia)) {
            if ($status -eq "OK_PDF") { $evidencia = "OK_PDF" } else { $evidencia = "NAO_ENCONTRADO" }
        }

        $obs = [string]$m.OBS
        if ([string]::IsNullOrWhiteSpace($obs)) {
            $obs = "Reconciliado para base canonica ($nivel)."
        }

        $canonicalRows += [pscustomobject]@{
            UF = [string]$ref.UF
            INSTITUICAO = [string]$ref.INSTITUICAO
            MODALIDADE = [string]$ref.MODALIDADE
            NOME_POLO_OU_CAMPUS = [string]$ref.NOME_POLO_OU_CAMPUS
            MUNICIPIO_POLO = [string]$ref.MUNICIPIO_POLO
            CURSO = [string]$curso
            URL_FONTE = [string]$m.URL_FONTE
            URL_DOWNLOAD_PDF = [string]$m.URL_DOWNLOAD_PDF
            URL_DOWNLOAD_PDF_LIMPA = [string]$m.URL_DOWNLOAD_PDF_LIMPA
            STATUS_LINK = [string]$status
            HASH_OU_ID_PDF_CANONICO = [string]$m.HASH_OU_ID_PDF_CANONICO
            PPC_COMPARTILHADO = [string]$ppcCompartilhado
            GRUPO_COMPARTILHAMENTO_ID = [string]$m.GRUPO_COMPARTILHAMENTO_ID
            QTD_POLOS_NO_GRUPO = [string]$m.QTD_POLOS_NO_GRUPO
            TIPO_VINCULO = [string]$tipoVinculo
            ANO_PPC = [string]$m.ANO_PPC
            LOCALIDADE_DOCUMENTO = [string]$m.LOCALIDADE_DOCUMENTO
            NOME_ARQUIVO_LOCAL = [string]$m.NOME_ARQUIVO_LOCAL
            CAMINHO_ARQUIVO_LOCAL = [string]$m.CAMINHO_ARQUIVO_LOCAL
            EVIDENCIA_MINIMA = [string]$evidencia
            OBS = [string]$obs
            ACAO_RECOMENDADA = [string]$acao
        }
    }
    else {
        if (-not $matchStats.ContainsKey("SEM_MATCH")) { $matchStats["SEM_MATCH"] = 0 }
        $matchStats["SEM_MATCH"]++

        $canonicalRows += [pscustomobject]@{
            UF = [string]$ref.UF
            INSTITUICAO = [string]$ref.INSTITUICAO
            MODALIDADE = [string]$ref.MODALIDADE
            NOME_POLO_OU_CAMPUS = [string]$ref.NOME_POLO_OU_CAMPUS
            MUNICIPIO_POLO = [string]$ref.MUNICIPIO_POLO
            CURSO = "Licenciatura em Matematica"
            URL_FONTE = ""
            URL_DOWNLOAD_PDF = ""
            URL_DOWNLOAD_PDF_LIMPA = ""
            STATUS_LINK = "NAO_ENCONTRADO"
            HASH_OU_ID_PDF_CANONICO = ""
            PPC_COMPARTILHADO = "NAO"
            GRUPO_COMPARTILHAMENTO_ID = ""
            QTD_POLOS_NO_GRUPO = ""
            TIPO_VINCULO = "POLO_ESPECIFICO"
            ANO_PPC = ""
            LOCALIDADE_DOCUMENTO = ""
            NOME_ARQUIVO_LOCAL = ""
            CAMINHO_ARQUIVO_LOCAL = ""
            EVIDENCIA_MINIMA = "NAO_ENCONTRADO"
            OBS = "Sem match no consolidado anterior; requer nova busca oficial."
            ACAO_RECOMENDADA = "NOVA_BUSCA"
        }
    }
}

$quarantineRows = $sourceRows | Where-Object { -not $_._Used } | ForEach-Object {
    [pscustomobject]@{
        UF = [string]$_.UF
        INSTITUICAO = [string]$_.INSTITUICAO
        MODALIDADE = [string]$_.MODALIDADE
        NOME_POLO_OU_CAMPUS = [string]$_.NOME_POLO_OU_CAMPUS
        MUNICIPIO_POLO = [string]$_.MUNICIPIO_POLO
        CURSO = [string]$_.CURSO
        URL_FONTE = [string]$_.URL_FONTE
        URL_DOWNLOAD_PDF = [string]$_.URL_DOWNLOAD_PDF
        URL_DOWNLOAD_PDF_LIMPA = [string]$_.URL_DOWNLOAD_PDF_LIMPA
        STATUS_LINK = [string]$_.STATUS_LINK
        HASH_OU_ID_PDF_CANONICO = [string]$_.HASH_OU_ID_PDF_CANONICO
        PPC_COMPARTILHADO = [string]$_.PPC_COMPARTILHADO
        GRUPO_COMPARTILHAMENTO_ID = [string]$_.GRUPO_COMPARTILHAMENTO_ID
        QTD_POLOS_NO_GRUPO = [string]$_.QTD_POLOS_NO_GRUPO
        TIPO_VINCULO = [string]$_.TIPO_VINCULO
        ANO_PPC = [string]$_.ANO_PPC
        LOCALIDADE_DOCUMENTO = [string]$_.LOCALIDADE_DOCUMENTO
        NOME_ARQUIVO_LOCAL = [string]$_.NOME_ARQUIVO_LOCAL
        CAMINHO_ARQUIVO_LOCAL = [string]$_.CAMINHO_ARQUIVO_LOCAL
        EVIDENCIA_MINIMA = [string]$_.EVIDENCIA_MINIMA
        OBS = [string]$_.OBS
        ACAO_RECOMENDADA = [string]$_.ACAO_RECOMENDADA
    }
}

$canonicalRows | Select-Object $ExpectedColumns | Export-Csv -Path $OutCanonical -NoTypeInformation -Encoding UTF8
$quarantineRows | Select-Object $ExpectedColumns | Export-Csv -Path $OutQuarantine -NoTypeInformation -Encoding UTF8

$statusSummary = $canonicalRows | Group-Object STATUS_LINK | Sort-Object Name

Write-Host "Base canonica gerada com $($canonicalRows.Count) linhas em: $OutCanonical" -ForegroundColor Green
Write-Host "Base quarentena gerada com $($quarantineRows.Count) linhas em: $OutQuarantine" -ForegroundColor Yellow

Write-Host "Resumo de status (base canonica):" -ForegroundColor Cyan
foreach ($g in $statusSummary) {
    Write-Host ("  {0}: {1}" -f $g.Name, $g.Count)
}

Write-Host "Resumo de nivel de match:" -ForegroundColor Cyan
foreach ($k in ($matchStats.Keys | Sort-Object)) {
    Write-Host ("  {0}: {1}" -f $k, $matchStats[$k])
}

if ($SetAsMain) {
    $mainPath = Join-Path (Split-Path $OutCanonical -Parent) "mapeamento_ppc_polos.csv"
    if (Test-Path $mainPath) {
        $ts = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupPath = Join-Path (Split-Path $mainPath -Parent) ("mapeamento_ppc_polos_PRE_RECON_{0}.csv" -f $ts)
        Copy-Item -Path $mainPath -Destination $backupPath -Force
        Write-Host "Backup do CSV principal salvo em: $backupPath" -ForegroundColor DarkGray
    }

    Copy-Item -Path $OutCanonical -Destination $mainPath -Force
    Write-Host "CSV principal atualizado para base canonica: $mainPath" -ForegroundColor Green
}

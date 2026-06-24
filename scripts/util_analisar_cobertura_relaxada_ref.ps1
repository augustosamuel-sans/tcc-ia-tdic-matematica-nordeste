param(
    [string]$RootPath = "c:\Users\augus\Music\TCC\Data\new_date"
)

$ErrorActionPreference = "Stop"

$refDir = Join-Path $RootPath "dados_iniciais_ref\data_2_estrutura"
$consPath = Join-Path $RootPath "output_csv\mapeamento_ppc_polos.csv"
$outPath = Join-Path $RootPath "output_csv\auditoria_base_ref\COBERTURA_RELAXADA_REF.csv"

function Normalize-Text([string]$text) {
    if ([string]::IsNullOrWhiteSpace($text)) { return "" }
    $norm = $text.Trim().Normalize([Text.NormalizationForm]::FormD)
    $sb = New-Object System.Text.StringBuilder
    foreach ($ch in $norm.ToCharArray()) {
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($ch) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$sb.Append($ch)
        }
    }
    $plain = $sb.ToString().Normalize([Text.NormalizationForm]::FormC).ToLowerInvariant()
    $plain = $plain -replace "[\u2018\u2019\u0060\u00B4]", "'"
    $plain = $plain -replace "[^\p{L}\p{Nd}\s\-\(\)'/]", " "
    return (($plain -replace "\s+", " ").Trim())
}

function Normalize-Modalidade([string]$m) {
    $x = Normalize-Text $m
    if ($x -match "distancia|ead") { return "EAD" }
    if ($x -match "presencial") { return "PRESENCIAL" }
    return $x.ToUpperInvariant()
}

function Normalize-Instituicao([string]$inst) {
    if ([string]::IsNullOrWhiteSpace($inst)) { return "" }
    $raw = $inst.Trim()
    if ($raw -match "\(([A-Za-z0-9]{2,10})\)") { return $matches[1].ToUpperInvariant() }
    $compact = ($raw -replace "\s+", "")
    if ($compact -match "^[A-Z0-9]{2,10}$") { return $compact.ToUpperInvariant() }
    if ($raw -match "\b([A-Z]{2,10})\b") { return $matches[1].ToUpperInvariant() }
    return (Normalize-Text $raw).ToUpperInvariant()
}

$cons = Import-Csv -Path $consPath
$ix1 = @{}
$ix2 = @{}
$ix3 = @{}

foreach ($r in $cons) {
    $uf = ([string]$r.UF).ToUpperInvariant()
    $inst = Normalize-Instituicao ([string]$r.INSTITUICAO)
    $mod = Normalize-Modalidade ([string]$r.MODALIDADE)
    $nome = Normalize-Text ([string]$r.NOME_POLO_OU_CAMPUS)
    $mun = Normalize-Text ([string]$r.MUNICIPIO_POLO)

    $k1 = "$uf||$inst||$mod||$nome||$mun"
    $k2 = "$uf||$inst||$mod||$mun"
    $k3 = "$uf||$mod||$mun"
    $ix1[$k1] = $true
    $ix2[$k2] = $true
    $ix3[$k3] = $true
}

$rows = @()
$files = Get-ChildItem -Path $refDir -Filter "Pesquisa_*.csv" -File | Sort-Object Name
foreach ($f in $files) {
    $uf = ($f.BaseName -replace "^Pesquisa_", "").ToUpperInvariant()
    $lines = Get-Content -Path $f.FullName -Encoding Default | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
    $parsed = $lines | ConvertFrom-Csv -Header "INSTITUICAO","MODALIDADE","NOME_POLO_OU_CAMPUS","MUNICIPIO_POLO"

    foreach ($r in $parsed) {
        $inst = Normalize-Instituicao ([string]$r.INSTITUICAO)
        $mod = Normalize-Modalidade ([string]$r.MODALIDADE)
        $nome = Normalize-Text ([string]$r.NOME_POLO_OU_CAMPUS)
        $mun = Normalize-Text ([string]$r.MUNICIPIO_POLO)

        $k1 = "$uf||$inst||$mod||$nome||$mun"
        $k2 = "$uf||$inst||$mod||$mun"
        $k3 = "$uf||$mod||$mun"

        $nivel = if ($ix1.ContainsKey($k1)) { "L1_STRICT" }
            elseif ($ix2.ContainsKey($k2)) { "L2_INST_MUN" }
            elseif ($ix3.ContainsKey($k3)) { "L3_MUN_MODAL" }
            else { "SEM_COBERTURA" }

        $rows += [pscustomobject]@{
            UF = $uf
            INSTITUICAO = [string]$r.INSTITUICAO
            MODALIDADE = [string]$r.MODALIDADE
            NOME_POLO_OU_CAMPUS = [string]$r.NOME_POLO_OU_CAMPUS
            MUNICIPIO_POLO = [string]$r.MUNICIPIO_POLO
            NIVEL_COBERTURA = $nivel
        }
    }
}

$rows | Export-Csv -Path $outPath -NoTypeInformation -Encoding UTF8

$resumo = $rows |
    Group-Object UF,NIVEL_COBERTURA |
    ForEach-Object {
        [pscustomobject]@{
            UF = $_.Group[0].UF
            NIVEL_COBERTURA = $_.Group[0].NIVEL_COBERTURA
            QTD = $_.Count
        }
    } |
    Sort-Object UF,NIVEL_COBERTURA

$resumo | Format-Table -AutoSize
Write-Output ("TOTAL_REF=" + $rows.Count)
Write-Output ("L1_STRICT=" + (@($rows | Where-Object { $_.NIVEL_COBERTURA -eq "L1_STRICT" }).Count))
Write-Output ("L2_INST_MUN=" + (@($rows | Where-Object { $_.NIVEL_COBERTURA -eq "L2_INST_MUN" }).Count))
Write-Output ("L3_MUN_MODAL=" + (@($rows | Where-Object { $_.NIVEL_COBERTURA -eq "L3_MUN_MODAL" }).Count))
Write-Output ("SEM_COBERTURA=" + (@($rows | Where-Object { $_.NIVEL_COBERTURA -eq "SEM_COBERTURA" }).Count))
Write-Output ("Relatorio: " + $outPath)

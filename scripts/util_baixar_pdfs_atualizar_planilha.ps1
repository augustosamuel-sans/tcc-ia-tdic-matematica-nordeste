param(
    [string]$UF = "AL",
    [string]$RootPath = "c:\Users\augus\Music\TCC\Data\new_date",
    [int]$TimeoutSec = 60
)

$ErrorActionPreference = "Stop"

$csvPath = Join-Path $RootPath "output_csv\mapeamento_ppc_polos.csv"
$pdfDir = Join-Path $RootPath ("pdfs_baixados\" + $UF)
$logDir = Join-Path $RootPath "logs"
$logPath = Join-Path $logDir ("DOWNLOAD_" + $UF + "_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")

if (!(Test-Path $csvPath)) { throw "CSV nao encontrado: $csvPath" }
if (!(Test-Path $pdfDir)) { New-Item -ItemType Directory -Path $pdfDir | Out-Null }
if (!(Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

function Remove-Accents([string]$text) {
    if ([string]::IsNullOrWhiteSpace($text)) { return "" }
    $normalized = $text.Normalize([Text.NormalizationForm]::FormD)
    $sb = New-Object System.Text.StringBuilder
    foreach ($c in $normalized.ToCharArray()) {
        if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($c) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$sb.Append($c)
        }
    }
    return $sb.ToString().Normalize([Text.NormalizationForm]::FormC)
}

function Sanitize([string]$text) {
    $t = Remove-Accents $text
    $t = $t -replace '[^A-Za-z0-9]+', '_'
    $t = $t.Trim('_')
    if ($t.Length -gt 64) { $t = $t.Substring(0,64) }
    if ([string]::IsNullOrWhiteSpace($t)) { return "NA" }
    return $t
}

function Clean-Url([string]$url) {
    if ([string]::IsNullOrWhiteSpace($url)) { return "" }
    $u = $url.Trim()
    $u = $u -replace '\s*\[(web|page):\d+\]\s*$', ''
    $u = $u.Trim('"')
    if ($u -match '\.\.\.') { return "" }
    if ($u -notmatch '^https?://') { return "" }
    return $u
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

function Get-HeaderBytes([string]$path, [int]$count=8) {
    $fs = [System.IO.File]::OpenRead($path)
    try {
        $buf = New-Object byte[] $count
        $null = $fs.Read($buf, 0, $count)
        return $buf
    }
    finally { $fs.Close() }
}

function Get-FileSha256([string]$path) {
    $hash = Get-FileHash -Path $path -Algorithm SHA256
    return $hash.Hash
}

$rows = Import-Csv -Path $csvPath
Ensure-Columns $rows @("LOCALIDADE_DOCUMENTO","NOME_ARQUIVO_LOCAL","CAMINHO_ARQUIVO_LOCAL","URL_DOWNLOAD_PDF_LIMPA")

$target = $rows | Where-Object { $_.UF -eq $UF }

# Agrupar por URL limpa para compartilhar o mesmo PDF quando aplicavel.
$groups = $target |
    ForEach-Object {
        $_ | Add-Member -NotePropertyName __URL_LIMPA -NotePropertyValue (Clean-Url $_.URL_DOWNLOAD_PDF) -Force
        $_
    } |
    Group-Object __URL_LIMPA

$downloaded = 0
$failed = 0
$skipped = 0
$docIndex = 1

foreach ($g in $groups) {
    $url = $g.Name
    $groupRows = $g.Group

    if ([string]::IsNullOrWhiteSpace($url)) {
        foreach ($r in $groupRows) {
            $r.URL_DOWNLOAD_PDF_LIMPA = ""
            if ([string]::IsNullOrWhiteSpace($r.STATUS_LINK) -or $r.STATUS_LINK -eq "OK_PDF") {
                $r.STATUS_LINK = "NAO_ENCONTRADO"
            }
            if ($r.ACAO_RECOMENDADA -eq "OK") { $r.ACAO_RECOMENDADA = "NOVA_BUSCA" }
        }
        $skipped += $groupRows.Count
        continue
    }

    $base = $groupRows[0]
    $isShared = ($groupRows.Count -gt 1) -or ($base.PPC_COMPARTILHADO -match 'SIM')

    $municipios = $groupRows | ForEach-Object { $_.MUNICIPIO_POLO } | Where-Object { $_ } | Select-Object -Unique
    $polos = $groupRows | ForEach-Object { $_.NOME_POLO_OU_CAMPUS } | Where-Object { $_ } | Select-Object -Unique

    $localidade = if ($isShared) {
        "POLOS_" + $polos.Count + "__" + (($municipios | ForEach-Object { Sanitize $_ }) -join "_")
    } else {
        "POLO__" + (Sanitize $base.NOME_POLO_OU_CAMPUS) + "__" + (Sanitize $base.MUNICIPIO_POLO)
    }

    if ($localidade.Length -gt 100) { $localidade = $localidade.Substring(0,100) }

    $ano = if ([string]::IsNullOrWhiteSpace($base.ANO_PPC)) { "NA" } else { Sanitize $base.ANO_PPC }
    $inst = Sanitize $base.INSTITUICAO
    $tipo = if ($base.MODALIDADE -match 'Dist') { 'EAD' } else { 'PRESENCIAL' }
    $docId = 'DOC' + ('{0:D4}' -f $docIndex)

    $fileName = "${UF}__${inst}__${tipo}__${localidade}__${ano}__${docId}.pdf"
    $filePath = Join-Path $pdfDir $fileName
    $tmpPath = $filePath + ".tmp"

    # Reuse existing local file for the same cleaned URL to prevent duplicates.
    $existingLocal = $rows |
        Where-Object {
            $_.UF -eq $UF -and
            $_.URL_DOWNLOAD_PDF_LIMPA -eq $url -and
            $_.CAMINHO_ARQUIVO_LOCAL -and
            (Test-Path $_.CAMINHO_ARQUIVO_LOCAL)
        } |
        Select-Object -First 1

    if ($existingLocal) {
        $existingPath = $existingLocal.CAMINHO_ARQUIVO_LOCAL
        $existingName = Split-Path -Path $existingPath -Leaf
        $existingHash = ""
        try { $existingHash = Get-FileSha256 -path $existingPath } catch { $existingHash = "" }

        foreach ($r in $groupRows) {
            $r.URL_DOWNLOAD_PDF_LIMPA = $url
            $r.STATUS_LINK = "OK_PDF"
            $r.LOCALIDADE_DOCUMENTO = $localidade
            $r.NOME_ARQUIVO_LOCAL = $existingName
            $r.CAMINHO_ARQUIVO_LOCAL = $existingPath
            if ($existingHash) { $r.HASH_OU_ID_PDF_CANONICO = $existingHash }
            if ([string]::IsNullOrWhiteSpace($r.ACAO_RECOMENDADA) -or $r.ACAO_RECOMENDADA -eq "NOVA_BUSCA") {
                $r.ACAO_RECOMENDADA = "OK"
            }
            if ($isShared) {
                $r.PPC_COMPARTILHADO = "SIM"
                if ([string]::IsNullOrWhiteSpace($r.QTD_POLOS_NO_GRUPO)) {
                    $r.QTD_POLOS_NO_GRUPO = [string]$groupRows.Count
                }
                if ([string]::IsNullOrWhiteSpace($r.TIPO_VINCULO)) {
                    $r.TIPO_VINCULO = "INSTITUCIONAL_COMPARTILHADO"
                }
            }
        }

        Add-Content -Path $logPath -Value ("REUSE | " + $existingName + " | " + $url)
        $downloaded += $groupRows.Count
        continue
    }

    try {
        Invoke-WebRequest -Uri $url -OutFile $tmpPath -MaximumRedirection 8 -TimeoutSec $TimeoutSec -ErrorAction Stop
        $header = Get-HeaderBytes -path $tmpPath -count 5
        $signature = [System.Text.Encoding]::ASCII.GetString($header)

        if ($signature -ne "%PDF-") {
            Remove-Item -LiteralPath $tmpPath -ErrorAction SilentlyContinue
            foreach ($r in $groupRows) {
                $r.URL_DOWNLOAD_PDF_LIMPA = $url
                $r.STATUS_LINK = "HTML_INTERMEDIARIO"
                $r.LOCALIDADE_DOCUMENTO = $localidade
                $r.NOME_ARQUIVO_LOCAL = ""
                $r.CAMINHO_ARQUIVO_LOCAL = ""
                if ($r.ACAO_RECOMENDADA -eq "OK") { $r.ACAO_RECOMENDADA = "NOVA_BUSCA" }
            }
            Add-Content -Path $logPath -Value ("NAO_PDF | " + $url)
            $failed += $groupRows.Count
            continue
        }

        Move-Item -LiteralPath $tmpPath -Destination $filePath -Force
        $fileHash = ""
        try { $fileHash = Get-FileSha256 -path $filePath } catch { $fileHash = "" }

        foreach ($r in $groupRows) {
            $r.URL_DOWNLOAD_PDF_LIMPA = $url
            $r.STATUS_LINK = "OK_PDF"
            $r.LOCALIDADE_DOCUMENTO = $localidade
            $r.NOME_ARQUIVO_LOCAL = $fileName
            $r.CAMINHO_ARQUIVO_LOCAL = $filePath
            if ($fileHash) { $r.HASH_OU_ID_PDF_CANONICO = $fileHash }
            if ([string]::IsNullOrWhiteSpace($r.ACAO_RECOMENDADA) -or $r.ACAO_RECOMENDADA -eq "NOVA_BUSCA") {
                $r.ACAO_RECOMENDADA = "OK"
            }
            if ($isShared) {
                $r.PPC_COMPARTILHADO = "SIM"
                if ([string]::IsNullOrWhiteSpace($r.QTD_POLOS_NO_GRUPO)) {
                    $r.QTD_POLOS_NO_GRUPO = [string]$groupRows.Count
                }
                if ([string]::IsNullOrWhiteSpace($r.TIPO_VINCULO)) {
                    $r.TIPO_VINCULO = "INSTITUCIONAL_COMPARTILHADO"
                }
            }
        }

        Add-Content -Path $logPath -Value ("OK | " + $fileName + " | " + $url)
        $downloaded += $groupRows.Count
        $docIndex++
    }
    catch {
        Remove-Item -LiteralPath $tmpPath -ErrorAction SilentlyContinue
        foreach ($r in $groupRows) {
            $r.URL_DOWNLOAD_PDF_LIMPA = $url
            if ($_.Exception.Message -match '404') {
                $r.STATUS_LINK = "404"
            }
            elseif ($_.Exception.Message -match '403|401|forbidden|unauthorized') {
                $r.STATUS_LINK = "BLOQUEADO"
            }
            else {
                if ([string]::IsNullOrWhiteSpace($r.STATUS_LINK) -or $r.STATUS_LINK -eq "OK_PDF") {
                    $r.STATUS_LINK = "NAO_ENCONTRADO"
                }
            }
            $r.LOCALIDADE_DOCUMENTO = $localidade
            $r.NOME_ARQUIVO_LOCAL = ""
            $r.CAMINHO_ARQUIVO_LOCAL = ""
            if ($r.ACAO_RECOMENDADA -eq "OK") { $r.ACAO_RECOMENDADA = "NOVA_BUSCA" }
        }
        Add-Content -Path $logPath -Value ("ERRO | " + $url + " | " + $_.Exception.Message)
        $failed += $groupRows.Count
    }
}

$rows |
    Select-Object UF,INSTITUICAO,MODALIDADE,NOME_POLO_OU_CAMPUS,MUNICIPIO_POLO,CURSO,URL_FONTE,URL_DOWNLOAD_PDF,URL_DOWNLOAD_PDF_LIMPA,STATUS_LINK,HASH_OU_ID_PDF_CANONICO,PPC_COMPARTILHADO,GRUPO_COMPARTILHAMENTO_ID,QTD_POLOS_NO_GRUPO,TIPO_VINCULO,ANO_PPC,LOCALIDADE_DOCUMENTO,NOME_ARQUIVO_LOCAL,CAMINHO_ARQUIVO_LOCAL,EVIDENCIA_MINIMA,OBS,ACAO_RECOMENDADA |
    Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8

Write-Output ("UF=" + $UF + " | baixados=" + $downloaded + " | falhas=" + $failed + " | ignorados=" + $skipped)
Write-Output ("Log: " + $logPath)

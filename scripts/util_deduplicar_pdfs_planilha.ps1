param(
    [string]$UF = "AL",
    [string]$RootPath = "c:\Users\augus\Music\TCC\Data\new_date"
)

$ErrorActionPreference = "Stop"

$csvPath = Join-Path $RootPath "output_csv\mapeamento_ppc_polos.csv"
$pdfDir = Join-Path $RootPath ("pdfs_baixados\" + $UF)
$logDir = Join-Path $RootPath "logs"
$logPath = Join-Path $logDir ("DEDUP_" + $UF + "_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")

if (!(Test-Path $csvPath)) { throw "CSV nao encontrado: $csvPath" }
if (!(Test-Path $pdfDir)) { throw "Pasta de PDFs nao encontrada: $pdfDir" }
if (!(Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

function Extract-PolosCount([string]$name) {
    if ($name -match 'POLOS_(\d+)') { return [int]$matches[1] }
    return 0
}

$rows = Import-Csv -Path $csvPath
$files = Get-ChildItem -Path $pdfDir -Filter "*.pdf"
if ($files.Count -eq 0) {
    Write-Output "Nenhum PDF para deduplicar em $pdfDir"
    exit 0
}

$fileInfo = @()
foreach ($f in $files) {
    $h = Get-FileHash -Path $f.FullName -Algorithm SHA256
    $fileInfo += [pscustomobject]@{
        Path = $f.FullName
        Name = $f.Name
        Hash = $h.Hash
        PolosCount = Extract-PolosCount $f.Name
        Length = $f.Length
        LastWrite = $f.LastWriteTimeUtc
    }
}

$groups = $fileInfo | Group-Object Hash
$removed = 0
$kept = 0
$orphansRemoved = 0

foreach ($g in $groups) {
    $items = $g.Group
    if ($items.Count -eq 1) { continue }

    # Keep candidate with highest POLOS count, then newest, then shortest name.
    $keep = $items |
        Sort-Object @{Expression='PolosCount';Descending=$true}, @{Expression='LastWrite';Descending=$true}, @{Expression={ $_.Name.Length };Descending=$false} |
        Select-Object -First 1

    $kept++
    Add-Content -Path $logPath -Value ("KEEP | " + $keep.Name + " | HASH=" + $keep.Hash)

    foreach ($dup in ($items | Where-Object { $_.Path -ne $keep.Path })) {
        # Update CSV references from duplicate path to keep path
        foreach ($r in $rows) {
            if ($r.CAMINHO_ARQUIVO_LOCAL -eq $dup.Path) {
                $r.CAMINHO_ARQUIVO_LOCAL = $keep.Path
                $r.NOME_ARQUIVO_LOCAL = $keep.Name
                $r.HASH_OU_ID_PDF_CANONICO = $keep.Hash
                if ([string]::IsNullOrWhiteSpace($r.URL_DOWNLOAD_PDF_LIMPA) -and $r.URL_DOWNLOAD_PDF) {
                    $r.URL_DOWNLOAD_PDF_LIMPA = $r.URL_DOWNLOAD_PDF
                }
            }
        }

        Remove-Item -LiteralPath $dup.Path -Force
        Add-Content -Path $logPath -Value ("REMOVE_DUP | " + $dup.Name + " -> " + $keep.Name)
        $removed++
    }
}

# Fill hash for all rows that point to existing files.
foreach ($r in $rows) {
    if ($r.UF -ne $UF) { continue }
    if ($r.CAMINHO_ARQUIVO_LOCAL -and (Test-Path $r.CAMINHO_ARQUIVO_LOCAL)) {
        if ([string]::IsNullOrWhiteSpace($r.HASH_OU_ID_PDF_CANONICO)) {
            try {
                $r.HASH_OU_ID_PDF_CANONICO = (Get-FileHash -Path $r.CAMINHO_ARQUIVO_LOCAL -Algorithm SHA256).Hash
            } catch {}
        }
    }
}

$rows |
    Select-Object UF,INSTITUICAO,MODALIDADE,NOME_POLO_OU_CAMPUS,MUNICIPIO_POLO,CURSO,URL_FONTE,URL_DOWNLOAD_PDF,URL_DOWNLOAD_PDF_LIMPA,STATUS_LINK,HASH_OU_ID_PDF_CANONICO,PPC_COMPARTILHADO,GRUPO_COMPARTILHAMENTO_ID,QTD_POLOS_NO_GRUPO,TIPO_VINCULO,ANO_PPC,LOCALIDADE_DOCUMENTO,NOME_ARQUIVO_LOCAL,CAMINHO_ARQUIVO_LOCAL,EVIDENCIA_MINIMA,OBS,ACAO_RECOMENDADA |
    Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8

# Remove orphan files not referenced by CSV after dedup.
$referenced = $rows |
    Where-Object { $_.UF -eq $UF -and $_.CAMINHO_ARQUIVO_LOCAL -and (Test-Path $_.CAMINHO_ARQUIVO_LOCAL) } |
    Select-Object -ExpandProperty CAMINHO_ARQUIVO_LOCAL -Unique

$finalFiles = Get-ChildItem -Path $pdfDir -Filter "*.pdf"
foreach ($f in $finalFiles) {
    if ($referenced -notcontains $f.FullName) {
        Remove-Item -LiteralPath $f.FullName -Force
        Add-Content -Path $logPath -Value ("REMOVE_ORPHAN | " + $f.Name)
        $orphansRemoved++
    }
}

$finalFiles = Get-ChildItem -Path $pdfDir -Filter "*.pdf"
Write-Output ("UF=" + $UF + " | arquivos_finais=" + $finalFiles.Count + " | duplicados_removidos=" + $removed + " | orfaos_removidos=" + $orphansRemoved + " | grupos_dedup=" + $kept)
Write-Output ("Log: " + $logPath)

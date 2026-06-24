param(
    [string]$RootPath = "c:\Users\augus\Music\TCC\Data\new_date"
)

$ErrorActionPreference = "Stop"

$csvPath = Join-Path $RootPath "output_csv\mapeamento_ppc_polos.csv"
$outBase = Join-Path $RootPath "output_csv"
$porEstadoDir = Join-Path $outBase "por_estado"
$segPorEstadoDir = Join-Path $outBase "seguranca_por_estado"
$segGlobalPath = Join-Path $outBase "SEGURANCA_PDF_POLOS_TODOS_ESTADOS.csv"
$resUfPath = Join-Path $outBase "RESUMO_SEGURANCA_POR_UF.csv"

if (!(Test-Path $csvPath)) {
    throw "CSV nao encontrado: $csvPath"
}
if (!(Test-Path $porEstadoDir)) { New-Item -ItemType Directory -Path $porEstadoDir | Out-Null }
if (!(Test-Path $segPorEstadoDir)) { New-Item -ItemType Directory -Path $segPorEstadoDir | Out-Null }

function Ensure-Columns($rows, [string[]]$cols) {
    foreach ($r in $rows) {
        foreach ($c in $cols) {
            if (-not ($r.PSObject.Properties.Name -contains $c)) {
                Add-Member -InputObject $r -MemberType NoteProperty -Name $c -Value ""
            }
        }
    }
}

$rows = Import-Csv -Path $csvPath
if ($rows.Count -eq 0) {
    Write-Output "CSV vazio. Nada para atualizar."
    exit 0
}

Ensure-Columns $rows @(
    "UF","STATUS_LINK","HASH_OU_ID_PDF_CANONICO","URL_DOWNLOAD_PDF_LIMPA",
    "INSTITUICAO","NOME_POLO_OU_CAMPUS","MUNICIPIO_POLO",
    "NOME_ARQUIVO_LOCAL","CAMINHO_ARQUIVO_LOCAL","PPC_COMPARTILHADO"
)

$ufs = $rows | Where-Object { -not [string]::IsNullOrWhiteSpace($_.UF) } | Select-Object -ExpandProperty UF -Unique | Sort-Object

# 1) CSVs individuais por estado
foreach ($uf in $ufs) {
    $stateCsv = Join-Path $porEstadoDir ("mapeamento_ppc_polos_" + $uf + ".csv")
    $rows | Where-Object { $_.UF -eq $uf } | Export-Csv -Path $stateCsv -NoTypeInformation -Encoding UTF8
}

# 2) Seguranca de vinculo PDF x polos (somente OK_PDF)
$ok = $rows | Where-Object { $_.STATUS_LINK -eq "OK_PDF" }
$segRows = @()
foreach ($r in $ok) {
    $docKey = ""
    if ($r.HASH_OU_ID_PDF_CANONICO -and $r.HASH_OU_ID_PDF_CANONICO.Trim() -ne "") {
        $docKey = $r.HASH_OU_ID_PDF_CANONICO
    } elseif ($r.URL_DOWNLOAD_PDF_LIMPA -and $r.URL_DOWNLOAD_PDF_LIMPA.Trim() -ne "") {
        $docKey = $r.URL_DOWNLOAD_PDF_LIMPA
    } elseif ($r.NOME_ARQUIVO_LOCAL -and $r.NOME_ARQUIVO_LOCAL.Trim() -ne "") {
        $docKey = $r.NOME_ARQUIVO_LOCAL
    } else {
        $docKey = "SEM_CHAVE_DOC"
    }

    $certeza = "BAIXA"
    if ($docKey -ne "SEM_CHAVE_DOC" -and $r.CAMINHO_ARQUIVO_LOCAL -and $r.CAMINHO_ARQUIVO_LOCAL.Trim() -ne "") {
        $certeza = "ALTA"
    } elseif ($docKey -ne "SEM_CHAVE_DOC") {
        $certeza = "MEDIA"
    }

    $segRows += [pscustomobject]@{
        UF = $r.UF
        DOC_KEY = $docKey
        QTD_POLOS_MESMO_DOC = 0
        CERTEZA_VINCULO = $certeza
        INSTITUICAO = $r.INSTITUICAO
        NOME_POLO_OU_CAMPUS = $r.NOME_POLO_OU_CAMPUS
        MUNICIPIO_POLO = $r.MUNICIPIO_POLO
        NOME_ARQUIVO_LOCAL = $r.NOME_ARQUIVO_LOCAL
        CAMINHO_ARQUIVO_LOCAL = $r.CAMINHO_ARQUIVO_LOCAL
        PPC_COMPARTILHADO = $r.PPC_COMPARTILHADO
    }
}

$docCounts = @{}
$segRows | Group-Object UF,DOC_KEY | ForEach-Object {
    $docCounts[$_.Name] = $_.Count
}

$segRowsFinal = $segRows | ForEach-Object {
    $k = $_.UF + ", " + $_.DOC_KEY
    $_.QTD_POLOS_MESMO_DOC = $docCounts[$k]
    $_
}

$segRowsFinal |
    Sort-Object UF,DOC_KEY,INSTITUICAO,NOME_POLO_OU_CAMPUS |
    Export-Csv -Path $segGlobalPath -NoTypeInformation -Encoding UTF8

# 3) Seguranca por estado + resumo por UF
$summary = @()
foreach ($uf in $ufs) {
    $ufRows = $rows | Where-Object { $_.UF -eq $uf }
    $ufSeg = $segRowsFinal | Where-Object { $_.UF -eq $uf }

    $segUfPath = Join-Path $segPorEstadoDir ("SEGURANCA_PDF_POLOS_" + $uf + ".csv")
    $ufSeg | Sort-Object DOC_KEY,INSTITUICAO,NOME_POLO_OU_CAMPUS | Export-Csv -Path $segUfPath -NoTypeInformation -Encoding UTF8

    $summary += [pscustomobject]@{
        UF = $uf
        LINHAS_TOTAIS = $ufRows.Count
        OK_PDF = ($ufRows | Where-Object { $_.STATUS_LINK -eq "OK_PDF" }).Count
        DOCS_CANONICOS_UNICOS = ($ufSeg | Select-Object -ExpandProperty DOC_KEY -Unique).Count
        VINCULO_ALTA = ($ufSeg | Where-Object { $_.CERTEZA_VINCULO -eq "ALTA" }).Count
        VINCULO_MEDIA = ($ufSeg | Where-Object { $_.CERTEZA_VINCULO -eq "MEDIA" }).Count
        VINCULO_BAIXA = ($ufSeg | Where-Object { $_.CERTEZA_VINCULO -eq "BAIXA" }).Count
    }
}

$summary | Sort-Object UF | Export-Csv -Path $resUfPath -NoTypeInformation -Encoding UTF8

Write-Output ("CSVs por estado gerados em: " + $porEstadoDir)
Write-Output ("Seguranca global atualizada: " + $segGlobalPath)
Write-Output ("Resumo por UF atualizado: " + $resUfPath)
Write-Output ("UFs atualizadas: " + ($ufs -join ","))

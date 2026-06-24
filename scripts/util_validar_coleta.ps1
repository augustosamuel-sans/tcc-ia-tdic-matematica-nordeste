param(
    [string]$UF = "AL",
    [string]$RootPath = "c:\Users\augus\Music\TCC\Data\new_date"
)

$ErrorActionPreference = "Stop"

$inputDir = Join-Path $RootPath ("coleta_md_por_estado\" + $UF)
$inputDirAtual = Join-Path $inputDir "atual"
if (!(Test-Path $inputDir)) {
    Write-Error "Pasta nao encontrada: $inputDir"
}

$fileCandidates = @()
$fileCandidates += (Get-ChildItem -Path $inputDir -File -Filter "*.md" -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '^LEIA_ME' })
$fileCandidates += (Get-ChildItem -Path $inputDirAtual -File -Filter "*.md" -ErrorAction SilentlyContinue | Where-Object { $_.Name -notmatch '^LEIA_ME' })
$files = $fileCandidates | Sort-Object FullName -Unique
if ($files.Count -eq 0) {
    Write-Output "Nenhum arquivo .md em $inputDir ou $inputDirAtual"
    exit 0
}

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

function Split-YamlDocuments([string]$yamlBlock) {
    if ([string]::IsNullOrWhiteSpace($yamlBlock)) { return @() }
    $docs = $yamlBlock -split '(?m)^\s*---\s*$'
    return $docs | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
}

function Is-BlockComplete([string]$yamlBlock) {
    $required = @('instituicao', 'modalidade', 'nome_polo_ou_campus', 'municipio_polo', 'url_fonte', 'status_link')
    foreach ($k in $required) {
        if ($yamlBlock -notmatch ($k + ':\s*("(?!\.\.\.).+"|(?!\.\.\.|\s*$).+)')) {
            return $false
        }
    }
    return $true
}

$rows = @()
foreach ($f in $files) {
    $content = Get-Content -Path $f.FullName -Raw -Encoding UTF8
    $blocks = Get-YamlBlocks $content

    $completeCount = 0
    $templateCount = 0
    foreach ($b in $blocks) {
        $docs = Split-YamlDocuments $b
        if ($docs.Count -eq 0) { $docs = @($b) }
        foreach ($d in $docs) {
            if (Is-BlockComplete $d) { $completeCount++ }
            if ($d -match '(?m)^\s*[-\s]*[A-Za-z0-9_]+:\s*"?\.\.\."?\s*$') { $templateCount++ }
        }
    }

    $hasEvidence = $content -match 'evidencia_literal:\s*"[^\.][^"]+"'

    $status = if ($blocks.Count -eq 0) { "SEM_YAML" }
        elseif ($completeCount -gt 0 -and $templateCount -gt 0) { "MISTO" }
        elseif ($completeCount -gt 0) { "YAML_PREENCHIDO" }
        else { "YAML_TEMPLATE" }

    $rows += [pscustomobject]@{
        arquivo = $f.Name
        yaml_blocos = $blocks.Count
        yaml_completos = $completeCount
        yaml_template = $templateCount
        status = $status
        tem_evidencia = $hasEvidence
    }
}

$rows | Format-Table -AutoSize

$ok = @($rows | Where-Object { $_.status -eq "YAML_PREENCHIDO" }).Count
$misto = @($rows | Where-Object { $_.status -eq "MISTO" }).Count
$template = @($rows | Where-Object { $_.status -eq "YAML_TEMPLATE" }).Count
$semYaml = @($rows | Where-Object { $_.status -eq "SEM_YAML" }).Count

Write-Output ""
Write-Output ("Resumo UF=" + $UF + ": YAML_PREENCHIDO=" + $ok + "; MISTO=" + $misto + "; YAML_TEMPLATE=" + $template + "; SEM_YAML=" + $semYaml)

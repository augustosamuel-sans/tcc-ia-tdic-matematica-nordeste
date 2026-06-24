param(
    [Parameter(Mandatory=$true)]
    [string]$UF,
    [string]$RootPath = "c:\Users\augus\Music\TCC\Data\new_date"
)

$ErrorActionPreference = "Stop"

function Resolve-ScriptPath([string]$fileName, [string]$rootPath, [string]$selfPath) {
    $candidates = @()
    if (-not [string]::IsNullOrWhiteSpace($selfPath)) {
        $candidates += (Join-Path $selfPath $fileName)
    }
    $candidates += (Join-Path (Join-Path $rootPath "script") $fileName)
    $candidates += (Join-Path $rootPath $fileName)

    foreach ($c in ($candidates | Select-Object -Unique)) {
        if (Test-Path $c) { return $c }
    }
    throw "Script nao encontrado: $fileName"
}

$validar = Resolve-ScriptPath -fileName "util_validar_coleta.ps1" -rootPath $RootPath -selfPath $PSScriptRoot
$consolidar = Resolve-ScriptPath -fileName "util_consolidar_yaml_csv.ps1" -rootPath $RootPath -selfPath $PSScriptRoot
$baixar = Resolve-ScriptPath -fileName "util_baixar_pdfs_atualizar_planilha.ps1" -rootPath $RootPath -selfPath $PSScriptRoot
$dedup = Resolve-ScriptPath -fileName "util_deduplicar_pdfs_planilha.ps1" -rootPath $RootPath -selfPath $PSScriptRoot
$atualizar = Resolve-ScriptPath -fileName "util_atualizar_relatorios_qualidade.ps1" -rootPath $RootPath -selfPath $PSScriptRoot

foreach ($s in @($validar, $consolidar, $baixar, $dedup, $atualizar)) {
    if (!(Test-Path $s)) {
        throw "Script nao encontrado: $s"
    }
}

Write-Output ("[1/4] Validando coleta " + $UF)
& $validar -UF $UF -RootPath $RootPath

Write-Output ("[2/4] Consolidando YAML -> CSV " + $UF)
& $consolidar -UF $UF -RootPath $RootPath

Write-Output ("[3/4] Baixando PDFs e atualizando planilha " + $UF)
& $baixar -UF $UF -RootPath $RootPath

Write-Output ("[4/5] Deduplicando arquivos e planilha " + $UF)
& $dedup -UF $UF -RootPath $RootPath

Write-Output ("[5/5] Atualizando CSVs por estado e relatorios de seguranca")
& $atualizar -RootPath $RootPath

Write-Output ("Pipeline finalizado para UF=" + $UF)

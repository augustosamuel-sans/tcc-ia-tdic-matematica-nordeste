param(
	[string]$RootPath = "c:\Users\augus\Music\TCC\Data\new_date"
)

$ErrorActionPreference = "Stop"

$refDir = Join-Path $RootPath "dados_iniciais_ref\data_2_estrutura"
$consolidadoPath = Join-Path $RootPath "output_csv\mapeamento_ppc_polos.csv"
$outDir = Join-Path $RootPath "output_csv\auditoria_base_ref"

if (!(Test-Path $refDir)) {
	throw "Pasta de referencia nao encontrada: $refDir"
}
if (!(Test-Path $consolidadoPath)) {
	throw "CSV consolidado nao encontrado: $consolidadoPath"
}
if (!(Test-Path $outDir)) {
	New-Item -ItemType Directory -Path $outDir | Out-Null
}

function Normalize-Text([string]$text) {
	if ([string]::IsNullOrWhiteSpace($text)) { return "" }
	$t = $text.Trim()
	$norm = $t.Normalize([Text.NormalizationForm]::FormD)
	$sb = New-Object System.Text.StringBuilder
	foreach ($ch in $norm.ToCharArray()) {
		if ([Globalization.CharUnicodeInfo]::GetUnicodeCategory($ch) -ne [Globalization.UnicodeCategory]::NonSpacingMark) {
			[void]$sb.Append($ch)
		}
	}
	$plain = $sb.ToString().Normalize([Text.NormalizationForm]::FormC)
	$plain = $plain -replace "[\u2018\u2019\u0060\u00B4]", "'"
	$plain = $plain -replace "[^\p{L}\p{Nd}\s\-\(\)'/]+", " "
	return (($plain.ToLowerInvariant()) -replace "\s+", " ").Trim()
}

function Normalize-UF([string]$uf) {
	return (Normalize-Text $uf).ToUpperInvariant()
}

function Normalize-Modalidade([string]$modalidade) {
	$m = Normalize-Text $modalidade
	if ($m -match "distancia|ead") { return "EAD" }
	if ($m -match "presencial") { return "PRESENCIAL" }
	return $m.ToUpperInvariant()
}

function Get-InstituicaoCodigo([string]$instituicao) {
	if ([string]::IsNullOrWhiteSpace($instituicao)) { return "" }

	$raw = $instituicao.Trim()
	if ($raw -match "\(([A-Za-z0-9]{2,10})\)") {
		return $matches[1].ToUpperInvariant()
	}

	$compact = ($raw -replace "\s+", "")
	if ($compact -match "^[A-Z0-9]{2,10}$") {
		return $compact.ToUpperInvariant()
	}

	if ($raw -match "\b([A-Z]{2,10})\b") {
		return $matches[1].ToUpperInvariant()
	}

	return (Normalize-Text $raw).ToUpperInvariant()
}

function Build-KeyStrict([string]$uf, [string]$inst, [string]$mod, [string]$nome, [string]$mun) {
	return @(
		(Normalize-UF $uf),
		(Get-InstituicaoCodigo $inst),
		(Normalize-Modalidade $mod),
		(Normalize-Text $nome),
		(Normalize-Text $mun)
	) -join "||"
}

function Build-KeySoft([string]$uf, [string]$nome, [string]$mun) {
	return @(
		(Normalize-UF $uf),
		(Normalize-Text $nome),
		(Normalize-Text $mun)
	) -join "||"
}

$refRowsRaw = @()
$refFiles = Get-ChildItem -Path $refDir -Filter "Pesquisa_*.csv" -File | Sort-Object Name
foreach ($f in $refFiles) {
	$uf = ($f.BaseName -replace "^Pesquisa_", "").ToUpperInvariant()
	$lines = Get-Content -Path $f.FullName -Encoding Default | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
	$parsed = $lines | ConvertFrom-Csv -Header "INSTITUICAO","MODALIDADE","NOME_POLO_OU_CAMPUS","MUNICIPIO_POLO"
	foreach ($r in $parsed) {
		$refRowsRaw += [pscustomobject]@{
			UF = $uf
			INSTITUICAO = [string]$r.INSTITUICAO
			MODALIDADE = [string]$r.MODALIDADE
			NOME_POLO_OU_CAMPUS = [string]$r.NOME_POLO_OU_CAMPUS
			MUNICIPIO_POLO = [string]$r.MUNICIPIO_POLO
			KEY_STRICT = Build-KeyStrict -uf $uf -inst ([string]$r.INSTITUICAO) -mod ([string]$r.MODALIDADE) -nome ([string]$r.NOME_POLO_OU_CAMPUS) -mun ([string]$r.MUNICIPIO_POLO)
			KEY_SOFT = Build-KeySoft -uf $uf -nome ([string]$r.NOME_POLO_OU_CAMPUS) -mun ([string]$r.MUNICIPIO_POLO)
		}
	}
}

$refByStrict = $refRowsRaw | Group-Object KEY_STRICT
$refBySoft = $refRowsRaw | Group-Object KEY_SOFT
$refRowsUniqueStrict = $refByStrict | ForEach-Object { $_.Group[0] }

$consolidado = Import-Csv -Path $consolidadoPath
$consRows = @()
foreach ($r in $consolidado) {
	$consRows += [pscustomobject]@{
		UF = [string]$r.UF
		INSTITUICAO = [string]$r.INSTITUICAO
		MODALIDADE = [string]$r.MODALIDADE
		NOME_POLO_OU_CAMPUS = [string]$r.NOME_POLO_OU_CAMPUS
		MUNICIPIO_POLO = [string]$r.MUNICIPIO_POLO
		STATUS_LINK = [string]$r.STATUS_LINK
		URL_FONTE = [string]$r.URL_FONTE
		URL_DOWNLOAD_PDF = [string]$r.URL_DOWNLOAD_PDF
		KEY_STRICT = Build-KeyStrict -uf ([string]$r.UF) -inst ([string]$r.INSTITUICAO) -mod ([string]$r.MODALIDADE) -nome ([string]$r.NOME_POLO_OU_CAMPUS) -mun ([string]$r.MUNICIPIO_POLO)
		KEY_SOFT = Build-KeySoft -uf ([string]$r.UF) -nome ([string]$r.NOME_POLO_OU_CAMPUS) -mun ([string]$r.MUNICIPIO_POLO)
	}
}

$refStrictSet = @{}
foreach ($g in $refByStrict) { $refStrictSet[$g.Name] = $true }
$refSoftSet = @{}
foreach ($g in $refBySoft) { $refSoftSet[$g.Name] = $true }

$consStrictSet = @{}
foreach ($r in $consRows) { $consStrictSet[$r.KEY_STRICT] = $true }
$consSoftSet = @{}
foreach ($r in $consRows) { $consSoftSet[$r.KEY_SOFT] = $true }

$consAudit = foreach ($r in $consRows) {
	$matchStrict = $refStrictSet.ContainsKey($r.KEY_STRICT)
	$matchSoft = $refSoftSet.ContainsKey($r.KEY_SOFT)
	$status = if ($matchStrict) { "MATCH_STRICT" } elseif ($matchSoft) { "MATCH_SOFT" } else { "OUT_OF_REF" }
	[pscustomobject]@{
		UF = $r.UF
		INSTITUICAO = $r.INSTITUICAO
		MODALIDADE = $r.MODALIDADE
		NOME_POLO_OU_CAMPUS = $r.NOME_POLO_OU_CAMPUS
		MUNICIPIO_POLO = $r.MUNICIPIO_POLO
		STATUS_LINK = $r.STATUS_LINK
		STATUS_AUDITORIA = $status
		URL_FONTE = $r.URL_FONTE
		URL_DOWNLOAD_PDF = $r.URL_DOWNLOAD_PDF
	}
}

$refMissing = foreach ($r in $refRowsUniqueStrict) {
	$hasStrict = $consStrictSet.ContainsKey($r.KEY_STRICT)
	$hasSoft = $consSoftSet.ContainsKey($r.KEY_SOFT)
	if (-not $hasStrict) {
		[pscustomobject]@{
			UF = $r.UF
			INSTITUICAO = $r.INSTITUICAO
			MODALIDADE = $r.MODALIDADE
			NOME_POLO_OU_CAMPUS = $r.NOME_POLO_OU_CAMPUS
			MUNICIPIO_POLO = $r.MUNICIPIO_POLO
			COBERTURA = if ($hasSoft) { "SOFT_ONLY" } else { "SEM_MATCH" }
		}
	}
}

$outConsAudit = Join-Path $outDir "CONSOLIDADO_AUDITORIA_REFERENCIA.csv"
$outExcedentes = Join-Path $outDir "EXCEDENTES_OUT_OF_REF.csv"
$outMissing = Join-Path $outDir "FALTANTES_DA_REFERENCIA.csv"
$outResumo = Join-Path $outDir "RESUMO_AUDITORIA_POR_UF.csv"

$consAudit | Export-Csv -Path $outConsAudit -NoTypeInformation -Encoding UTF8
($consAudit | Where-Object { $_.STATUS_AUDITORIA -eq "OUT_OF_REF" }) | Export-Csv -Path $outExcedentes -NoTypeInformation -Encoding UTF8
$refMissing | Export-Csv -Path $outMissing -NoTypeInformation -Encoding UTF8

$ufs = @((($refRowsRaw | Select-Object -ExpandProperty UF) + ($consRows | Select-Object -ExpandProperty UF)) | Sort-Object -Unique)

$resumo = foreach ($uf in $ufs) {
	$refUFAll = @($refRowsRaw | Where-Object { $_.UF -eq $uf })
	$refUFUnique = @($refRowsUniqueStrict | Where-Object { $_.UF -eq $uf })
	$consUF = @($consAudit | Where-Object { $_.UF -eq $uf })
	$missUF = @($refMissing | Where-Object { $_.UF -eq $uf })

	[pscustomobject]@{
		UF = $uf
		REF_LINHAS = $refUFAll.Count
		REF_UNICAS = $refUFUnique.Count
		REF_DUPLICADAS = ($refUFAll.Count - $refUFUnique.Count)
		CONS_TOTAL = $consUF.Count
		CONS_MATCH_STRICT = @($consUF | Where-Object { $_.STATUS_AUDITORIA -eq "MATCH_STRICT" }).Count
		CONS_MATCH_SOFT = @($consUF | Where-Object { $_.STATUS_AUDITORIA -eq "MATCH_SOFT" }).Count
		CONS_OUT_OF_REF = @($consUF | Where-Object { $_.STATUS_AUDITORIA -eq "OUT_OF_REF" }).Count
		REF_FALTANTE_STRICT = $missUF.Count
		REF_FALTANTE_SEM_MATCH = @($missUF | Where-Object { $_.COBERTURA -eq "SEM_MATCH" }).Count
	}
}

$resumo | Sort-Object UF | Export-Csv -Path $outResumo -NoTypeInformation -Encoding UTF8

$totalRefLinhas = $refRowsRaw.Count
$totalRefUnicas = $refRowsUniqueStrict.Count
$totalCons = $consRows.Count
$totalOut = @($consAudit | Where-Object { $_.STATUS_AUDITORIA -eq "OUT_OF_REF" }).Count
$totalMiss = $refMissing.Count

Write-Output ("Auditoria concluida.")
Write-Output ("REF_TOTAL_LINHAS=" + $totalRefLinhas)
Write-Output ("REF_TOTAL_UNICAS=" + $totalRefUnicas)
Write-Output ("CONSOLIDADO_TOTAL=" + $totalCons)
Write-Output ("CONSOLIDADO_OUT_OF_REF=" + $totalOut)
Write-Output ("REFERENCIA_FALTANTE_STRICT=" + $totalMiss)
Write-Output ("Resumo: " + $outResumo)
Write-Output ("Excedentes: " + $outExcedentes)
Write-Output ("Faltantes: " + $outMissing)

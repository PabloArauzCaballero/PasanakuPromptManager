# Contrato propuesto de eventos UX P0. Solo pruebas sintéticas; no instrumenta la app.
$ErrorActionPreference = 'Stop'

$pasosPorFlujo = @{
    alta = @('inicio', 'datos', 'otp', 'documento', 'vida', 'contrato', 'resultado')
    inicio = @('portada', 'saldo', 'mi_estado')
    aporte = @('revision', 'envio', 'resultado')
}
$resultados = @('viewed', 'completed', 'abandoned', 'error', 'offline', 'uncertain')
$campos = @('event', 'schema', 'flow', 'step', 'outcome')

function Test-EventoP0([string]$json) {
    try { $evento = ConvertFrom-Json -InputObject $json } catch { return $false }
    if ($null -eq $evento -or $evento -is [array]) { return $false }
    $propiedades = @($evento.PSObject.Properties.Name)
    if ($propiedades.Count -ne $campos.Count) { return $false }
    foreach ($propiedad in $propiedades) {
        if ($propiedad -cnotin $campos) { return $false }
    }
    if ($evento.event -isnot [string] -or $evento.event -cne 'ux_p0_step') { return $false }
    if ($evento.schema -isnot [int] -or $evento.schema -ne 1) { return $false }
    if ($evento.flow -isnot [string] -or -not $pasosPorFlujo.ContainsKey($evento.flow)) { return $false }
    if ($evento.step -isnot [string] -or $evento.step -cnotin $pasosPorFlujo[$evento.flow]) { return $false }
    if ($evento.outcome -isnot [string] -or $evento.outcome -cnotin $resultados) { return $false }
    return $true
}

$casos = @(
    @{ nombre = 'alta válida'; json = '{"event":"ux_p0_step","schema":1,"flow":"alta","step":"otp","outcome":"completed"}'; esperado = $true },
    @{ nombre = 'aporte incierto válido'; json = '{"event":"ux_p0_step","schema":1,"flow":"aporte","step":"envio","outcome":"uncertain"}'; esperado = $true },
    @{ nombre = 'importe prohibido'; json = '{"event":"ux_p0_step","schema":1,"flow":"aporte","step":"envio","outcome":"viewed","monto":350}'; esperado = $false },
    @{ nombre = 'identificador prohibido'; json = '{"event":"ux_p0_step","schema":1,"flow":"alta","step":"otp","outcome":"completed","usuario_id":"sintetico"}'; esperado = $false },
    @{ nombre = 'texto libre prohibido'; json = '{"event":"ux_p0_step","schema":1,"flow":"alta","step":"otp","outcome":"mensaje libre"}'; esperado = $false },
    @{ nombre = 'paso de otro flujo'; json = '{"event":"ux_p0_step","schema":1,"flow":"aporte","step":"documento","outcome":"viewed"}'; esperado = $false },
    @{ nombre = 'objeto extra prohibido'; json = '{"event":"ux_p0_step","schema":1,"flow":"inicio","step":"saldo","outcome":"viewed","datos":{"telefono":"sintetico"}}'; esperado = $false },
    @{ nombre = 'JSON inválido'; json = '{'; esperado = $false }
)

$fallos = 0
foreach ($caso in $casos) {
    $actual = Test-EventoP0 $caso.json
    if ($actual -ne $caso.esperado) {
        Write-Output "FAIL: $($caso.nombre)"
        $fallos++
    } else {
        Write-Output "PASS: $($caso.nombre)"
    }
}
if ($fallos -gt 0) { exit 1 }
Write-Output "PASS: $($casos.Count)/$($casos.Count) casos sintéticos; no son payloads de TEST"

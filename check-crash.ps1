$events = Get-WinEvent -FilterHashtable @{LogName='Application'; Id=1000} -MaxEvents 8 -ErrorAction SilentlyContinue | Where-Object { $_.Message -match 'Hermes' }
if (-not $events) { Write-Host 'NO_CRASH_EVENTS'; exit }
foreach ($e in $events | Select-Object -First 3) {
  Write-Host ('TIME: ' + $e.TimeCreated.ToString('yyyy-MM-dd HH:mm:ss'))
  $lines = $e.Message -split "`r?`n"
  foreach ($l in $lines) {
    if ($l -match 'Faulting application name|Faulting module name|Exception code|Fault offset') { Write-Host ('  ' + $l.Trim()) }
  }
}

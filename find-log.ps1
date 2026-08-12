$paths = @('C:\Users\covhnw\AppData\Local', 'C:\Users\covhnw\AppData\Roaming')
foreach ($p in $paths) {
  Get-ChildItem -Path $p -Filter 'chrome_debug.log' -Recurse -Depth 4 -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host ('FOUND: ' + $_.FullName + '  ' + $_.LastWriteTime.ToString('HH:mm:ss'))
  }
}
Write-Host 'DONE'

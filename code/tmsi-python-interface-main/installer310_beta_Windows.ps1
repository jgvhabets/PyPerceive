param(
      $o
)

if (![bool]$o) {
      $o = ".venv_310_beta"
}     

if (!(Test-Path $o)) {
      New-Item -Path $o -ItemType "directory" | Out-Null
}

$o = Resolve-Path $o

$current = Get-Location

$python310 = py -3.10 --version
if ($python310 -like "*Python 3.10 not found!*") {
      Write-Error "`n`nPython 3.10 not found! Download and install it!"
      Start-Process "https://www.python.org/downloads/release/python-3102/"
      Exit
}
else {
      Write-Host "Well done, you have the right python version"
}

py -3.10 -m venv $o

cd $o
$activate = "./Scripts/activate"
& $activate

cd $current

pip install -r .\requirements310_Windows.txt

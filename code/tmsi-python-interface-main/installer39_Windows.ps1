param(
    $o
)

if(![bool]$o)
{
      $o = ".venv"
}     

if (!(Test-Path $o))
{
    New-Item -Path $o -ItemType "directory" | Out-Null
}

$o = Resolve-Path $o

$current = Get-Location

$python39 = py -3.9 --version
if($python39 -like "*Python 3.9 not found!*") {
      Write-Error "`n`nPython 3.9 not found! Download and install it!"
      Start-Process "https://www.python.org/downloads/release/python-3912/"
      Exit
} else {
      Write-Host "Well done, you have the right python version"
}

py -3.9 -m venv $o

cd $o
$activate = "./Scripts/activate"
& $activate

cd $current

pip install -r .\requirements39_Windows.txt

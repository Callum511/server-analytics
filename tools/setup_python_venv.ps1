#Requires -RunAsAdministrator

$repoRootFolder = Split-Path $PSScriptRoot -Parent
$requirementsFile = Join-Path -Path $repoRootFolder -ChildPath "tools\python_requirements.txt"
$requirementsFileDev = Join-Path -Path $repoRootFolder -ChildPath "tools\python_dev_requirements.txt"
$requirementsFileTest = Join-Path -Path $repoRootFolder -ChildPath "tools\python_test_requirements.txt"

$venvDir = Join-Path -Path $repoRootFolder -ChildPath ".venv"
# check platform
$platform = $env:OS
if ($platform -eq "Windows_NT") {
    Write-Host "Windows"
} else {
    Write-Host "Linux"
}

if ($platform -eq "Windows_NT") {
    $rawBasePythonDir = ho((python -c "import sys;print(sys.base_prefix);sys.exit()") | Out-String).Trim()
    $basePythonDir = Resolve-Path $rawBasePythonDir
    $BasePythonExe = Join-Path -Path $basePythonDir -ChildPath "python.exe"
} else {
    $rawBasePythonDir = "/usr/bin"
    $basePythonDir = Resolve-Path $rawBasePythonDir
    $BasePythonExe = Join-Path -Path $basePythonDir -ChildPath "python3"
}





Push-Location $repoRootFolder

Write-Host $(`
    "`n"+`
    "Upgrading system pip" +`
    "`n--------------------`n" )`
    -ForegroundColor Yellow

& $BasePythonExe.Trim() -m pip install --upgrade pip



Write-Host $(`
    "`n" +`
    "creating fresh venv in "        +`
    $venvDir.Trim() +`
    "`n-----------------------------------------------------------------------------`n"       )`
    -ForegroundColor Yellow


& $BasePythonExe.Trim() -m venv --clear --upgrade-deps $venvDir

if ($? -eq $False) {exit}
if ($platform -eq "Windows_NT") {
    $venvExecutable = Join-Path -Path $venvDir -ChildPath "Scripts\python.exe"
} else {
    $venvExecutable = Join-Path -Path $venvDir -ChildPath "bin/python3"
}

& $venvExecutable -m pip install --upgrade wheel
& $venvExecutable -m pip install --upgrade PEP517
& $venvExecutable -m pip install --upgrade python-dotenv
Write-Host $(`
    "`n"+`
    "Installing Dependencies from " +`
    $requirementsFile.Trim() +`
    "`n-----------------------------------------------------------------------------------------------`n" )`
    -ForegroundColor Yellow

& $venvExecutable -m pip install -U -r $requirementsFile
if ($? -eq $False) {exit}
Write-Host $(`
    "`n"+`
    "Installing DEV Dependencies from " +`
    $requirementsFileDev.Trim() +`
    "`n-----------------------------------------------------------------------------------------------`n" )`
    -ForegroundColor Yellow




& $venvExecutable -m pip install -r $requirementsFileDev
if ($? -eq $False) {exit}


Write-Host $(`
    "`n"+`
    "Installing Project itself as editable " +`
    $requirementsFileDev.Trim() +`
    "`n-----------------------------------------------------------------------------------------------`n" )`
    -ForegroundColor Yellow



& $venvExecutable -m pip install -e $repoRootFolder
if ($? -eq $False) {exit}




Write-Host $(`
    "`n"+`
    "`n-----------------------------------------------------" +`
    "`n=====================================================`n" +`
    "                     Finished" +`
    "`n=====================================================`n" +`
    "-----------------------------------------------------`n" )`
    -ForegroundColor Yellow

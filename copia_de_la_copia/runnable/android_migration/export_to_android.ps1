<#
Simple script para copiar los archivos de android_migration al proyecto Android destino.
Uso: .\export_to_android.ps1 -DestinationProject "D:\AndroidProjects\MyApp" -PackageName "com.miempresa.miapp"
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$DestinationProject,

    [Parameter(Mandatory=$false)]
    [string]$PackageName = "com.example.app"
)

$here = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
$src = Join-Path $here '.'
$srcFiles = @('MainActivity.kt','MainViewModel.kt','FileRepository.kt','MainScreen.kt')
$asset = Join-Path $here '..\..\assets\fondo.png'

# Build destination paths
$pkgPath = $PackageName -replace '\.','\\'
$destJava = Join-Path $DestinationProject "app\src\main\java\$pkgPath"
$destResDrawable = Join-Path $DestinationProject 'app\src\main\res\drawable'

# Create folders
New-Item -ItemType Directory -Force -Path $destJava | Out-Null
New-Item -ItemType Directory -Force -Path $destResDrawable | Out-Null

# Copy Kotlin files and replace package line
foreach ($f in $srcFiles) {
    $srcf = Join-Path $src $f
    if (Test-Path $srcf) {
        $content = Get-Content $srcf -Raw
        # replace package declaration
        $content = $content -replace '^package\s+.*', "package $PackageName"
        $destf = Join-Path $destJava $f
        $content | Out-File -FilePath $destf -Encoding UTF8
        Write-Output "Copied $f -> $destf"
    } else {
        Write-Warning "Missing source file: $srcf"
    }
}

# Copy asset
if (Test-Path $asset) {
    Copy-Item $asset -Destination (Join-Path $destResDrawable 'fondo.png') -Force
    Write-Output "Copied asset fondo.png -> $destResDrawable"
} else {
    Write-Warning "Asset not found: $asset"
}

# Copy helper snippets
$helpers = @('gradle_module_snippet.gradle','AndroidManifest_snippet.xml')
foreach ($h in $helpers) {
    $srcf = Join-Path $src $h
    if (Test-Path $srcf) {
        Copy-Item $srcf -Destination $DestinationProject -Force
        Write-Output "Copied helper $h -> $DestinationProject"
    }
}

Write-Output "\nDone. Now open the project in Android Studio and merge the snippets into build.gradle and AndroidManifest.xml."

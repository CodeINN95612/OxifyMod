@echo off
setlocal enabledelayedexpansion

REM Oxify Mod Version Switcher (Batch Version)
REM This is a simplified version switcher for Windows users

if "%~2"=="" (
    echo Usage: %0 ^<minecraft_version^> ^<mod_version^>
    echo Example: %0 1.21.1 1.2.0
    echo.
    echo This script will update gradle.properties with the new versions
    echo and attempt to build the mod. You may need to manually update
    echo fabric.mod.json and other dependencies.
    exit /b 1
)

set MINECRAFT_VERSION=%~1
set MOD_VERSION=%~2
set FULL_MOD_VERSION=%MINECRAFT_VERSION%-%MOD_VERSION%

echo Updating Oxify mod to Minecraft %MINECRAFT_VERSION%, mod version %MOD_VERSION%
echo ================================================================

REM Check if gradle.properties exists
if not exist "gradle.properties" (
    echo Error: gradle.properties not found in current directory
    echo Please run this script from the Oxify mod root directory
    exit /b 1
)

REM Backup gradle.properties
copy gradle.properties gradle.properties.backup >nul
echo Created backup: gradle.properties.backup

REM Update gradle.properties
echo Updating gradle.properties...

REM Create a temporary PowerShell script to do the replacements
echo $content = Get-Content 'gradle.properties' -Raw > temp_update.ps1
echo $content = $content -replace 'minecraft_version=.*', 'minecraft_version=%MINECRAFT_VERSION%' >> temp_update.ps1
echo $content = $content -replace 'mod_version=.*', 'mod_version=%FULL_MOD_VERSION%' >> temp_update.ps1
echo Set-Content 'gradle.properties' $content >> temp_update.ps1

powershell -ExecutionPolicy Bypass -File temp_update.ps1
del temp_update.ps1

echo ✓ gradle.properties updated

echo.
echo WARNING: You may need to manually update the following:
echo - fabric.mod.json (Minecraft version dependency)
echo - yarn_mappings version in gradle.properties
echo - fabric_version in gradle.properties
echo - loader_version in gradle.properties
echo.
echo Check https://fabricmc.net/develop for the latest versions

echo.
echo ================================================================
echo Cleaning project...
call gradlew.bat clean

if !errorlevel! neq 0 (
    echo Clean failed, but continuing...
)

echo.
echo ================================================================
echo Building project...
call gradlew.bat build

if !errorlevel! equ 0 (
    echo.
    echo ================================================================
    echo ✓ Build completed successfully!
    echo ✓ Oxify mod is now configured for Minecraft %MINECRAFT_VERSION%
    
    if exist "build\libs" (
        echo.
        echo Built JAR files:
        dir /b build\libs\*.jar 2>nul
    )
) else (
    echo.
    echo ================================================================
    echo ✗ Build failed!
    echo This is likely due to breaking changes in the Fabric API.
    echo You may need to manually update dependencies and code.
    echo.
    echo To restore the previous version, copy gradle.properties.backup back:
    echo copy gradle.properties.backup gradle.properties
)

echo.
pause

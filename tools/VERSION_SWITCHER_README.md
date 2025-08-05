# Oxify Mod Version Switcher

This directory contains scripts to easily switch between Minecraft versions for the Oxify mod.

**Location:** All version switcher tools are located in the `tools/` directory to keep the project organized.

## Files

- `version_switcher.py` - Full-featured Python script with automatic dependency resolution
- `version_switcher.bat` - Simple Windows batch script
- `requirements.txt` - Python dependencies
- `VERSION_SWITCHER_README.md` - This file

## Setup

### Python Script (Recommended)

1. Navigate to the tools directory:
   ```bash
   cd tools
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

All commands should be run from the `tools/` directory:

```bash
# Basic usage
python version_switcher.py <minecraft_version> <mod_version>

# Examples
python version_switcher.py 1.21.1 1.2.0
python version_switcher.py 1.20.4 1.1.0

# Skip confirmation prompts
python version_switcher.py 1.21.4 1.3.1 --yes

# Get help
python version_switcher.py --help
```

### What it does

1. Fetches the latest compatible versions from Fabric Meta API:
   - Latest Yarn mappings for the Minecraft version
   - Latest Fabric Loader version
   - Latest Fabric API version for the Minecraft version

2. Updates the following files:
   - `gradle.properties` - All version properties
   - `src/main/resources/fabric.mod.json` - Minecraft version dependency

3. Cleans and builds the project

4. Reports success/failure and shows built JAR files

### Windows Batch Script

For Windows users who prefer not to install Python:

```cmd
cd tools
version_switcher.bat <minecraft_version> <mod_version>

REM Example
version_switcher.bat 1.21.1 1.2.0
```

### Limitations

- Only updates `gradle.properties` with basic version changes
- Does not automatically fetch latest dependency versions
- You need to manually check and update:
  - `yarn_mappings` in `gradle.properties`
  - `fabric_version` in `gradle.properties` 
  - `loader_version` in `gradle.properties`
  - Minecraft version in `src/main/resources/fabric.mod.json`

### Manual Version Updates

Check https://fabricmc.net/develop for the latest versions of:
- Yarn mappings
- Fabric Loader
- Fabric API

## Files Modified

Both scripts modify these files:

1. **gradle.properties**
   - `minecraft_version` - Target Minecraft version
   - `mod_version` - Full mod version (minecraft_version-mod_version)
   - `yarn_mappings` - Yarn mappings version (Python script only)
   - `loader_version` - Fabric Loader version (Python script only) 
   - `fabric_version` - Fabric API version (Python script only)

2. **src/main/resources/fabric.mod.json**
   - `depends.minecraft` - Minecraft version constraint (Python script only)
   - `depends.fabricloader` - Fabric Loader version constraint (Python script only)

## Backup

The batch script creates `gradle.properties.backup` before making changes. The Python script does not create backups by default, so consider committing your changes to git before running.

## Expected Build Failures

The scripts will attempt to build the mod, but builds may fail due to:

1. **Breaking changes in Fabric API** - Methods may have been renamed, moved, or removed
2. **Minecraft API changes** - Minecraft itself may have breaking changes between versions
3. **Incompatible dependency versions** - Some combinations of versions may not work together

This is expected and normal. The purpose of the script is to:
1. Automate the tedious version configuration changes
2. Quickly test if the mod builds without code changes
3. Identify what needs to be manually fixed

## Troubleshooting

### Build Fails with "Could not resolve dependency"
- Check that the Minecraft version exists and is supported by Fabric
- Verify the Fabric API version supports your Minecraft version
- Try a different combination of versions

### Build Fails with Compilation Errors  
- This indicates breaking API changes
- You'll need to manually update the Java code to work with the new versions
- Check the Fabric documentation for migration guides

### "No minecraft_version property found"
- Make sure you're running the script from the Oxify mod root directory
- Verify `gradle.properties` exists and contains the expected properties

## Version History

The mod currently supports these tested versions:
- Minecraft 1.21.4 with mod version 1.3.1 (current)
- Minecraft 1.21.1 with mod version 1.2.0 (from build artifacts)

When switching to a new version, you're essentially testing if the mod code is compatible with that version of Minecraft and Fabric.

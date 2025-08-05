# Oxify Mod Version Switcher

This directory contains scripts to easily switch between Minecraft versions for the Oxify mod.

**Location:** All version switcher tools are located in the `tools/` directory to keep the project organized.

## Files

- `version_switcher.py` - Full-featured Python script with automatic dependency resolution
- `requirements.txt` - Python dependencies
- `VERSION_SWITCHER_README.md` - This file

## Setup

### Python Script

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

1. Fetches the latest compatible versions from various APIs:
   - Latest Yarn mappings for the Minecraft version
   - Latest Fabric Loader version
   - Latest Fabric API version for the Minecraft version
   - Latest Gradle version
   - Latest Fabric Loom version

2. Updates the following files:
   - `gradle.properties` - All version properties
   - `src/main/resources/fabric.mod.json` - Minecraft version and fabric-api dependency
   - `gradle/wrapper/gradle-wrapper.properties` - Gradle wrapper version
   - `build.gradle` - Fabric Loom plugin version

3. Runs setup and build tasks:
   - Cleans the project
   - Runs `gradlew genSources` to generate mappings
   - Runs `gradlew vscode` to setup VS Code integration
   - Builds the project

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

The Python script modifies these files:

1. **gradle.properties**
   - `minecraft_version` - Target Minecraft version
   - `mod_version` - Full mod version (minecraft_version-mod_version)
   - `yarn_mappings` - Yarn mappings version
   - `loader_version` - Fabric Loader version
   - `fabric_version` - Fabric API version

2. **src/main/resources/fabric.mod.json**
   - `depends.minecraft` - Minecraft version constraint
   - `depends.fabricloader` - Fabric Loader version constraint  
   - `depends.fabric-api` - Fabric API version constraint

3. **gradle/wrapper/gradle-wrapper.properties**
   - `distributionUrl` - Updated to latest Gradle version

4. **build.gradle**
   - `fabric-loom` plugin version - Updated to latest Loom version

The batch script only modifies `gradle.properties` with basic version changes.

## Backup

The batch script creates `gradle.properties.backup` before making changes. The Python script does not create backups by default, so consider committing your changes to git before running.

## Expected Build Failures

The script will attempt to build the mod, but builds may fail due to:

1. **Breaking changes in Fabric API** - Methods may have been renamed, moved, or removed
2. **Minecraft API changes** - Minecraft itself may have breaking changes between versions
3. **Incompatible dependency versions** - Some combinations of versions may not work together
4. **Gradle/Loom compatibility issues** - New versions may have different requirements

This is expected and normal. The purpose of the script is to:
1. Automate the tedious version configuration changes
2. Update all build tools to their latest versions
3. Generate proper mappings and IDE integration
4. Quickly test if the mod builds without code changes
5. Identify what needs to be manually fixed

## Additional Setup Steps

The script now also runs:
- `gradlew genSources` - Generates decompiled Minecraft sources for better IDE support
- `gradlew vscode` - Sets up VS Code integration with proper classpath and debugging

If these steps fail, you may need to run them manually after the version switch.

## Troubleshooting

### Build Fails with "Could not resolve dependency"
- Check that the Minecraft version exists and is supported by Fabric
- Verify the Fabric API version supports your Minecraft version
- Try a different combination of versions

### Build Fails with Compilation Errors  
- This indicates breaking API changes
- You'll need to manually update the Java code to work with the new versions
- Check the Fabric documentation for migration guides

### "genSources" or "vscode" Tasks Fail
- These are not critical for the mod to work, but help with development
- Try running them manually: `gradlew genSources` and `gradlew vscode`
- If they continue to fail, you can develop without them but may have limited IDE support

### Gradle Wrapper Update Issues
- If the new Gradle version is incompatible, you may need to downgrade
- Check the Fabric Loom compatibility matrix for supported Gradle versions
- Manually edit `gradle/wrapper/gradle-wrapper.properties` if needed

### Fabric Loom Version Issues
- If the latest Loom version is incompatible, you may see build script errors
- Check the Fabric Loom releases page for compatibility notes
- You can manually downgrade the version in `build.gradle` if needed

### "No minecraft_version property found"
- Make sure you're running the script from the Oxify mod root directory
- Verify `gradle.properties` exists and contains the expected properties

### Network/API Issues
- If version fetching fails, the script uses fallback versions
- You can manually check and update versions from:
  - https://fabricmc.net/develop
  - https://gradle.org/releases/
  - https://github.com/FabricMC/fabric-loom/releases

## Version History

The mod currently supports these tested versions:
- Minecraft 1.21.4 with mod version 1.3.1 (current)
- Minecraft 1.21.1 with mod version 1.2.0 (from build artifacts)

When switching to a new version, you're essentially testing if the mod code is compatible with that version of Minecraft and Fabric.

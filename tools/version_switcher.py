#!/usr/bin/env python3
"""
Oxify Mod Version Switcher

This script automatically updates the Minecraft and mod versions for the Oxify mod,
updates all necessary configuration files, and attempts to build the mod.

Usage:
    python version_switcher.py <minecraft_version> <mod_version>

Example:
    python version_switcher.py 1.21.1 1.2.0
    python version_switcher.py 1.20.4 1.1.0
"""

import sys
import os
import subprocess
import re
import json
import argparse
from pathlib import Path
import requests
from typing import Dict, Optional, Tuple

class VersionSwitcher:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.gradle_properties = project_root / "gradle.properties"
        self.fabric_mod_json = project_root / "src" / "main" / "resources" / "fabric.mod.json"
        
    def get_latest_mappings(self, minecraft_version: str) -> Optional[str]:
        """Get the latest yarn mappings for a Minecraft version from Fabric Meta API"""
        try:
            url = f"https://meta.fabricmc.net/v2/versions/yarn/{minecraft_version}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return data[0]["version"]  # Get the latest mapping
        except Exception as e:
            print(f"Warning: Could not fetch latest yarn mappings: {e}")
        return None
    
    def get_latest_loader_version(self) -> Optional[str]:
        """Get the latest Fabric Loader version"""
        try:
            url = "https://meta.fabricmc.net/v2/versions/loader"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return data[0]["version"]
        except Exception as e:
            print(f"Warning: Could not fetch latest loader version: {e}")
        return None
    
    def get_latest_fabric_api_version(self, minecraft_version: str) -> Optional[str]:
        """Get the latest Fabric API version for a Minecraft version"""
        try:
            url = f"https://meta.fabricmc.net/v2/versions/fabric-api/{minecraft_version}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data:
                    return data[0]["version"]
        except Exception as e:
            print(f"Warning: Could not fetch latest fabric API version: {e}")
        return None
    
    def suggest_versions(self, minecraft_version: str) -> Dict[str, str]:
        """Suggest appropriate versions for dependencies"""
        suggestions = {}
        
        print(f"Fetching latest versions for Minecraft {minecraft_version}...")
        
        # Get yarn mappings
        yarn_mappings = self.get_latest_mappings(minecraft_version)
        if yarn_mappings:
            suggestions["yarn_mappings"] = yarn_mappings
            print(f"  Latest yarn mappings: {yarn_mappings}")
        else:
            # Fallback pattern
            suggestions["yarn_mappings"] = f"{minecraft_version}+build.1"
            print(f"  Using fallback yarn mappings: {suggestions['yarn_mappings']}")
        
        # Get loader version
        loader_version = self.get_latest_loader_version()
        if loader_version:
            suggestions["loader_version"] = loader_version
            print(f"  Latest loader version: {loader_version}")
        else:
            suggestions["loader_version"] = "0.16.9"  # Fallback
            print(f"  Using fallback loader version: {suggestions['loader_version']}")
        
        # Get Fabric API version
        fabric_version = self.get_latest_fabric_api_version(minecraft_version)
        if fabric_version:
            suggestions["fabric_version"] = fabric_version
            print(f"  Latest Fabric API version: {fabric_version}")
        else:
            # Fallback: use base minecraft version without patch (e.g., 1.21.2 -> 1.21)
            base_version = '.'.join(minecraft_version.split('.')[:-1])
            suggestions["fabric_version"] = f"0.100.0+{base_version}"
            print(f"  Using fallback Fabric API version: {suggestions['fabric_version']}")
            print(f"    (Specific version for {minecraft_version} not found, using {base_version} base)")
        
        return suggestions
    
    def update_gradle_properties(self, minecraft_version: str, mod_version: str, suggestions: Dict[str, str]):
        """Update the gradle.properties file with new versions"""
        print("Updating gradle.properties...")
        
        if not self.gradle_properties.exists():
            raise FileNotFoundError(f"gradle.properties not found at {self.gradle_properties}")
        
        content = self.gradle_properties.read_text(encoding='utf-8')
        
        # Update versions
        content = re.sub(r'minecraft_version=.*', f'minecraft_version={minecraft_version}', content)
        content = re.sub(r'mod_version=.*', f'mod_version={minecraft_version}-{mod_version}', content)
        
        # Update suggested versions
        if "yarn_mappings" in suggestions:
            content = re.sub(r'yarn_mappings=.*', f'yarn_mappings={suggestions["yarn_mappings"]}', content)
        
        if "loader_version" in suggestions:
            content = re.sub(r'loader_version=.*', f'loader_version={suggestions["loader_version"]}', content)
        
        if "fabric_version" in suggestions:
            content = re.sub(r'fabric_version=.*', f'fabric_version={suggestions["fabric_version"]}', content)
        
        self.gradle_properties.write_text(content, encoding='utf-8')
        print("✓ gradle.properties updated successfully")
    
    def update_fabric_mod_json(self, minecraft_version: str, suggestions: Dict[str, str]):
        """Update the fabric.mod.json file with new Minecraft version dependency"""
        print("Updating fabric.mod.json...")
        
        if not self.fabric_mod_json.exists():
            raise FileNotFoundError(f"fabric.mod.json not found at {self.fabric_mod_json}")
        
        with open(self.fabric_mod_json, 'r', encoding='utf-8') as f:
            mod_json = json.load(f)
        
        # Update Minecraft version dependency
        if "depends" in mod_json:
            mod_json["depends"]["minecraft"] = f"~{minecraft_version}"
            
            # Update fabricloader version if we have a suggestion
            if "loader_version" in suggestions:
                mod_json["depends"]["fabricloader"] = f">={suggestions['loader_version']}"
        
        with open(self.fabric_mod_json, 'w', encoding='utf-8') as f:
            json.dump(mod_json, f, indent=2, ensure_ascii=False)
        
        print("✓ fabric.mod.json updated successfully")
    
    def clean_project(self):
        """Clean the project build directory"""
        print("Cleaning project...")
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run([str(self.project_root / 'gradlew.bat'), 'clean'], 
                                      cwd=self.project_root, 
                                      capture_output=True, 
                                      text=True,
                                      timeout=300)
            else:  # Unix-like
                result = subprocess.run([str(self.project_root / 'gradlew'), 'clean'], 
                                      cwd=self.project_root, 
                                      capture_output=True, 
                                      text=True,
                                      timeout=300)
            
            if result.returncode == 0:
                print("✓ Project cleaned successfully")
                return True
            else:
                print(f"✗ Clean failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("✗ Clean timed out")
            return False
        except Exception as e:
            print(f"✗ Clean failed: {e}")
            return False
    
    def build_project(self):
        """Build the project"""
        print("Building project...")
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run([str(self.project_root / 'gradlew.bat'), 'build'], 
                                      cwd=self.project_root, 
                                      capture_output=True, 
                                      text=True,
                                      timeout=600)
            else:  # Unix-like
                result = subprocess.run([str(self.project_root / 'gradlew'), 'build'], 
                                      cwd=self.project_root, 
                                      capture_output=True, 
                                      text=True,
                                      timeout=600)
            
            if result.returncode == 0:
                print("✓ Build completed successfully!")
                
                # Look for built JAR files
                build_libs = self.project_root / "build" / "libs"
                if build_libs.exists():
                    jar_files = list(build_libs.glob("*.jar"))
                    if jar_files:
                        print(f"✓ Built JAR files:")
                        for jar_file in jar_files:
                            print(f"  - {jar_file.name}")
                
                return True
            else:
                print(f"✗ Build failed!")
                print(f"Error output:\n{result.stderr}")
                print(f"Standard output:\n{result.stdout}")
                return False
                
        except subprocess.TimeoutExpired:
            print("✗ Build timed out (10 minutes)")
            return False
        except Exception as e:
            print(f"✗ Build failed: {e}")
            return False
    
    def switch_version(self, minecraft_version: str, mod_version: str, auto_yes: bool = False):
        """Main method to switch versions and build the mod"""
        print(f"🔄 Switching Oxify mod to Minecraft {minecraft_version}, mod version {mod_version}")
        print("=" * 60)
        
        # Get version suggestions
        suggestions = self.suggest_versions(minecraft_version)
        
        # Show what will be updated
        print(f"\nThe following files will be updated:")
        print(f"  - gradle.properties")
        print(f"  - src/main/resources/fabric.mod.json")
        print(f"\nVersion changes:")
        print(f"  - Minecraft: {minecraft_version}")
        print(f"  - Mod: {minecraft_version}-{mod_version}")
        print(f"  - Yarn mappings: {suggestions.get('yarn_mappings', 'N/A')}")
        print(f"  - Fabric Loader: {suggestions.get('loader_version', 'N/A')}")
        print(f"  - Fabric API: {suggestions.get('fabric_version', 'N/A')}")
        
        if not auto_yes:
            confirm = input("\nProceed with these changes? (y/N): ")
            if confirm.lower() not in ['y', 'yes']:
                print("Aborted.")
                return False
        
        try:
            # Update files
            self.update_gradle_properties(minecraft_version, mod_version, suggestions)
            self.update_fabric_mod_json(minecraft_version, suggestions)
            
            print("\n" + "=" * 60)
            print("📁 Files updated successfully!")
            
            # Clean and build
            print("\n" + "=" * 60)
            if self.clean_project():
                print("\n" + "=" * 60)
                success = self.build_project()
                
                if success:
                    print("\n" + "=" * 60)
                    print("🎉 Version switch completed successfully!")
                    print(f"✓ Oxify mod is now configured for Minecraft {minecraft_version}")
                    return True
                else:
                    print("\n" + "=" * 60)
                    print("⚠️  Version switch completed, but build failed.")
                    print("This is likely due to breaking changes in the Fabric API.")
                    print("You may need to manually update the code to fix compatibility issues.")
                    return False
            else:
                print("⚠️  Could not clean project, skipping build.")
                return False
                
        except Exception as e:
            print(f"✗ Error during version switch: {e}")
            return False

def validate_minecraft_version(version: str) -> bool:
    """Validate that the Minecraft version format is correct"""
    pattern = r'^\d+\.\d+(\.\d+)?$'
    return bool(re.match(pattern, version))

def validate_mod_version(version: str) -> bool:
    """Validate that the mod version format is correct"""
    pattern = r'^\d+\.\d+(\.\d+)?$'
    return bool(re.match(pattern, version))

def main():
    parser = argparse.ArgumentParser(
        description="Switch Minecraft and mod versions for the Oxify mod",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python version_switcher.py 1.21.1 1.2.0
  python version_switcher.py 1.20.4 1.1.0 --yes
  python version_switcher.py 1.21.4 1.3.1 -y
        """
    )
    
    parser.add_argument('minecraft_version', 
                        help='Minecraft version (e.g., 1.21.1, 1.20.4)')
    parser.add_argument('mod_version', 
                        help='Mod version (e.g., 1.2.0, 1.1.0)')
    parser.add_argument('-y', '--yes', 
                        action='store_true',
                        help='Skip confirmation prompts')
    parser.add_argument('--project-root', 
                        type=Path,
                        default=Path.cwd().parent,
                        help='Path to the project root (default: parent directory)')
    
    args = parser.parse_args()
    
    # Validate versions
    if not validate_minecraft_version(args.minecraft_version):
        print(f"Error: Invalid Minecraft version format: {args.minecraft_version}")
        print("Expected format: X.Y or X.Y.Z (e.g., 1.21.1, 1.20.4)")
        sys.exit(1)
    
    if not validate_mod_version(args.mod_version):
        print(f"Error: Invalid mod version format: {args.mod_version}")
        print("Expected format: X.Y or X.Y.Z (e.g., 1.2.0, 1.1.0)")
        sys.exit(1)
    
    # Check if we're in a valid project directory
    project_root = args.project_root.resolve()
    if not (project_root / "gradle.properties").exists():
        print(f"Error: No gradle.properties found in {project_root}")
        print("Please run this script from the Oxify mod root directory.")
        sys.exit(1)
    
    # Initialize version switcher and run
    switcher = VersionSwitcher(project_root)
    success = switcher.switch_version(args.minecraft_version, args.mod_version, args.yes)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

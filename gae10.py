import os
import subprocess
import zipfile
import configparser
import xml.etree.ElementTree as ET
from PIL import Image
import glob
import re
import shutil
import sys
import time
import threading
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

ANDROID_BANNER = f""" {Fore.GREEN}
      /\\_/\\
     ( o.o )  GAE V 1.0
      > ^ <
     Support me https://buymeacoffee.com/9boom
"""

class Spinner:
    def __init__(self):
        self.spinner_chars = '⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
        self.stop_running = False
        self.spinner_thread = None

    def spin(self):
        i = 0
        while not self.stop_running:
            sys.stdout.write(f'\r{self.spinner_chars[i]} ')
            sys.stdout.flush()
            time.sleep(0.1)
            i = (i + 1) % len(self.spinner_chars)
        sys.stdout.write('\r')

    def start(self):
        self.stop_running = False
        self.spinner_thread = threading.Thread(target=self.spin)
        self.spinner_thread.start()

    def stop(self):
        self.stop_running = True
        if self.spinner_thread:
            self.spinner_thread.join()

def print_color(message, color=Fore.WHITE):
    print(f"{color}{message}{Style.RESET_ALL}")

def run_command(command, error_message):
    spinner = Spinner()
    try:
        spinner.start()
        result = subprocess.run(
            command,
            check=True,
            shell=False,
            capture_output=True,
            text=True
        )
        spinner.stop()
        print_color(f"\r[SUCCESS] Command executed: {' '.join(command)}", Fore.GREEN)
        return result
    except subprocess.CalledProcessError as e:
        spinner.stop()
        print_color(f"\r{error_message}: {e}", Fore.RED)
        print_color(f"Error output:\n{e.stderr}", Fore.YELLOW)
        raise
    except Exception as e:
        spinner.stop()
        raise

def show_banner():
    print(ANDROID_BANNER)
    print_color("Godot Android Exporter Toolkit v1.0", Fore.CYAN)
    print_color("----------------------------------\n", Fore.WHITE)

def decompile_apk(apk_path, decompiled_dir):
    print_color("\n=== PREPARING A TEMPLATE ===", Fore.CYAN)
    run_command(["apktool", "d", "-f", "-o", decompiled_dir, apk_path], "Decompilation failed")

def read_properties():
    print_color("\n=== READING PROPERTIES ===", Fore.CYAN)
    properties_path = os.path.join(os.getcwd(), "properties.gae")

    if not os.path.exists(properties_path):
        raise FileNotFoundError("properties.gae not found in current directory")

    config = configparser.ConfigParser()
    with open(properties_path, 'r', encoding='utf-8') as f:
        config.read_string('[DEFAULT]\n' + f.read())

    print_color("Loaded properties:", Fore.GREEN)
    for key in config['DEFAULT']:
        print_color(f"{key}: {config['DEFAULT'][key]}", Fore.YELLOW)

    return config['DEFAULT']

def update_app_name(decompiled_dir, app_name):
    print_color("\n=== UPDATING APP NAME ===", Fore.CYAN)
    values_dirs = glob.glob(os.path.join(decompiled_dir, 'res', 'values*'))

    for values_dir in values_dirs:
        strings_path = os.path.join(values_dir, 'strings.xml')
        if not os.path.exists(strings_path):
            continue

        print_color(f"Processing: {strings_path}", Fore.MAGENTA)
        tree = ET.parse(strings_path)
        root = tree.getroot()

        for string_elem in root.findall('string'):
            if string_elem.get('name') == 'godot_project_name_string':
                print_color(f"Found godot_project_name_string: {string_elem.text} -> {app_name}", Fore.YELLOW)
                string_elem.text = app_name

        tree.write(strings_path, encoding='utf-8', xml_declaration=True)

def update_version_info(decompiled_dir, version_code, version_name):
    print_color("\n=== UPDATING VERSION INFO ===", Fore.CYAN)
    manifest_path = os.path.join(decompiled_dir, "AndroidManifest.xml")
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    ns = {'android': 'http://schemas.android.com/apk/res/android'}

    # Update versionCode
    if ET.QName(ns['android'], 'versionCode') in root.attrib:
        print_color(f"Updating versionCode: {root.attrib[ET.QName(ns['android'], 'versionCode')]} -> {version_code}", Fore.YELLOW)
    root.attrib[ET.QName(ns['android'], 'versionCode')] = version_code

    # Update versionName
    if ET.QName(ns['android'], 'versionName') in root.attrib:
        print_color(f"Updating versionName: {root.attrib[ET.QName(ns['android'], 'versionName')]} -> {version_name}", Fore.YELLOW)
    root.attrib[ET.QName(ns['android'], 'versionName')] = version_name

    tree.write(manifest_path, encoding='utf-8', xml_declaration=True)
    print_color(f"Updated versions: versionName={version_name}, versionCode={version_code}", Fore.GREEN)

def update_package_name(decompiled_dir, new_package):
    print_color("\n=== UPDATING PACKAGE NAME ===", Fore.CYAN)
    manifest_path = os.path.join(decompiled_dir, "AndroidManifest.xml")

    with open(manifest_path, 'r+', encoding='utf-8') as f:
        content = f.read()
        pattern = r'\bcom\.nineboom\.AGT\b'
        replaced_content = re.sub(pattern, new_package, content)

        if content != replaced_content:
            print_color(f"Replaced package: com.nineboom.AGT -> {new_package}", Fore.YELLOW)
            f.seek(0)
            f.write(replaced_content)
            f.truncate()
        else:
            print_color("No package name replacements needed", Fore.YELLOW)

def update_sdk_versions(decompiled_dir, min_sdk, target_sdk):
    print_color("\n=== UPDATING SDK VERSIONS ===", Fore.CYAN)
    manifest_path = os.path.join(decompiled_dir, "AndroidManifest.xml")
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    ns = {'android': 'http://schemas.android.com/apk/res/android'}

    uses_sdk = root.find('uses-sdk')
    if uses_sdk is None:
        uses_sdk = ET.SubElement(root, 'uses-sdk')
        print_color("Created new uses-sdk element", Fore.YELLOW)

    uses_sdk.set(ET.QName(ns['android'], 'minSdkVersion'), min_sdk)
    uses_sdk.set(ET.QName(ns['android'], 'targetSdkVersion'), target_sdk)

    tree.write(manifest_path, encoding='utf-8', xml_declaration=True)
    print_color(f"Updated SDK versions: minSdk={min_sdk}, targetSdk={target_sdk}", Fore.GREEN)

def calculate_icon_size(mipmap_dir):
    size_mapping = {
        'ldpi': 36,
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
        'xxxhdpi': 192,
        'anydpi': 512,
        'v4': 512
    }

    for qualifier, size in size_mapping.items():
        if qualifier in mipmap_dir:
            return (size, size)
    return (512, 512)

def replace_icons(decompiled_dir, icon_path):
    print_color("\n=== REPLACING ICONS ===", Fore.CYAN)
    try:
        original_icon = Image.open(icon_path)
        mipmap_dirs = glob.glob(os.path.join(decompiled_dir, 'res', 'mipmap-*'))

        for mipmap_dir in mipmap_dirs:
            size = calculate_icon_size(mipmap_dir)
            print_color(f"Processing {os.path.basename(mipmap_dir)} - Size: {size[0]}x{size[1]}", Fore.MAGENTA)

            resized_icon = original_icon.resize(size, Image.Resampling.LANCZOS)

            for icon_file in ['icon.png', 'icon_background.png', 'icon_foreground.png']:
                target_path = os.path.join(mipmap_dir, icon_file)
                if os.path.exists(target_path):
                    resized_icon.save(target_path)
                    print_color(f"Replaced: {target_path}", Fore.GREEN)

    except Exception as e:
        print_color(f"Error replacing icons: {e}", Fore.RED)
        raise

def check_and_copy_cl_file(assets_dir):
    print_color("\n=== ADJUSTING APP SCREEN APPROPRIATE  ===", Fore.CYAN)
    cl_source = os.path.join(os.getcwd(), "_cl_")
    cl_dest = os.path.join(assets_dir, "_cl_")

    if not os.path.exists(cl_dest):
        if os.path.exists(cl_source):
            shutil.copy(cl_source, cl_dest)
            print_color("Copied _cl_ file to assets", Fore.GREEN)
        else:
            print_color("Warning: _cl_ file not found in script directory!", Fore.YELLOW)
    else:
        print_color("_cl_ file already exists in assets", Fore.GREEN)

def rebuild_and_sign(decompiled_dir, properties):
    print_color("\n=== BUILDING APP & SIGNING ===", Fore.CYAN)

    # Rebuild APK
    unsigned_apk = "unsigned.apk"
    run_command(["apktool", "b", decompiled_dir, "-o", unsigned_apk], "Build failed")

    # Zipalign
    aligned_apk = "aligned.apk"
    run_command(["zipalign", "-f", "-p", "4", unsigned_apk, aligned_apk], "Zipalign failed")

    # Sign APK
    signed_apk = f"{properties['app_name']}_{properties['version_code']}.apk"
    sign_cmd = [
        "apksigner", "sign",
        "--ks", properties['keystone_path'],
        "--ks-key-alias", properties['keystone_user'],
        "--ks-pass", f"pass:{properties['keystone_pass']}",
        "--key-pass", f"pass:{properties['keystone_pass']}",
        aligned_apk
    ]
    run_command(sign_cmd, "Signing failed")
    os.rename(aligned_apk, signed_apk)
    print_color(f"\n{Fore.GREEN}=== PROCESS COMPLETED ===", Fore.GREEN)
    print_color(f"Final APK: {signed_apk}", Fore.CYAN)

def main():
    show_banner()
    try:
        apk_path = 'android_godot_template_signed.apk'
        decompiled_dir = "decompiled_apk"

        properties = read_properties()
        decompile_apk(apk_path, decompiled_dir)

        # Update core properties
        update_app_name(decompiled_dir, properties['app_name'])
        update_package_name(decompiled_dir, properties['package_name'])
        update_sdk_versions(decompiled_dir,
                           properties['minSdkVersion'],
                           properties['targetSdkVersion'])
        update_version_info(decompiled_dir,
                           properties['version_code'],
                           properties['version_name'])

        # Handle project assets
        assets_dir = os.path.join(decompiled_dir, 'assets')
        if 'project_zip_path' in properties:
            print_color("\n=== EXTRACTING PROJECT ZIP ===", Fore.CYAN)
            with zipfile.ZipFile(properties['project_zip_path'], 'r') as zip_ref:
                zip_ref.extractall(assets_dir)
                print_color(f"Extracted to: {assets_dir}", Fore.GREEN)

            # Check and copy _cl file
            check_and_copy_cl_file(assets_dir)

        # Replace icons
        if 'icon_path' in properties:
            replace_icons(decompiled_dir, properties['icon_path'])

        # Rebuild and sign
        rebuild_and_sign(decompiled_dir, properties)

    except Exception as e:
        print_color(f"\n{Fore.RED}=== PROCESS FAILED ===", Fore.RED)
        print_color(f"Error: {e}", Fore.RED)
        exit(1)

if __name__ == "__main__":
    main()

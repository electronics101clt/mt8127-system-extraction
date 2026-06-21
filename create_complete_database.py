#!/usr/bin/env python3
"""
Create Complete System Database
Combines all analysis passes into a single comprehensive JSON database
"""

import json
from collections import defaultdict
from pass2_system_binaries import annotate_binary, annotate_library, annotate_hal, annotate_framework
from mtk_vendor_knowledge import (
    get_vendor_binary_function, get_vendor_hal_function,
    get_vendor_lib_function, get_vendor_app_function
)

def categorize_complete(path):
    """Complete categorization with all knowledge databases"""

    entry = {
        'path': path,
        'name': path.split('/')[-1],
        'category': 'Unknown',
        'type': 'unknown',
        'subsystem': None,
        'function': 'Not documented',
        'keywords': [],
        'importance': 'low',
        'partition': 'other'
    }

    # Determine partition
    if path.startswith('/system'):
        entry['partition'] = 'system'
    elif path.startswith('/vendor'):
        entry['partition'] = 'vendor'
    elif path.startswith('/data'):
        entry['partition'] = 'data'
    elif path.startswith('/proc'):
        entry['partition'] = 'proc'
        entry['category'] = 'Virtual Filesystem - /proc'
        entry['type'] = 'virtual'
        entry['subsystem'] = 'Kernel'
        entry['function'] = 'Process and kernel information pseudo-filesystem'
        entry['keywords'] = ['kernel', 'proc', 'virtual']
        return entry
    elif path.startswith('/sys'):
        entry['partition'] = 'sys'
        entry['category'] = 'Virtual Filesystem - /sys'
        entry['type'] = 'virtual'
        entry['subsystem'] = 'Kernel'
        entry['function'] = 'Sysfs - kernel device/driver/module information'
        entry['keywords'] = ['kernel', 'sysfs', 'virtual', 'devices']
        return entry
    elif path.startswith('/dev'):
        entry['partition'] = 'dev'
        entry['category'] = 'Device Node'
        entry['type'] = 'device'
        entry['subsystem'] = 'Kernel/Hardware'
        entry['function'] = 'Device file node for hardware access'
        entry['keywords'] = ['device', 'hardware']
        return entry

    basename = entry['name']

    # Detect if directory
    is_dir = not ('.' in basename or basename in [
        'init', 'ueventd.rc', 'default.prop', 'fstab.enableswap'
    ])

    if is_dir and not path.endswith(('.apk', '.so', '.jar', '.xml', '.prop')):
        entry['category'] = 'Directory'
        entry['type'] = 'directory'
        entry['function'] = f'Directory: {basename}'
        return entry

    # === BINARIES ===
    if ('/bin/' in path or '/xbin/' in path) and not '.' in basename:
        entry['category'] = 'Binary/Executable'
        entry['type'] = 'executable'
        entry['keywords'] = ['binary', 'executable']

        # Try vendor knowledge first
        if entry['partition'] == 'vendor':
            entry['function'] = get_vendor_binary_function(basename)
            entry['subsystem'] = 'Vendor/MTK'

            # Importance for known vendor binaries
            if 'MTK' in entry['function'] or 'Autochips' in entry['function']:
                entry['importance'] = 'medium'
                if 'daemon' in entry['function'].lower() or 'service' in entry['function'].lower():
                    entry['importance'] = 'high'
        else:
            entry['function'] = annotate_binary(basename)

            # Importance
            critical = ['init', 'servicemanager', 'surfaceflinger', 'zygote', 'installd', 'vold', 'netd']
            high = ['adbd', 'audioserver', 'mediaserver', 'cameraserver']
            if basename in critical:
                entry['importance'] = 'critical'
            elif basename in high:
                entry['importance'] = 'high'

        # Categorize by name
        if 'audio' in basename.lower():
            entry['subsystem'] = 'Audio'
            entry['keywords'].append('audio')
        elif 'camera' in basename.lower():
            entry['subsystem'] = 'Camera'
            entry['keywords'].append('camera')
        elif 'graphics' in basename.lower() or 'surface' in basename.lower():
            entry['subsystem'] = 'Graphics'
            entry['keywords'].append('graphics')
        elif 'media' in basename.lower():
            entry['subsystem'] = 'Media'
            entry['keywords'].append('media')

    # === LIBRARIES ===
    elif path.endswith('.so'):
        entry['type'] = 'library'
        entry['keywords'] = ['library', 'native']

        if '/hw/' in path:
            entry['category'] = 'HAL Module'
            entry['importance'] = 'high'
            entry['keywords'].append('hal')

            if entry['partition'] == 'vendor':
                entry['function'] = get_vendor_hal_function(basename)
                entry['subsystem'] = 'Vendor HAL'
            else:
                entry['function'] = annotate_hal(path)
                entry['subsystem'] = 'HAL'

        else:
            entry['category'] = 'Native Library'

            if entry['partition'] == 'vendor':
                entry['function'] = get_vendor_lib_function(basename)
                entry['subsystem'] = 'Vendor/MTK'
            else:
                entry['function'] = annotate_library(basename)

        # Subsystem categorization
        if 'audio' in basename.lower():
            entry['keywords'].append('audio')
        if 'camera' in basename.lower():
            entry['keywords'].append('camera')
        if any(x in basename.lower() for x in ['graphics', 'egl', 'gles', 'gralloc', 'gui']):
            entry['keywords'].append('graphics')
        if 'media' in basename.lower():
            entry['keywords'].append('media')

    # === APPLICATIONS ===
    elif path.endswith('.apk'):
        entry['type'] = 'apk'
        entry['keywords'] = ['app', 'application']

        if entry['partition'] == 'vendor':
            entry['category'] = 'Vendor Application'
            entry['function'] = get_vendor_app_function(basename)
            entry['subsystem'] = 'Vendor Apps'
            entry['importance'] = 'medium'
        else:
            if '/priv-app/' in path:
                entry['category'] = 'Privileged System App'
                entry['importance'] = 'high'
            else:
                entry['category'] = 'System App'
                entry['importance'] = 'medium'

            # App name without .apk
            app_name = basename.replace('.apk', '')

            # Known critical apps
            if app_name in ['SystemUI', 'Settings']:
                entry['importance'] = 'critical'
                entry['subsystem'] = 'System UI'
                entry['function'] = f'Critical system app: {app_name}'
            else:
                entry['function'] = f'Application: {app_name}'

    # === FRAMEWORK ===
    elif path.endswith('.jar'):
        entry['category'] = 'Framework JAR'
        entry['type'] = 'jar'
        entry['subsystem'] = 'Framework'
        entry['keywords'] = ['framework', 'java']
        entry['function'] = annotate_framework(basename)

        if basename in ['framework.jar', 'services.jar']:
            entry['importance'] = 'critical'
        else:
            entry['importance'] = 'high'

    # === COMPILED CODE ===
    elif path.endswith('.odex') or path.endswith('.vdex') or path.endswith('.oat'):
        entry['category'] = 'Compiled Bytecode'
        entry['type'] = 'compiled'
        entry['subsystem'] = 'ART/Dalvik'
        entry['function'] = f'Optimized DEX bytecode for faster app loading'
        entry['keywords'] = ['compiled', 'bytecode', 'dex', 'art']

    # === CONFIGURATION ===
    elif path.endswith('.xml'):
        entry['category'] = 'Configuration File'
        entry['type'] = 'xml'
        entry['keywords'] = ['config', 'xml']

        if '/permissions/' in path:
            entry['subsystem'] = 'Security/Permissions'
            entry['function'] = 'System permission definition'
            entry['importance'] = 'high'
        else:
            entry['subsystem'] = 'Configuration'
            entry['function'] = f'XML configuration: {basename}'

    elif path.endswith('.prop') or 'build.prop' in path or path == '/default.prop':
        entry['category'] = 'Properties File'
        entry['type'] = 'properties'
        entry['subsystem'] = 'Configuration'
        entry['function'] = 'System build/runtime properties'
        entry['keywords'] = ['properties', 'config']
        entry['importance'] = 'high'

    elif path.endswith('.rc'):
        entry['category'] = 'Init Script'
        entry['type'] = 'rc'
        entry['subsystem'] = 'Boot/Init'
        entry['function'] = 'Init system configuration script'
        entry['keywords'] = ['init', 'boot', 'startup']
        entry['importance'] = 'high'

    # === MEDIA/ASSETS ===
    elif any(path.endswith(ext) for ext in ['.ttf', '.otf']):
        entry['category'] = 'Font File'
        entry['type'] = 'font'
        entry['subsystem'] = 'UI/Assets'
        entry['function'] = f'System font: {basename}'
        entry['keywords'] = ['font', 'ui', 'assets']

    elif any(path.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']):
        entry['category'] = 'Image Asset'
        entry['type'] = 'image'
        entry['subsystem'] = 'UI/Assets'
        entry['function'] = f'UI image asset: {basename}'
        entry['keywords'] = ['image', 'ui', 'assets']

    elif any(path.endswith(ext) for ext in ['.ogg', '.mp3', '.wav', '.m4a']):
        entry['category'] = 'Audio Asset'
        entry['type'] = 'audio'
        entry['subsystem'] = 'UI/Assets'
        entry['function'] = f'System sound: {basename}'
        entry['keywords'] = ['audio', 'sound', 'ui', 'assets']

    elif path.endswith('.zip') and 'bootanimation' in path:
        entry['category'] = 'Boot Animation'
        entry['type'] = 'animation'
        entry['subsystem'] = 'Boot'
        entry['function'] = 'System boot animation'
        entry['keywords'] = ['boot', 'animation']
        entry['importance'] = 'medium'

    return entry

def main():
    print("=== Creating Complete System Database ===\n")

    # Load device tree
    print("Loading device tree...")
    with open('device-tree-annotated.txt', 'r', encoding='utf-8', errors='ignore') as f:
        paths = [line.strip() for line in f if line.strip()]

    print(f"Processing {len(paths)} entries...")

    results = []
    stats = defaultdict(int)

    for i, path in enumerate(paths):
        if i % 20000 == 0 and i > 0:
            print(f"  Progress: {i}/{len(paths)} ({i*100//len(paths)}%)")

        entry = categorize_complete(path)
        results.append(entry)
        stats[entry['category']] += 1

    print("\nSaving complete database...")
    with open('complete-system-database.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Statistics
    subsystems = defaultdict(int)
    partitions = defaultdict(int)
    importance = defaultdict(int)

    for entry in results:
        if entry['subsystem']:
            subsystems[entry['subsystem']] += 1
        partitions[entry['partition']] += 1
        importance[entry['importance']] += 1

    print("\n" + "="*60)
    print("DATABASE CREATION COMPLETE")
    print("="*60)

    print(f"\nTotal entries: {len(results)}")
    print(f"Output file: complete-system-database.json")
    print(f"File size: {len(json.dumps(results))} bytes")

    print("\n=== Statistics ===\n")

    print("By Partition:")
    for part, count in sorted(partitions.items(), key=lambda x: x[1], reverse=True):
        print(f"  {part:.<20} {count:>8}")

    print("\nBy Category (top 20):")
    for cat, count in sorted(stats.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {cat:.<40} {count:>6}")

    print("\nBy Subsystem (top 20):")
    for sub, count in sorted(subsystems.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {sub:.<40} {count:>6}")

    print("\nBy Importance:")
    for imp, count in sorted(importance.items(), key=lambda x: ['critical', 'high', 'medium', 'low'].index(x[0]) if x[0] in ['critical', 'high', 'medium', 'low'] else 99):
        print(f"  {imp:.<20} {count:>8}")

    print("\n✓ Complete system database created successfully!")

if __name__ == '__main__':
    main()

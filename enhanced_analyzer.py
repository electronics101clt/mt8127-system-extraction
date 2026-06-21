#!/usr/bin/env python3
"""
Enhanced System Analyzer - Pass 2
Uses knowledge database to provide detailed function descriptions
"""

import json
import sys
from pass2_system_binaries import (
    annotate_binary, annotate_library, annotate_hal, annotate_framework,
    BINARY_FUNCTIONS, LIBRARY_FUNCTIONS
)

def analyze_app(path):
    """Analyze an APK and determine its function"""
    basename = path.split('/')[-1].replace('.apk', '')

    # Known system apps
    app_functions = {
        'Settings': 'System settings application',
        'SystemUI': 'System UI - status bar, navigation bar, notifications, quick settings',
        'Launcher': 'Home screen launcher',
        'Phone': 'Dialer and in-call UI',
        'Contacts': 'Contacts management',
        'ContactsProvider': 'Contacts database provider',
        'Mms': 'SMS/MMS messaging application',
        'Camera': 'Camera application',
        'Gallery': 'Photo and video gallery',
        'Browser': 'Web browser',
        'Calendar': 'Calendar application',
        'CalendarProvider': 'Calendar database provider',
        'Music': 'Music player',
        'DownloadProvider': 'Download manager provider',
        'MediaProvider': 'Media database provider',
        'Bluetooth': 'Bluetooth settings and management',
        'PackageInstaller': 'APK installation UI',
        'DocumentsUI': 'File picker and document manager',
        'Shell': 'ADB shell backend',
        'KeyChain': 'Certificate and key management',
        'PrintSpooler': 'Print service',
        'Telecom': 'Telephony connection service',
        'TelephonyProvider': 'Telephony database provider',
        'NfcNci': 'NFC service',
        'PacProcessor': 'Proxy Auto-Config processor',
        'ProxyHandler': 'Proxy configuration handler',
        'SharedStorageBackup': 'Backup for shared storage',
        'ExternalStorageProvider': 'External storage provider',
        'FusedLocation': 'Fused location provider (GPS + network)',
        'InputDevices': 'Input device configuration',
        'CertInstaller': 'Certificate installer',
        'WallpaperCropper': 'Wallpaper image cropper',
        'LiveWallpapers': 'Live wallpaper support',
        'LiveWallpapersPicker': 'Live wallpaper picker',
        'VpnDialogs': 'VPN connection dialogs',
        'UserDictionaryProvider': 'User dictionary for keyboard',
    }

    # Check for known apps
    for key, desc in app_functions.items():
        if key.lower() in basename.lower():
            return desc

    # Heuristic categorization
    if 'provider' in basename.lower():
        return f'Content provider: {basename}'
    elif 'service' in basename.lower():
        return f'System service: {basename}'
    elif any(x in basename.lower() for x in ['music', 'video', 'audio', 'media']):
        return f'Media application: {basename}'
    elif any(x in basename.lower() for x in ['bt', 'bluetooth', 'wifi', 'nfc']):
        return f'Connectivity application: {basename}'
    elif 'launcher' in basename.lower():
        return f'Launcher: {basename}'

    return f'Application: {basename}'

def get_detailed_category(path):
    """Get detailed category and function for a path"""

    result = {
        'path': path,
        'category': 'Unknown',
        'type': 'unknown',
        'subsystem': None,
        'function': 'Unknown',
        'keywords': [],
        'importance': 'low'  # low, medium, high, critical
    }

    basename = path.split('/')[-1]

    # === BINARIES ===
    if '/bin/' in path and '.' not in basename:
        result['category'] = 'Binary/Executable'
        result['type'] = 'executable'
        result['function'] = annotate_binary(basename)

        # Determine importance
        critical_bins = ['init', 'servicemanager', 'surfaceflinger', 'zygote',
                        'installd', 'vold', 'netd']
        high_bins = ['adbd', 'audioserver', 'mediaserver', 'cameraserver',
                    'wpa_supplicant', 'rild']

        if basename in critical_bins:
            result['importance'] = 'critical'
        elif basename in high_bins:
            result['importance'] = 'high'
        elif basename in BINARY_FUNCTIONS:
            result['importance'] = 'medium'

        # Determine subsystem
        if 'audio' in basename:
            result['subsystem'] = 'Audio'
            result['keywords'] = ['audio', 'sound']
        elif 'surface' in basename or 'graphics' in basename:
            result['subsystem'] = 'Graphics'
            result['keywords'] = ['graphics', 'display']
        elif 'media' in basename or 'codec' in basename:
            result['subsystem'] = 'Media'
            result['keywords'] = ['media', 'codec']
        elif 'camera' in basename:
            result['subsystem'] = 'Camera'
            result['keywords'] = ['camera']
        elif 'net' in basename or 'wifi' in basename or 'bt' in basename:
            result['subsystem'] = 'Networking'
            result['keywords'] = ['network', 'connectivity']
        elif basename in ['init', 'ueventd', 'bootstat']:
            result['subsystem'] = 'Boot/Init'
            result['keywords'] = ['boot', 'init']
        elif 'log' in basename or 'dump' in basename or 'debug' in basename:
            result['subsystem'] = 'Debug/Logging'
            result['keywords'] = ['debug', 'logging']

    # === LIBRARIES ===
    elif path.endswith('.so'):
        result['type'] = 'library'

        if '/hw/' in path:
            result['category'] = 'HAL Module'
            result['function'] = annotate_hal(path)
            result['importance'] = 'high'
            result['subsystem'] = 'HAL'
            result['keywords'] = ['hal', 'hardware']
        else:
            result['category'] = 'Native Library'
            result['function'] = annotate_library(basename)

            # Categorize by name
            if basename in LIBRARY_FUNCTIONS:
                result['importance'] = 'high'

            if 'audio' in basename:
                result['subsystem'] = 'Audio'
                result['keywords'] = ['audio']
            elif any(x in basename for x in ['surface', 'gui', 'EGL', 'GLES', 'graphics']):
                result['subsystem'] = 'Graphics'
                result['keywords'] = ['graphics']
            elif 'media' in basename or 'stagefright' in basename:
                result['subsystem'] = 'Media'
                result['keywords'] = ['media']
            elif 'camera' in basename:
                result['subsystem'] = 'Camera'
                result['keywords'] = ['camera']
            elif 'binder' in basename:
                result['subsystem'] = 'IPC'
                result['keywords'] = ['ipc', 'binder']
                result['importance'] = 'critical'

    # === APPLICATIONS ===
    elif path.endswith('.apk'):
        result['type'] = 'apk'
        result['function'] = analyze_app(path)

        if '/priv-app/' in path:
            result['category'] = 'Privileged System App'
            result['importance'] = 'high'
        else:
            result['category'] = 'System App'
            result['importance'] = 'medium'

        result['keywords'] = ['app', 'application']

        # Determine subsystem
        basename_lower = basename.lower()
        if 'systemui' in basename_lower or 'settings' in basename_lower:
            result['subsystem'] = 'System UI'
            result['importance'] = 'critical'
        elif 'phone' in basename_lower or 'contacts' in basename_lower or 'mms' in basename_lower:
            result['subsystem'] = 'Communication'
        elif 'camera' in basename_lower:
            result['subsystem'] = 'Camera'
        elif any(x in basename_lower for x in ['music', 'video', 'media', 'gallery']):
            result['subsystem'] = 'Media'

    # === FRAMEWORK ===
    elif path.endswith('.jar'):
        result['category'] = 'Framework JAR'
        result['type'] = 'jar'
        result['function'] = annotate_framework(basename)
        result['subsystem'] = 'Framework'
        result['keywords'] = ['framework', 'java']

        if 'framework.jar' in basename or 'services.jar' in basename:
            result['importance'] = 'critical'
        else:
            result['importance'] = 'high'

    # === CONFIGURATION ===
    elif path.endswith('.xml'):
        result['category'] = 'Configuration File'
        result['type'] = 'xml'
        result['keywords'] = ['config', 'xml']

        if '/permissions/' in path:
            result['function'] = 'System permission definition'
            result['subsystem'] = 'Security/Permissions'
            result['importance'] = 'high'
        elif '/etc/' in path:
            result['function'] = f'System configuration: {basename}'
            result['subsystem'] = 'Configuration'
        else:
            result['function'] = f'Configuration file: {basename}'

    elif path.endswith('.prop') or 'build.prop' in path:
        result['category'] = 'Properties File'
        result['type'] = 'properties'
        result['function'] = 'System build/runtime properties'
        result['subsystem'] = 'Configuration'
        result['keywords'] = ['properties', 'config']
        result['importance'] = 'high'

    # === MEDIA/ASSETS ===
    elif any(path.endswith(ext) for ext in ['.ttf', '.otf']):
        result['category'] = 'Font'
        result['type'] = 'font'
        result['function'] = f'System font: {basename}'
        result['subsystem'] = 'UI/Assets'
        result['keywords'] = ['font', 'ui', 'assets']

    elif any(path.endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
        result['category'] = 'Image Asset'
        result['type'] = 'image'
        result['function'] = f'UI image asset: {basename}'
        result['subsystem'] = 'UI/Assets'
        result['keywords'] = ['image', 'ui', 'assets']

    elif any(path.endswith(ext) for ext in ['.ogg', '.mp3', '.wav']):
        result['category'] = 'Audio Asset'
        result['type'] = 'audio'
        result['function'] = f'System sound: {basename}'
        result['subsystem'] = 'UI/Assets'
        result['keywords'] = ['audio', 'sound', 'ui', 'assets']

    # === FIRMWARE ===
    elif any(ext in path for ext in ['/firmware/', '.bin', '.img', '.fw']) and '/system/' not in path:
        result['category'] = 'Firmware Blob'
        result['type'] = 'firmware'
        result['function'] = f'Hardware firmware: {basename}'
        result['subsystem'] = 'Hardware/Firmware'
        result['keywords'] = ['firmware', 'hardware', 'blob']

    return result

def main():
    print("Enhanced Analyzer - Pass 2")
    print("Loading system partition data...")

    with open('system-partition.txt', 'r') as f:
        paths = [line.strip() for line in f]

    print(f"Analyzing {len(paths)} entries...")
    results = []

    for i, path in enumerate(paths):
        if i % 500 == 0:
            print(f"  Progress: {i}/{len(paths)} ({i*100//len(paths)}%)")

        analysis = get_detailed_category(path)
        results.append(analysis)

    print(f"\nSaving enhanced analysis...")
    with open('system-detailed-analysis.json', 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Generate statistics
    from collections import Counter
    categories = Counter(r['category'] for r in results)
    subsystems = Counter(r['subsystem'] for r in results if r['subsystem'])
    importance = Counter(r['importance'] for r in results)

    print("\n=== Analysis Complete ===")
    print(f"Total entries: {len(results)}")
    print(f"\nCategories:")
    for cat, count in categories.most_common():
        print(f"  {cat:.<40} {count:>5}")

    print(f"\nSubsystems:")
    for sub, count in subsystems.most_common():
        print(f"  {sub:.<40} {count:>5}")

    print(f"\nImportance:")
    for imp, count in importance.most_common():
        print(f"  {imp:.<40} {count:>5}")

    print(f"\nOutput saved to: system-detailed-analysis.json")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
MT8127 System Analysis Tool
Categorizes and documents all files in the Android system
"""

import json
import re
from pathlib import Path
from collections import defaultdict

class SystemAnalyzer:
    def __init__(self, tree_file):
        self.tree_file = tree_file
        self.entries = []
        self.stats = defaultdict(int)

    def load_tree(self):
        """Load device tree file"""
        print(f"Loading {self.tree_file}...")
        with open(self.tree_file, 'r', encoding='utf-8', errors='ignore') as f:
            self.entries = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(self.entries)} entries")

    def categorize_entry(self, path):
        """Categorize a single file/directory path"""

        # Default entry structure
        entry = {
            'path': path,
            'type': 'unknown',
            'category': 'uncategorized',
            'subsystem': None,
            'function': None,
            'keywords': []
        }

        # Determine if file or directory (simple heuristic - has extension or known file)
        basename = path.split('/')[-1]
        is_file = '.' in basename or basename in ['init', 'ueventd.rc', 'default.prop']

        entry['type'] = 'file' if is_file else 'directory'

        # === TOP LEVEL DIRECTORIES ===

        # Virtual filesystems
        if path.startswith('/proc'):
            entry['category'] = 'Virtual Filesystem'
            entry['subsystem'] = 'Kernel'
            entry['function'] = 'Process and kernel information pseudo-filesystem'
            entry['keywords'] = ['kernel', 'proc', 'virtual', 'debug']

        elif path.startswith('/sys'):
            entry['category'] = 'Virtual Filesystem'
            entry['subsystem'] = 'Kernel'
            entry['function'] = 'Sysfs - kernel device/driver information'
            entry['keywords'] = ['kernel', 'sysfs', 'virtual', 'devices', 'drivers']

        elif path.startswith('/dev'):
            entry['category'] = 'Device Nodes'
            entry['subsystem'] = 'Kernel'
            entry['function'] = 'Device file nodes for hardware access'
            entry['keywords'] = ['devices', 'hardware', 'drivers']

            # Subcategorize device nodes
            if '/dev/block' in path:
                entry['subsystem'] = 'Storage'
                entry['function'] = 'Block device nodes for storage'
                entry['keywords'].extend(['storage', 'block', 'partitions'])
            elif '/dev/graphics' in path or '/dev/fb' in path:
                entry['subsystem'] = 'Graphics'
                entry['function'] = 'Graphics/framebuffer devices'
                entry['keywords'].extend(['display', 'framebuffer', 'graphics'])
            elif '/dev/input' in path:
                entry['subsystem'] = 'Input'
                entry['function'] = 'Input device nodes (touch, buttons, etc.)'
                entry['keywords'].extend(['input', 'touch', 'buttons', 'sensors'])
            elif '/dev/snd' in path:
                entry['subsystem'] = 'Audio'
                entry['function'] = 'Audio device nodes'
                entry['keywords'].extend(['audio', 'sound', 'alsa'])
            elif '/dev/video' in path or '/dev/camera' in path:
                entry['subsystem'] = 'Camera/Video'
                entry['function'] = 'Video/camera device nodes'
                entry['keywords'].extend(['camera', 'video'])

        # Config/mount points
        elif path.startswith('/config'):
            entry['category'] = 'Configuration'
            entry['subsystem'] = 'Kernel'
            entry['function'] = 'ConfigFS - kernel configuration filesystem'
            entry['keywords'] = ['config', 'kernel']

        elif path.startswith('/acct'):
            entry['category'] = 'Accounting'
            entry['subsystem'] = 'Kernel'
            entry['function'] = 'CPU accounting cgroup mount point'
            entry['keywords'] = ['cgroup', 'cpu', 'accounting']

        elif path.startswith('/d'):
            entry['category'] = 'Debug'
            entry['subsystem'] = 'Kernel'
            entry['function'] = 'DebugFS mount point'
            entry['keywords'] = ['debug', 'debugfs', 'kernel']

        # Storage/data
        elif path.startswith('/data'):
            entry['category'] = 'User Data'
            entry['subsystem'] = 'Storage'
            entry['function'] = 'User and app data partition'
            entry['keywords'] = ['storage', 'data', 'apps', 'user']

        elif path.startswith('/cache'):
            entry['category'] = 'Cache'
            entry['subsystem'] = 'Storage'
            entry['function'] = 'System cache partition'
            entry['keywords'] = ['cache', 'storage', 'temporary']

        elif path.startswith('/mnt') or path.startswith('/storage'):
            entry['category'] = 'Mount Points'
            entry['subsystem'] = 'Storage'
            entry['function'] = 'Storage mount points'
            entry['keywords'] = ['storage', 'mount', 'external']

        elif path.startswith('/sdcard'):
            entry['category'] = 'External Storage'
            entry['subsystem'] = 'Storage'
            entry['function'] = 'SD card symlink/mount'
            entry['keywords'] = ['sdcard', 'storage', 'external']

        # Boot/init
        elif path.startswith('/sbin'):
            entry['category'] = 'Boot Binaries'
            entry['subsystem'] = 'Boot'
            entry['function'] = 'Recovery/boot mode binaries'
            entry['keywords'] = ['boot', 'recovery', 'init']

        elif path == '/init' or path.endswith('.rc') and path.count('/') == 1:
            entry['category'] = 'Init Scripts'
            entry['subsystem'] = 'Boot'
            entry['function'] = 'System initialization scripts'
            entry['keywords'] = ['init', 'boot', 'startup']

        elif path == '/default.prop':
            entry['category'] = 'Build Properties'
            entry['subsystem'] = 'Configuration'
            entry['function'] = 'Default system properties'
            entry['keywords'] = ['properties', 'config', 'build']

        # OEM/vendor partitions
        elif path.startswith('/oem'):
            entry['category'] = 'OEM Partition'
            entry['subsystem'] = 'Vendor'
            entry['function'] = 'OEM customization partition'
            entry['keywords'] = ['oem', 'vendor', 'customization']

        elif path.startswith('/protect_f') or path.startswith('/protect_s'):
            entry['category'] = 'MTK Protected Storage'
            entry['subsystem'] = 'Vendor/MTK'
            entry['function'] = 'MediaTek protected data partition'
            entry['keywords'] = ['mtk', 'protected', 'vendor', 'storage']

        # === /SYSTEM PARTITION ===
        elif path.startswith('/system'):
            entry['category'] = 'System'

            # System binaries
            if '/system/bin/' in path:
                entry['category'] = 'System Binary'
                entry['type'] = 'executable'
                entry['subsystem'] = 'Core'
                entry['function'] = f'System executable: {basename}'
                entry['keywords'] = ['binary', 'executable', 'system']

                # Identify specific binaries
                if 'audio' in basename.lower():
                    entry['subsystem'] = 'Audio'
                    entry['keywords'].append('audio')
                elif 'surface' in basename.lower() or 'ui' in basename.lower():
                    entry['subsystem'] = 'Graphics/UI'
                    entry['keywords'].extend(['graphics', 'ui'])
                elif 'media' in basename.lower() or 'codec' in basename.lower():
                    entry['subsystem'] = 'Media'
                    entry['keywords'].extend(['media', 'codec'])
                elif 'network' in basename.lower() or 'wifi' in basename.lower() or 'bt' in basename.lower():
                    entry['subsystem'] = 'Network/Connectivity'
                    entry['keywords'].extend(['network', 'connectivity'])
                elif 'camera' in basename.lower():
                    entry['subsystem'] = 'Camera'
                    entry['keywords'].append('camera')

            # System xbin (extended binaries)
            elif '/system/xbin/' in path:
                entry['category'] = 'Extended Binary'
                entry['type'] = 'executable'
                entry['subsystem'] = 'Core'
                entry['function'] = f'Extended system utility: {basename}'
                entry['keywords'] = ['binary', 'executable', 'utility', 'system']

            # Native libraries
            elif path.endswith('.so'):
                entry['category'] = 'Native Library'
                entry['type'] = 'library'
                entry['function'] = f'Native shared library: {basename}'
                entry['keywords'] = ['library', 'native', 'so']

                # Categorize by path and name
                if '/system/lib/hw/' in path or '/system/lib64/hw/' in path:
                    entry['category'] = 'HAL Library'
                    entry['subsystem'] = 'HAL'
                    entry['function'] = f'Hardware Abstraction Layer: {basename}'
                    entry['keywords'].extend(['hal', 'hardware'])

                    if 'audio' in basename:
                        entry['subsystem'] = 'Audio HAL'
                        entry['keywords'].append('audio')
                    elif 'camera' in basename:
                        entry['subsystem'] = 'Camera HAL'
                        entry['keywords'].append('camera')
                    elif 'gralloc' in basename or 'graphics' in basename:
                        entry['subsystem'] = 'Graphics HAL'
                        entry['keywords'].extend(['graphics', 'display'])
                    elif 'sensors' in basename:
                        entry['subsystem'] = 'Sensors HAL'
                        entry['keywords'].append('sensors')
                    elif 'gps' in basename or 'gnss' in basename:
                        entry['subsystem'] = 'GPS HAL'
                        entry['keywords'].extend(['gps', 'location'])

                else:
                    # General library categorization by name
                    if 'audio' in basename.lower():
                        entry['subsystem'] = 'Audio'
                        entry['keywords'].append('audio')
                    elif 'camera' in basename.lower():
                        entry['subsystem'] = 'Camera'
                        entry['keywords'].append('camera')
                    elif 'media' in basename.lower() or 'codec' in basename.lower():
                        entry['subsystem'] = 'Media'
                        entry['keywords'].extend(['media', 'codec'])
                    elif 'surface' in basename.lower() or 'ui' in basename.lower() or 'gui' in basename.lower():
                        entry['subsystem'] = 'Graphics/UI'
                        entry['keywords'].extend(['graphics', 'ui'])
                    elif 'binder' in basename.lower():
                        entry['subsystem'] = 'IPC/Binder'
                        entry['keywords'].extend(['ipc', 'binder'])

            # Applications
            elif path.endswith('.apk'):
                entry['category'] = 'Application'
                entry['type'] = 'apk'
                entry['keywords'] = ['app', 'application']

                if '/system/priv-app/' in path:
                    entry['category'] = 'Privileged Application'
                    entry['function'] = f'Privileged system app: {basename}'
                    entry['keywords'].append('privileged')
                elif '/system/app/' in path:
                    entry['function'] = f'System application: {basename}'
                else:
                    entry['function'] = f'Application: {basename}'

                # Categorize by name
                app_name = basename.replace('.apk', '')
                if any(x in app_name.lower() for x in ['settings', 'systemui']):
                    entry['subsystem'] = 'System UI'
                    entry['keywords'].extend(['ui', 'settings'])
                elif any(x in app_name.lower() for x in ['phone', 'dialer', 'contacts']):
                    entry['subsystem'] = 'Telephony'
                    entry['keywords'].extend(['phone', 'telephony'])
                elif any(x in app_name.lower() for x in ['camera']):
                    entry['subsystem'] = 'Camera'
                    entry['keywords'].append('camera')
                elif any(x in app_name.lower() for x in ['bluetooth', 'nfc', 'wifi']):
                    entry['subsystem'] = 'Connectivity'
                    entry['keywords'].append('connectivity')

            # Framework
            elif path.endswith('.jar'):
                entry['category'] = 'Framework JAR'
                entry['type'] = 'jar'
                entry['subsystem'] = 'Framework'
                entry['function'] = f'Java framework library: {basename}'
                entry['keywords'] = ['framework', 'java', 'jar']

            # Configuration files
            elif path.endswith('.xml'):
                entry['category'] = 'Configuration'
                entry['type'] = 'xml'
                entry['function'] = f'XML configuration: {basename}'
                entry['keywords'] = ['config', 'xml']

                if '/permissions/' in path:
                    entry['subsystem'] = 'Permissions'
                    entry['function'] = 'System permissions definition'
                    entry['keywords'].extend(['permissions', 'security'])

            elif path.endswith('.prop') or 'build.prop' in path:
                entry['category'] = 'Build Properties'
                entry['type'] = 'properties'
                entry['function'] = 'System build properties'
                entry['keywords'] = ['properties', 'build', 'config']

            # Media/assets
            elif any(path.endswith(ext) for ext in ['.ttf', '.otf']):
                entry['category'] = 'Font'
                entry['type'] = 'font'
                entry['subsystem'] = 'Media/Assets'
                entry['function'] = f'System font: {basename}'
                entry['keywords'] = ['font', 'media', 'assets']

            elif any(path.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp']):
                entry['category'] = 'Image'
                entry['type'] = 'image'
                entry['subsystem'] = 'Media/Assets'
                entry['function'] = f'System image: {basename}'
                entry['keywords'] = ['image', 'media', 'assets']

            elif any(path.endswith(ext) for ext in ['.ogg', '.mp3', '.wav']):
                entry['category'] = 'Audio Asset'
                entry['type'] = 'audio'
                entry['subsystem'] = 'Media/Assets'
                entry['function'] = f'System sound: {basename}'
                entry['keywords'] = ['audio', 'sound', 'media', 'assets']

            elif path.endswith('.zip') and 'bootanimation' in path:
                entry['category'] = 'Boot Animation'
                entry['type'] = 'animation'
                entry['subsystem'] = 'Boot'
                entry['function'] = 'System boot animation'
                entry['keywords'] = ['boot', 'animation', 'media']

            # Firmware
            elif any(path.endswith(ext) for ext in ['.bin', '.img', '.fw']):
                if '/vendor/firmware' in path or '/system/vendor/firmware' in path:
                    entry['category'] = 'Firmware'
                    entry['type'] = 'firmware'
                    entry['subsystem'] = 'Hardware'
                    entry['function'] = f'Hardware firmware blob: {basename}'
                    entry['keywords'] = ['firmware', 'hardware', 'blob']

        # === /VENDOR PARTITION ===
        elif path.startswith('/vendor'):
            entry['category'] = 'Vendor'

            # Vendor binaries
            if '/vendor/bin/' in path:
                entry['category'] = 'Vendor Binary'
                entry['type'] = 'executable'
                entry['subsystem'] = 'Vendor/MTK'
                entry['function'] = f'Vendor executable: {basename}'
                entry['keywords'] = ['binary', 'executable', 'vendor', 'mtk']

            # Vendor libraries
            elif path.endswith('.so'):
                entry['category'] = 'Vendor Library'
                entry['type'] = 'library'
                entry['subsystem'] = 'Vendor/MTK'
                entry['function'] = f'Vendor shared library: {basename}'
                entry['keywords'] = ['library', 'vendor', 'mtk']

                if '/vendor/lib/hw/' in path or '/vendor/lib64/hw/' in path:
                    entry['category'] = 'Vendor HAL'
                    entry['function'] = f'Vendor HAL implementation: {basename}'
                    entry['keywords'].append('hal')

            # Vendor apps
            elif path.endswith('.apk'):
                entry['category'] = 'Vendor Application'
                entry['type'] = 'apk'
                entry['subsystem'] = 'Vendor/MTK'
                entry['function'] = f'Vendor application: {basename}'
                entry['keywords'] = ['app', 'vendor', 'mtk']

            # Vendor firmware
            elif '/vendor/firmware' in path:
                entry['category'] = 'Vendor Firmware'
                entry['type'] = 'firmware'
                entry['subsystem'] = 'Vendor/MTK'
                entry['function'] = f'Vendor firmware blob: {basename}'
                entry['keywords'] = ['firmware', 'vendor', 'mtk']

            # Vendor config
            elif path.endswith('.xml') or path.endswith('.conf'):
                entry['category'] = 'Vendor Configuration'
                entry['subsystem'] = 'Vendor/MTK'
                entry['function'] = f'Vendor configuration: {basename}'
                entry['keywords'] = ['config', 'vendor', 'mtk']

        # Root directory files
        elif path.startswith('/root'):
            entry['category'] = 'Root Directory'
            entry['subsystem'] = 'System'
            entry['function'] = 'Root user home directory'
            entry['keywords'] = ['root']

        # Etc symlink
        elif path.startswith('/etc'):
            entry['category'] = 'Configuration Symlink'
            entry['subsystem'] = 'System'
            entry['function'] = 'Symlink to /system/etc'
            entry['keywords'] = ['config', 'symlink']

        # Charger
        elif path.startswith('/charger'):
            entry['category'] = 'Charger Mode'
            entry['subsystem'] = 'Boot'
            entry['function'] = 'Charger mode assets/binary'
            entry['keywords'] = ['charger', 'boot', 'power']

        # Bugreports
        elif path.startswith('/bugreports'):
            entry['category'] = 'Bug Reports'
            entry['subsystem'] = 'Debug'
            entry['function'] = 'Bug report storage'
            entry['keywords'] = ['debug', 'bugreport']

        # Update stats
        self.stats[entry['category']] += 1

        return entry

    def analyze(self):
        """Analyze all entries"""
        print("Analyzing entries...")
        analyzed = []

        for i, path in enumerate(self.entries):
            if i % 10000 == 0:
                print(f"  Progress: {i}/{len(self.entries)} ({i*100//len(self.entries)}%)")

            entry = self.categorize_entry(path)
            analyzed.append(entry)

        print(f"Analysis complete: {len(analyzed)} entries categorized")
        return analyzed

    def save_json(self, analyzed, output_file):
        """Save analyzed data to JSON"""
        print(f"Saving to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analyzed, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(analyzed)} entries")

    def print_stats(self):
        """Print categorization statistics"""
        print("\n=== Categorization Statistics ===")
        for category, count in sorted(self.stats.items(), key=lambda x: x[1], reverse=True):
            print(f"  {category}: {count}")
        print(f"\nTotal categories: {len(self.stats)}")


def main():
    analyzer = SystemAnalyzer('device-tree-annotated.txt')
    analyzer.load_tree()
    analyzed = analyzer.analyze()
    analyzer.save_json(analyzed, 'system-database.json')
    analyzer.print_stats()

    print("\n✓ Analysis complete!")
    print(f"  Output: system-database.json")
    print(f"  Total entries: {len(analyzed)}")

if __name__ == '__main__':
    main()

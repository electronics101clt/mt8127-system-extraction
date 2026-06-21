#!/usr/bin/env python3
"""
Update all remaining generic explanations with research from web search
"""

# Additional Unix/Linux commands
UNIX_COMMANDS_COMPLETE = {
    'blockdev': 'Query and set block device (disk/SSD/USB) properties',
    'cal': 'Display calendar for current or specified month/year',
    'chcon': 'Change SELinux security context of files/directories',
    'chgrp': 'Change group ownership of files',
    'chroot': 'Change root directory - run command in isolated filesystem environment',
    'chrt': 'Change real-time scheduling attributes - set process priority and CPU scheduling policy',
    'cksum': 'Calculate CRC32 checksum and byte count for file verification',
    'clear': 'Clear terminal screen',
    'cmp': 'Compare two files byte-by-byte',
    'comm': 'Compare two sorted files line-by-line',
    'cpio': 'Archive utility for backup and restore operations',
    'cut': 'Extract columns/fields from text files',
    'dirname': 'Strip filename from file path - return directory path only',
    'dos2unix': 'Convert DOS/Windows line endings (CRLF) to Unix (LF)',
    'egrep': 'Extended grep - search files using extended regular expressions',
    'env': 'Display or set environment variables for command execution',
    'exfat': 'exFAT filesystem utilities',
    'exfatfsck': 'Check and repair exFAT filesystem errors',
    'expand': 'Convert tabs to spaces in text files',
    'expr': 'Evaluate mathematical and string expressions',
    'fallocate': 'Preallocate disk space for files without writing data - fast file creation',
    'false': 'Return false exit status (exit code 1) - used in shell scripts',
    'fgrep': 'Fast grep - search for fixed strings (no regex)',
    'file': 'Determine file type by examining file contents',
    'flock': 'Manage file locks - prevent concurrent access by multiple processes',
    'free': 'Display memory usage statistics (RAM and swap)',
    'getenforce': 'Get current SELinux enforcement mode (enforcing/permissive/disabled)',
    'getprop': 'Get Android system property value',
    'groups': 'Display user group memberships',
    'gunzip': 'Decompress gzip-compressed files',
    'gzip': 'Compress files using gzip algorithm',
    'hostapd': 'Host Access Point daemon - turn device into WiFi access point (hotspot)',
    'hostapd_cli': 'Command-line interface for hostapd - configure and debug WiFi AP',
    'hostname': 'Display or set system hostname',
    'hotplug': 'Handle hardware hotplug events - notify system when devices are connected/disconnected',
    'hw': 'Hardware utilities directory',
}

# HIDL HAL services with detailed explanations
HIDL_SERVICES = {
    'android.hardware.audio@2.0-service-mediatek': 'HIDL HAL service - MTK audio subsystem (input/output/routing/mixing)',
    'android.hardware.bluetooth@1.0-service-mediatek': 'HIDL HAL service - MTK Bluetooth stack (pairing/connections/profiles)',
    'android.hardware.broadcastradio@1.1-service': 'HIDL HAL service - FM/AM/DAB radio tuning and scanning',
    'android.hardware.cas@1.0-service': 'HIDL HAL service - Conditional Access System for encrypted TV/video streams',
    'android.hardware.configstore@1.0-service': 'HIDL HAL service - Build configuration flags (deprecated in Android 10)',
    'android.hardware.drm@1.0-service': 'HIDL HAL service - Digital Rights Management for protected media playback',
    'android.hardware.drm@1.0-service.widevine': 'HIDL HAL service - Google Widevine DRM for Netflix/streaming services',
    'android.hardware.gatekeeper@1.0-service': 'HIDL HAL service - Password authentication with throttling (lockscreen security)',
    'android.hardware.graphics.allocator@2.0-service': 'HIDL HAL service - GPU memory buffer allocation (Gralloc)',
    'android.hardware.graphics.composer@2.1-service': 'HIDL HAL service - Hardware compositor for display layers (HWC)',
    'android.hardware.keymaster@3.0-service': 'HIDL HAL service - Cryptographic key generation and secure storage',
    'android.hardware.light@2.0-service-mediatek': 'HIDL HAL service - MTK LED/backlight brightness control',
    'android.hardware.media.omx@1.0-service': 'HIDL HAL service - OpenMAX media codecs (video/audio encoding/decoding)',
    'android.hardware.memtrack@1.0-service': 'HIDL HAL service - GPU and hardware memory usage tracking',
    'android.hardware.wifi@1.0-service': 'HIDL HAL service - WiFi connection management and scanning',
    'camerahalserver': 'Camera HAL server - manages camera hardware access',
    'camhal3lite': 'Camera HAL 3 lite implementation - simplified camera interface',
    'power_native_test': 'Power HAL native test utility',
    'rilproxy': 'Radio Interface Layer proxy - modem communication interface',
    'vendor.autochips.hardware.audio@1.0-service': 'HIDL HAL service - Autochips audio subsystem',
    'vendor.autochips.hardware.backcar@1.0-service': 'HIDL HAL service - Autochips backup/reverse camera control',
    'vendor.autochips.hardware.dvr@1.0-service': 'HIDL HAL service - Autochips dashboard camera recording (DVR)',
    'vendor.autochips.hardware.metalogo@1.0-service': 'HIDL HAL service - Autochips boot logo display control',
    'vendor.autochips.hardware.usb@1.1-service': 'HIDL HAL service - Autochips USB device management',
    'vendor.mediatek.hardware.gnss@1.1-service': 'HIDL HAL service - MTK GNSS/GPS location services',
    'vendor.mediatek.hardware.keymanage@1.0-service': 'HIDL HAL service - MTK cryptographic key management',
    'vendor.mediatek.hardware.keymaster_attestation@1.0-service': 'HIDL HAL service - MTK key attestation for verified boot',
    'vendor.mediatek.hardware.mtkcodecservice@1.1-service': 'HIDL HAL service - MTK hardware media codec (video/audio encoding/decoding)',
    'vendor.mediatek.hardware.power@1.1-service': 'HIDL HAL service - MTK power management and CPU frequency scaling',
}

def update_explanation(path, current_line):
    """Update explanation with researched information"""

    if ' | ' not in current_line:
        return current_line

    path_part, explanation = current_line.strip().split(' | ', 1)
    basename = path.split('/')[-1]

    # Update Unix commands
    if explanation.startswith('Vendor binary:'):
        cmd_name = explanation.split(': ')[1]
        if cmd_name in UNIX_COMMANDS_COMPLETE:
            return f"{path} | {UNIX_COMMANDS_COMPLETE[cmd_name]}\n"

    # Update HIDL services (exact basename match)
    if basename in HIDL_SERVICES:
        return f"{path} | {HIDL_SERVICES[basename]}\n"

    # Update directory with no explanation
    if '/lost+found' in path and not explanation.startswith('Lost+found') and not explanation.startswith('Filesystem recovery'):
        return f"{path} | Lost+found directory for filesystem recovery\n"

    return current_line

print("Loading file...")
with open('device-tree-annotated.txt', 'r') as f:
    lines = f.readlines()

print("Updating explanations...")
output = []
updated = 0

for i, line in enumerate(lines):
    if i % 50000 == 0:
        print(f"  {i}/{len(lines)}")

    new_line = update_explanation(line.strip() if ' | ' in line else line.strip(), line)
    if new_line != line:
        updated += 1
    output.append(new_line if new_line.endswith('\n') else new_line + '\n')

print(f"\nWriting file...")
with open('device-tree-annotated.txt', 'w') as f:
    f.writelines(output)

print(f"Done! Updated {updated} explanations with web research")

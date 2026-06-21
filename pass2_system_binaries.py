#!/usr/bin/env python3
"""
Pass 2: Document system binaries and their functions
"""

import json

# Known Android system binary functions
BINARY_FUNCTIONS = {
    # Core Android services
    'adbd': 'Android Debug Bridge daemon - enables USB debugging and adb connection',
    'servicemanager': 'Binder service manager - central IPC registry for all system services',
    'surfaceflinger': 'Graphics compositor - composites all UI layers and renders to display',
    'audioserver': 'Audio service - manages audio routing, mixing, and hardware access',
    'mediaserver': 'Media codec server - handles audio/video encoding and decoding',
    'cameraserver': 'Camera service - manages camera hardware and video capture',
    'bootanimation': 'Boot animation renderer - shows boot animation during startup',

    # System utilities
    'app_process': 'Zygote launcher - starts Dalvik/ART virtual machine and forks app processes',
    'app_process32': 'Zygote launcher for 32-bit apps',
    'installd': 'Package installer daemon - handles APK installation and management',
    'vold': 'Volume daemon - manages storage devices and partitions',
    'netd': 'Network daemon - manages network interfaces and routing',
    'wpa_supplicant': 'WiFi authentication service - handles WiFi connection and security',
    'rild': 'Radio Interface Layer daemon - manages cellular modem communication',

    # Package management
    'pm': 'Package Manager CLI - install/uninstall/query packages',
    'cmd': 'Generic command dispatcher for system services',
    'am': 'Activity Manager CLI - start activities, broadcast intents, etc.',
    'sm': 'Storage Manager CLI - manage storage devices',

    # Input/Display
    'input': 'Input event injector - simulate touch/key events',
    'uiautomator': 'UI testing automation tool',
    'screencap': 'Screenshot capture utility',
    'screenrecord': 'Screen recording utility',

    # Debug/Development
    'logcat': 'System log viewer',
    'dumpsys': 'Dump system service state for debugging',
    'dumpstate': 'Collect full system state for bug reports',
    'bugreport': 'Generate comprehensive bug report',
    'debuggerd': 'Crash handler and debugger',
    'atrace': 'System trace utility for performance analysis',

    # SELinux
    'setenforce': 'Set SELinux enforcement mode (enforcing/permissive)',
    'getenforce': 'Get current SELinux enforcement mode',
    'restorecon': 'Restore SELinux security contexts',
    'runcon': 'Run command with specified SELinux context',

    # System properties
    'getprop': 'Get system property values',
    'setprop': 'Set system property values',
    'watchprops': 'Watch system property changes',

    # File operations
    'toolbox': 'Android toolbox - collection of system utilities',
    'toybox': 'Modern Android toolbox replacement',
    'sh': 'Shell interpreter',
    'mksh': 'MirBSD Korn Shell - default Android shell',

    # Boot/Init
    'init': 'System init process - first user-space process, starts all services',
    'ueventd': 'Device node manager - creates /dev nodes for hardware',
    'bootstat': 'Boot time statistics collector',

    # Hardware
    'thermal': 'Thermal management daemon',
    'thermalmanager': 'Thermal policy manager',
    'healthd': 'Battery health daemon',
    'lmkd': 'Low Memory Killer daemon - kills processes when memory is low',

    # MTK-specific
    'atcid': 'MediaTek AT command interface daemon',
    'atci_service': 'MediaTek AT command service',
    'nvram_daemon': 'MediaTek NVRAM (calibration data) daemon',
    'mtk_agpsd': 'MediaTek GPS daemon',
    'mtkmal': 'MediaTek MAL (modem abstraction layer)',
    'gsm0710muxd': 'GSM multiplexer daemon for modem communication',

    # Network utilities
    'ping': 'ICMP ping utility',
    'ping6': 'IPv6 ping utility',
    'netstat': 'Network statistics',
    'ifconfig': 'Network interface configuration',
    'ip': 'Advanced network configuration tool',
    'iptables': 'Firewall configuration',
    'tc': 'Traffic control utility',

    # File system
    'make_ext4fs': 'Create ext4 filesystem',
    'e2fsck': 'ext2/3/4 filesystem check and repair',
    'resize2fs': 'Resize ext2/3/4 filesystem',
    'tune2fs': 'Tune ext2/3/4 filesystem parameters',

    # Bluetooth
    'btif': 'Bluetooth interface daemon',
    'bt_drv': 'Bluetooth driver interface',

    # DRM/Media
    'drmserver': 'Digital Rights Management server',
    'mediadrmserver': 'Media DRM server for protected content',
}

# Library categories and functions
LIBRARY_FUNCTIONS = {
    # Framework
    'libandroid_runtime.so': 'Android runtime - JNI bindings between Java framework and native code',
    'libandroid.so': 'NDK Android API implementation',
    'libbinder.so': 'Binder IPC library - inter-process communication',
    'libutils.so': 'Core utility library - strings, threads, memory management',
    'libcutils.so': 'C utility library - properties, logging, atomics',
    'liblog.so': 'Logging library - Android log functions',

    # Graphics
    'libsurfaceflinger.so': 'SurfaceFlinger compositor implementation',
    'libgui.so': 'Graphics UI library - Surface, BufferQueue',
    'libui.so': 'UI library - PixelFormat, Region, GraphicBuffer',
    'libEGL.so': 'EGL graphics interface',
    'libGLESv1_CM.so': 'OpenGL ES 1.x implementation',
    'libGLESv2.so': 'OpenGL ES 2.0 implementation',
    'libGLESv3.so': 'OpenGL ES 3.0 implementation',

    # Audio
    'libaudioflinger.so': 'AudioFlinger audio mixing server',
    'libaudioclient.so': 'Audio client library',
    'libaudioutils.so': 'Audio utility functions',
    'libaudioroute.so': 'Audio routing library',
    'libtinyalsa.so': 'Tiny ALSA library for audio hardware access',

    # Media
    'libstagefright.so': 'Media codec framework',
    'libmedia.so': 'Media framework library',
    'libcamera_client.so': 'Camera client library',
    'libcamera_metadata.so': 'Camera metadata handling',

    # Hardware
    'libhardware.so': 'Hardware abstraction layer loader',
    'libhardware_legacy.so': 'Legacy HAL compatibility',
    'libpower.so': 'Power management library',

    # Crypto/Security
    'libcrypto.so': 'OpenSSL cryptography library',
    'libssl.so': 'OpenSSL SSL/TLS library',
    'libkeystore_binder.so': 'Keystore binder interface',

    # C/C++ standard
    'libc.so': 'Bionic C standard library',
    'libm.so': 'Math library',
    'libstdc++.so': 'C++ standard library',
    'libc++.so': 'LLVM C++ standard library',

    # RIL/Telephony
    'libril.so': 'Radio Interface Layer library',
    'libreference-ril.so': 'Reference RIL implementation',

    # Sensors
    'libsensorservice.so': 'Sensor service implementation',
}

# HAL (Hardware Abstraction Layer) modules
HAL_FUNCTIONS = {
    'audio.primary': 'Primary audio HAL - implements audio hardware interface',
    'audio.a2dp': 'Bluetooth A2DP audio output HAL',
    'audio.usb': 'USB audio HAL',
    'audio.r_submix': 'Remote submix audio HAL for screen recording',

    'gralloc': 'Graphics memory allocator HAL',
    'hwcomposer': 'Hardware composer HAL for display optimization',
    'memtrack': 'Memory tracking HAL',

    'camera': 'Camera HAL',

    'sensors': 'Sensors HAL - accelerometer, gyroscope, etc.',

    'gps': 'GPS/GNSS location HAL',

    'lights': 'LED/backlight control HAL',
    'power': 'Power management HAL',
    'thermal': 'Thermal management HAL',

    'keystore': 'Hardware keystore HAL',
    'gatekeeper': 'Gatekeeper authentication HAL',

    'radio': 'Cellular radio HAL',
    'bluetooth': 'Bluetooth HAL',
    'wifi': 'WiFi HAL',
    'nfc': 'NFC HAL',
}

# Framework services (JAR files)
FRAMEWORK_SERVICES = {
    'framework.jar': 'Core Android framework - all Android APIs',
    'services.jar': 'System services implementation',
    'am.jar': 'Activity Manager service',
    'pm.jar': 'Package Manager service',
    'android.policy.jar': 'Policy manager (PhoneWindowManager)',
    'ext.jar': 'Framework extensions',
    'telephony-common.jar': 'Telephony framework',
    'ims-common.jar': 'IMS (VoLTE) framework',
    'wifi-service.jar': 'WiFi service implementation',
}

def annotate_binary(name):
    """Get function description for a binary"""
    return BINARY_FUNCTIONS.get(name, f'Unknown system binary: {name}')

def annotate_library(name):
    """Get function description for a library"""
    base = name.split('/')[-1]
    return LIBRARY_FUNCTIONS.get(base, f'Native library: {base}')

def annotate_hal(path):
    """Get function description for HAL module"""
    basename = path.split('/')[-1]
    # HAL naming: type.variant.so (e.g., audio.primary.mt8127.so)
    parts = basename.replace('.so', '').split('.')
    if len(parts) >= 2:
        hal_type = f"{parts[0]}.{parts[1]}"
        return HAL_FUNCTIONS.get(hal_type, f'HAL module: {hal_type}')
    return f'HAL module: {basename}'

def annotate_framework(name):
    """Get function description for framework JAR"""
    base = name.split('/')[-1]
    return FRAMEWORK_SERVICES.get(base, f'Framework component: {base}')

if __name__ == '__main__':
    print("Binary function database loaded")
    print(f"  {len(BINARY_FUNCTIONS)} binaries documented")
    print(f"  {len(LIBRARY_FUNCTIONS)} libraries documented")
    print(f"  {len(HAL_FUNCTIONS)} HAL modules documented")
    print(f"  {len(FRAMEWORK_SERVICES)} framework services documented")

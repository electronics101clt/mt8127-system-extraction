#!/usr/bin/env python3
"""
Apply XDA forum knowledge to improve explanations
Based on research from XDA forums and Android source documentation
"""

# Enhanced explanations based on XDA forums and AOSP documentation
XDA_ENHANCED = {
    # Core Android Services (from XDA and AOSP docs)
    'surfaceflinger': 'SurfaceFlinger compositor - accepts buffers from apps, composites them, and sends final frame to display via GPU EGL',
    'audioserver': 'Audio server - hosts audio I/O, policy manager for audio routing, and FM radio service',
    'mediaserver': 'Media playback/recording server - handles codecs for audio/video encoding and decoding',
    'cameraserver': 'Camera server - controls camera hardware and provides video frames for recording',
    'netd': 'Network daemon - manages network connections (WiFi, Bluetooth, USB), DNS, tethering, and firewall',
    'vold': 'Volume daemon - detects and mounts/unmounts external storage (SD cards, USB) and manages encryption',
    'installd': 'Install daemon - handles APK installation with root permissions, creates app directories, sets SELinux contexts',
    'servicemanager': 'Binder service manager - central registry for IPC, allows services to register and clients to discover them',
    'zygote': 'Zygote process - preloads Android framework and forks new app processes for fast launch',
    'zygote64': 'Zygote 64-bit - preloads framework and forks 64-bit app processes',

    # MTK-specific (from XDA MediaTek forums)
    'nvram_daemon': 'MTK NVRAM daemon - manages non-volatile RAM storing IMEI, WiFi/BT calibration, and device config',
    'nvram_agent_binder': 'MTK NVRAM agent - binder interface for NVRAM access',
    'mtk_agpsd': 'MTK Assisted GPS daemon - handles GPS/AGPS positioning services',
    'aee_aedv': 'MTK Android Exception Engine daemon - captures crash dumps and kernel panics for debugging',
    'aee_archive': 'MTK AEE archive manager - compresses and stores crash dumps',
    'aee_dumpstate': 'MTK AEE dump collector - gathers full system state on crashes',
    'thermal_manager': 'MTK thermal manager - monitors SoC temperature and throttles CPU/GPU to prevent overheating',
    'thermald': 'MTK thermal daemon - enforces thermal policies and cooling actions',
    'ccci_fsd': 'MTK CCCI filesystem daemon - manages modem-AP shared filesystem via Cross-Core Communication Interface',
    'ccci_rpcd': 'MTK CCCI RPC daemon - handles Remote Procedure Calls between modem and application processor',
    'gsm0710muxd': 'GSM 07.10 multiplexer - multiplexes AT commands to cellular modem over single serial interface',
    'mtk_md_ctrl': 'MTK modem control service - starts/stops modem and handles modem exceptions',
    'program_binary_service': 'MTK shader program service - manages compiled GPU shader binaries for faster loading',
    'pq': 'MTK Picture Quality daemon - controls display color enhancement, sharpness, and contrast',
    'aal': 'MTK Adaptive Ambient Light - auto-adjusts screen brightness based on content and ambient light',

    # HAL (Hardware Abstraction Layer) - from Android source docs
    'gralloc': 'Graphics allocator HAL - manages GPU memory buffers shared between display, GPU, and camera',
    'hwcomposer': 'Hardware composer HAL - uses hardware overlays to composite windows instead of GPU blending',
    'audio.primary': 'Primary audio HAL - implements audio input/output routing and mixing for built-in hardware',
    'audio.a2dp': 'Bluetooth A2DP audio HAL - routes audio to Bluetooth headphones/speakers',
    'audio.usb': 'USB audio HAL - supports USB audio devices (headphones, DACs, microphones)',
    'audio.r_submix': 'Remote submix HAL - captures audio for screen recording',
    'camera': 'Camera HAL - provides interface to camera sensors, ISP, and image processing pipeline',
    'sensors': 'Sensors HAL - abstracts accelerometer, gyroscope, magnetometer, and other sensors',
    'gps': 'GPS HAL - interfaces with GPS/GNSS receiver for location services',
    'lights': 'Lights HAL - controls LED indicators, backlight brightness, and notification LEDs',
    'power': 'Power HAL - manages CPU frequency scaling, deep sleep states, and power hints from framework',
    'thermal': 'Thermal HAL - monitors temperature sensors and reports thermal status to framework',
    'keystore': 'Keystore HAL - provides hardware-backed cryptographic key storage',
    'gatekeeper': 'Gatekeeper HAL - hardware-backed password verification for lockscreen',
    'memtrack': 'Memory tracking HAL - reports GPU and other hardware memory usage for debugging',

    # System services
    'init': 'Init process - first userspace process, parses init.rc scripts, starts daemons and Zygote',
    'ueventd': 'UEvent daemon - creates /dev device nodes when kernel reports hardware events',
    'adbd': 'Android Debug Bridge daemon - enables USB/TCP debugging, file transfer, and shell access',
    'logd': 'Log daemon - central logging service, receives logs from kernel and apps',
    'lmkd': 'Low Memory Killer daemon - kills background processes when RAM is critically low',
    'healthd': 'Health daemon - monitors battery status, charging state, and reports to framework',
    'rild': 'Radio Interface Layer daemon - communicates with cellular modem for calls/SMS/data',
    'wpa_supplicant': 'WiFi supplicant - handles WiFi authentication (WPA/WPA2/WPA3) and connection management',
    'debuggerd': 'Debug daemon - catches app crashes, generates tombstones with stack traces',
    'drmserver': 'DRM server - manages Digital Rights Management for protected media content',

    # Framework libraries
    'libbinder.so': 'Binder IPC library - implements inter-process communication used by all Android services',
    'libandroid_runtime.so': 'Android runtime - JNI bridge between Java framework and native code',
    'libsurfaceflinger.so': 'SurfaceFlinger library - core compositor implementation',
    'libaudioflinger.so': 'AudioFlinger library - audio mixing and routing engine',
    'libstagefright.so': 'Stagefright library - media codec framework for encoding/decoding audio/video',
    'libcamera_client.so': 'Camera client library - app-facing camera API implementation',
    'libgui.so': 'Graphics UI library - Surface, BufferQueue, and window management',
    'libui.so': 'UI library - GraphicBuffer, PixelFormat, and low-level UI primitives',
    'libEGL.so': 'EGL library - interface between OpenGL ES and native windowing system',
    'libGLESv2.so': 'OpenGL ES 2.0 library - GPU-accelerated 3D graphics API',
    'libGLESv3.so': 'OpenGL ES 3.0 library - enhanced GPU graphics with geometry shaders and compute',
}

# Improve existing explanations
def enhance_explanation(path, current_explanation):
    """Enhance explanation with XDA/AOSP knowledge"""

    basename = path.split('/')[-1]

    # Check if we have XDA-sourced enhancement
    if basename in XDA_ENHANCED:
        return XDA_ENHANCED[basename]

    # HAL modules
    if basename.endswith('.so') and '/hw/' in path:
        # Parse HAL name (e.g., audio.primary.mt8127.so)
        parts = basename.replace('.so', '').split('.')
        if len(parts) >= 2:
            hal_base = f"{parts[0]}.{parts[1]}"
            if hal_base in XDA_ENHANCED:
                return XDA_ENHANCED[hal_base]

    # Library enhancements
    if basename in XDA_ENHANCED:
        return XDA_ENHANCED[basename]

    return current_explanation

print("Loading annotations...")
with open('device-tree-annotated.txt', 'r') as f:
    lines = f.readlines()

output = []
improved = 0

print("Applying XDA-sourced improvements...")
for i, line in enumerate(lines):
    if i % 50000 == 0:
        print(f"  {i}/{len(lines)}")

    if ' | ' in line:
        path, explanation = line.strip().split(' | ', 1)
        new_exp = enhance_explanation(path, explanation)
        if new_exp != explanation:
            improved += 1
            output.append(f"{path} | {new_exp}\n")
        else:
            output.append(line)
    else:
        output.append(line)

print(f"\nWriting enhanced file...")
with open('device-tree-annotated.txt', 'w') as f:
    f.writelines(output)

print(f"Done! Improved {improved} explanations with XDA/AOSP knowledge")

#!/usr/bin/env python3
"""
MTK Vendor Component Knowledge Database
Documents MediaTek and Autochips vendor-specific components
"""

# MediaTek vendor binaries
MTK_VENDOR_BINARIES = {
    # AEE (Android Exception Engine) - MTK crash/debug system
    'aee_aedv': 'MTK Android Exception Engine daemon - crash handler and debug logger',
    'aee_archivev': 'MTK AEE archive manager - manages crash dumps',
    'aee_dumpstatev': 'MTK AEE dump state collector - collects system state on crashes',
    'aeev': 'MTK AEE main service',

    # NVRAM - MTK non-volatile RAM manager for calibration data
    'nvram_daemon': 'MTK NVRAM daemon - manages calibration data (WiFi, BT, IMEI, etc.)',
    'nvram_backup_binder': 'MTK NVRAM backup service',

    # GPS/Location
    'mtk_agpsd': 'MTK Assisted GPS daemon - GPS/GNSS location service',
    'mtk_gnss_agent': 'MTK GNSS agent',
    'flp_mtk': 'MTK Fused Location Provider',

    # Modem/Radio
    'mtkmal': 'MTK MAL (Modem Abstraction Layer) - modem communication',
    'gsm0710muxd': 'GSM 07.10 multiplexer daemon - multiplexes AT commands to modem',
    'mtk_md_ctrl': 'MTK modem control service',
    'ccci_fsd': 'MTK CCCI (Cross Core Communication Interface) file system daemon',
    'ccci_rpcd': 'MTK CCCI RPC daemon',

    # Thermal management
    'thermal_manager': 'MTK thermal management daemon',
    'thermald': 'MTK thermal daemon',
    'thermal': 'MTK thermal policy service',

    # Display/Graphics
    'program_binary_service': 'MTK shader binary program service',
    'pq': 'MTK Picture Quality daemon - display enhancement',
    'aal': 'MTK Adaptive Ambient Light service - auto brightness',

    # Camera
    'camerahalserver': 'MTK camera HAL server',
    'camhal3lite': 'MTK camera HAL 3 lite implementation',
    'camera3_capture': 'MTK camera capture service',
    'cam_isp_mgr': 'MTK camera ISP manager',

    # Audio
    'audio_param_service': 'MTK audio parameter service',
    'audio_control_service': 'MTK audio control service',

    # Power/Battery
    'batterywarning': 'MTK battery warning service',
    'meta_tst': 'MTK META test mode service',
    'thermal_log': 'MTK thermal logging service',

    # HIDL HAL servers (Hardware Interface Definition Language)
    'android.hardware.audio@2.0-service-mediatek': 'MTK audio HAL 2.0 HIDL service',
    'android.hardware.bluetooth@1.0-service-mediatek': 'MTK Bluetooth HAL HIDL service',
    'android.hardware.broadcastradio@1.1-service': 'Broadcast Radio HAL service',
    'android.hardware.camera.provider@2.4-service-mediatek': 'MTK camera HAL service',
    'android.hardware.configstore@1.0-service': 'Config store HAL service',
    'android.hardware.drm@1.0-service': 'DRM HAL service',
    'android.hardware.drm@1.0-service.widevine': 'Widevine DRM service',
    'android.hardware.gatekeeper@1.0-service': 'Gatekeeper authentication HAL',
    'android.hardware.graphics.allocator@2.0-service': 'Graphics allocator HAL',
    'android.hardware.graphics.composer@2.1-service': 'Hardware composer HAL',
    'android.hardware.keymaster@3.0-service': 'Keymaster crypto HAL',
    'android.hardware.light@2.0-service-mediatek': 'MTK LED/backlight control HAL',
    'android.hardware.media.omx@1.0-service': 'OpenMAX media codec HAL',
    'android.hardware.memtrack@1.0-service': 'Memory tracking HAL',
    'android.hardware.wifi@1.0-service': 'WiFi HAL service',

    # Autochips specific
    'autobt': 'Autochips Bluetooth service',
    'chg_mcu_val': 'Change MCU value - head unit MCU communication',
    'dongled': 'Dongle daemon - USB dongle management',

    # Vendor HAL services
    'vendor.autochips.hardware.audio@1.0-service': 'Autochips audio HAL service',
    'vendor.autochips.hardware.backcar@1.0-service': 'Autochips backup camera HAL service',
    'vendor.autochips.hardware.dvr@1.0-service': 'Autochips DVR (dash cam) HAL service',
    'vendor.autochips.hardware.metalogo@1.0-service': 'Autochips boot logo HAL service',
    'vendor.autochips.hardware.usb@1.1-service': 'Autochips USB HAL service',
}

# MTK/Vendor HAL implementations
MTK_HAL_MODULES = {
    # Audio HAL
    'audio.primary.ac8227l.so': 'Primary audio HAL for AC8227L platform - main audio routing/mixing',
    'audio.r_submix.ac8227l.so': 'Remote submix audio HAL - for screen recording audio',
    'audio.usb.ac8227l.so': 'USB audio HAL - USB audio device support',
    'audio_policy.stub.so': 'Audio policy HAL stub',

    # MTK audio HIDL
    'android.hardware.audio@2.0-impl-mediatek.so': 'MTK audio HAL 2.0 HIDL implementation',
    'android.hardware.audio.effect@2.0-impl.so': 'Audio effects HAL implementation',

    # Graphics HAL
    'gralloc.ac8227l.so': 'Graphics memory allocator HAL - GPU memory management',
    'hwcomposer.ac8227l.so': 'Hardware composer HAL - display composition optimization',
    'android.hardware.graphics.allocator@2.0-impl.so': 'Graphics allocator HIDL',
    'android.hardware.graphics.composer@2.1-impl.so': 'Hardware composer HIDL',
    'android.hardware.graphics.mapper@2.0-impl.so': 'Graphics mapper HIDL',

    # Camera HAL
    'android.hardware.camera.provider@2.4-impl-mediatek.so': 'MTK camera HAL provider',
    'vendor.mediatek.hardware.camera.ccap@1.0-impl.so': 'MTK camera capture HAL',

    # GPS HAL
    'gps.ac8227l.so': 'GPS/GNSS HAL for AC8227L',
    'flp.ac8227l.so': 'Fused Location Provider HAL',
    'vendor.mediatek.hardware.gnss@1.1-impl.so': 'MTK GNSS HAL implementation',

    # Bluetooth HAL
    'android.hardware.bluetooth@1.0-impl-mediatek.so': 'MTK Bluetooth HAL implementation',

    # Power/Thermal HAL
    'power.ac8227l.so': 'Power management HAL',
    'thermal.ac8227l.so': 'Thermal management HAL',
    'vendor.mediatek.hardware.power@1.1-impl.so': 'MTK power HAL',

    # Security HAL
    'gatekeeper.ac8227l.so': 'Gatekeeper authentication HAL',
    'keystore.ac8227l.so': 'Hardware keystore HAL',
    'android.hardware.keymaster@3.0-impl.so': 'Keymaster crypto HAL',
    'vendor.mediatek.hardware.keymaster_attestation@1.0-impl.so': 'MTK key attestation',
    'vendor.mediatek.hardware.keymanage@1.0-impl.so': 'MTK key management',

    # Memory
    'memtrack.ac8227l.so': 'Memory tracking HAL - GPU/graphics memory usage',
    'android.hardware.memtrack@1.0-impl.so': 'Memory tracking HIDL',

    # Sensors (if present)
    'sensors.ac8227l.so': 'Sensors HAL - accelerometer, gyroscope, etc.',

    # Lights/LED
    'lights.ac8227l.so': 'LED and backlight control HAL',
    'android.hardware.light@2.0-impl-mediatek.so': 'MTK light HAL',

    # Media codec
    'vendor.mediatek.hardware.mtkcodecservice@1.1-impl.so': 'MTK hardware codec service',

    # NVRAM
    'vendor.mediatek.hardware.nvram@1.0-impl.so': 'MTK NVRAM HAL',

    # DRM
    'android.hardware.drm@1.0-impl.so': 'DRM HAL implementation',

    # Autochips custom HAL
    'vendor.autochips.hardware.audio.audhw_auxin@1.0-impl.so': 'Autochips AUX input audio HAL',
    'vendor.autochips.hardware.audio.audhw_effect@1.0-impl.so': 'Autochips audio effects HAL',
    'vendor.autochips.hardware.backcar@1.0-impl.so': 'Autochips backup camera HAL',
    'vendor.autochips.hardware.metalogo@1.0-impl.so': 'Autochips boot logo HAL',

    # Misc
    'vibrator.default.so': 'Vibrator HAL (likely stub for head unit)',
    'local_time.default.so': 'Local time HAL',
}

# MTK vendor libraries (important ones)
MTK_VENDOR_LIBS = {
    # Camera
    'libcam.camadapter.so': 'MTK camera adapter library',
    'libcam_utils.so': 'MTK camera utilities',
    'libcameracustom.so': 'MTK camera customization library',
    'libcam.camshot.so': 'MTK camera shot library',

    # Audio
    'libaudiocompensationfilter.so': 'MTK audio compensation filter',
    'libaudiocomponentengine.so': 'MTK audio component engine',
    'libaudiocustparam.so': 'MTK audio custom parameters',
    'libaudiomtkdcremoval.so': 'MTK audio DC removal',
    'libaudiosetting.so': 'MTK audio settings library',

    # Graphics
    'libgralloc_extra.so': 'MTK gralloc extensions',
    'libgui_ext.so': 'MTK GUI extensions',
    'libpq_cust.so': 'MTK picture quality customization',
    'libpq_prot.so': 'MTK picture quality protection',

    # Media
    'libmtkjpeg.so': 'MTK JPEG codec',
    'libmtk_mmutils.so': 'MTK multimedia utilities',

    # NVRAM
    'libnvram.so': 'MTK NVRAM library',
    'libnvram_daemon_callback.so': 'MTK NVRAM daemon callback',
    'libcustom_nvram.so': 'MTK custom NVRAM',

    # Misc MTK
    'libmtkcam_fwkutils.so': 'MTK camera framework utilities',
    'libmtk_drvb.so': 'MTK driver bridge',
    'libcam.client.so': 'MTK camera client',
}

# Vendor Apps
VENDOR_APPS = {
    'MTKLoggerProxy.apk': 'MTK Logger Proxy - debugging and log collection',
    'Gallery2Gif.apk': 'Gallery GIF support extension',
    'Gallery2Pq.apk': 'Gallery picture quality enhancement',
    'Gallery2PqTool.apk': 'Gallery PQ tuning tool',
    'Gallery2Raw.apk': 'Gallery RAW image support',
    'Gallery2Root.apk': 'Main Gallery app with MTK extensions',
    'Calculator.apk': 'Calculator app',
    'CanBus.apk': 'CAN bus integration app for vehicle data',
    'GalaRadio.apk': 'Radio application',
    'PveNaviGuide.apk': 'Navigation guide/interface',
    'zlink_wireless.apk': 'ZLink wireless phone mirroring',
    'netflix.apk': 'Netflix streaming app',
    'Chrome.apk': 'Google Chrome browser',
    'spotify.apk': 'Spotify music streaming',
    'waze.apk': 'Waze navigation',
    'herego.apk': 'HereGo navigation',
}

def get_vendor_binary_function(name):
    """Get function description for vendor binary"""
    return MTK_VENDOR_BINARIES.get(name, f'Vendor binary: {name}')

def get_vendor_hal_function(name):
    """Get function description for vendor HAL"""
    return MTK_HAL_MODULES.get(name, f'Vendor HAL module: {name}')

def get_vendor_lib_function(name):
    """Get function description for vendor library"""
    return MTK_VENDOR_LIBS.get(name, f'Vendor library: {name}')

def get_vendor_app_function(name):
    """Get function description for vendor app"""
    app_name = name.replace('.apk', '')
    return VENDOR_APPS.get(name, f'Vendor application: {app_name}')

if __name__ == '__main__':
    print("MTK/Vendor Knowledge Database")
    print(f"  Vendor binaries: {len(MTK_VENDOR_BINARIES)}")
    print(f"  Vendor HAL modules: {len(MTK_HAL_MODULES)}")
    print(f"  Vendor libraries: {len(MTK_VENDOR_LIBS)}")
    print(f"  Vendor apps: {len(VENDOR_APPS)}")

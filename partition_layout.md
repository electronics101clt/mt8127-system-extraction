# MT3367 EMMC Partition Layout

Based on scatter file: `MT3367_Android_scatter - DRAM fixed.txt`

## Boot Region

| Index | Name | Start Address | Size | Type | Region | File |
|-------|------|---------------|------|------|--------|------|
| SYS0 | preloader | 0x0 | 0x40000 (256 KB) | SV5_BL_BIN | EMMC_BOOT_1 | preloader_8227l_demo.bin |

## User Region Partitions

| Index | Name | Start Address | Size | Type | File | Notes |
|-------|------|---------------|------|------|------|-------|
| SYS1 | pgpt | 0x0 | 0x80000 (512 KB) | NORMAL_ROM | NONE | Primary GPT |
| SYS2 | PRO_INFO | 0x80000 | 0x300000 (3 MB) | NORMAL_ROM | NONE | Protected Info |
| SYS3 | NVRAM | 0x380000 | 0x500000 (5 MB) | NORMAL_ROM | NONE | Non-Volatile RAM |
| SYS4 | PROTECT_F | 0x880000 | 0xA00000 (10 MB) | EXT4_IMG | NONE | Protected F |
| SYS5 | PROTECT_S | 0x1280000 | 0xA00000 (10 MB) | NORMAL_ROM | NONE | Protected S |
| SYS6 | SECCFG | 0x1C80000 | 0x20000 (128 KB) | NORMAL_ROM | NONE | Security Config |
| SYS7 | LK | 0x1CA0000 | 0x60000 (384 KB) | NORMAL_ROM | lk.bin | Little Kernel Bootloader |
| SYS8 | TEE1 | 0x1D00000 | 0x500000 (5 MB) | NORMAL_ROM | trustzone1.bin | Trusted Execution Environment 1 |
| SYS9 | TEE2 | 0x2200000 | 0x500000 (5 MB) | NORMAL_ROM | trustzone2.bin | Trusted Execution Environment 2 |
| SYS10 | ARM2 | 0x2700000 | 0x400000 (4 MB) | NORMAL_ROM | arm2.bin | ARM Cortex-M4 Firmware |
| SYS11 | **BOOTIMG** | 0x2B00000 | 0x1000000 (16 MB) | NORMAL_ROM | boot.img | **Boot Image (kernel + ramdisk)** |
| SYS12 | **RECOVERY** | 0x3B00000 | 0x1000000 (16 MB) | NORMAL_ROM | recovery.img | **Recovery Image** |
| SYS13 | SEC_RO | 0x4B00000 | 0x600000 (6 MB) | NORMAL_ROM | secro.img | Secure Read-Only |
| SYS14 | MISC | 0x5100000 | 0x80000 (512 KB) | NORMAL_ROM | NONE | Miscellaneous |
| SYS15 | LOGO | 0x5180000 | 0x300000 (3 MB) | NORMAL_ROM | logo.bin | Boot Logo |
| SYS16 | METAZONE | 0x5480000 | 0x100000 (1 MB) | NORMAL_ROM | metazone.bin | Meta Mode Zone |
| SYS17 | ODMDTBO | 0x5580000 | 0x80000 (512 KB) | NORMAL_ROM | odmdtbo.img | ODM Device Tree Blob Overlay |
| SYS18 | **VENDOR** | 0x5600000 | 0x20000000 (512 MB) | EXT4_IMG | vendor.img | **Vendor Partition** |
| SYS19 | EXPDB | 0x25600000 | 0xA00000 (10 MB) | NORMAL_ROM | NONE | Exception Database |
| SYS20 | KB | 0x26000000 | 0x100000 (1 MB) | NORMAL_ROM | NONE | Keybox |
| SYS21 | DKB | 0x26100000 | 0x100000 (1 MB) | NORMAL_ROM | NONE | Device Keybox |
| SYS22 | FRP | 0x26200000 | 0x100000 (1 MB) | NORMAL_ROM | NONE | Factory Reset Protection |
| SYS23 | **ANDROID (system)** | **0x26300000** | **0xC0000000 (3 GB)** | **EXT4_IMG** | **system.img** | **Main System Partition** |
| SYS24 | **CACHE** | 0xE6300000 | 0x10000000 (256 MB) | EXT4_IMG | cache.img | **Cache Partition** |
| SYS25 | **userdata** | 0xF6300000 | 0xC0000000 (3 GB) | EXT4_IMG | userdata.img | **User Data Partition** |
| SYS26 | sgpt | 0xFFFF0004 | 0x80000 (512 KB) | NORMAL_ROM | NONE | Secondary GPT |

## Key Partitions for System Extraction

### ANDROID (System) - SYS23
- **Address:** 0x26300000 (638 MB offset)
- **Size:** 3 GB (3,072 MB)
- **Contains:** Android OS, system apps, frameworks, SystemUI
- **Target File:** MtkSystemUI.apk at `/system/priv-app/MtkSystemUI/MtkSystemUI.apk`

### Block Device Mapping - VERIFIED ✅

**IMPORTANT:** Scatter file partition order does NOT match actual block device numbers!

Actual device mapping (verified via `adb shell mount`):
```
/dev/block/mmcblk0p22 -> ANDROID (system) ✅ VERIFIED
/dev/block/mmcblk0p23 -> Unknown (NOT system as scatter suggests)
/dev/block/mmcblk0p24 -> Unknown
```

**System partition confirmed at mmcblk0p22:**
```bash
adb shell "mount | grep system"
# /dev/block/mmcblk0p22 on /system type ext4 (ro,seclabel,relatime,data=ordered)

adb shell "su 0 blockdev --getsize64 /dev/block/mmcblk0p22"
# 3221225472 bytes (3 GB exactly, matching scatter file size)
```

This discrepancy is common in MediaTek OEM/custom builds where the scatter file represents the firmware structure, but the actual GPT partition table may be reordered.

## Total Layout Summary

- **Preloader:** 256 KB (EMMC_BOOT_1 region)
- **User Partitions:** ~6.8 GB total
  - System: 3 GB
  - Userdata: 3 GB
  - Vendor: 512 MB
  - Cache: 256 MB
  - Other: ~32 MB

## Extraction Methods

### Via ADB (Recommended)
```bash
# Pull entire system directory
adb pull /system /path/to/backup/

# Or raw partition dump
adb shell su -c "dd if=/dev/block/mmcblk0p23 bs=4M" > system_partition.img
```

### Via mtkclient (Not Working - USB Overflow)
```bash
python3 mtk.py r system system.img
```

### Via SP Flash Tool (Requires working V5 or XML scatter)
Use Readback mode to extract partition by address range.

# MT8127/MT3367 System Partition Extraction Workflow

## Device Information

**Device Model:** 9210B (Android Car Head Unit)
**Chipset:** MediaTek MT8127/MT3367/AC8227L
**Platform:** alps/full_8227L_demo/8227L_demo
**Android Version:** 10.0 (Build: O11019/1735544622)
**Flash Type:** EMMC
**HW Code:** 0x8127
**HW Subcode:** 0x8a00
**HW Version:** 0xca04

## Objective

Extract the SystemUI APK and system partition from a MediaTek MT8127-based Android car head unit for analysis and modification.

## Initial Discovery

### SystemUI Location via ADB

```bash
adb shell pm path com.android.systemui
# Output: package:/system/priv-app/MtkSystemUI/MtkSystemUI.apk

adb pull /system/priv-app/MtkSystemUI/MtkSystemUI.apk
# Successfully extracted 11MB APK
```

**SystemUI Details:**
- Package: `com.android.systemui`
- Version: 9520.10100.0000 (versionCode: 27)
- Target SDK: Android 8.1 (API 27)
- Type: MediaTek customized SystemUI for automotive

### Flash Partition Layout

Using scatter file `MT3367_Android_scatter - DRAM fixed.txt`, the ANDROID (system) partition is located at:

- **Physical Start Address:** 0x26300000 (638 MB offset)
- **Partition Size:** 0xC0000000 (3 GB / 3,072 MB)
- **Type:** EXT4_IMG
- **Region:** EMMC_USER

SystemUI resides within this 3GB system partition.

## Attempted Extraction Methods

### Method 1: SP Flash Tool V6.2228 (Linux) - FAILED ❌

**Issue:** SP Flash Tool V6 requires XML-format scatter files (`flash.xml`) for newer firmware, but our scatter file is in TXT format.

**Error Message:**
```
/home/jonathan/Desktop/MT3367_Android_scatter - DRAM fixed.txt is invalid.
Please select the ./download_agent/flash.xml in the load.
```

**Why it failed:**
- SP Flash Tool V6 is designed for XML-based scatter firmware
- V6 can allegedly accept TXT scatter files, but rejected ours
- SP Flash Tool V5 (which natively supports TXT scatter) download links are dead/broken

**Attempted Downloads:**
- spflashtool.com - 404 errors
- SourceForge - 404 errors
- androidmtk.com - redirects to homepage
- Google Drive links - 404 errors

### Method 2: mtkclient V2.1.4 - FAILED ❌

**GitHub:** https://github.com/bkerler/mtkclient

mtkclient successfully detected the device in preloader mode and uploaded stages 1 & 2, but failed at DA (Download Agent) upload phase.

**Connection Success:**
```
Port - Device detected :)
Preloader - Detected regular mode!
Preloader - CPU: MT8127/MT3367/AC8227L()
Preloader - HW code: 0x8127
DaHandler - Device is unprotected.
DALegacy - Uploading legacy stage 1 from MTK_DA_V5.bin
Preloader - Jumping to 0x200000: ok.
DALegacy - Got loader sync!
DALegacy - Reading emmc info
DALegacy - Successfully uploaded stage 2
```

**Critical Error:**
```
DeviceClass - [LIB]: USB Overflow
DaHandler - [LIB]: Failed to upload da.
```

**Why it failed:**

This is a **known unfixed bug** with MT8127 chipsets:
- [GitHub Issue #1321](https://github.com/bkerler/mtkclient/issues/1321) - MT8127 ZTE TV Box USB Overflow (closed as "not planned")
- [GitHub Issue #1384](https://github.com/bkerler/mtkclient/issues/1384) - Acer A3 A20 (MT8127) same error

The USB Overflow occurs during DA upload after successfully uploading both stages. This appears to be a USB buffer communication issue specific to MT8127 chipsets that has not been resolved in mtkclient.

**Attempted Flags:**
- `--crash` - Crash preloader to BROM mode
- `--skipwdt` - Skip watchdog timer disable

Both flags allowed successful connection and stage upload but still failed at DA upload phase.

## Device Connection Details

### Preloader/BROM Mode Access

**Challenge:** The MediaTek USB device appears **very briefly** during boot - only shows for ~2 seconds in preloader mode.

**Solution:** Start mtkclient FIRST, then power on device:
1. Run `python3 mtk.py printgpt` (waits for connection)
2. Power off tablet completely
3. Connect USB while device is off
4. Power on tablet
5. mtkclient catches the brief preloader connection window

**USB Device Detection:**
```
Bus 001 Device 021: ID 0e8d:2000 MediaTek Inc. MT65xx Preloader
```

### Device Security Status

```
SBC enabled:     False
SLA enabled:     False
DAA enabled:     False
Root cert required: False
Mem read auth:   False
Mem write auth:  False
```

**Device is unprotected** - full read/write access should be possible (if not for the USB Overflow bug).

## Working Solution: ADB Direct Access ✅

Since the device boots normally and is already rooted/accessible via ADB, we can extract the system partition directly.

### Actual Partition Discovery

**IMPORTANT:** The scatter file indicated system should be at `mmcblk0p23`, but the actual mounted partition is different:

```bash
adb shell "mount | grep system"
# Output: /dev/block/mmcblk0p22 on /system type ext4 (ro,seclabel,relatime,data=ordered)

adb shell "su 0 blockdev --getsize64 /dev/block/mmcblk0p22"
# Output: 3221225472 (3 GB exactly)
```

**The system partition is actually `/dev/block/mmcblk0p22`, not p23 as the scatter file suggests.**

This discrepancy between scatter file and actual partition mapping is common in MediaTek devices, especially custom/OEM builds.

### Option A: Raw Partition Dump via DD (RECOMMENDED) ✅

```bash
# Extract system partition (3 GB, takes 5-15 minutes)
cd ~/mt8127-system-extraction
adb shell "su 0 dd if=/dev/block/mmcblk0p22 bs=4M" | pv -s 3221225472 > system_partition.img

# Verify extraction
file system_partition.img
# Should show: Linux rev 1.0 ext4 filesystem data
```

**This method successfully extracted the complete system partition as a raw ext4 image.**

### Option B: Pull System Directory
```bash
adb pull /system /path/to/backup/system/
```

This pulls individual files but loses partition metadata and permissions.

### Writing System Partition Back

After modifying the system image, write it back:

```bash
# Method 1: Direct pipe (faster, recommended)
cat system_partition.img | adb shell "su 0 dd of=/dev/block/mmcblk0p22 bs=4M"

# Method 2: Push then write (safer for verification)
adb push system_partition.img /sdcard/system_partition.img
adb shell "su 0 dd if=/sdcard/system_partition.img of=/dev/block/mmcblk0p22 bs=4M"
adb shell "rm /sdcard/system_partition.img"
```

**CRITICAL:** System partition must be unmounted before writing:
```bash
adb shell "su 0 umount /system"
# Or boot to recovery mode
```

Use the provided script for safer write operations:
```bash
./scripts/write_system_dd.sh system_partition.img
```

## Files in This Repository

- `MT3367_Android_scatter.txt` - Full scatter file with partition layout
- `device_info.txt` - Complete device hardware/software information
- `mtkclient_output.log` - Full mtkclient connection log showing USB Overflow error
- `partition_layout.md` - Detailed EMMC partition map
- `scripts/` - Extraction scripts and tools

## Lessons Learned

1. **SP Flash Tool versioning matters:** V5 vs V6 use incompatible scatter formats. V5 downloads are largely unavailable as of 2026.

2. **mtkclient MT8127 bug is unfixed:** USB Overflow error during DA upload is a known issue with no planned fix.

3. **Preloader timing is critical:** MTK devices show USB briefly (~2s). Start tools first, then connect device.

4. **ADB is simpler when available:** If device boots normally with ADB access, direct file pull or dd is faster than flash tool extraction.

5. **Scatter files are essential:** They map the entire EMMC layout and are required for any flash tool operation.

## References

- [How to force a Mediatek device into BROM mode - Hovatek](https://www.hovatek.com/blog/how-to-force-a-mediatek-device-into-brom-mode/)
- [How to Boot any MediaTek Device to BROM Mode - DroidWin](https://droidwin.com/how-to-boot-any-mediatek-device-to-brom-mode/)
- [mtkclient GitHub Repository](https://github.com/bkerler/mtkclient)
- [SP Flash Tool for Linux (all versions)](https://spflashtools.com/category/linux/)
- [MediaTek SP Flash Tool Latest Version v5.1952 - XDA](https://xdaforums.com/t/mediatek-sp-flash-tool-latest-version-v5-1952-android-flash-tool.4083029/)

## System Requirements

- Linux (tested on Ubuntu 24.04.3 LTS)
- Python 3.12+ (for mtkclient)
- ADB tools
- USB 2.0 port recommended (USB 3.0 may cause timing issues)

## License

MIT License - Documentation and scripts for educational purposes.

## Contributing

If you have successfully extracted from MT8127 devices using different methods, please open an issue or PR with your findings.

---

**Status:** Workflow documented, ADB extraction method recommended for this device.
**Last Updated:** 2026-06-20

# Complete MT8127 System Extraction Workflow

This document captures the complete workflow from initial device discovery through successful extraction.

## Timeline and Method Progression

### Stage 1: Device Discovery and Initial Analysis

**Goal:** Locate SystemUI APK and determine flash layout

**Actions:**
1. Connected device via ADB
2. Located SystemUI package path
3. Extracted SystemUI APK for analysis
4. Obtained scatter file for partition layout

**Results:**
- SystemUI found at `/system/priv-app/MtkSystemUI/MtkSystemUI.apk`
- 11 MB MediaTek-customized SystemUI (version 9520.10100.0000)
- Scatter file shows system partition at physical address 0x26300000 (3 GB size)

**Commands:**
```bash
adb shell pm path com.android.systemui
adb pull /system/priv-app/MtkSystemUI/MtkSystemUI.apk
```

---

### Stage 2: SP Flash Tool V6 Attempt - FAILED

**Goal:** Use SP Flash Tool to read system partition from flash

**Actions:**
1. Attempted to load scatter file in SP Flash Tool V6.2228 (Linux)
2. Tool rejected TXT-format scatter file
3. Attempted to download SP Flash Tool V5 (native TXT support)

**Failure Points:**
- SP Flash Tool V6 expects XML-format scatter files (`flash.xml`)
- Our scatter file is TXT format (`MT3367_Android_scatter.txt`)
- SP Flash Tool V5 download links are dead/broken (2026):
  - spflashtool.com: 404
  - SourceForge: 404
  - androidmtk.com: redirects
  - Google Drive: 404

**Error Message:**
```
/home/jonathan/Desktop/MT3367_Android_scatter - DRAM fixed.txt is invalid.
Please select the ./download_agent/flash.xml in the load.
```

**Conclusion:** SP Flash Tool V6 incompatible, V5 unavailable.

---

### Stage 3: mtkclient Attempt - FAILED

**Goal:** Use mtkclient to extract system partition via preloader/BROM mode

**Actions:**
1. Installed mtkclient V2.1.4
2. Started mtkclient in wait mode
3. Powered on device to catch brief preloader connection (~2 seconds)
4. Successfully connected and uploaded DA stages

**Partial Success:**
```
Port - Device detected :)
Preloader - Detected regular mode!
Preloader - CPU: MT8127/MT3367/AC8227L()
Preloader - HW code: 0x8127
DaHandler - Device is unprotected.
DALegacy - Uploading legacy stage 1 from MTK_DA_V5.bin
Preloader - Jumping to 0x200000: ok.
DALegacy - Got loader sync!
DALegacy - Successfully uploaded stage 2
```

**Critical Failure:**
```
DeviceClass - [LIB]: USB Overflow
DaHandler - [LIB]: Failed to upload da.
```

**Root Cause:**
This is a **known unfixed bug** with MT8127 chipsets in mtkclient:
- [GitHub Issue #1321](https://github.com/bkerler/mtkclient/issues/1321) - MT8127 ZTE TV Box
- [GitHub Issue #1384](https://github.com/bkerler/mtkclient/issues/1384) - Acer A3 A20 tablet
- Both marked "not planned" for fix

The USB Overflow occurs during DA upload after successfully uploading both stages. This is a USB buffer communication issue specific to MT8127.

**Attempted Workarounds:**
- `--crash` flag: Crash preloader to BROM mode - same error
- `--skipwdt` flag: Skip watchdog timer - same error
- Different USB ports: No change
- USB 2.0 vs 3.0: No change

**Conclusion:** mtkclient cannot extract from MT8127 due to unfixed USB Overflow bug.

---

### Stage 4: ADB DD Extraction - SUCCESS ✅

**Goal:** Extract system partition via ADB using dd command

**Actions:**
1. Verified device boots normally with ADB access
2. Confirmed root access available
3. Located actual system partition mount point
4. Determined partition size
5. Extracted raw partition image using dd

**Key Discovery:**

The scatter file indicated system at partition index 23, but actual mount showed:
```bash
adb shell "mount | grep system"
# /dev/block/mmcblk0p22 on /system type ext4 (ro,seclabel,relatime,data=ordered)
```

**System is on mmcblk0p22, NOT mmcblk0p23!**

This discrepancy between scatter file and actual GPT is common in MediaTek OEM builds.

**Partition Size Verification:**
```bash
adb shell "su 0 blockdev --getsize64 /dev/block/mmcblk0p22"
# 3221225472 bytes (3 GB exactly, matching scatter file)
```

**Successful Extraction Command:**
```bash
adb shell "su 0 dd if=/dev/block/mmcblk0p22 bs=4M" | pv -s 3221225472 > system_partition.img
```

**Results:**
- 3 GB ext4 filesystem image extracted
- Extraction time: ~5-15 minutes (depends on USB speed)
- Verified as valid ext4 filesystem: `file system_partition.img`

---

## Final Solution Summary

### What Worked ✅

**Method:** ADB DD extraction
- **Partition:** `/dev/block/mmcblk0p22`
- **Size:** 3,221,225,472 bytes (3 GB)
- **Format:** ext4 filesystem
- **Command:** `adb shell "su 0 dd if=/dev/block/mmcblk0p22 bs=4M" | pv > system_partition.img`

### What Failed ❌

1. **SP Flash Tool V6** - TXT scatter file incompatible (needs XML)
2. **SP Flash Tool V5** - Download links dead/broken
3. **mtkclient** - Known MT8127 USB Overflow bug (unfixed)

---

## Write-Back Procedure

To flash modified system partition back to device:

### Method 1: Direct Pipe (Recommended)
```bash
cat system_partition.img | adb shell "su 0 dd of=/dev/block/mmcblk0p22 bs=4M"
```

### Method 2: Push Then Write (Safer)
```bash
adb push system_partition.img /sdcard/
adb shell "su 0 dd if=/sdcard/system_partition.img of=/dev/block/mmcblk0p22 bs=4M"
adb shell "rm /sdcard/system_partition.img"
```

### Prerequisites for Write-Back:
1. **Unmount system partition:**
   ```bash
   adb shell "su 0 umount /system"
   ```
   Or boot to recovery mode

2. **Verify image integrity:**
   ```bash
   file system_partition.img
   # Must show: Linux rev 1.0 ext4 filesystem data
   ```

3. **Check sizes match:**
   ```bash
   # Image size must be ≤ partition size
   stat -c%s system_partition.img
   adb shell "su 0 blockdev --getsize64 /dev/block/mmcblk0p22"
   ```

### Using Provided Script:
```bash
./scripts/write_system_dd.sh system_partition.img
```

The script includes safety checks:
- Verifies ADB connection
- Confirms root access
- Checks partition size vs image size
- Validates ext4 filesystem format
- Prompts for confirmation before writing
- Automatically unmounts /system

---

## Key Learnings

### 1. Scatter Files vs Actual Partition Layout
The scatter file represents the **flash layout** used during firmware creation/flashing, but the actual GPT partition table on the device may differ. Always verify with `mount` or `/proc/partitions`.

### 2. MediaTek Preloader Timing
MTK devices in preloader/BROM mode show USB connection very briefly (~2 seconds). Solution: Start flash tools FIRST, then power on device. Tools will catch the brief connection window.

### 3. MT8127 mtkclient Limitation
MT8127 chipsets have a known USB Overflow bug in mtkclient during DA upload. No workaround exists as of 2026. GitHub issues #1321 and #1384 document this.

### 4. SP Flash Tool Version Incompatibility
- V5: Uses TXT scatter files
- V6: Uses XML scatter files (with some TXT support claimed but unreliable)
- V5 downloads are largely unavailable as of 2026

### 5. ADB is Simpler When Available
If the device boots normally with root ADB access, direct dd extraction is:
- Faster than flash tools
- More reliable (no hardware mode quirks)
- Easier to script and automate
- Bidirectional (read and write)

---

## Tools and Requirements

### Hardware:
- MT8127/MT3367 device with USB connection
- USB 2.0 cable recommended (better timing for preloader)

### Software:
- **ADB tools** (Android Debug Bridge)
- **pv** (Pipe Viewer) - for progress monitoring
- **Root access** on device (su binary)
- Optional: mtkclient V2.1.4 (for device info, not extraction)
- Optional: SP Flash Tool V6.2228 (unusable for this device)

### Linux Packages:
```bash
sudo apt-get install android-tools-adb pv
```

---

## Repository Contents

```
mt8127-system-extraction/
├── README.md                      # Main documentation
├── WORKFLOW.md                    # This file - complete timeline
├── device_info.txt               # Hardware/software specs
├── partition_layout.md           # EMMC partition map
├── MT3367_Android_scatter.txt    # Original scatter file
├── mtkclient_output.log          # USB Overflow error log
└── scripts/
    ├── extract_system_dd.sh      # Extract via ADB dd
    ├── pull_system_dir.sh        # Pull /system directory
    └── write_system_dd.sh        # Write system image back
```

---

## Success Metrics

✅ **Achieved:**
- SystemUI APK extracted (11 MB)
- Complete system partition extracted (3 GB)
- Partition layout documented
- Write-back procedure verified
- Workflow fully documented

❌ **Not Achieved:**
- Flash tool extraction (incompatibility issues)
- mtkclient extraction (MT8127 bug)

**Overall Result:** Mission accomplished via alternative method (ADB dd).

---

**Last Updated:** 2026-06-20
**Status:** Complete and verified working

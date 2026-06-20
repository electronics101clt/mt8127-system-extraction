#!/bin/bash
# Write system partition back to MT8127 device via ADB using dd
# Usage: ./write_system_dd.sh <system_partition.img>

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <system_partition.img>"
    exit 1
fi

INPUT_FILE="$1"
PARTITION="/dev/block/mmcblk0p22"  # Actual system partition (not p23!)
BLOCK_SIZE="4M"

echo "MT8127 System Partition Write via DD"
echo "====================================="
echo ""
echo "WARNING: This will OVERWRITE the system partition!"
echo "Make sure you have a backup and the correct image file."
echo ""
echo "Input file: $INPUT_FILE"
echo "Target partition: $PARTITION"
echo "Block size: $BLOCK_SIZE"
echo ""

# Verify input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "ERROR: Input file not found: $INPUT_FILE"
    exit 1
fi

# Check if device is connected
if ! adb devices | grep -q "device$"; then
    echo "ERROR: No ADB device connected"
    exit 1
fi

# Check if root access is available
if ! adb shell "su 0 id" 2>/dev/null | grep -q "uid=0"; then
    echo "ERROR: Root access not available"
    exit 1
fi

# Get file size
FILE_SIZE=$(stat -c%s "$INPUT_FILE")
FILE_SIZE_MB=$((FILE_SIZE / 1024 / 1024))

echo "Image file size: $FILE_SIZE bytes ($FILE_SIZE_MB MB)"
echo ""

# Verify partition exists and get size
PARTITION_SIZE=$(adb shell "su 0 blockdev --getsize64 $PARTITION" 2>/dev/null | tr -d '\r')
PARTITION_SIZE_MB=$((PARTITION_SIZE / 1024 / 1024))

echo "Target partition size: $PARTITION_SIZE bytes ($PARTITION_SIZE_MB MB)"
echo ""

if [ "$FILE_SIZE" -gt "$PARTITION_SIZE" ]; then
    echo "ERROR: Image file ($FILE_SIZE_MB MB) is larger than partition ($PARTITION_SIZE_MB MB)"
    exit 1
fi

# Verify image is ext4
if ! file "$INPUT_FILE" | grep -q "ext4"; then
    echo "WARNING: Image file does not appear to be ext4 filesystem"
    echo "File type: $(file "$INPUT_FILE")"
    read -p "Continue anyway? (yes/no): " CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        echo "Aborted."
        exit 1
    fi
fi

echo "FINAL WARNING: This will overwrite /system partition!"
read -p "Type 'YES' to continue: " FINAL_CONFIRM

if [ "$FINAL_CONFIRM" != "YES" ]; then
    echo "Aborted."
    exit 1
fi

# Check if system is mounted and unmount if necessary
if adb shell "mount | grep -q '/system'"; then
    echo ""
    echo "System partition is mounted. Attempting to unmount..."
    if adb shell "su 0 umount /system" 2>/dev/null; then
        echo "System unmounted successfully."
    else
        echo "ERROR: Failed to unmount /system"
        echo "You may need to boot to recovery mode first."
        exit 1
    fi
fi

echo ""
echo "Writing system partition..."
echo "This will take 5-15 minutes..."
echo ""

# Write partition using direct pipe method
pv -s "$FILE_SIZE" "$INPUT_FILE" | adb shell "su 0 dd of=$PARTITION bs=$BLOCK_SIZE" 2>&1

if [ $? -eq 0 ]; then
    echo ""
    echo "SUCCESS! System partition written."
    echo ""
    echo "IMPORTANT: Reboot the device to verify the changes."
    echo "If the device doesn't boot, you can restore from backup."
else
    echo ""
    echo "ERROR: Write failed"
    exit 1
fi

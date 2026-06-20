#!/bin/bash
# Extract MT8127 system partition via ADB using dd
# Usage: ./extract_system_dd.sh [output_file]

set -e

OUTPUT_FILE="${1:-system_partition.img}"
PARTITION="/dev/block/mmcblk0p23"  # Adjust if needed
BLOCK_SIZE="4M"

echo "MT8127 System Partition Extraction via DD"
echo "=========================================="
echo ""
echo "Output file: $OUTPUT_FILE"
echo "Partition: $PARTITION"
echo "Block size: $BLOCK_SIZE"
echo ""

# Check if device is connected
if ! adb devices | grep -q "device$"; then
    echo "ERROR: No ADB device connected"
    exit 1
fi

# Check if root access is available
if ! adb shell su -c "id" 2>/dev/null | grep -q "uid=0"; then
    echo "ERROR: Root access not available"
    exit 1
fi

# Verify partition exists
if ! adb shell su -c "ls $PARTITION" 2>/dev/null; then
    echo "ERROR: Partition $PARTITION not found"
    echo "Listing available partitions:"
    adb shell su -c "ls -l /dev/block/platform/*/by-name/"
    exit 1
fi

# Get partition size
PARTITION_SIZE=$(adb shell su -c "blockdev --getsize64 $PARTITION" 2>/dev/null | tr -d '\r')
PARTITION_SIZE_MB=$((PARTITION_SIZE / 1024 / 1024))

echo "Partition size: $PARTITION_SIZE bytes ($PARTITION_SIZE_MB MB)"
echo ""
echo "Starting extraction..."
echo "This may take several minutes..."
echo ""

# Extract partition
adb shell su -c "dd if=$PARTITION bs=$BLOCK_SIZE" | pv -s "$PARTITION_SIZE" > "$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "SUCCESS! System partition extracted to: $OUTPUT_FILE"
    echo ""
    echo "File details:"
    ls -lh "$OUTPUT_FILE"
    echo ""
    echo "Verify with: file $OUTPUT_FILE"
    file "$OUTPUT_FILE"
else
    echo ""
    echo "ERROR: Extraction failed"
    exit 1
fi

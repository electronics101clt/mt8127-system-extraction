#!/bin/bash
# Pull entire /system directory via ADB
# Usage: ./pull_system_dir.sh [output_directory]

set -e

OUTPUT_DIR="${1:-./system_backup}"

echo "MT8127 System Directory Pull via ADB"
echo "====================================="
echo ""
echo "Output directory: $OUTPUT_DIR"
echo ""

# Check if device is connected
if ! adb devices | grep -q "device$"; then
    echo "ERROR: No ADB device connected"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Pulling /system directory..."
echo "This may take 10-30 minutes depending on size..."
echo ""

# Pull system directory
adb pull /system "$OUTPUT_DIR/system"

if [ $? -eq 0 ]; then
    echo ""
    echo "SUCCESS! System directory pulled to: $OUTPUT_DIR/system"
    echo ""
    echo "Directory size:"
    du -sh "$OUTPUT_DIR/system"
    echo ""
    echo "SystemUI location:"
    find "$OUTPUT_DIR/system" -name "MtkSystemUI.apk" -ls
else
    echo ""
    echo "ERROR: Pull failed"
    exit 1
fi

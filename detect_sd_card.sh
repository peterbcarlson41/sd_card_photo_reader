#!/bin/bash

# Load the .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Environment variables
SDCARD_NAME="${SDCARD_NAME:-DefaultSDCardName}"
TARGET_DIR="${TARGET_DIR:-/default/target/directory}"
PHOTO_SUBDIRECTORY="${PHOTO_SUBDIRECTORY:-DefaultPhotoSubdirectory}"

# Check for SD Card
check_sd_card() {
    if diskutil list | grep -q "$SDCARD_NAME"; then
        return 0
    else
        return 1
    fi
}

# Copy files with year and month organization
copy_files_from_sd_subdirectory() {
    SD_CARD_PATH="/Volumes/$SDCARD_NAME"
    FOUND_SUBDIRECTORY=$(find "$SD_CARD_PATH" -type d -name "$PHOTO_SUBDIRECTORY" -print -quit)

    if [ -n "$FOUND_SUBDIRECTORY" ]; then
        for file in "$FOUND_SUBDIRECTORY"/*; do
            if [ -f "$file" ]; then
                # Use exiftool to get the creation date
                year_month=$(exiftool -DateTimeOriginal -d "%Y:%B" "$file" | awk -F': ' '{print $2}')
                year=$(echo $year_month | cut -d: -f1)
                month=$(echo $year_month | cut -d: -f2)

                # Fallback to file modification date if exif data is not available
                if [ -z "$year" ] || [ -z "$month" ]; then
                    year=$(date -r "$file" "+%Y")
                    month=$(date -r "$file" "+%B")
                fi

                # Create directory structure and copy file
                mkdir -p "$TARGET_DIR/$year/$month"
                cp -nv "$file" "$TARGET_DIR/$year/$month/"
            fi
        done
    else
        echo "Subdirectory named $PHOTO_SUBDIRECTORY not found in $SD_CARD_PATH."
    fi
}

# Main loop
while true; do
    if check_sd_card; then
        echo "SD Card $SDCARD_NAME detected."
        copy_files_from_sd_subdirectory
        echo "Files copied to $TARGET_DIR."

        while check_sd_card; do
            sleep 5
        done
    fi
    sleep 5
done

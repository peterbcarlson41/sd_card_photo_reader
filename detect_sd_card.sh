#!/bin/bash

# Load the .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Environment variables
SDCARD_NAME="${SDCARD_NAME:-DefaultSDCardName}"
TARGET_DIR="${TARGET_DIR:-/default/target/directory}"
PHOTO_SUBDIRECTORY="${PHOTO_SUBDIRECTORY:-DefaultPhotoSubdirectory}"
LAST_PROCESSED_FILE="$TARGET_DIR/.last_processed_date.txt"

# Check for SD Card
check_sd_card() {
    if diskutil list | grep -q "$SDCARD_NAME"; then
        return 0
    else
        return 1
    fi
}

# Function to convert date to a numeric value for comparison (macOS version)
convert_date_to_numeric() {
    date -j -f "%Y%m%d%H%M%S" "$1" "+%Y%m%d%H%M%S"
}

# Function to copy files with year, month, and optional subdirectory organization
copy_files_from_sd_subdirectory() {
    SD_CARD_PATH="/Volumes/$SDCARD_NAME"
    FOUND_SUBDIRECTORY=$(find "$SD_CARD_PATH" -type d -name "$PHOTO_SUBDIRECTORY" -print -quit)
    LAST_PROCESSED_TIMESTAMP=$(cat "$LAST_PROCESSED_FILE" 2>/dev/null || echo "19700101000000")

    if [ -n "$FOUND_SUBDIRECTORY" ]; then
        new_files_found=false
        latest_timestamp=$LAST_PROCESSED_TIMESTAMP

        for file in "$FOUND_SUBDIRECTORY"/*; do
            if [ -f "$file" ]; then
                file_timestamp=$(date -r "$file" "+%Y%m%d%H%M%S")
                
                if [ "$file_timestamp" -gt "$LAST_PROCESSED_TIMESTAMP" ]; then
                    year=${file_timestamp:0:4}
                    month_num=${file_timestamp:4:2}
                    month=$(LC_TIME=en_US.UTF-8 date -j -f "%m" "$month_num" "+%B")

                    target_directory="$TARGET_DIR/$year/$month"
                    mkdir -p "$target_directory"

                    cp -p "$file" "$target_directory/"

                    [ "$file_timestamp" -gt "$latest_timestamp" ] && latest_timestamp=$file_timestamp
                    new_files_found=true
                fi
            fi
        done

        echo "$latest_timestamp" > "$LAST_PROCESSED_FILE"

        if [ "$new_files_found" = true ]; then
            echo "Files copied to $TARGET_DIR/$year/$month."
        else
            echo "No new files to copy."
        fi
    else
        echo "Subdirectory named $PHOTO_SUBDIRECTORY not found in $SD_CARD_PATH."
    fi
}

# Main loop
while true; do
    if check_sd_card; then
        echo "SD Card $SDCARD_NAME detected."
        copy_files_from_sd_subdirectory
        
        while check_sd_card; do
            sleep 5
        done
    fi
    sleep 5
done

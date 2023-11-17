#!/bin/bash

# Load the .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Environment variables
SDCARD_NAME="${SDCARD_NAME:-DefaultSDCardName}"

# Check for SD Card
check_sd_card() {
    if diskutil list | grep -q "$SDCARD_NAME"; then
        return 0
    else
        return 1
    fi
}

# Main loop
while true; do
    if check_sd_card; then
        echo "SD Card $SDCARD_NAME detected."
        # Run the photo_manager.py script
        python3 photo_manager.py
    fi
    sleep 5
done

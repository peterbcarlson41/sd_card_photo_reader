# SD Card File Reader Script

This script automatically reads files from a specified SD Card and transfers them to a designated directory. It is particularly useful for quickly organizing photos into a file system.

## Prerequisites

- **Operating System**: MacOS System.
- **Dependencies**: Install ExifTool. Run the following command in Terminal:

  brew install exiftool

## Setup Instructions

### Step 1: Set Up Environment Variables

- **Create Environment File**: In the cloned directory, create a file named `.env`.

### Step 2: Grant Terminal Full Disk Access

1. **System Preferences**: Open System Preferences and navigate to Security & Privacy.
2. **Privacy Tab**: Click on the Privacy tab.
3. **Full Disk Access**: Scroll down in the list on the left and select Full Disk Access.
4. **Unlock for Changes**: Click the lock icon at the bottom left to enable changes. Enter your administrator password.
5. **Add Terminal**: Click the + button under the list of applications with Full Disk Access. Navigate to the Utilities folder and select Terminal (or iTerm, if used). For scripts running from an IDE or other applications, add those applications here.
6. **Relaunch Terminal**: Close and reopen the Terminal for the changes to take effect.

### Step 3: Script Permissions

- Ensure your script file `detect_sd_card.sh` is executable. Run `chmod +x detect_sd_card.sh` in the Terminal.

---

With these setup steps, your SD Card files will be efficiently read and organized with minimal manual intervention.

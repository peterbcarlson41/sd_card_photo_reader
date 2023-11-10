This is a script that automatically reads the files from a specified SD Card to a Specified directory.

Helpful for quickly sorting photos into a file system.

The following setup instructions apply to a MacOS System:

Setup:

1. Set up your environment variables:

Create a file named ".env" in the cloned directory

2. Ensure that you give the terminal full disk access:

System Preferences: Open System Preferences and go to Security & Privacy.
Privacy Tab: Click on the Privacy tab.
Full Disk Access: In the list on the left, scroll down and select Full Disk Access.
Unlock to Make Changes: Click the lock icon at the bottom left to make changes. You will need to enter your administrator password.
Add Terminal: Click the + button under the list of applications that have Full Disk Access, navigate to the Utilities folder, and select Terminal (or iTerm if you use it). For scripts running from an IDE or other applications, you need to add those specific applications instead.
Relaunch Terminal: After adding Terminal to the list, close and reopen it for the changes to take effect.
Script Permissions:

Make sure your script file (detect_sd_card.sh) is executable. You can set this permission by running chmod +x detect_sd_card.sh in the Terminal.

3. Install necessary dependencies:

brew install exiftool

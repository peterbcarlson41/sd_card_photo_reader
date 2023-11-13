import os
import time
import datetime
import shutil
from pathlib import Path
import subprocess
from PIL import Image
from PIL.ExifTags import TAGS
import threading
import queue
import re

# Load .env file
def load_dotenv(dotenv_path='.env'):
    if Path(dotenv_path).is_file():
        with open(dotenv_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

# Call the function to load the environment variables
load_dotenv()

# Environment variables
SDCARD_NAME = os.getenv('SDCARD_NAME')
TARGET_DIR = os.getenv('TARGET_DIR')
PHOTO_SUBDIRECTORY = os.getenv('PHOTO_SUBDIRECTORY')
LAST_PROCESSED_FILE = os.path.join(TARGET_DIR, '.last_processed_date.txt')

# Check for SD Card
def check_sd_card():
    result = subprocess.run(['diskutil', 'list'], capture_output=True, text=True)
    return SDCARD_NAME in result.stdout

# Function to get capture date from EXIF data
def get_capture_date(file):
    try:
        with Image.open(file) as img:
            exif_data = img._getexif()
            if exif_data is not None:
                for tag_id in exif_data:
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':
                        return datetime.datetime.strptime(exif_data[tag_id], '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"Error reading EXIF data for {file}: {e}")
    return None

# Function to check if the file should be copied
def should_copy_file(file):
    # Check if the file is hidden (starts with a dot)
    if file.name.startswith('.'):
        return False

    # Example: Copy only certain image types
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    return file.suffix.lower() in allowed_extensions

# Function to prompt the user for a directory name with a timeout
def prompt_directory_name(default, timeout=10):
    print(f"Enter a name for the new directory (default '{default}' in {timeout}s): ", end='', flush=True)

    q = queue.Queue()

    def user_input():
        try:
            name = input()
            if not name.strip():
                q.put(default)
            elif re.match(r'^[a-zA-Z0-9_\- ]+$', name):
                q.put(f"{default}_{name}")
            else:
                print("Invalid directory name. Using default.")
                q.put(default)
        except:
            q.put(default)

    t = threading.Thread(target=user_input)
    t.daemon = True
    t.start()

    try:
        return q.get(block=True, timeout=timeout)
    except queue.Empty:
        print("No input received. Using default.")
        return default

# Copy files from SD subdirectory
def copy_files_from_sd_subdirectory():
    sd_card_path = f'/Volumes/{SDCARD_NAME}'
    found_subdirectory = None

    for subdir in Path(sd_card_path).rglob(PHOTO_SUBDIRECTORY):
        found_subdirectory = subdir
        break

    if found_subdirectory:
        new_files_found = False
        latest_timestamp = '19700101000000'
        most_recent_file_timestamp = latest_timestamp

        if Path(LAST_PROCESSED_FILE).is_file():
            with open(LAST_PROCESSED_FILE, 'r') as f:
                latest_timestamp = f.read().strip()

        eligible_files = []
        for file in found_subdirectory.glob('*'):
            if file.is_file() and should_copy_file(file):
                capture_date = get_capture_date(file)
                if capture_date:
                    file_timestamp = capture_date.strftime("%Y%m%d%H%M%S")
                else:
                    file_timestamp = datetime.datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y%m%d%H%M%S")

                if file_timestamp > latest_timestamp:
                    eligible_files.append((file, file_timestamp))
                    if file_timestamp > most_recent_file_timestamp:
                        most_recent_file_timestamp = file_timestamp

        date_directory_names = {}

        for file, file_timestamp in eligible_files:
            year = file_timestamp[:4]
            month_num = file_timestamp[4:6]
            month = datetime.datetime.strptime(month_num, "%m").strftime("%B")
            day = file_timestamp[6:8]

            target_directory = Path(TARGET_DIR, year, month)
            date_key = f"{year}-{month_num}-{day}"

            if date_key not in date_directory_names:
                # Prompt for directory name
                day_directory_name = prompt_directory_name(date_key)
                date_directory_names[date_key] = day_directory_name
            else:
                # Use the existing named directory for this date
                day_directory_name = date_directory_names[date_key]

            day_directory = target_directory / day_directory_name
            day_directory.mkdir(parents=True, exist_ok=True)

            shutil.copy2(file, day_directory)
            new_files_found = True


        if new_files_found and most_recent_file_timestamp != latest_timestamp:
            with open(LAST_PROCESSED_FILE, 'w') as f:
                f.write(most_recent_file_timestamp)

            print(f"Files copied to {day_directory}.")
        else:
            print("No new files to copy.")
    else:
        print(f"Subdirectory named {PHOTO_SUBDIRECTORY} not found in {sd_card_path}.")

# Main loop
while True:
    if check_sd_card():
        print(f"SD Card {SDCARD_NAME} detected.")
        copy_files_from_sd_subdirectory()
        
        while check_sd_card():
            time.sleep(5)
    time.sleep(5)

import unittest
import os
from photo_manager import (
    check_sd_card,
    get_capture_date,
    should_copy_file,
    prompt_directory_name,
)

class TestFileManager(unittest.TestCase):

    def test_check_sd_card(self):
        # You may need to customize this test based on your environment
        # Simulate an SD card being detected
        os.environ['SDCARD_NAME'] = 'MySDCard'
        self.assertTrue(check_sd_card())

        # Simulate no SD card detected
        os.environ['SDCARD_NAME'] = 'NonExistentSDCard'
        self.assertFalse(check_sd_card())

    def test_get_capture_date(self):
        # You may need to customize this test based on your test image file
        file_with_exif = 'test_image_with_exif.jpg'
        file_without_exif = 'test_image_without_exif.jpg'

        # Test a file with EXIF data
        capture_date = get_capture_date(file_with_exif)
        self.assertIsNotNone(capture_date)

        # Test a file without EXIF data
        capture_date = get_capture_date(file_without_exif)
        self.assertIsNone(capture_date)

    def test_should_copy_file(self):
        # Test with valid file extensions
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        for ext in valid_extensions:
            file = f'test_image{ext}'
            self.assertTrue(should_copy_file(file))

        # Test with an invalid extension
        invalid_extension = 'test_file.txt'
        self.assertFalse(should_copy_file(invalid_extension))

    def test_prompt_directory_name(self):
        # Test with valid directory name input
        input_values = ['Test123', 'valid-name', 'Test Directory']
        for value in input_values:
            with unittest.mock.patch('builtins.input', side_effect=[value]):
                directory_name = prompt_directory_name('DefaultName')
                self.assertEqual(directory_name, 'DefaultName_' + value)

        # Test with empty input (should use the default)
        with unittest.mock.patch('builtins.input', side_effect=['']):
            directory_name = prompt_directory_name('DefaultName')
            self.assertEqual(directory_name, 'DefaultName')

        # Test with invalid characters in input (should use the default)
        with unittest.mock.patch('builtins.input', side_effect=['$InvalidName']):
            directory_name = prompt_directory_name('DefaultName')
            self.assertEqual(directory_name, 'DefaultName')

if __name__ == '__main__':
    unittest.main()

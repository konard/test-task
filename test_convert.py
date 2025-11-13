#!/usr/bin/env python3
"""
Tests for the convert_archive.py script.
"""

import unittest
import tempfile
import zipfile
from pathlib import Path
import shutil
import sys

# Add the parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent))

from convert_archive import detect_encoding, convert_to_utf8


class TestEncodingDetection(unittest.TestCase):
    """Test encoding detection functionality."""

    def setUp(self):
        """Create a temporary directory for test files."""
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def test_detect_utf8(self):
        """Test detection of UTF-8 encoded file."""
        test_file = self.test_dir / "test_utf8.txt"
        test_file.write_text("Hello World! Привет мир!", encoding='utf-8')

        result = detect_encoding(test_file)
        self.assertIn(result['encoding'].lower(), ['utf-8', 'ascii'])

    def test_detect_windows1251(self):
        """Test detection of Windows-1251 encoded file."""
        test_file = self.test_dir / "test_cp1251.txt"
        # Create a file with Windows-1251 encoding
        with open(test_file, 'wb') as f:
            f.write("Привет мир!".encode('windows-1251'))

        result = detect_encoding(test_file)
        self.assertEqual(result['encoding'].lower(), 'windows-1251')

    def test_convert_windows1251_to_utf8(self):
        """Test conversion from Windows-1251 to UTF-8."""
        # Create source file in Windows-1251
        source_file = self.test_dir / "source.txt"
        test_text = "Привет мир! Hello World!"
        with open(source_file, 'wb') as f:
            f.write(test_text.encode('windows-1251'))

        # Convert to UTF-8
        output_file = self.test_dir / "output.txt"
        convert_to_utf8(source_file, 'windows-1251', output_file)

        # Verify the output
        self.assertTrue(output_file.exists())

        # Read and verify content
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, test_text)

    def test_convert_preserves_content(self):
        """Test that conversion preserves file content accurately."""
        # Create a file with mixed content
        source_file = self.test_dir / "mixed.txt"
        test_text = """program UnBasedCode;
Этот код полностью базонезависимый.
В качестве пайлоада - запускает на выполнение калькулятор.
"""
        with open(source_file, 'wb') as f:
            f.write(test_text.encode('windows-1251'))

        # Convert
        output_file = self.test_dir / "mixed_utf8.txt"
        convert_to_utf8(source_file, 'windows-1251', output_file)

        # Verify
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertEqual(content, test_text)


class TestScriptIntegration(unittest.TestCase):
    """Integration tests for the full script workflow."""

    def setUp(self):
        """Create a temporary directory and test ZIP file."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.create_test_zip()

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.test_dir)

    def create_test_zip(self):
        """Create a test ZIP file with Windows-1251 encoded content."""
        self.zip_path = self.test_dir / "test.zip"
        self.test_content = "Тестовый файл в Windows-1251"

        # Create a file with Windows-1251 encoding
        temp_file = self.test_dir / "test_file.txt"
        with open(temp_file, 'wb') as f:
            f.write(self.test_content.encode('windows-1251'))

        # Create ZIP
        with zipfile.ZipFile(self.zip_path, 'w') as zf:
            zf.write(temp_file, 'test_file.txt')

        # Remove the temp file
        temp_file.unlink()

    def test_zip_unpacking(self):
        """Test that ZIP files can be unpacked correctly."""
        from convert_archive import unpack_zip

        extract_dir = self.test_dir / "extracted"
        files = unpack_zip(self.zip_path, extract_dir)

        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].exists())
        self.assertEqual(files[0].name, "test_file.txt")


if __name__ == '__main__':
    unittest.main()

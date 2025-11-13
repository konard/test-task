#!/usr/bin/env python3
"""
Script to download a ZIP archive, unpack it, detect encoding, and convert to UTF-8.
"""

import argparse
import os
import sys
import zipfile
from pathlib import Path
from urllib.request import urlretrieve
import chardet


def download_file(url: str, output_path: Path) -> None:
    """Download a file from URL to the specified path."""
    print(f"Downloading {url}...")
    urlretrieve(url, output_path)
    print(f"Downloaded to {output_path}")


def unpack_zip(zip_path: Path, extract_dir: Path) -> list[Path]:
    """Unpack a ZIP archive and return list of extracted files."""
    print(f"Unpacking {zip_path}...")
    extract_dir.mkdir(parents=True, exist_ok=True)

    extracted_files = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        extracted_files = [extract_dir / name for name in zip_ref.namelist()]

    print(f"Extracted {len(extracted_files)} file(s) to {extract_dir}")
    return extracted_files


def detect_encoding(file_path: Path) -> dict:
    """Detect the encoding of a file using chardet."""
    print(f"Detecting encoding of {file_path.name}...")

    with open(file_path, 'rb') as f:
        raw_data = f.read()

    result = chardet.detect(raw_data)
    encoding = result['encoding']
    confidence = result['confidence']

    print(f"Detected encoding: {encoding} (confidence: {confidence:.2%})")
    return result


def convert_to_utf8(file_path: Path, source_encoding: str, output_path: Path) -> None:
    """Convert a file from source encoding to UTF-8."""
    print(f"Converting {file_path.name} from {source_encoding} to UTF-8...")

    with open(file_path, 'rb') as f:
        content = f.read()

    # Decode from source encoding
    text = content.decode(source_encoding)

    # Encode to UTF-8
    utf8_content = text.encode('utf-8')

    # Write to output file
    with open(output_path, 'wb') as f:
        f.write(utf8_content)

    print(f"Converted file saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Download ZIP archive, unpack, detect encoding, and convert to UTF-8'
    )
    parser.add_argument(
        'url',
        help='URL of the ZIP file to download'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('.'),
        help='Output directory for converted files (default: current directory)'
    )
    parser.add_argument(
        '--keep-temp',
        action='store_true',
        help='Keep temporary files (downloaded ZIP and unpacked files)'
    )

    args = parser.parse_args()

    # Create output directory
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create temp directory
    temp_dir = output_dir / 'temp'
    temp_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Download ZIP file
        zip_filename = args.url.split('/')[-1]
        zip_path = temp_dir / zip_filename
        download_file(args.url, zip_path)

        # Unpack ZIP
        extract_dir = temp_dir / 'unpacked'
        extracted_files = unpack_zip(zip_path, extract_dir)

        # Process each extracted file
        converted_files = []
        for file_path in extracted_files:
            if file_path.is_file():
                # Detect encoding
                encoding_info = detect_encoding(file_path)
                source_encoding = encoding_info['encoding']

                # Skip if already UTF-8
                if source_encoding.lower() in ['utf-8', 'ascii']:
                    print(f"{file_path.name} is already in UTF-8/ASCII, copying as-is...")
                    output_path = output_dir / file_path.name
                    with open(file_path, 'rb') as src, open(output_path, 'wb') as dst:
                        dst.write(src.read())
                    converted_files.append(output_path)
                else:
                    # Convert to UTF-8
                    output_path = output_dir / file_path.name
                    convert_to_utf8(file_path, source_encoding, output_path)
                    converted_files.append(output_path)

        print("\n" + "=" * 60)
        print("Conversion complete!")
        print(f"Converted {len(converted_files)} file(s):")
        for file in converted_files:
            print(f"  - {file}")

    finally:
        # Cleanup temp files unless --keep-temp is specified
        if not args.keep_temp:
            import shutil
            print(f"\nCleaning up temporary files in {temp_dir}...")
            shutil.rmtree(temp_dir)
        else:
            print(f"\nTemporary files kept in {temp_dir}")


if __name__ == '__main__':
    main()

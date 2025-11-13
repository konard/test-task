# test-task

## Archive Encoding Converter

This repository contains a Python tool to download ZIP archives, unpack them, detect file encodings, and convert files to UTF-8.

### Problem

The task was to:
1. Download http://rouse.drkb.ru/tmp/unbased_workout.zip
2. Unpack the archive
3. Detect the encoding of files inside
4. Convert them to UTF-8

### Solution

The archive contains a Delphi source file (`UnBasedCode.dpr`) encoded in **Windows-1251** (Cyrillic). The tool automatically detects this encoding and converts it to UTF-8.

### Usage

#### Requirements

```bash
pip install -r requirements.txt
```

#### Basic Usage

```bash
python3 convert_archive.py <URL> [--output-dir <directory>] [--keep-temp]
```

#### Example

```bash
# Convert the specified archive
python3 convert_archive.py http://rouse.drkb.ru/tmp/unbased_workout.zip --output-dir output

# Keep temporary files for inspection
python3 convert_archive.py http://rouse.drkb.ru/tmp/unbased_workout.zip --keep-temp
```

### Features

- **Automatic encoding detection** using `chardet` library
- **Multiple encoding support** (Windows-1251, ISO-8859-1, UTF-8, ASCII, etc.)
- **Batch processing** of multiple files in ZIP archives
- **Smart handling** of already UTF-8 encoded files
- **Cleanup** of temporary files (optional)
- **Comprehensive test suite**

### Testing

Run the test suite to verify functionality:

```bash
python3 test_convert.py -v
```

All tests should pass successfully.

### Results

The original file contained Russian text in Windows-1251 encoding:
```
Этот код полностью базонезависимый.
В качестве пайлоада - запускает на выполнение калькулятор на любой NT системе.
Объяснить - по какому принципу работает.
Пользоваться интеренетом и отладчиком разрешено.
Время на ответ 4 часа.
```

After conversion to UTF-8, the text is properly displayed and can be processed by UTF-8 compatible tools.
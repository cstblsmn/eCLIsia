# eCLIsia
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Unlicense](https://img.shields.io/badge/License-Unlicense-blue.svg)](https://unlicense.org/)

**eCLIsia** is a command-line tool designed to read and search Bible translations offline. It supports parsing specific chapters and verses and searching for text within translations, and allows multiple translations to be viewed at the same time.

## Installation

Just download the `eclisia.py` and `eclisiaconf.py` scripts from this repository.

## Dependencies
```
pip install requests
```

## Usage and options
### `eclisiaconf.py`
This file has to be in the same directory as `eclisia.py`.

By default, eCLIsia will look for a folder called `translations` in the working directory, but that can be changed inside this file.

When no translations are found inside the `translations` folder, the script moves on to download `EnglishKJBible.xml` (KJV). The names of the books of the Bible are in English by default, but they can be changed manually. Other languages can be added as well - just add a list of strings for each Testament.
### `eclisia.py`
Below are all the possible ways to call this script:
```
eclisia.py <book> <chapters>
eclisia.py <book> <chapters> <translation>
eclisia.py <book> <chapters> <translation> -c <one>
eclisia.py <book> <chapters> <translation> -c <one> <two> <more>
eclisia.py -l
eclisia.py -s "<string>" <translation>
eclisia.py -s "<string>" <book> <translation>
eclisia.py -s "<string>" <book> <translation> -c <one>
eclisia.py -s "<string>" <book> <translation> -c <one> <two> <more>
```
If a translation is not found inside the `translations` folder, the script will download it from [this repository](https://github.com/Beblia/Holy-Bible-XML-Format). After that, it's possible to change the filename to something shorter (like `kjv` instead of `EnglishKJBible`).

`<chapters>` can be written in these formats:
```
1       (all verses in chapter 1)
1:2     (chapter 1, verse 2)
1:2-    (all verses in chapter 1 starting from verse 2)
1:2-5   (chapter 1, verses 2 to 5)
```

This is the output of `eclisia.py -h`:
```
usage: eclisia.py [-h] [-l] [-c COMPARE [COMPARE ...]] [-s SEARCH] [book] [chapter] [translation]

a command-line tool designed to read and search Bible translations offline.

positional arguments:
  book                  Name of a book of the Bible
  chapter               Chapter and/or verses
  translation           Name of a Bible translation

options:
  -h, --help            show this help message and exit
  -l, --list            List all installed Bible translations
  -c COMPARE [COMPARE ...], --compare COMPARE [COMPARE ...]
                        Additional Bible translations
  -s SEARCH, --search SEARCH
                        Search a string in a book or translation
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[Unlicense](UNLICENSE)

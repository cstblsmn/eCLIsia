import argparse
import re
import sys
import os
import requests
import xml.etree.ElementTree as ET

from eclisiaconf import TRANSLATION_DIR, TRANSLATION_DEF, BIBLE

def parse_chapter(numbers):
    try:
        match = re.match(r'^(\d+)(?::(\d+))?(?:-(\d*))?$', numbers)
        if not match:
            raise AttributeError

        chapter = int(match.group(1)) 
        v_start = int(match.group(2)) if match.group(2) else None
        v_end = 0 if match.group(3) == '' else (int(match.group(3)) if match.group(3) else None)

        return chapter, v_start, v_end
    except AttributeError:
        print(f"Invalid chapter or verse number: \"{numbers}\"")
        sys.exit(1)

def download_translation(url, translation):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(os.path.join(TRANSLATION_DIR, translation), 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return True

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        sys.exit(1)
    except requests.exceptions.RequestException as err:
        print(f"Error during request: {err}")
        sys.exit(1)
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
        sys.exit(1)

def check_translation(translation):
    translation_file = f"{TRANSLATION_DIR}/{translation}.xml"
    if not os.path.isfile(translation_file):
        print(f"{translation} was not found. Downloading from the online repository...")
        
        translation_repo = "https://raw.githubusercontent.com/Beblia/Holy-Bible-XML-Format/master"
        if download_translation(f"{translation_repo}/{translation}.xml", f"{translation}.xml"):
            change_name = input(f"Translation downloaded succesfully as {translation}.xml. Want to change its name? [y/n]\n")
            if change_name == "y" or change_name == "Y":
                new_name = input("What do you want to call this translation?\n")
                new_file = f"{TRANSLATION_DIR}/{new_name}.xml"
                os.rename(translation_file, new_file)
                return new_name
    return translation

def parse_verses(translation, testament, book, chapter, v_start, v_end):
    all_verses = []

    try:
        tree = ET.parse(f"{TRANSLATION_DIR}/{translation}.xml")
        root = tree.getroot()
        xpath = f"./testament[@name='{testament}']/book[@number='{book+1}']/chapter[@number='{chapter}']"
        chapter = root.find(xpath)
        
        verses = chapter.findall('verse')
        
        if v_start is None and v_end is None:
            for verse in verses:
                v_num = int(verse.get('number'))
                verse_text = verse.text
                all_verses.append(f"{v_num}: {verse_text}")
        elif v_start is not None and v_end is None:
            for verse in verses:
                v_num = int(verse.get('number'))
                if v_num == int(v_start):
                    verse_text = verse.text
                    all_verses.append(f"{v_num}: {verse_text}")
        elif v_start is not None and v_end is not None:
            for verse in verses:
                v_num = int(verse.get('number'))
                if (v_num >= int(v_start)) and (v_end == 0 or v_num <= int(v_end)):
                    verse_text = verse.text
                    all_verses.append(f"{v_num}: {verse_text}")
        
        return all_verses

    except ET.ParseError as e:
        print(f"Error parsing the XML file for translation {translation}: {e}")
        return all_verses
    except Exception as e:
        print(f"An unexpected error occurred while parsing verses: {e}")
        return all_verses

def find_index(matrix, book_name):
    for testament_index, testament in enumerate(matrix):
        for language_index, language in enumerate(testament):
            if book_name in language:
                book_index = language.index(book_name)
                if testament_index:
                    return "New", book_index + 39
                return "Old", book_index
    return None, None

def search_verses(translation, search_string, testament_name=None, book_number=None):
    tree = ET.parse(f"{TRANSLATION_DIR}/{translation}.xml")
    root = tree.getroot()

    results = []

    if testament_name and book_number:
        testament = root.find(f"./testament[@name='{testament_name}']")

        book = testament.find(f"./book[@number='{book_number}']")

        for chapter in book.findall('chapter'):
            for verse in chapter.findall('verse'):
                if search_string.lower() in verse.text.lower():
                    results.append({
                        'testament': testament.get('name'),
                        'book': book.get('number'),
                        'chapter': chapter.get('number'),
                        'verse': verse.get('number'),
                        'text': verse.text
                    })
    else:
        results = [
            {
                'testament': testament.get('name'),
                'book': book.get('number'),
                'chapter': chapter.get('number'),
                'verse': verse.get('number'),
                'text': verse.text
            }
            for testament in root.findall('testament')
            for book in testament.findall('book')
            for chapter in book.findall('chapter')
            for verse in chapter.findall('verse')
            if search_string.lower() in verse.text.lower()
        ]
    
    return results

def find_istances(translation, verses, search_string):
    for v in verses:
        i_test = 0 if v["testament"] == "Old" else 1
        i_book = int(v["book"]) % 39 # Goes back to 0 after end of OT
        
        try:
            book = BIBLE[i_test][0][i_book]
        except IndexError:
            pass
        chapter = v["chapter"]
        verse = v["verse"]
        content = re.sub(re.escape(search_string), search_string.upper(), v["text"], flags=re.IGNORECASE)
        print(f"{book} {chapter}:{verse} | {content}")
    print(f">>> {len(verses)} verses have been found in {translation}\n")

def list_translations():
    try:
        print(f">>> Installed translations in \"{TRANSLATION_DIR}\":")
        
        for i, file in enumerate(os.listdir(TRANSLATION_DIR)):
            if os.path.isfile(os.path.join(TRANSLATION_DIR, file)):
                file_name, _ = os.path.splitext(file)
                print(i, file_name)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='a command-line tool designed to read and search Bible translations offline.')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--list', action='store_true', help='List all installed Bible translations')
    group.add_argument('book', type=str, nargs='?', help='Name of a book of the Bible')

    parser.add_argument('chapter', nargs='?', type=str, help='Chapter and/or verses')
    parser.add_argument('translation', nargs='?', type=str, help='Name of a Bible translation')
    parser.add_argument('-c', '--compare', nargs='+', type=str, help='Additional Bible translations')
    parser.add_argument('-s', '--search', type=str, help='Search a string in a book or translation')

    args = parser.parse_args()

    # Check translation folder and files
    if not os.path.exists(TRANSLATION_DIR):
        os.makedirs(TRANSLATION_DIR)
    if not args.translation:
        args.translation = TRANSLATION_DEF
    args.translation = check_translation(args.translation)
    if args.compare:
        for i, c in enumerate(args.compare):
            args.compare[i] = check_translation(c)

    # Run -l
    if args.list:
        list_translations()
        return

    # Run -s
    if args.search:
        # Check if there are two arguments (book and translation)
        if args.chapter:
            testament, book = find_index(BIBLE, args.book)
            if not testament:
                print(f"Couldn't find a book named \"{args.book}\"")
                sys.exit(1)
            args.translation = args.chapter
            find_istances(args.translation, search_verses(args.translation, args.search, testament, book+1), args.search)
        else:
            args.translation = args.book
            find_istances(args.translation, search_verses(args.book, args.search), args.search)
        if args.compare:
            for c in args.compare:
                find_istances(c, search_verses(c, args.search), args.search)
        return

    # Run without flags
    if not args.book or not args.chapter:
        parser.error('The following arguments are required: <book>, <chapter>')
    testament, book = find_index(BIBLE, args.book)
    if not testament:
        print(f"Couldn't find a book named \"{args.book}\"")
        sys.exit(1)
    verses = [parse_verses(args.translation, testament, book, *parse_chapter(args.chapter))]
    if args.compare:
        for i, c in enumerate(args.compare):
            c = check_translation(c)
            verses.append(parse_verses(c, testament, book, *parse_chapter(args.chapter)))
    v_rows = len(verses)
    v_cols = len(verses[0])
    for col in range(v_cols):
        for row in range(v_rows):
            print(verses[row][col])
        print("")

if __name__ == "__main__":
    main()
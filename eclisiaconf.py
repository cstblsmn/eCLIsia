import os
WORKING_PATH = os.path.abspath(__file__)
WORKING_DIR = os.path.dirname(WORKING_PATH)
TRANSLATION_DIR = os.path.join(WORKING_DIR, "translations")
# TRANSLATION_DIR = your/path/to/translations
TRANSLATION_DEF = "EnglishKJBible"

BIBLE = [
    # Old Testament
    [
        # English
        ['genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy', 'joshua', 'judges', 'ruth', '1-samuel', '2-samuel', '1-kings', '2-kings', '1-chronicles', '2-chronicles', 'ezra', 'nehemiah', 'esther', 'job', 'psalms', 'proverbs', 'ecclesiastes', 'song-of-songs', 'isaiah', 'jeremiah', 'lamentations', 'ezekiel', 'daniel', 'hosea', 'joel', 'amos', 'obadiah', 'jonah', 'micah', 'nahum', 'habakkuk', 'zephaniah', 'haggai', 'zechariah', 'malachi']
    ],
    # New Testament
    [
        # English
        ['matthew', 'mark', 'luke', 'john', 'acts', 'romans', '1-corinthians', '2-corinthians', 'galatians', 'ephesians', 'philippians', 'colossians', '1-thessalonians', '2-thessalonians', '1-timothy', '2-timothy', 'titus', 'philemon', 'hebrews', 'james', '1-peter', '2-peter', '1-john', '2-john', '3-john', 'jude', 'revelation', '']
    ]
]

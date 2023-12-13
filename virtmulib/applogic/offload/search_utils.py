import os
import os
import re
import string
import unidecode
import pkgutil

STOPWORDS = pkgutil.get_data('virtmulib.applogic.offload', "stopwords").decode('utf-8')


def remove_blacklist_chars(fn):
    """Sanitise strings that will be used as filenames on the OS

    Args:
            fn (str): The unsanitised filename

    Returns:
            str: The sanitised filename
    """
    os_blacklist = '\\/:*?"<>|'
    fn = fn.replace('"', "'")
    return "".join([letter for letter in fn if letter not in os_blacklist])


def filter_out_stopwords_punc(lst):
    """Sanitize text for search be removing common english stopwords as well as punctuation

    Args:
            lst (list): A list of words, resulting fron a string split() by spaces

    Returns:
            list: A subset of the args with stopwords and punc elements removed
    """
    return [
        word
        for word in lst
        if not (
            word in STOPWORDS
            or word in string.punctuation
            or len(word) < 2
        )
    ]


def remove_accents(lst):
    """Simplify accented letters to the base letters used in english
    Args:
            lst (list): A list of words, resulting fron a string split() by spaces

    Returns:
            list: The list of words with all accents removes
    """
    return [unidecode.unidecode(word) for word in lst]


def replace_symbols_with_spaces(text):
    """Another search aid, remove symbols from search text
    Args:
            text (str): Pre-Search text

    Returns:
            str: Text with all symbols removed
    """
    text = re.sub(r"[^\w^\-]", " ", text)
    text = re.sub(r"[\W\s][\d\-]+[\W\s]", " ", text)
    dashed = re.findall(r"\w+\-\w+", text)

    dashed = " ".join(dashed)
    dashed = re.sub(r"\-", " ", dashed)
    text = text + " " + dashed
    text = re.sub(" +", " ", text)
    return text


def two_in(st1, st2, limit=2):
    """Atleast [limit] number of text tokens in st1 occur in st2

    Args:
            st1 (str): The source string
            st2 (st2): The destination string
            limit (int): Min num of tokens in st1 to be found in st2. Default is 2, hence func name

    Returns:
            bool: True if condition of function is met, and False otherwise
    """
    st1 = replace_symbols_with_spaces(st1.lower().strip())
    st2 = replace_symbols_with_spaces(st2.lower().strip())

    st1_words = filter_out_stopwords_punc(st1.split(" "))
    st2_words = filter_out_stopwords_punc(st2.split(" "))

    if len(st1_words) == 0 or len(st2_words) == 0:
        st1_words = st1
        st2_words = st2

    st1_words = remove_accents(st1_words)
    st2_words = remove_accents(st2_words)

    limit = min(len(st1_words), len(st2_words), limit)

    intersection = len(set(st1_words) & set(st2_words))

    return intersection >= limit

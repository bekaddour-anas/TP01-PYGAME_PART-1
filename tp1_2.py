
import re
import sys


def clean_text(text):
    """Remove punctuation from a text."""
    punct = "+.*/?,;\'#"

    for p in punct:
        text = text.replace(p, "")

    return text


def tokenize(text):
    """Convert text into a list of words."""
    return text.split()


def tokenize2(text):
    """Split text using one or more whitespace characters."""
    spaces = r"\s+"
    words = re.split(spaces, text.strip())
    return words


def word_freq(words):
    """Count the occurrences of each word."""
    index = {}

    for w in words:
        if w in index:
            index[w] += 1
        else:
            index[w] = 1

    return index


def most_common_word(words_freq_table):
    """Return the most frequent word."""
    frequent = None
    frequency = 0

    for word in words_freq_table:
        if words_freq_table[word] > frequency:
            frequent = word
            frequency = words_freq_table[word]

    return frequent


def read_file(filename):
    """Read all the text from a file."""
    try:
        with open(filename, "r", encoding="utf-8") as fl:
            text = fl.read()
    except OSError:
        print("Can't open file:", filename)
        sys.exit(1)

    return text


def main():
    text = """Surprise steepest recurred landlord mr wandered amounted of.
Continuing devonshire but considered its. Rose past oh shew roof
is song neat. Do depend better praise do friend garden an wonder to.
Intention age nay otherwise but breakfast.
Around garden beyond to extent by."""

    text = clean_text(text)
    print("Clean text:")
    print(text)

    words = tokenize(text)
    print("\nWords:")
    print(words)

    words_nb = word_freq(words)
    print("\nWord frequencies:")
    print(words_nb)

    try:
        data = read_file("f1.txt")
    except SystemExit:
        return

    print("\nFile content:")
    print(data)

    words = tokenize(data)
    word_freq_table = word_freq(words)

    print("\nFrequency table:")
    print(word_freq_table)

    freqw = most_common_word(word_freq_table)

    if freqw is not None:
        print(
            "Most frequent word is:",
            freqw,
            word_freq_table[freqw]
        )


if __name__ == "__main__":
    main()

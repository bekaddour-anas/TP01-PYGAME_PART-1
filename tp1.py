import string
import re
import sys
def clean_text(text):

 punct = "+.*/?,;\'#"
 for p in punct:
    text = text.replace(p," hh ")
 return text



def tokenize(tokens):
    # Convert text into tokens, return a list of tokens (words)
    return tokens.split()

def tokenize2(text):
    """
    Convert text into tokens, return a list of tokens (words)
    """
    spaces = r"\s+"
    words = re.split(spaces, text)
    return words

def word_freq(words):

 #Counts words and return a dictionary of words with their occurrences

 index = {}
 for w in words:
  if w in index:
    index[w] += 1
  else:
    index[w] = 1
 return index


def most_common_word(words_freq_table):
 
 #Counts words and return a dictionary of words with their occurrences
 
 frequent =""
 frequency = 0
 for word in words_freq_table:
  if words_freq_table[word] > frequency:
   frequent = word
   frequency = words_freq_table[word]
 return frequent

def read_file(filename):
    """
    Read text from a file
    """
    try:
        fl = open(filename, "r", encoding="utf-8")
        text = fl.read()
        fl.close()  # Always a good idea to close the file when done!
    except:
        print("Can't open file:", filename)
        sys.exit()
        
    return text
def main(args):
    text = "Surprise steepest recurred landlord mr wandered amounted of. Continuing devonshire but considered its."
    text = clean_text(text)
    words = tokenize(text)
    tokens2 = tokenize2(text)

    print(words)
    print("2694849489484 ++ ",tokens2,"\n")
    words_nb = word_freq(words)
    print("Word frequencies:", words_nb)
    
    word_freq_table=most_common_word(words_nb)
    print("  ",word_freq_table)
    print(read_file("f1.txt"))
    
if __name__ == "__main__":
    main(None)
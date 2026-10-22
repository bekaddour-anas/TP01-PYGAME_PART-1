
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Character encoding declaration (UTF-8)
# to support multilingual text.

print("Salam Alykom")

# Variables declaration
# Python determines the type automatically.

age = 125
print("type of age:", type(age))

salaire = 3.14
print("type of salaire:", type(salaire))

name = "Ahmed"
print("type of name:", type(name))

# String substitution using % formatting

s2 = "I am %s" % name
s3 = "I am %d old" % age

print(s2, s3)

# Lists

liste = [1, 2, 31, 4]

print("type of ls:", type(liste))
print(liste)

# Add an element to the list

liste.append(5)
print(liste)

# Word list

wordlist = ["I", "am", "learning", "english"]

# Flow Control

a = 15

if a > 15:
    print("a is greater than 15")

elif a <= 15 and a >= 10:
    print("a between 10 and 15")

else:
    print("a is less than 10")

# Test if an element belongs to a list

a = 5

if a in liste:
    print("a exists in list")

# Loops

for word in wordlist:
    print(word)

# Loops and tests
# Count occurrences of a character in a string

chaine = """The sky, oh the sky! It stretches above us, vast and endless.

The sky is a canvas, a canvas of blue, blue like the ocean on a clear summer day. It's a canvas of possibilities, possibilities as vast as the sky itself."""

caractere = "e"
cpt = 0

for c in chaine:
    if c == caractere:
        cpt += 1

print("Char %s exists %d times" % (caractere, cpt))

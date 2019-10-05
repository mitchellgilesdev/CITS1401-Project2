import math as m
import os


def main(textfile1, textfile2, feature):
    """

    :param textfile1:
    :param textfile2:
    :param feature: allowed names are "punctuation", "unigrams", "conjunctions",  "composite".
    :return:
    """
    features = {"punctuation": punctuation, "unigrams": unigrams, "conjunctions": conjunctions, "composite": composite}

    dist = None
    profile1 = {}
    profile2 = {}

    # check files exist
    f1 = open(textfile1, "r")
    f2 = open(textfile2, "r")
    lines1 = f1.readlines()
    lines2 = f2.readlines()

    if feature not in features:
        raise Exception("Invalid feature you input: {}".format(feature))

    func = features.get(feature)
    profile1 = func(lines1)
    profile2 = func(lines2)

    dist = distance(profile1, profile2)

    return dist, profile1, profile2


def conjunctions(lines1):
    conj_list = {
        "also": 0, "although": 0, "and": 0, "as": 0, "because": 0, "before": 0, "but": 0, "for": 0, "if": 0,
        "nor": 0, "of": 0, "or": 0, "since": 0, "that": 0, "though": 0, "until": 0, "when": 0, "whenever": 0,
        "whereas": 0, "which": 0, "while": 0, "yet": 0
    }

    for line in lines1:
        words = line.split()
        for word in words:
            word = word.lower()
            new_word = ""
            for char in word:
                if char.isalpha():
                    new_word += char
            if new_word in conj_list:
                conj_list.update({new_word: conj_list.get(new_word) + 1})

    return conj_list


def unigrams():
    return None


def punctuation():
    return None


def composite():
    return None


def distance(dict1, dict2):
    # sort the list of keys, loop through the keys to index into dict
    keys = set.union(set(dict1.keys()), set(dict2.keys()))
    diff_sqrd = 0
    for key in keys:
        if key in dict1 and key in dict2:
            diff_sqrd += m.pow(dict1.get(key) - dict2.get(key), 2)
        elif key in dict1:
            diff_sqrd += m.pow(dict1.get(key) - 0, 2)
        else:
            diff_sqrd += m.pow(0 - dict2.get(key), 2)
    return m.sqrt(diff_sqrd)


"""
Notes:
SENTENCE -> sequence of words followed by (.?!) followed by 
            (quotation mark, whitespace[space/tab/newline])

1) Create a profile of the inputs using dictionaries (contains the number of occurrences of 
   case insensitive words as well as punctuation)
    -> words counted are dependent on the input feature
        = "punctuation", "unigrams", "conjunctions", "composite"

Conjunctions: count the number of occurrences of the following words
        "also", "although", "and", "as", "because", "before", "but", "for", "if", "nor", "of",
        "or", "since", "that", "though", "until", "when", "whenever", "whereas",
        "which", "while", "yet"

Unigrams: count the occurrences of each word in the files. e.g. for
        This is a Document.
        This is only a document
        A test should not cause problem

        The word count will be: "a":3, "document":2, "this":2, "is":2, "only":1,
        "should":1, "not""1, "cause":1, "problem":1

Punctuation: 
            - counts certain pieces of punctuation (comma and semicolon).
            - count single quotes (only when they appear as apostrophes i.e. won't, can't
            - count dash (-), only when surrounded by letters as compound word e.g. comp-word
            - any other punctuation letters e.g. '.' when not at the end of a sentence SHOULD be 
            regarded as whitespace, so server to end words. 
            Strings of digits are also words. Therefore 3.1415 is regarded as two words
            Note: "--" is regarded as a space character in some texts.
            
Composite: number of occurrences of punctuations and conjunctions
            - add two further parameters relating to the text 
            (average words per sentence, average sentences per paragraph)
            Paragraph -> any number of sentences followed by a blank line or by the end of text.
            
- 

"""

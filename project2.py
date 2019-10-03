import math as m
import os


def main(textfile1, textfile2, feature):
    """

    :param textfile1:
    :param textfile2:
    :param feature: allowed names are "punctuation", "unigrams", "conjunctions",  "composite".
    :return:
    """
    dist = None
    profile1 = {}
    profile2 = {}
    return dist, profile1, profile2


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

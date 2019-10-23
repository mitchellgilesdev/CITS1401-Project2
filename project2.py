"""
CITS1401 Project 2
Author: Mitchell Giles
Student No: 22490361
"""

import math as m
import os


def main(textfile1, textfile2, feature):
    """
    :param textfile1:  a string containing the path of the 1st text file to analyse
    :param textfile2:  a string containing the path of the 1st text file to analyse
    :param feature:    allowed names are "punctuation", "unigrams", "conjunctions",  "composite".
    :return dist:      the distance calculated between two texts
            profile1:  the dictionary of {words:count} created for the 1st text based on the feature parameter
            profile2:  the dictionary of {words:count} created for the 2nd text based on the feature parameter
    """
    features = {"punctuation": punctuation, "unigrams": unigrams, "conjunctions": conjunctions, "composite": composite}

    dist = None
    profile1 = {}
    profile2 = {}

    # check files exist and handle error gracefully
    try:
        f1 = open(textfile1, "r")
    except FileNotFoundError:
        # Used as the print function cannot be used
        exit("textfile1 Not Found: {}".format(textfile1))
    try:
        f2 = open(textfile2, "r")
    except FileNotFoundError:
        # Used as the print function cannot be used as the project brief
        exit("textfile2 Not Found: {}".format(textfile2))

    lines1 = f1.readlines()
    lines2 = f2.readlines()

    if feature not in features:
        raise Exception("Invalid feature you input: {}".format(feature))

    func = features.get(feature)
    profile1 = func(lines1)
    profile2 = func(lines2)
    dist = distance(profile1, profile2)

    f1.close()
    f2.close()

    return round(dist, 4), profile1, profile2


def conjunctions(lines):
    """
    Generates the profile if the parameter is conjunctions.
    :param lines: a list of all of the lines in the file.
    :return: a dictionary of the number of occurrences of each conjunction
    """
    conj_list = {
        "also": 0, "although": 0, "and": 0, "as": 0, "because": 0, "before": 0, "but": 0, "for": 0, "if": 0,
        "nor": 0, "of": 0, "or": 0, "since": 0, "that": 0, "though": 0, "until": 0, "when": 0, "whenever": 0,
        "whereas": 0, "which": 0, "while": 0, "yet": 0
    }

    for line in lines:
        line = line.replace("--", " ")
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


def unigrams(lines):
    """
    Generates the profile if the parameter is unigrams.
    :param lines: a list of all of the lines in the file.
    :return: a dictionary of the number of occurrences of each word
    """
    profile = {}
    for line in lines:
        words = line.split()
        for word in words:
            word = word.lower()
            new_word = ""
            for char in word:
                if char.isalpha():
                    new_word += char
            if new_word not in profile:
                profile.update({new_word: 1})
            else:
                profile.update({new_word: profile.get(new_word) + 1})

    return profile


def punctuation(lines):
    """
    Generates the profile if the parameter is punctuation.
    :param lines: a list of all of the lines in the file.
    :return: a dictionary of the number of occurrences of selected punctuation characters.
    """
    profile = {',': 0, ';': 0, '-': 0, "'": 0}

    for line in lines:
        words = line.split()
        for word in words:
            word = word.lower()
            i = 0
            for i, character in enumerate(word):
                # only focus on the characters to be measured, ignore the rest as whitespace
                if character == ',' or character == ';':
                    profile.update({character: profile.get(character) + 1})
                    continue
                if i == len(word) - 1:
                    continue
                if character == '-' and word[i + 1] == '-':
                    continue
                if character == "'" or character == '-':
                    if (i - 1) >= 0 and word[i - 1].isalpha() and word[i + 1].isalpha():
                        profile.update({character: profile.get(character) + 1})
                        continue

    return profile


def composite(lines):
    """
    Generates the profile using conjunctions, punctuation and average words_per_sentence and
    sentences_per_paragraph
    :param lines: a list of all of the lines in the file.
    :return: a dictionary of the conjunctions, punctuations and averages and their respective counts.
    """
    composite_profile = {
        "also": 0, "although": 0, "and": 0, "as": 0, "because": 0, "before": 0, "but": 0, "for": 0, "if": 0,
        "nor": 0, "of": 0, "or": 0, "since": 0, "that": 0, "though": 0, "until": 0, "when": 0, "whenever": 0,
        "whereas": 0, "which": 0, "while": 0, "yet": 0, ',': 0, ';': 0, '-': 0, "'": 0,
        'words_per_sentence': 0, 'sentences_per_par': 0
    }
    conjunctions_profile = conjunctions(lines)
    punctuation_profile = punctuation(lines)

    for key in conjunctions_profile:
        composite_profile.update({key: conjunctions_profile.get(key)})
    for key in punctuation_profile:
        composite_profile.update({key: punctuation_profile.get(key)})

    wps, spp = text_averages(lines)
    composite_profile.update({"words_per_sentence": round(wps, 4)})
    composite_profile.update({"sentences_per_par": round(spp, 4)})

    return composite_profile


def text_averages(lines):
    """
    Calculate the average words per sentence and sentences per paragraph
    :param lines: a list of the lines
    :return:
    """

    current_sentence = ""
    num_paragraphs = 0
    sentences = []
    skip_next = False

    # get a list of all of the sentences in the text.
    for i, line in enumerate(lines):
        line_index = 0
        for char in line:
            # check end of current_sentence
            if skip_next:
                skip_next = False
                continue
            if char == '?' or char == '!' or char == '.':
                # ensure that quotations after punctuation are not counted as a new words.
                if line[line_index + 1] == '"' or line[line_index + 1] == "'":
                    skip_next = True
                if line_index == (len(line) - 1) or line[line_index + 1].isspace() or line[line_index + 1] == "'" or \
                        line[line_index + 1] == '"':
                    current_sentence += char
                    sentences.append(current_sentence)
                    current_sentence = ""
            else:
                current_sentence += char
            line_index += 1
        if i == (len(lines) - 1):
            num_paragraphs += 1
            continue
        elif lines[i + 1].isspace():
            num_paragraphs += 1
        current_sentence += " "

    total_words = 0

    # format the sentence to effectively split into words.
    for sentence in sentences:
        sentence = sentence.replace("--", " ")
        sentence = sentence.replace('.', " ")
        sentence = sentence.replace('\n', " ")
        words = sentence.split()
        total_words += len(words)

    averageWPS = total_words / len(sentences)
    averageSPP = len(sentences) / num_paragraphs

    return averageWPS, averageSPP


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

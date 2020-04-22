from src.training_data_preprocessing.NLP_utils import NLP_utils
from src.training_data_preprocessing.standardNLP import StanfordNLP
from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import *
import json
import nltk
import re


utils = NLP_utils()
sNLP = StanfordNLP()

list_of_phrase = []

def traverse(t):
    try:
        t.label()

    except AttributeError:
        return

    if t.label() == "ROOT":
        #print('Phrase : ', t.leaves())
        list_of_phrase.append(utils.list_to_string(t.leaves()))

    elif t.label() == "NP":
        #print('NP Phrase : ', t.leaves())

        if t.__len__() == 1:
            child = t[0]
            if child.label() == "NN" or child.label() == "NNS" or child.label() == "NNP" or child.label() == "NNPS":
                #print(' 1 NP - NN : ', child.leaves())
                list_of_phrase.append(utils.list_to_string(child.leaves()))
            elif child.label() == "VBG":  # include present particle
                #print(' 1 NP - NN : ', child.leaves())
                list_of_phrase.append(utils.list_to_string(child.leaves()))

        else:  # when it's not only child
            Adj_tokens = []
            NP_tokens = []
            for child in t:
                if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP" :
                    traverse(child)
                else:  # it is word level
                    for child in t:
                        if child.label() == "NN" or child.label() == "NNS" or child.label() == "NNP" or child.label() == "NNPS" or child.label() == "JJ":
                            NP_tokens.append(utils.list_to_string(child.leaves()))

                        elif child.label() == "JJS":  # adjective superlative
                            Adj_tokens.append(utils.list_to_string(child.leaves()))

                    break

            if Adj_tokens.__len__() != 0:
                #print('ADJ Phrase : ', Adj_tokens)
                list_of_phrase.append(utils.list_to_string(Adj_tokens))

            if NP_tokens.__len__() != 0:
                #print(' 2 NP - NN Phrase : ', NP_tokens)
                list_of_phrase.append(utils.list_to_string(NP_tokens))

        return  #FIX - otherwise, it repeats

    #elif t.label() == "VP":    #ToDo : future
        #print('VP Phrase : ', t.leaves())

    elif t.label() == "PP":
        #print('PP Phrase : ', t.leaves())
        # save IN such as at, in
        if t.__len__() == 1:
            child = t[0]
            if child.label() == "IN":
                #print(' IN : ', child.leaves())
                list_of_phrase.append(utils.list_to_string(child.leaves()))
        else:
            for child in t:
                if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP":
                    traverse(child)
                else:  # it is word level

                    """
                    # -------------------------------------------------
                    # OPTION 1 : split only token such as in, at, by
                    # -------------------------------------------------

                    Preposition_tokens = []
                    NP_tokens = []
                    for child in t:
                        if child.label() == "IN":
                            Preposition_tokens.append(list_to_string(child.leaves()))
                        if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP":
                            traverse(child)

                    if Preposition_tokens.__len__() != 0:
                        print('Prepositional Phrase : ', Preposition_tokens)
                        list_of_phrase.append(list_to_string(Preposition_tokens))

                    break
                    """

                    """
                    # --------------------------
                    # OPTION 2 : split phrase
                    # --------------------------
                    print("Phrase : ", t.leaves())
                    list_of_phrase.append(list_to_string(t.leaves()))
                    break
                    """

                    #----------------------------------------------------------------------
                    # OPTION 3 : take all phrase include prepostion and NP phrase inside
                    #----------------------------------------------------------------------
                    Preposition_tokens = []
                    NP_tokens = []
                    for child in t:
                        if child.label() == "IN":
                            Preposition_tokens.append(utils.list_to_string(t.leaves()))   # add whole prepositional phrase
                        if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP":
                            traverse(child)

                    if Preposition_tokens.__len__() != 0:
                        #print('Prepositional Phrase : ', Preposition_tokens)
                        list_of_phrase.append(utils.list_to_string(Preposition_tokens))

                    break

        return

    #elif t.label() == "ADJP":  # Adjective Phrase #ToDo : future
        #print('ADJP Phrase : ', t.leaves())

    #elif t.label() == "ADVP": # Adverb Phrase #ToDo:future
        #print('ADVP Phrase : ', t.leaves())

    for child in t:
        traverse(child)



def traverse(t, phrase_list):

    try:
        t.label()

    except AttributeError:
        return

    if t.label() == "ROOT":
        #print('Phrase : ', t.leaves())
        phrase_list.append(utils.list_to_string(t.leaves()))

    elif t.label() == "NP":
        #print('NP Phrase : ', t.leaves())

        if t.__len__() == 1:
            child = t[0]
            if child.label() == "NN" or child.label() == "NNS" or child.label() == "NNP" or child.label() == "NNPS":
                #print(' 1 NP - NN : ', child.leaves())
                phrase_list.append(utils.list_to_string(child.leaves()))
            elif child.label() == "VBG":  # include present particle
                #print(' 1 NP - NN : ', child.leaves())
                phrase_list.append(utils.list_to_string(child.leaves()))

        else:  # when it's not only child
            Adj_tokens = []
            NP_tokens = []
            for child in t:
                if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP" :
                    traverse(child, phrase_list)
                else:  # it is word level
                    for child in t:
                        if child.label() == "NN" or child.label() == "NNS" or child.label() == "NNP" or child.label() == "NNPS" or child.label() == "JJ":
                            NP_tokens.append(utils.list_to_string(child.leaves()))

                        elif child.label() == "JJS":  # adjective superlative
                            Adj_tokens.append(utils.list_to_string(child.leaves()))

                    break

            if Adj_tokens.__len__() != 0:
                #print('ADJ Phrase : ', Adj_tokens)
                phrase_list.append(utils.list_to_string(Adj_tokens))

            if NP_tokens.__len__() != 0:
                #print(' 2 NP - NN Phrase : ', NP_tokens)
                phrase_list.append(utils.list_to_string(NP_tokens))

        return  #FIX - otherwise, it repeats

    #elif t.label() == "VP":    #ToDo : future
        #print('VP Phrase : ', t.leaves())

    elif t.label() == "PP":
        #print('PP Phrase : ', t.leaves())
        # save IN such as at, in
        if t.__len__() == 1:
            child = t[0]
            if child.label() == "IN":
                #print(' IN : ', child.leaves())
                phrase_list.append(utils.list_to_string(child.leaves()))
        else:
            for child in t:
                if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP":
                    traverse(child, phrase_list)
                else:  # it is word level

                    """
                    # -------------------------------------------------
                    # OPTION 1 : split only token such as in, at, by
                    # -------------------------------------------------

                    Preposition_tokens = []
                    NP_tokens = []
                    for child in t:
                        if child.label() == "IN":
                            Preposition_tokens.append(list_to_string(child.leaves()))
                        if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP":
                            traverse(child)

                    if Preposition_tokens.__len__() != 0:
                        print('Prepositional Phrase : ', Preposition_tokens)
                        phrase_list.append(list_to_string(Preposition_tokens))

                    break
                    """

                    """
                    # --------------------------
                    # OPTION 2 : split phrase
                    # --------------------------
                    print("Phrase : ", t.leaves())
                    phrase_list.append(list_to_string(t.leaves()))
                    break
                    """

                    #----------------------------------------------------------------------
                    # OPTION 3 : take all phrase include prepostion and NP phrase inside
                    #----------------------------------------------------------------------
                    Preposition_tokens = []
                    NP_tokens = []
                    for child in t:
                        if child.label() == "IN":
                            Preposition_tokens.append(utils.list_to_string(t.leaves()))   # add whole prepositional phrase
                        if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP":
                            traverse(child, phrase_list)

                    if Preposition_tokens.__len__() != 0:
                        #print('Prepositional Phrase : ', Preposition_tokens)
                        phrase_list.append(utils.list_to_string(Preposition_tokens))

                    break

        return

    elif t.label() == "ADJP":  # Adjective Phrase
        if t.__len__() == 1:
            child = t[0]
            if child.label() == "JJ" or child.label() == "JJR" or child.label() == "JJS":
                phrase_list.append(utils.list_to_string(child.leaves()))
        else:
            for child in t:
                if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP":
                    traverse(child, phrase_list)
                else:  # it is word level
                    Adj_tokens = []

                    for child in t:
                        if child.label() == "JJ" or child.label() == "NN" or child.label() == "NNS" or child.label() == "NNP":
                            Adj_tokens.append(utils.list_to_string(child.leaves()))  # add whole prepositional phrase
                        if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP":
                            traverse(child, phrase_list)

                    if Adj_tokens.__len__() != 0:
                        phrase_list.append(utils.list_to_string(Adj_tokens))

                    break
        return


    elif t.label() == "ADVP":  # Adverb Phrase
        if t.__len__() == 1:
            child = t[0]
            if child.label() == "RB" or child.label() == "RBS":
                phrase_list.append(utils.list_to_string(child.leaves()))

    elif t.label() == "WHNP": #WH-noun phrase
        if t.__len__() > 1:
            for child in t:
                if child.label() == "NP" or child.label() == "VP" or child.label() == "PP" or child.label() == "ADJP" or child.label() == "ADVP":
                    traverse(child, phrase_list)
                else:  # it is word level
                    Adj_tokens = []

                    for child in t:
                        if child.label() == "JJ" or child.label() == "NN" or child.label() == "NNS" or child.label() == "NNP" or child.label() == "ADJP":
                            Adj_tokens.append(utils.list_to_string(child.leaves()))  # add whole prepositional phrase

                    if Adj_tokens.__len__() != 0:
                        phrase_list.append(utils.list_to_string(Adj_tokens))

                    #break
            return


    for child in t:
        traverse(child, phrase_list)



def show_parse_tree(text):
    from nltk.parse.corenlp import CoreNLPParser
    stanford = CoreNLPParser('http://localhost:9000')
    next(stanford.raw_parse(text)).draw()


def debug(text):
    debug_phrase_list = []
    #text = "Which dry cleaner will be open along my way home"  # MVP 6
    print('raw query : ', text)
    parsed_text = sNLP.parse(text)
    print('parsed : \n', parsed_text)
    show_parse_tree(text)
    normalized_parsed_query = re.sub('[\r\n]', '', parsed_text)
    print('parsed query without newline : ', normalized_parsed_query)
    print('')
    #list_of_phrase = []
    tree = ParentedTree.fromstring(normalized_parsed_query)
    traverse(tree, debug_phrase_list)
    print('Sequence of Phrase : ', debug_phrase_list)


def create_input_sequences():
    # -------------------------
    # read queries

    import pandas as pd
    queries = "C:/Users/shong/PycharmProjects/ngls_query/Intent-Slot-Tagging-Model/src/data/mvp_queries.txt"
    f = open(queries, "r")
    splitted_phrases = "C:/Users/shong/PycharmProjects/ngls_query/Intent-Slot-Tagging-Model/src/data/mvp_input_sequences.csv"
    splitted_input_file = open(splitted_phrases, "w")

    for line in f:
        print('query : ', line)
        line = normalizeString(unicodeToAscii(line))
        parsed_text = sNLP.parse(line)
        normalized_parsed_query = re.sub('[\r\n]', '', parsed_text)
        list_of_phrase = []
        tree = ParentedTree.fromstring(normalized_parsed_query)
        traverse(tree, list_of_phrase)
        print('Sequence of Phrase : ', utils.list_to_string_with_comma(list_of_phrase))
        print('\n')
        list_of_phrase_with_comma = utils.list_to_string_with_comma(list_of_phrase)
        splitted_input_file.write(list_of_phrase_with_comma)
        splitted_input_file.write('\n')

    f.close()


import unicodedata

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters


def normalizeString(s):
    s = unicodeToAscii(s.lower().strip())
    s = re.sub(r"([.!?])", r" \1", s)
    s = re.sub(r"[^a-zA-Z.!?]+", r" ", s)
    return s



# --------------------
#  test a query
text = "Which CTA stations in Lakeview Chicago have bike-sharing stations?" #FIXME : WHNP
debug(normalizeString(unicodeToAscii(text)))


# --------------------
# run queries
#create_input_sequences()

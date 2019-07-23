from typing import Dict, List, Set, Tuple, NamedTuple
import nltk
from nltk.corpus import wordnet, stopwords
from nltk.tokenize import word_tokenize
from dataclasses import dataclass


@dataclass
class B_Word:
    word: str
    stem: str
    g_tag: str


class LanguageTools:
    wnl = nltk.WordNetLemmatizer()
    stop_word_set = set(stopwords.words('english'))

    def __init__(self):
        pass

    @staticmethod
    def is_word(word: str) -> bool:
        if wordnet.synsets(word):
            return True
        return False

    @staticmethod
    def return_base_words(tagged_words: List[Tuple[str, str]]) -> List[B_Word]:
        r_list: List[B_Word] = []
        for tagged_word in tagged_words:
            word = tagged_word[0]
            grammar_tag = tagged_word[1]
            stem = LanguageTools.wnl.lemmatize(word, pos=LanguageTools._get_wordnet_pos(grammar_tag))

            r_list.append(B_Word(word=word, stem=stem, g_tag=grammar_tag))
        return r_list

    @staticmethod
    def return_base_words_from_string(text: str) -> List[B_Word]:
        word_list = LanguageTools.tokenize(text)
        tag_words = LanguageTools.tag_words(word_list)
        stemmed_words = LanguageTools.return_base_words(tag_words)
        return stemmed_words

    @staticmethod
    def get_paths(word: str, g_type: str):
        r_paths: List[List] = []
        w_synsets = wordnet.synsets(word, pos=LanguageTools._get_wordnet_pos(g_type))

        w_synsets_length = len(w_synsets)
        for i in range(0, w_synsets_length):
            r_paths.append([])

            word_set = w_synsets[i]
            paths = word_set.hypernym_paths()
            for path in paths:
                for synset in path:
                    r_paths[i].append(synset._name)
        return r_paths

    @staticmethod
    def is_stop_word(text: str):
        if text in LanguageTools.stop_word_set:
            return True
        else:
            return False

    @staticmethod
    def get_paths_as_words(word: str, g_type: str):
        r_set = set()
        w_synsets = wordnet.synsets(word, pos=LanguageTools._get_wordnet_pos(g_type))

        w_synsets_length = len(w_synsets)
        for i in range(0, w_synsets_length):
            word_set = w_synsets[i]
            paths = word_set.hypernym_paths()
            for path in paths:
                for synset in path:
                    word = synset._name.split('.')[0]
                    if word not in r_set:
                        r_set.add(word)
        return r_set

    @staticmethod
    def tokenize(words: str) -> List[str]:
        return word_tokenize(words.lower())

    @staticmethod
    def tag_words(words: List[str]):
        length = len(words)

        for i in range(0, length):
            word = words[i]
            if word.find('-'):
                split = word.split('-')
                is_all_words = True
                for s_word in split:
                    if not LanguageTools.is_word(s_word):
                        is_all_words = False

                if is_all_words:
                    words.pop(i)
                    for j in range(0, len(split)):
                        words.insert(i+j, split[j])
        return nltk.pos_tag(words)

    @staticmethod
    def _get_wordnet_pos(treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        elif treebank_tag.startswith('S'):
            return wordnet.ADJ_SAT
        else:
            return wordnet.NOUN
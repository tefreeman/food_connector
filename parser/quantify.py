import re
from typing import Dict, List
from language_tools import LanguageTools
from word import Word

_neg_prefixes = re.compile(r'\A(un|non)')
_neg_suffixes = re.compile(r'(less|free)$')


def quantify_pre_suf(word_object: Word):
    quant_val = 1

    neg_pre = list(filter(None, _neg_prefixes.split(word_object.word)))
    neg_suf = list(filter(None, _neg_suffixes.split(word_object.word)))

    if len(neg_pre) > 1:
        if LanguageTools.is_word(neg_pre[1]):
            quant_val *= -1
    if len(neg_suf) > 1:
        if LanguageTools.is_word(neg_suf[0]):
            quant_val *= -1

    return quant_val


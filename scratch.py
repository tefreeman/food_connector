from language_tools import LanguageTools


test = LanguageTools.tokenize('Extra-virgin olive oil')
test1 = LanguageTools.tag_words(test)
print(test1)

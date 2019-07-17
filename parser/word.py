from language_tools import LanguageTools


class Word:

    def __init__(self, word: str, stem: str, g_tag: str):
        self.id = -1
        self.word = word
        self.stem = stem
        self.g_tag = g_tag
        self.is_brand = False
        self.is_unique = True
        self.is_word = LanguageTools.is_word(self.stem)
        self.freq = 0

        self.tree = LanguageTools.get_paths(stem, g_tag)
        self.pos_ingredients = set()
        self.neg_ingredients = set()

    def add_ingredient_id(self, ingredient_id: int, quantification_val: int):
        if quantification_val >= 0:
            self.freq += 1
            self.pos_ingredients.add(ingredient_id)
        else:
            self.freq += 1
            self.neg_ingredients.add(ingredient_id)

        if self.freq > 1:
            self.is_unique = False

    def to_json(self):
        return {
            'id': self.id,
            'word': self.word,
            'stem': self.stem,
            'g_tag': self.g_tag,
            'is_brand': self.is_brand,
            'is_unique': self.is_unique,
            'is_word': self.is_word,
            'freq': self.freq,
            'tree': self.tree,
            'pids': list(self.pos_ingredients),
            'nids': list(self.neg_ingredients)
        }

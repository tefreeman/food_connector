from language_tools import LanguageTools
from word import Word
from quantify import quantify_pre_suf
from config import Config
from ingredients_processor import IngredientsProcessor
import pymongo
from brands_processor import BrandsProcessor
from recipe import Recipe, RecipeFeatures
from matcher import Matcher
from probablity import Probability, ProbFeatureKeys
from server import app
import time
from train import Train

def main():
    s1 = time.time()
    IngredientsProcessor()
    print('Ingredient Processor Init Time:  ', time.time() - s1)
    s2 = time.time()
    prob = Probability(500)
    print('Probability Init Time:  ', time.time() - s2)
    print('Starting training from matches col')
    s3 = time.time()
    Train.init_examples()
    print('Training Time:  ', time.time()-s3)
    acc = Train.calc_accuracy()
    print(acc)
    return s1


if __name__ == '__main__':
    s1 =    main()
    app.run(port='5002')
    print('ready after : ', time.time() - s1)

from scipy.stats import norm
from typing import List, Dict, Tuple
import math
from enum import Enum


class KeyType(Enum):
    NUMBER = 0
    F_NUMBER = 1
    LIST = 2
    DICT = 3
    F_DICT = 4


class ProbFeatureKeys(Enum):
    MATCH_COUNT = 0, KeyType.NUMBER
    NON_MATCH_COUNT = 1, KeyType.NUMBER
    REL_MATCH_COUNT = 2, KeyType.NUMBER
    MATCH_FREQ = 3, KeyType.F_NUMBER
    UNKNOWN_MATCH_COUNT = 4, KeyType.NUMBER
    MATCH_G_TAG = 5, KeyType.F_DICT
    MATCH_TREE_COUNT = 6, KeyType.DICT
    TOTAL_MATCH_FREQ = 7, KeyType.NUMBER
    TOTAL_NON_MATCH_FREQ = 8, KeyType.NUMBER
    AVG_MATCH_FREQ = 9, KeyType.NUMBER
    AVG_NON_MATCH_FREQ = 10, KeyType.NUMBER
    MATCH_TREE_DEPTH_FREQ = 11, KeyType.LIST


class BucketFeature:
    def __init__(self, name, min_count = 500):
        self._name = name
        self._min_count = min_count
        self.total = 0
        self.p_total = 0
        self.n_total = 0
        self._counts = {}

    def push(self, bucket: int, type_: bool):
        self.total += 1
        if str(bucket) not in self._counts:
            self._counts[str(bucket)] = [0, 0]
        if type_:
            self._counts[str(bucket)][0] += 1
            self.p_total += 1
        else:
            self.n_total += 1
            self._counts[str(bucket)][1] += 1

    def calc_prob(self, x: int):
        if self.total > self._min_count:
            if str(x) in self._counts:
                return self._counts[str(x)][0] / self._counts[str(x)][1]
        return 1.0

    def get_as_json(self):
        return {self._name: self._counts}

    def get_normalized_match_freq(self, total_examples):
        return self.p_total / total_examples


class Probability:
    _features = {}
    _total_matching_examples = 0
    _total_non_matching_examples = 0
    _activated_features = {}
    _required_num_examples = 0
    _required_match_freq = 0

    def __init__(self, _required_num_examples=500):
        Probability._required_num_examples = _required_num_examples

        if len(Probability._features) < 1:
            Probability.init_feature_distributions()

    @staticmethod
    def init_feature_distributions():
        for feature_key in ProbFeatureKeys:
            if feature_key.value[1] is KeyType.NUMBER or feature_key.value[1] is KeyType.F_NUMBER:
                Probability._features[feature_key.name] = BucketFeature(feature_key.name)
            elif feature_key.value[1] is KeyType.DICT or feature_key.value[1] is KeyType.F_DICT:
                Probability._features[feature_key.name] = {}
            elif feature_key.value[1] is KeyType.LIST:
                Probability._features[feature_key.name] = []
                for i in range(0, 100):
                    Probability._features[feature_key.name].append(BucketFeature(str(i)))

    @staticmethod
    def _check_if_active(f_key, key_str: None):
        if key_str is None:
            if f_key.name in Probability._activated_features:
                return True
        else:
            if f_key.name in Probability._activated_features:
                if key_str in Probability._activated_features[f_key.name]:
                    return True
        return False

    @staticmethod
    def _calc_feature_prob(f_key, x, key_str=None):
        if Probability._check_if_active(f_key, key_str):
            if key_str is None:
                return Probability._features[f_key.name].calc_prob(x)
            else:
                return Probability._features[f_key.name][key_str].calc_prob(x)
        else:
            return 1.0

    @staticmethod
    def _calc_feature_dict_prob(f_key, d: Dict):
        prob = 1.0
        for item in d.items():
            prob *= Probability._calc_feature_prob(f_key, x=item[1], key_str=item[0])
        return prob

    @staticmethod
    def calculate_prob(recipe_feature):
        prob = 1.0
        prob *= Probability._calc_feature_prob(ProbFeatureKeys.MATCH_COUNT, recipe_feature.match_count)
        prob *= Probability._calc_feature_prob(ProbFeatureKeys.NON_MATCH_COUNT, recipe_feature.non_match_count)
        # prob *= Probability._calc_feature_prob(ProbFeatureKeys.REL_MATCH_COUNT, recipe_feature.rel_match_count)
        return prob

    @staticmethod
    def add_example_to_dist(recipe_feature_set, example_state=True):
        g_features = Probability._features
        r_features = recipe_feature_set.get_as_dict()

        for feature in r_features.items():
            if ProbFeatureKeys[feature[0]].value[1] == KeyType.NUMBER:
                g_features[feature[0]].push(feature[1], example_state)
            elif ProbFeatureKeys[feature[0]].value[1] == KeyType.F_NUMBER:
                g_features[feature[0]].push(Probability._bucketize_float(feature[1]), example_state)
            elif ProbFeatureKeys[feature[0]].value[1] == KeyType.DICT:
                Probability._add_dict_to_distribution(g_features[feature[0]], feature[1], example_state)
            elif ProbFeatureKeys[feature[0]].value[1] == KeyType.LIST:
                Probability._add_list_to_distribution(g_features[feature[0]], feature[1], example_state)
            elif ProbFeatureKeys[feature[0]].value[1] == KeyType.F_DICT:
                Probability._add_dict_freq_to_dist(g_features[feature[0]], feature[1], example_state)

        if example_state:
            Probability._total_matching_examples += 1
        else:
            Probability._total_non_matching_examples += 1

    @staticmethod
    def _bucketize_float(f: float, bucket_size=20) -> int:
        n = round(f * 100)
        return bucket_size * round(n / bucket_size)

    @staticmethod
    def _add_list_to_distribution(features: List, li: List[float], example_state):
        length = len(li)
        for i in range(0, length):
            features[i].push(Probability._bucketize_float(li[i]), example_state)

    @staticmethod
    def _add_dict_to_distribution(features: Dict, d: Dict, s: bool):
        for prop in d.items():
            if prop[0] not in features:
                features[prop[0]] = BucketFeature(prop[0])
            features[prop[0]].push(prop[0], s)

    @staticmethod
    def _add_dict_freq_to_dist(features: Dict, d: Dict, s: bool):
        for prop in d.items():
            if prop[0] not in features:
                features[prop[0]] = BucketFeature(prop[0])
            features[prop[0]].push(Probability._bucketize_float(prop[1]), s)

    @staticmethod
    def _find_feature(f_key: ProbFeatureKeys, str_key: str = None):
        if str_key is None:
            return Probability._features[f_key.name]
        else:
            if str_key in Probability._features[f_key.name]and str_key:
                return Probability._features[f_key.name]
            else:
                return None

    @staticmethod
    def _set_feature_status(f_key: ProbFeatureKeys, status: bool, str_key: str = None,):
        if str_key is None:
            if f_key.name not in Probability._activated_features:
                if status:
                    Probability._activated_features[f_key.name] = f_key
            else:
                if not status:
                    del Probability._activated_features[f_key.name]
        else:
            if f_key.name not in Probability._activated_features:
                Probability._activated_features[f_key.name] = {}
            if str_key not in Probability._activated_features[f_key.name]:
                if status:
                    Probability._activated_features[f_key.name][str_key] = str_key
            else:
                if not status:
                    del Probability._activated_features[f_key.name][str_key]

    @staticmethod
    def _check_num_examples(feature_key: ProbFeatureKeys, key_str: str = None):
        if key_str is None:
            feature: BucketFeature = Probability._features[feature_key.name]
        else:
            if key_str in Probability._features[feature_key.name]:
                feature: BucketFeature = Probability._features[feature_key.name][key_str]
            else:
                return False
        normalized_match_freq = feature.get_normalized_match_freq(Probability._total_matching_examples)
        if feature.total >= Probability._required_num_examples and normalized_match_freq > Probability._required_match_freq:
            return True
        else:
            return False

    @staticmethod
    def check_set_feature_status():
        for feature_key in ProbFeatureKeys:
            if feature_key.value[1] is KeyType.NUMBER:
                if Probability._check_num_examples(feature_key):
                    Probability._set_feature_status(feature_key, True)

            elif feature_key.value[1] is KeyType.DICT:
                for str_key in Probability._features[feature_key.name].keys():
                    try:
                        if Probability._check_num_examples(feature_key, str_key):
                            Probability._set_feature_status(feature_key, True, str_key)
                    except:
                        pass

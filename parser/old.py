
class NormFeature:
    def __init__(self):
        self._num_examples = 0
        self._sum = 0
        self._mean = 0

        self._old_sum = 0
        self._old_mean = 0

        self.distribution = norm(loc=self.get_mean(), scale=self.get_standard_deviation())

    def get_cdf(self, x):
        return norm(loc=self.get_mean(), scale=self.get_standard_deviation()).pdf(x)

    def push(self, x):
        self._num_examples += 1

        if self._num_examples == 1:
            self._old_mean = x
            self._mean = x
            self._old_sum = 0.0
        else:
            self._mean = self._old_mean + (x - self._old_mean) / self._num_examples
            self._sum = self._old_sum + (x - self._old_mean) * (x - self._mean)

            self._old_mean = self._mean
            self._old_sum = self._sum

    def get_num_examples(self):
        return self._num_examples

    def get_mean(self):
        return self._mean

    def get_variance(self):
        if self._num_examples > 1:
            return self._sum / (self._num_examples - 1)
        else:
            return 0.0

    def get_standard_deviation(self):
        return math.sqrt(self.get_variance())

    def get_as_json(self):
        return [self.get_num_examples(), self.get_mean(), self.get_variance(), self.get_standard_deviation()]

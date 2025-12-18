import random

class SingleGoodHistogram:
    def __init__(self, bucket_size, bid_upper_bound):
        self.bucket_size = bucket_size
        self.bid_upper_bound = bid_upper_bound
        self.buckets = {}
        for b in range(0, bid_upper_bound, bucket_size):
            self.buckets[b] = 0.0
        self.total = 0.0

    def get_bucket(self, price):
        bucket = int(price // self.bucket_size) * self.bucket_size
        if bucket > self.bid_upper_bound:
            bucket = self.bid_upper_bound
        return bucket

    def add_record(self, price):
        """
        Add a price to the histogram.
        Increment the frequency of the bucket that contains the price.
        """
        for p in price:
            bucket = self.get_bucket(p)
            self.buckets[bucket] += 1
            self.total += 1
        # Update the bucket frequencies

    def smooth(self, alpha):
        """
        Smooth the histogram using the technique described in the handout.
        """

        for b in self.buckets:
            self.buckets[b] = (1 - alpha) * self.buckets[b]

    def update(self, new_hist, alpha):
        """ 
        Actually updating the histogram with new information: 
        1. Smooth the current histogram.
        2. Add the new histogram to the current histogram.
        """
        self.smooth(alpha)
        for b in self.buckets:
            self.buckets[b] += alpha * new_hist.buckets[b]
        self.total = sum(self.buckets.values())

    def sample(self):
        """ 
        Return a random sample from the histogram. 
        """
        r = random.uniform(0, self.total)
        cumulative = 0.0
        for bucket, frequency in self.buckets.items():
            cumulative += frequency
            if r <= cumulative:
                return bucket 

    
    def __repr__(self):
        return str(self.buckets)
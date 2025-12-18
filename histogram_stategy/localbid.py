from marginal_value import calculate_expected_marginal_value
from independent_histogram import IndependentHistogram


def expected_local_bid(goods, valuation_function, price_distribution, num_iterations=100, num_samples=50):
    """
    Iteratively computes a bid vector by updating bids to be the expected marginal value for each good.
    """
    b_old = {g: valuation_function({g}) for g in goods}

    for _ in range(num_iterations):
        b_new = b_old.copy()
        for selected_good in goods: #All is done in terms of dictionnary (not lists index)
            MV = calculate_expected_marginal_value(goods,selected_good,valuation_function,b_old,price_distribution)
            b_new[selected_good] = MV
        b_old = b_new

    return b_old

if __name__ == "__main__":
    def valuation(bundle): 
        if len(bundle) == 1: 
            return 10 
        elif len(bundle) == 2:
            return 80 
        elif len(bundle) == 3: 
            return 50 
        else: 
            return 0
    
    print(expected_local_bid(
        goods=["a", "b", "c"],
        valuation_function=valuation,
        price_distribution=IndependentHistogram(["a", "b", "c"], 
                                                [5, 5, 5], 
                                                [100, 100, 100]),
        num_iterations=10,
        num_samples=1000
    ))
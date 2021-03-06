from __future__ import unicode_literals

import numpy as np


def knn_density(x, data, k):
    """
        K nearest neighbor density estimate.

        References:
            Silverman (1986): Density Estimation for Statistics
            and Data Analysis. CRC press.

        Input:
            x       -   points where density is to be estimated.
            data    -   data set (one-dimensional).
            k       -   parameter for estimation.
    """
    data_sort = np.sort(data)
    I_k = [(data_sort[i], data_sort[i+k-1]) for i in range(len(data_sort)-k+1)]
    #d_k = [I_k_[1] - I_k_[0] for I_k_ in I_k]
    x_d_ks = [[max(x_-I_k_[0], I_k_[1]-x_) for I_k_ in I_k if x_ >= I_k_[0] and x_ <= I_k_[1]] for x_ in x]
    x_d_k = np.array([min(d_ks) if len(d_ks) > 0 else np.nan for d_ks in x_d_ks])
    x_d_k[x < data_sort[0]] = data_sort[k-1] - x[x < data_sort[0]]
    x_d_k[x > data_sort[-1]] = x[x > data_sort[-1]] - data_sort[-k]
    return k/(2*len(data)*x_d_k)


def auto_interval(data, k=5, beta=0.2, xmin=None, xmax=None, dx=None):
    """
        Selects an interval where the estimated density is above 
        beta divided by the length of [xmin, xmax], with the purpose to 
        leave outliers outside the interval.

        Input:

            data    -   data set (one-dimensional).
            k       -   parameter for knn density estimate.
            beta    -   parameter for density bound.
            xmin    -   lowest possible value for interval (also
                        affects density bound).
            xmax    -   highest possible value for interval (also
                        affects density bound).
            dx      -   grid size for which densities should be
                        estimated.
    """
    if xmin is None:
        xmin = np.min(data)
    if xmax is None:
        xmax = np.max(data)
    if dx is None:
        dx = (xmax-xmin)*1e-4
    dens_bound = beta/(xmax-xmin)
    x = np.arange(xmin, xmax+dx, dx)
    above_bound = x[knn_density(x, data, k) > dens_bound]
    return above_bound[0], above_bound[-1]


def get_I(data, I):
    if I is None:
        return (-np.inf, np.inf)
    if I == 'auto':
        return auto_interval(data)
    try:
        lower, upper = I
        return lower, upper
    except:
        I = I.copy()
        if not I.pop('type') == 'auto':
            raise ValueError("Wrong format of I, I = {}".format(I))
    return auto_interval(data, **I)


if __name__ == '__main__':

    import matplotlib.pyplot as plt

    data = np.random.randn(100)
    x = np.linspace(-3, 3, 200)
    k = 10
    plt.plot(x, knn_density(x, data, k))

    import statsmodels as sm
    faithful = sm.datasets.get_rdataset("faithful")
    data = faithful.data.eruptions
    x = np.linspace(0, 6, 200)
    k = 20
    plt.figure()
    plt.plot(x, knn_density(x, data, k))
    plt.hist(faithful.data.eruptions, np.arange(1.5, 5.5, 0.5), normed=True)
    xmin, xmax = auto_interval(data)
    plt.axvline(xmin)
    plt.axvline(xmax)
    plt.show()

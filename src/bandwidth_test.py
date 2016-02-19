import numpy as np
from scipy.signal import argrelextrema
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt

from .util.ApproxGaussianKDE import ApproxGaussianKDE as KDE


def silverman_bandwidth_pval(data, N_bootstrap=1000):
    h_crit = critical_bandwidth(data)
    var_data = np.var(data)
    KDE_h_crit = KernelDensity(kernel='gaussian', bandwidth=h_crit).fit(data.reshape(-1, 1))
    smaller_equal_crit_bandwidth = np.zeros((N_bootstrap,), dtype=np.bool_)
    for n in range(N_bootstrap):  # CHECK: Rescale bootstrap sample towards the mean?
        smaller_equal_crit_bandwidth[n] = is_unimodal_kde(
            h_crit, KDE_h_crit.sample(len(data)).ravel()/np.sqrt(1+h_crit**2/var_data))
    return np.mean(~smaller_equal_crit_bandwidth)


def critical_bandwidth(data, htol=1e-3):
    hmax = (np.max(data)-np.min(data))/2.0
    return bisection_search_unimodal(0, hmax, htol, data)


def bisection_search_unimodal(hmin, hmax, htol, data):
    '''
        Assuming fun(xmax) < 0.
    '''
    if hmax-hmin < htol:
        return (hmin + hmax)/2.0
    hnew = (hmin + hmax)/2.0
    #print "hnew = {}".format(hnew)
    if is_unimodal_kde(hnew, data):  # upper bound for bandwidth
        return bisection_search_unimodal(hmin, hnew, htol, data)
    return bisection_search_unimodal(hnew, hmax, htol, data)


def is_unimodal_kde(h, data):
    xtol = h*0.1  # TODO: Compute error given xtol.
    kde = KDE(data, h)
    x_new = np.linspace(np.min(data), np.max(data), 10)
    x = np.zeros(0,)
    y = np.zeros(0,)
    while True:
        y_new = kde.evaluate_prop(x_new)
        x = merge_into(x_new, x)
        y = merge_into(y_new, y)
        # fig, ax = plt.subplots()
        # ax.plot(x, y)
        # ax.scatter(x, y, marker='+')
        # ax.scatter(x_new, y_new, marker='+', color='red')
        if len(argrelextrema(np.hstack([[0], y, [0]]), np.greater)[0]) > 1:
            return False
        if x[1] - x[0] < xtol:
            return True
        x_new = (x[:-1]+x[1:])/2.0


def merge_into(z_new, z):
    if len(z) == 0:
        return z_new
    z_merged = np.zeros((2*len(z)-1,))
    z_merged[np.arange(0, len(z_merged), 2)] = z
    z_merged[np.arange(1, len(z_merged), 2)] = z_new
    return z_merged

if __name__ == '__main__':

    if 1:
        import time
        N = 1000
        data = np.hstack([np.random.randn(N/2), np.random.randn(N/4)+4])
        h = 0.1
        print "is_unimodal_kde(h, data) = {}".format(is_unimodal_kde(h, data))
        #plt.show()
        t0 = time.time()
        h_crit = critical_bandwidth(data)
        print "critical_bandwidth(data) = {}".format(h_crit)
        t1 = time.time()
        print "silverman_bandwidth_pval(data) = {}".format(silverman_bandwidth_pval(data))
        t2 = time.time()
        print "Critical bandwidth computation time: {}".format(t1-t0)
        print "Silverman test computation time: {}".format(t2-t1)

        fig, ax = plt.subplots()
        ax.hist(data, bins=50, normed=True)
        x_grid = np.linspace(np.min(data)-2, np.max(data)+2, 100)
        ax.plot(x_grid, KDE(data, h_crit).evaluate(x_grid), linewidth=2, color='black')
        plt.show()

    if 0:
        data = np.random.randn(1000)
        h = .5
        print "np.std(data) = {}".format(np.std(data))
        resamp = KernelDensity(kernel='gaussian', bandwidth=h).fit(data).sample(1000)/np.sqrt((1+h**2/np.var(data)))
        print "np.std(resamp) = {}".format(np.std(resamp))
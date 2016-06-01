import numpy as np


def sample_linear_density(nsamp, x0, w, y0, y1):
    m = y0
    k = y1-y0
    u = np.random.rand(nsamp)
    if k != 0:
        q = m/k
        return (-q + np.sign(q)*np.sqrt(q**2+(1+2*q)*u))*w + x0
    return u*w + x0


def fp_blurring(data, w):
    '''
        Blurs data using the frequency polygon. Data is assumed to
        be binned with bin width w. Purpose of blurring is to counter
        effect of binning.

        Ref: Minnotte (1997): Nonparametric Testing of Existence of Modes.

    '''
    y, x = np.histogram(data, bins=np.arange(min(data)-w/2, max(data)+1.5*w, w))
    y_count = np.hstack([[0], y, [0]])
    x_fp = np.zeros(2*len(x)-1)
    x_fp[0::2] = x
    x_fp[1::2] = (x[1:]+x[:-1])/2
    y_fp = np.zeros(2*len(x)-1)
    y_fp[1::2] = y
    y_fp[::2] = (y_count[1:]+y_count[:-1])*1./2

    n_fp = np.zeros(2*len(y), dtype=np.int)
    p_left = (y_count[:-2] + 3*y_count[1:-1])*1./(y_count[:-2] + 6*y_count[1:-1] + y_count[2:])
    n_fp[0::2] = np.random.binomial(y, p_left)
    n_fp[1::2] = y - n_fp[0::2]
    data_fp = []
    for n, x0, y0, y1 in zip(n_fp, x_fp[:-1], y_fp[:-1], y_fp[1:]):
        data_fp.append(sample_linear_density(n, x0, w*1./2, y0, y1))
    data_blurred = data.copy().astype(np.float)
    for i, (x0, x1) in enumerate(zip(x[:-1], x[1:])):
        ind = (data >= x0)*(data < x1)
        if len(ind) > 0:
            data_blurred[ind] = np.hstack(data_fp[(2*i):(2*i+2)])
    return data_blurred
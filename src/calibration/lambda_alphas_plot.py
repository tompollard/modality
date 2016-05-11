# lambda_alpha according to Hall & York 2001.
import numpy as np
import matplotlib.pyplot as plt

from .lambda_alphas_access import load_lambdas, print_all_lambdas

if 0:
    ## Hall-York calibration curve
    a1 = 0.94029
    a2 = -1.59914
    a3 = 0.17695
    a4 = 0.48971
    a5 = -1.77793
    a6 = 0.36162
    a7 = 0.42423

    lambda_al = lambda alpha: (a1*alpha**3 + a2*alpha**2 + a3*alpha + a4)/(alpha**3 + a5*alpha**2 + a6*alpha + a7)

    print "lambda_al(0.1) = {}".format(lambda_al(0.1))

    fig, ax = plt.subplots()

    alpha = np.linspace(0, 1)
    ax.plot(alpha, lambda_al(alpha))

    #alphas_comp = [0.03, 0.05, 0.1, 0.3]
    alphas_comp = [0.03, 0.05]
    test = 'bw'
    null = 'shoulder'
    lambda_alphas_comp = []
    for i, alpha in enumerate(alphas_comp):
        lambda_alphas_comp.append(load_lambdas(test, null, alpha))
    print "lambda_alphas_comp = {}".format(lambda_alphas_comp)

    for alpha, lambda_alphas in zip(alphas_comp, lambda_alphas_comp):
        ax.plot([alpha]*2, lambda_alphas, linewidth=4)
        ax.scatter([alpha]*2, lambda_alphas, marker='+', s=3)

    #fig.savefig('lambda_alpha_{}_{}.pdf'.format(test, null), format='pdf', bbox_inches='tight')
    plt.show()

if 1:

    alphas = np.arange(0.01, 0.99, 0.01)
    test = 'dip'
    null = 'normal'
    lambdas = 0*alphas
    for i, alpha in enumerate(alphas):
        lambdas[i] = load_lambdas(test, null, alpha)
    plt.plot(alphas, lambdas)

    test = 'dip'
    null = 'shoulder'
    lambdas = 0*alphas
    for i, alpha in enumerate(alphas):
        lambdas[i] = load_lambdas(test, null, alpha)
    plt.plot(alphas, lambdas)

    plt.show()


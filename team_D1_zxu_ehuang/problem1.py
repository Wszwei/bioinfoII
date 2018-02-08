""" 
Input: a positive integer n<=50
    
Output: An array A of length 2n in which A[k] represents the common logarithm 
of the probability that two diploid siblings share at least k of their 
2n chromosomes (we do not consider recombination for now).
"""

import math
import sys
from scipy.special import comb
from argparse import ArgumentParser


def binom(n, k, p=0.5):
    """ return P(X = k) where X ~ Binom(n,p) """
    return comb(n,k, False)*math.pow(p,k) * math.pow((1-p),(n-k))

def make_array(n):    
    """ 
    Creates array out of length 2n in which A[k] represents common log
    of the probability that two diploid siblings share at least k of their
    2n chromosomes (not considering recombination)
    """
    
    
    # Creates array binom_prob in which binom_prob[k] = P(X = k) 
    # where X ~ Binom(2*n, 1/2)
    binom_prob = []    
    iterate = list(range(2*n,-1,-1))
    iterate.reverse()
    for k in iterate:
        probability = binom(2*n, k)        
        binom_prob.append(probability)

    # Calculates cumulative binomial probability, 
    # excluding the first i values in binom_prob
    out = [math.log10(sum(binom_prob[:i])) for i in range(2*n, 0, -1)]    
    return out


def main(n):
    if n <= 0 or n>50:
        sys.stderr.write('integer input must be >0 and <=50\n')
        return
    print(make_array(n))
    
        
if __name__ == '__main__':
    parser = ArgumentParser(
            description='sample',
            prog='problem1.py')
    parser.add_argument('n', help='a positive integer n<=50',
                        type=int)
    args = parser.parse_args()
    main(args.n)




""" 
Input: a positive integer n<=50
    
Output: An array A of length 2n in which A[k] represents the common logarithm 
of the probability that two diploid siblings share at least k of their 
2n chromosomes (we do not consider recombination for now).
"""
# Eric Huang
# Group D, Problem 1 

import math
import sys
from scipy.special import comb


def binom(n, k, p=0.5):
    """ return P(X = k) where X ~ Binom(n,p) """
    return comb(n,k, False)*math.pow(p,k) * math.pow((1-p),(n-k))

def make_array(n):  
    # binom_prob[k]=P(X = k) where X ~ Binom(2*n, 1/2)
    binom_prob = []    
    iterate = list(range(2*n,-1,-1))
    iterate.reverse()
    for k in iterate:
        probability = binom(2*n, k)        
        binom_prob.append(probability)
    #print(binom_prob)

    out = [math.log10(sum(binom_prob[:i])) for i in range(2*n, 0, -1)]    
    return out

def main():
    print(make_array(int(sys.argv[1])))
    
        
if __name__ == '__main__':
    main()


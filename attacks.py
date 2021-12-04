import liblll
from merkle_hellman import *

def crack(public_key, ciphertext, l=None):
	## low density
    if l == None:
        matrix = liblll.create_matrix_from_knapsack(public_key, ciphertext)
        reduced_basis = liblll.lll_reduction(matrix)
        guess = liblll.best_vect_knapsack(reduced_basis)
        if 1 in guess:
            return convert_bits_to_string(''.join([str(x) for x in guess]))
	## shamir attack
    else:
        matrix = liblll.create_matrix_from_knapsack_shamir(public_key, l)
        reduced_basis = liblll.lll_reduction(matrix)
        guess = liblll.best_vect_knapsack_shamir(reduced_basis)
        _int = 2 ** ((l - 1) * l / 4 + (l - 1) * (len(public_key) - 2)) / guess[0].denominator
        u = (guess[0].numerator * _int)
        K = public_key[0]
        if u < 0:
            u *= -1
        sup_incr_seq = [0 for i in range(len(public_key))]

        for i in range(len(public_key)):
            sup_incr_seq[i] = (u * public_key[i]) % K
        if check_is_superincr(sup_incr_seq):
            d = increase_seq_solve(sup_incr_seq, ciphertext, u, K)
            return ''.join([str(x) for x in d])


def check_is_superincr(seq):
    n = len(seq)
    s = seq[0]
    for i in range(1, n):
        if seq[i] > s:
            s += seq[i]
        else:
            return False
    return True

def increase_seq_solve(seq, cipher, u, K):
    d = ['0' for i in range(len(seq))]
    s = cipher * u % K
    for i in range(len(seq) - 1, 0, -1):
        if s >= seq[i]:
             d[i] = '1'
             s -= seq[i]
    return d

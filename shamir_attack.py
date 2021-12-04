import time
from random import choice
import string
from attacks import *
from merkle_hellman import *


def attack(text):
    message = convert_string_to_bits(text)
    n = len(message)
    private_key, public_key, q, r = generate_keys(n)
    cipher = encrypt(message, public_key)
    t1 = time.clock()
    cracked = crack(public_key, cipher, 5)
    t2 = time.clock()
    if cracked is None:
        success = False
    else:
        print(cracked, message)
  #      print((private_key, public_key, q, r, text, message, cipher))
        success = True
    return success, t2 - t1


num_tests = 100
accuracy = {}
runtime = {}
chars = string.ascii_letters + string.digits + string.punctuation
for l in range(4, 13):
    correct = 0
    total_time = 0
    for i in range(num_tests):
        random_text = ""
        for n in range(l):
            random_text += choice(chars)
        success, working_time = attack(random_text)
        total_time += working_time
        if success:
            correct += 1
    accuracy[l] = correct / float(num_tests)
    runtime[l] = total_time / float(num_tests)
    print '%d : accuracy = %f : runtime = %f' % (8 * l, accuracy[l], runtime[l])


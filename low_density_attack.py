import time
from random import choice
import string
from merkle_hellman import *
from attacks import crack

def attack(text):
    message = convert_string_to_bits(text)
    n = len(message)
    private_key, public_key, q, r = generate_keys(n)
    cipher = encrypt(message, public_key)
    t1 = time.clock()
    cracked = crack(public_key, cipher)
    if cracked is None:
        success = False
    else:
        success = True
    #    print public_key
    #    print private_key
    #    print text
        print (message, cracked)
    #    print (q, r)
##    print success
    return success, time.clock() - t1

num_tests = 100
accuracy = {}
runtime = {}
chars = string.ascii_letters + string.digits + string.punctuation
for l in range(2, 11):
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

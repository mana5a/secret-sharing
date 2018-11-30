# import shamir_secret_sharing
from Crypto.Random import random as rn
import random
from Crypto.Util import number 

#To make it simple, we give the f(X)=5+3x+8x^2 as params. It is easy to do
# the test and write the code.

"""
Generate prime 
"""
p = rn.getrandbits(256)
g = 2
h = number.getPrime(256)



def create_verifies(params1, params2, p, g, h):
    verifies = []   
    for i in range(0, len(params1)):
        verifies.append((pow(g, params1[i], p) * pow(h, params2[i], p)) % p)
    return verifies




"""
Computes the LHS of the verification equation of Pedersen's VSS
"""
def lhs(verfies, i, t, p):
    powerall = [1]
    for each_t in range(1, t):
        powerall.append(int(pow(i, each_t)))
    left_val = 1
    for j in range(0, len(verfies)):
        c = pow(verfies[j], powerall[j], p)
        left_val *= c
        left_val %= int(p)
    return left_val % p

"""
"""
def verifies_shares(secrets1, secrets2, verifies, params,p,g):
    for i in range(0, len(secrets1)):
        left_value = lhs(verifies, i+1, len(params), p)
        right_value = (pow(g, (secrets1[i])%p, p)*pow(h, (secrets2[i])%p, p))%p
        if left_value == right_value:
            print ("Secret %d checked" % i)
        else:
            print ("Secret  %d modified" % i)



def encode(n):
    x = ord(n)
    if x > 32 and x < 127:
        return x - 33
    else:
        return -1


"""
Generates random prime number
SystemRandom generates large numbers
"""
def genRand(m):
    return random.SystemRandom().randint(0, m)

"""
Converts the given string to an integer of base 94 because all the keyboard ascii characters lie betwee 32 and 127
"""
def StringtoInt(s):
    n = len(s)
    f = 0
    for i in range(n):
        # create integer from base 94 string (characters)
        f += encode(s[i]) * (94 ** (n - i - 1))
    return f

def gen_params(s, min_party, prime):
    params = [s]
    for i in range(1, min_party):
        params.append(genRand(prime//40))
    return params

"""
Divides the key in to n parts respresenting each player
"""
def create_secret(parties, params, prime):
    secrets = []
    for i in range(1, parties):
        secret = params[0]
        for j in range(1, len(params)):
            secret += (params[j] * (pow(i, j, prime))) % prime
        secrets.append(int(secret % prime))
    return secrets

"""
Returns the mod inverse for the prime number
"""
def modInversePrime(k, prime):
    return pow(k, prime-2, prime)
"""
This function constructs the secrets from the given byte string formed from the original
text which is passed
"""
def construct_secret(secrets, min_party, prime):
    secret_pos = []
    for i in range(0, min_party):
        while True:
            value = genRand(len(secrets)-1)+1
            if value in secret_pos:
                continue
            else:
                break
        secret_pos.append(value)
    multi_all = 1
    for i in range(0, min_party):
        multi_all *= secret_pos[i]
        if len(secret_pos) % 2 == 0:
            multi_all *= -1
    ret = 0
    for i in range(0, min_party):
        lower = 1
        upper = multi_all / secret_pos[i]
        for j in range(0, min_party):
            if j == i:
                continue
            else:
                lower *= ((secret_pos[i] - secret_pos[j]) % prime)
                lower %= prime
        ret = int(((upper * modInversePrime(lower, prime)* secrets[secret_pos[i]-1])+prime+ret) % prime)
    return ret


def main():
    secret_string = "secrete"
    party = 3
    min_party = 2
    ##
    s = StringtoInt(secret_string)
    parties = int(party)
    min_party = int(min_party)
    params1 = gen_params(s, min_party, p)
    params2 = gen_params(s, min_party, p)
    secrets1 = create_secret(parties, params1, p)
    secrets2 = create_secret(parties, params2, p)
    secret = construct_secret(secrets1, min_party, p)
    verifies = create_verifies(params1, params2, p, g, h)
    verifies_shares(secrets1, secrets2, verifies, params2, p, g)
    print ("The secret you gave is " ,params1[0], "\n")

    print ("The rejoin code is " , secret)
    if params1[0] == secret:
        print ("Secret Recreated Succesfully")
    else:
        print ("Secret Could not be recreated")

    #We change secret2 3's secret and see whether we can check it out
#    secrets2[3] -= 1
    verifies_shares(secrets1, secrets2, verifies, params2, p, g)


main()

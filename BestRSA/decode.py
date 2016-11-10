import sympy
import os

def inv(x, m):
    return sympy.invert(x, m)

def crt_speedup_decrypt(cipher_text, private_key, primes, count_of_primes, n):
    plain_text = 0 

    for p, count in zip(primes, count_of_primes):
        m = p ** count
        phi_m = (p ** (count - 1)) * (p - 1)
        c = cipher_text % m
        remainder = pow(c, private_key % phi_m, m)
        M = n // m
        M_inv = inv(M, m)

        plain_text = (plain_text + remainder * M * M_inv) % n

    return plain_text

def get_prime_under(n):
    primes = [2]
    for i in range(3, n):
        sqrt = i ** (0.5)
        for p in primes:
            if p <= sqrt:
                if i % p == 0:
                    break
            else:
                primes.append(i)
                break
    return primes

def prime_factorize(n):
    primes = get_prime_under(65538)
    count = [0] * len(primes)
    for idx in range(len(primes)):
        while n % primes[idx] == 0 and n != 1:
            count[idx] += 1
            n = n // primes[idx]
    return primes, count, n

def phi_function(primes, count_of_primes):
    phi = 1
    for (p, c) in zip(primes, count_of_primes):
        phi = phi * ((p ** (c - 1)) * (p - 1))
    return phi


def main():
    with open('best_rsa.txt') as fp:
        data = [line.strip().split(' = ')[1] for line in fp]

    e = int(data[0])
    n = int(data[1])
    cipher_text = int(data[2])

    print('calculate prime factors')
    primes, count_of_primes, rest = prime_factorize(n)
    new_primes, new_count = [], []
    # output prime factors
    print('prime factors')
    for p, c in zip(primes, count_of_primes):
        if c > 0:
            print(p, ':', c)
            new_primes.append(p)
            new_count.append(c)
    print('rest: ', rest)
    primes, count_of_primes = new_primes, new_count
    
    print('calculate private key')
    phi_n = phi_function(primes, count_of_primes)
    private_key = int(inv(e, phi_n))
    print('decrypt plain text')
    plain_text = crt_speedup_decrypt(cipher_text, private_key, primes, count_of_primes, n)

    with open('flag', 'w') as fp:
        fp.write(hex(plain_text)[2:])
    os.system('xxd -r -ps flag > flag.gif')
if __name__ == '__main__':
    main()

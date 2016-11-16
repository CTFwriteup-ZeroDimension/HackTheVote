import telnetlib

def connect(host, ip):
    return telnetlib.Telnet(host, ip)

def readline(tel):
    return tel.read_until(b'\n').decode('utf8')

def pad(s):
    if len(s)%9 == 0:
        return s
    for i in range((9-(len(s)%9))):
        s.append(0)
    return s

def decode(seed, res):
    IV = []
    seed = pad(seed)
    print(seed)
    for i in range(9):
        if (len(seed) // 9) % 2 == 1:
            x = res[i//3][i%3]
        else:
            x = res[i%3][i//3]
        for j in range(len(seed)//9):
            if (i != 0) and (i != 8):
                print(i)
                if j % 2 == 0:
                    x ^= seed[i + j*9]
                else:
                    if (i%2) == 0:
                        x ^= seed[(8-i) + j*9]
                    else:
                        if i == 1:
                            x ^= seed[3 +j*9]
                        elif i == 3:
                            x ^= seed[1 +j*9]
                        elif i == 5:
                            x ^= seed[7 +j*9]
                        elif i == 7:
                            x ^= seed[5 +j*9]
            else:
                x ^= seed[i + j*9]

        IV.append(x)

    return IV[::3]+IV[1::3]+IV[2::3]
def main():
    connection = connect('vermatrix.pwn.democrat', '4201')
    line = readline(connection)
    seed = line.split(': ')[1][:-1]
    print(seed)
    res = []
    line = readline(connection)
    res.append([int(x) for x in line.strip().split(' ')])
    print(line)
    line = readline(connection)
    res.append([int(x) for x in line.strip().split(' ')])
    print(line)
    line = readline(connection)
    res.append([int(x) for x in line.strip().split(' ')])
    print(line)
    print(res)
    IV = decode([ord(c) for c in seed], res)
    connection.write((','.join([str(x) for x in IV])).encode('utf8'))
    print(readline(connection))
    
if __name__ == '__main__':
    main()
    

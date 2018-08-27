#!/usr/bin/python3

# RSA Common Modulus Attack
# described here: http://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf#page=4

def factor(n, e, d):
    """http://crypto.stackexchange.com/a/25910/17884

    n - modulus
    e - public exponent
    d - private exponent
    returns - (p, q) such that n = p*q
    """
    from fractions import gcd
    from random import randint

    while True:
        z = randint(2, n - 2)
        k, x = 0, e * d - 1

        while not x & 1:
            k += 1
            x //= 2

        t = pow(z, x, n)
        if t == 1 or t == (n - 1):
            continue

        bad_z = False
        for _ in range(k):
            u = pow(t, 2, n)

            if u == -1 % n:
                bad_z = True
                break

            if u == 1:
                p = gcd(n, t - 1)
                q = gcd(n, t + 1)
                assert n == p * q
                return p, q
            else:
                t = u

        if bad_z:
            continue

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x % m

def int_to_bin(n):
    binary = "{0:b}".format(plaintext)
    padding = (-len(binary) % 8) * "0"
    return padding + "{0:b}".format(plaintext)

def bin_to_str(b):
    import re
    return ''.join([chr(int(a, 2)) for a in re.findall('.{8}', b)])


# Alice's parameters
n = 19141787703521327390286370056875171594005886931320250659244134338981216112108952347954687473567564393213842444896016521745392359013294685479043627948409453256183505070146049086417516658470295063843337680836188135765422963418102676282978294020691341100869807673648250765346605825652828979015194292050045046751622010464091013970451954358743407892698397111199514992931319891190979966578126160693109385080730666746459584421720880855816414313585704166853162097314990917925530383702508176678560932269462903488356565005578968769223359341918619788938547932964103190016633520724351495747308446250305137153917895819082215796133
e = 3
d = 12761191802347551593524246704583447729337257954213500439496089559320810741405968231969791649045042928809228296597344347830261572675529790319362418632272968837455670046764032724278344438980196709228891787224125423843615308945401784188652196013794227400579871782432167176897737217101885986010129528033363364500896868372553204811641432289487210757759960161495262587114360257116105245440202963387232476059260221156790159047563440066928938924515978603056162783022771816004510479652971475855793478644515116054218724102826754154686918637858792618192507809311495753572634978708673068117161417763576515529050078521215534286579
c = 1965117917694938217375302220366398539902763064795622108041136745791388440275738900007815975893346051478958400276904491764508944567602447712645320520982038984551878860380633480547223813546655449554741793730049844094462927464399551456032404719973871551652852624807274951905716310391309072361894414294308621221246338840684074793516062795000751874942922228835158990726055333625059726023625112572345001495757869114557002925692227243621706957773577185070850008196901198041447818149122619756246375483954472276952781283235766029561185819346955953603891369326956246308177504570137438621107955957371993287782643422359515688643

# Factor the modulus
p, q = factor(n, e, d)

# Get Bob's private key
phi = (p - 1) * (q - 1)
e = 65537
d = modinv(e, phi)

plaintext = pow(c, d, n)
print(bin_to_str(int_to_bin(plaintext)))
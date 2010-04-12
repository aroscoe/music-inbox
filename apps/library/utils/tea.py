def encrypt(value, key):
    '''
    Encrypts value with key using the Tiny Encryption Algorithm.
    
    * value has to be an integer or a long
    * key has to be an integer array of length 4
    '''
    v0 = value >> 32; v1 = value & 0xFFFFFFFFL; sum=0
    delta=0x9e3779b9
    k0=key[0]; k1=key[1]; k2=key[2]; k3=key[3]
    for i in xrange(32):
        sum += delta
        v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1)
        v0 &= 0xFFFFFFFFL
        v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3)
        v1 &= 0xFFFFFFFFL
    
    return (v0 << 32) | (v1 & 0xFFFFFFFFL)

def decrypt(value, key):
    '''
    Decrypts a value with key using the Tiny Encryption Algorithm.
    
    * value has to be a long
    * key has to be an integer array of length 4
    '''
    v0 = value >> 32; v1 = value & 0xFFFFFFFFL; sum=0xC6EF3720
    delta=0x9e3779b9                 
    k0=key[0]; k1=key[1]; k2=key[2]; k3=key[3]
    for i in xrange(32):
        v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3)
        v1 &= 0xFFFFFFFFL
        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1)
        v0 &= 0xFFFFFFFFL
        sum -= delta
    return (v0 << 32) | (v1 & 0xFFFFFFFFL)


import random

#  ---------------Message to Encrypt------------------
message = "I have always thought the actions of men the best interpreters of their thoughts."
#  ---------------------------------------------------


#Max range for RSA Primes - User Selected
primeRange = 200


# ---------------Functions--------------------
#Test if Random Numbers are Prime (deterministic)
def isPrime(n):
  if n == 2 or n == 3: return True
  if n < 2 or n%2 == 0: return False
  if n < 9: return True
  if n%3 == 0: return False
  r = int(n**0.5)
  f = 5
  while f <= r:
    if n%f == 0: return False
    if n%(f+2) == 0: return False
    f +=6
  return True  

#initial prime number "guesses"
pKey = random.randrange(primeRange)
qKey = random.randrange(primeRange)

def genPrimes(pKey, qKey):
  # Are the guesses Primes?>Try Again
  while not isPrime(pKey):
  	  pKey = random.randrange(primeRange)
  while not isPrime(qKey):
	  qKey = random.randrange(primeRange)
  return (pKey, qKey)

#Modified gcd function from Math Mod. 
def checkCoPrime(a, b):
	while b:
		a, b = b, a%b
	if a == 1: return True
	return False
	
def egcd(c, d):
    if c == 0:
        return (c, 0, 1)
    else:
        g, y, x = egcd(d % c, c)
        return (g, x - (d // c) * y, y)

#Modular Inverse Formula
def modinv(c, m):
    g, x, y = egcd(c, m)
    #if g != 1:
    #    raise Exception('modular inverse does not exist')
    #else:
    return x % m
	
  
def genKey(pPrime, qPrime):
	n = pPrime * qPrime
	phi = (pPrime - 1) * (qPrime - 1)
	
	#Find a coPrime e value (Public Key)
	e = random.randint(1, phi)
	coPrime = checkCoPrime(e, phi)
	while not coPrime:
		e = random.randint(1, phi)
		coPrime = checkCoPrime(e, phi)
    #Find a multiplicative inverse for the coPrimes (Private Key)
	h = modinv(e, phi)
    
	return ((e,n), (h,n))
	
def encrypt(private, inText):
	key1, n = private
	cipher = [(ord(char) ** key1) % n for char in inText]
	return cipher
	
def decrypt(public, outText):
	key2, n = public
	plain = [chr((char ** key2) % n) for char in outText]
	return ''.join(plain)
  
    
# -------------------Main Block-------------------
#Set as equal nonprimes so we must guess new
pPrime = 2
qPrime = 2

#Find new nonequal primes for the KeyGen     
while (pPrime == qPrime):
  pPrime, qPrime = genPrimes(pKey, qKey)

#Create Public and Private Keys from Random Primes    
pubKey, privKey = genKey(pPrime, qPrime)
print("Hello!")
print("Your public key is", pubKey ,"and your private key is", privKey)

#Encrypt Message
encryptedMessage = encrypt(privKey, message)
print("Your encrypted message is: ")
print(''.join(map(lambda x: str(x), encryptedMessage)))

#Decrypt Message
print("Decrypting message with public key ", pubKey ," . . .")
print("Your message is:")
print(decrypt(pubKey, encryptedMessage))

from hashlib import sha256

# this is the same salt used in all passwords, we can retrieve this by creating a couple of accounts and using the sqlinjection payload with modified usernames
salt = '000000000000000000000000000078d2'.encode('utf-8')

# this is the admin password that was extracted using the same sqlinjection payload
t = '18821d89de11ab18488fdc0a01f1ddf4d290e198b0f80cd4974fc031dc2615a3'

with open('crackstation.txt', mode='r', encoding='ISO-8859-1') as f:
	i = 0
	for p in f:
		
		# i is used to keep track of how many combinations have been tried
		i += 1
		if i % 1000000 == 0:
			print(i)

		# removing the '\n' at the end of the line
		p = p[:-1]

		# hashing the guess using the fixed salt value
		hasher = sha256()
		hasher.update(salt)
		hasher.update(p.encode('utf-8'))

		# checking if we broke the password
		if hasher.hexdigest() == t:
			# printing plaintext value of broken password
			print(p)
			break
		

n = 600851475143

i = 2
prime_factor = []
while i**2 <= n:
	if n % i == 0:
		print(i)
		n //= i
		prime_factor.append(i)
	else:
		i += 1
prime_factor.append(n)

print(prime_factor)
print(max(prime_factor))
from functools import reduce 

class Number:
	def __init__(self, n: int):
		self.prime_factor = dict()
		i = 2
		while i**2 <= n:
			if n % i == 0:
				n //= i
				self.prime_factor[i] = self.prime_factor.get(i, 0) + 1
			else:
				i += 1
		self.prime_factor[n] = self.prime_factor.get(n, 0) + 1

def ppcm(list_of_int: list[int]) -> int:
	list_of_numbers = [Number(i) for i in list_of_int]
	ppcm = dict()
	for n in list_of_numbers:
		for prime, d in n.prime_factor.items():
			ppcm[prime] = max(ppcm.get(prime, 0), d)
	print(ppcm)
	ppcm_value = reduce(lambda x, y: x * y, [prime ** d for prime, d in ppcm.items()])
	return ppcm_value


print(ppcm(range(1,20)))
def find_exp():
	base = 7
	result = 59
	mod = 71
	for x in xrange(mod - 1):
		if ((base**x) % mod) == result:
			return x
	return -1

def main():
	print find_exp()

if __name__ == '__main__':
	main()
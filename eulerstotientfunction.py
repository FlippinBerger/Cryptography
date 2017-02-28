import sys

def Eulers(num):
	li = list(range(2,num))
	print li
	for x in li:
		if num % x is 0:
			CleanList(li, x)
	return li

def CleanList(li, x):
	for num in li:
		if num % x is 0:
			li.remove(num)
	return li

def main(argv):
	li = Eulers(int(sys.argv[1]))
	print li
	print len(li)


if __name__ == "__main__":
	main(sys.argv)
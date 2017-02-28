import sys

#abstraction of a Point on an elliptic curve
class Point:
	def __init__(self, x, y):
		self.X = x
		self.Y = y

	def Print(self):
		print '({0},{1})'.format(self.X, self.Y)

#checks the set for the given point before adding
def IsValidAddition(pt, s):
	for p in s:
		if (p.X == pt.X) and (p.Y == pt.Y):
			return False
	return True

#adds a point to the set s
def AddToSet(pt, s):
	if IsValidAddition(pt, s):
		s.add(pt)
		return s

#Extended Euclidean Algorithm
def EEA(a, b, mod):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return x % mod

#calculates the slope between 2 points
def CalcSlope(pt1, pt2, a, mod):
	if (pt1.X == pt2.X) and (pt1.Y == pt2.Y):
		numerator = 3 * (pt1.X ** 2) + a
		denominator = 2 * pt1.Y
	else:
		numerator = pt2.Y - pt1.Y
		denominator = pt2.X - pt1.X
	mult_inverse = EEA(denominator, mod, mod)
	return numerator * mult_inverse

#func to add 2 points together in terms of an elliptic curve
def AddPoints(pt1, pt2, a, b, mod):
	R = Point(0, 0)
	slope = CalcSlope(pt1, pt2, a, mod)
	R.X = ((slope ** 2) - pt1.X - pt2.X) % mod
	R.Y = ((slope * (pt1.X - R.X)) - pt1.Y) % mod
	return R

#func to reflect the point across the y axis
def ReflectPoint(pt, mod):
	newY = (pt.Y * -1) % mod 
	p = Point(pt.X, newY)
	return p

#func to make a dictionary of x to x^pow
def CreateDictToPower(mod, power):
	d = {}
	for x in xrange(mod):
		d[x] = (x**power) % mod
	return d

#func to make a dictionary from x to full elliptic equation
#for that given x
def CreateEquationDict(a, b, mod, cube_dict):
	d = {}
	for x in xrange(mod):
		d[x] = (cube_dict[x] + (a * x) + b) % mod
	return d

#Equation to find the square root from the square dict
def FindSquareRoot(square_dict, val, mod):
	for x in xrange(mod):
		if square_dict[x] == val:
			return x
	return -1

#func that finds all points on the given elliptic curve
def FindPoints(a, b, mod):
	point_set = set()
	square_dict = CreateDictToPower(mod, 2)
	print 'square_dict: {0}'.format(square_dict.values())
	cube_dict = CreateDictToPower(mod, 3)
	equation_dict = CreateEquationDict(a, b, mod, cube_dict)
	print 'equation_dict: {0}'.format(equation_dict.values())
	for x in xrange(mod):
		if equation_dict[x] in square_dict.values():
			square = FindSquareRoot(square_dict, equation_dict[x], mod)
			if square == -1:
				print 'You didn\'t find a square'
			else:
				AddToSet(Point(x, square), point_set)
	new_set = set()
	for pt in point_set:
		AddToSet(ReflectPoint(pt, mod), new_set)
	for pt in new_set:
		AddToSet(pt, point_set)
	return point_set

#multiply the Point by the num
def MultiplyPoint(pt, num, a, b, mod):
	curr_pt = Point(pt.X, pt.Y)
	for x in xrange(num - 1):
		curr_pt = AddPoints(curr_pt, pt, a, b, mod)
	return curr_pt


#pass in a and b values for elliptic curve equation
def main(argv):
	if len(argv) == 4:
		a_value = int(argv[1])
		b_value = int(argv[2])
		mod = int(argv[3])
	else:
		print 'Incorrect number of arguments given.'

	s = FindPoints(a_value, b_value, mod)
	print 'The number of points in this elliptic curve is {0}'.format(len(s))
	print '\nHere are the points on the curve:'
	for pt in s:
		pt.Print()

	#used for 10.15
	pt = Point(2, 7)

	print 'Point 3:'
	MultiplyPoint(pt, 3, 1, 6, 11).Print()

	print 'Point 7:'
	PB = MultiplyPoint(pt, 7, 1, 6, 11)
	PB.Print()

	Pm = Point(10, 9)
	new = MultiplyPoint(PB, 3, 1, 6, 11)

	print 'Cipher Point:'
	AddPoints(new, Pm, 1, 6, 11).Print()

	# Problem 10.15 part c
	pt = Point(8, 4)
	MultiplyPoint(pt, 7, 1, 6, 11).Print()

if __name__ == '__main__':
	main(sys.argv)
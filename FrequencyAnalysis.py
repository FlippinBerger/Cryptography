import Queue

class Char:
	def __init__(self, text, num):
		self.text = text
		self.priority = num
		self.subtext = ''

	def __cmp__(self, other):
		return self.priority > other.priority

class Digram:
	def __init__(self, text, num):
		self.text = text
		self.priority = num

	def __cmp__(self, other):
		return self.priority > other.priority

class Trigram:
	def __init__(self, text, num):
		self.text = text
		self.priority = num

	def __cmp__(self, other):
		return self.priority > other.priority


class VigenereSubcipher:
 	def __init__(self, string):
 		self.text = string
 		self.characters = {}
 		self.pq = Queue.PriorityQueue()

class Analyzer:
	#dictionary from character to number
	#of instances
	characters = {}

	#dict of digrams
	digrams = {}

	#dict of trigrams
	trigrams = {}

	plaintext = ''
	ciphertext = ''

	def __init__(self, string):
		self.text = string

		#used for gen sub ciphers
		self.charpq = Queue.PriorityQueue()
		self.dipq = Queue.PriorityQueue()
		self.tripq = Queue.PriorityQueue()

		#used for Vigenere Ciphers
		#position in key : list of letters to freq analyze
		self.vdict = {}
		self.vpqlist = []
		self.vpq = Queue.PriorityQueue()

	#sets up the characters dict
	def PopChars(self):
		for ch in self.text:
			#print ch,
			if ch in self.characters:
				self.characters[ch] += 1
			else:
				self.characters[ch] = 1
				print ch,

	#sets up the digrams dict
	def PopDis(self):
		count = 0
		for ch in self.text:
			if count == 0:
				count = 1
				continue
			else:
				if count + 2 >= len(self.text):
					break
				if self.text[count:count+2] in self.digrams:
					self.digrams[self.text[count:count+2]] += 1
				else:
					self.digrams[self.text[count:count+2]] = 1
				count += 1


	#sets up trigrams dict
	def PopTris(self):
		count = 0
		for ch in self.text:
			if count == 0 or count == 1:
				count += 1
				continue
			else:
				if count + 3 >= len(self.text):
					break
				if self.text[count:count+3] in self.trigrams:
					self.trigrams[self.text[count:count+3]] += 1
				else:
				 	self.trigrams[self.text[count:count+3]] = 1
				count += 1
 	
 	def PopAll(self):
 		self.PopChars()
 		self.PopDis()
 		self.PopTris()

 	def PopVigenere(self, key_length):
 		curr_round = 0
 		#get all the sub ciphers in the dictionary
 		while (curr_round < key_length):
 			subcipher = VigenereSubcipher('')
 			for i in range(curr_round, len(self.text), key_length):
 				subcipher.text += self.text[i]
 			self.vdict[curr_round] = subcipher
 			curr_round += 1
 		for i in range(0, key_length):
 			ciphertext = self.vdict[i]
 			for ch in ciphertext.text:
				if ch in ciphertext.characters:
					ciphertext.characters[ch] += 1
				else:
					ciphertext.characters[ch] = 1


	#calculates the frequency of each letter in the text
	def GetCharFrequency(self):
		for k in self.characters:
			self.charpq.put(Char(k, (float(self.characters[k])/len(self.text)) * -1))

	def GetDiFrequency(self):
		for k in self.digrams:
			self.dipq.put(Digram(k, (float(self.digrams[k])/len(self.digrams)) * -1))

	def GetTriFrequency(self):
		for k in self.trigrams:
			self.tripq.put(Trigram(k, (float(self.trigrams[k])/len(self.trigrams)) * -1))

	def GetAllFrequencies(self):
		self.GetCharFrequency()
		self.GetDiFrequency()
		self.GetTriFrequency()

	#calculates the frequencies of each letter set in Vigenere Ciphers
	def GetVigenereFrequencies(self):
		for subpos in self.vdict:
			subcipher = self.vdict[subpos]
			for k in subcipher.characters:
				subcipher.pq.put(Char(k, (float(subcipher.characters[k])/len(subcipher.text)) * -1))


	def PrintVigenereFrequencies(self, key_length):
		for i in range(0, key_length):
			print
			print 'Frequency of key letter {0}\n\n'.format(i+1)
			while not self.vdict[i].pq.empty():
				item = self.vdict[i].pq.get()
				print 'Block: {0}, Frequency: {1}'.format(item.text, item.priority * -1)

	def PrintFrequency(self, q):
		while not q.empty():
			item = q.get()
			print 'Block: {0}, Frequency: {1}'.format(item.text, item.priority * -1)

	def PrintAllFrequencies(self):
		print '\nPrinting Char Frequencies\n\n'
		self.PrintFrequency(self.charpq)
		print '\nPrinting Digram Frequencies\n\n'
		self.PrintFrequency(self.dipq)
		print '\nPrinting Trigram Frequencies\n\n'
		self.PrintFrequency(self.tripq)

	def DecryptVigenere(self, key, key_length):
		count = 0
		self.text.upper()
		for ch in self.text:
			new_letter = chr(((ord(ch) - ord(key[count % key_length])) % 26) + ord('A'))
			self.plaintext += new_letter
			count += 1

	def EncryptVigenere(self, key, key_length):
		count = 0
		self.text.upper()
		key.upper()
		for ch in self.text:
			new_letter = chr(((ord(ch) + ord(key[count % key_length])) % 26) + ord('A'))
			self.ciphertext += new_letter
			count += 1

	def CalcPopVar(self, container):
		sum = 0.0
		for i in range(container.qsize()):
			ch = container.get()
			sum = sum + (ch.priority - (1/26))**2
		sum = sum / 26
		return sum

	def CalcPopVarsOfSubciphers(self):
		var_list = []
		print 'length of dict: {0}'.format(len(self.vdict))
		for subpos in self.vdict:
			print 'pos: {0}'.format(subpos)
			subcipher = self.vdict[subpos]
			var_list.append(self.CalcPopVar(subcipher.pq))
		return var_list


	'''
	Complete mapping for Gen Sub problem B

	def BuildMessage(self):
		for ch in self.text:
			if ch == 'f':
				self.plaintext += 'W'
			elif ch == 'c':
				self.plaintext += 'E'
			elif ch == 'z':
				self.plaintext += 'H'
			elif ch == 'n':
				self.plaintext += 'L'
			elif ch == 'g':
				self.plaintext += 'A'
			elif ch == 's':
				self.plaintext += 'O'
			elif ch == 'd':
				self.plaintext += 'B'
			elif ch == 'y':
				self.plaintext += 'R'
			elif ch == 'u':
				self.plaintext += 'T'
			elif ch == 'x':
				self.plaintext += 'P'
			elif ch == 'p':
				self.plaintext += 'U'
			elif ch == 'w':
				self.plaintext += 'G'
			elif ch == 'h':
				self.plaintext += 'F'
			elif ch == 'k':
				self.plaintext += 'S'
			elif ch == 'j':
				self.plaintext += 'C'
			elif ch == 'i':
				self.plaintext += 'D'
			elif ch == 'o':
				self.plaintext += 'N'
			elif ch == 'l':
				self.plaintext += 'Y'
			elif ch == 'e':
				self.plaintext += 'I'
			elif ch == 'm':
				self.plaintext += 'M'
			elif ch == 'q':
				self.plaintext += 'J'
			elif ch == 'a':
				self.plaintext += 'V'
			else:
				self.plaintext += ch
	'''

	def PrintMessage(self):
		print self.plaintext

	def PrintEncryptedMessage(self):
		print self.ciphertext

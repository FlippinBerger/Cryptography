import sys
import FrequencyAnalysis

def main(argv):
	enc = FrequencyAnalysis.Analyzer(sys.argv[1])
	key = sys.argv[2]
	enc.EncryptVigenere(key, len(key))
	enc.PrintEncryptedMessage()

if __name__ == '__main__':
	main(sys.argv)
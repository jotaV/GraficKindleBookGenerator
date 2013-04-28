# -*- coding: latin1 -*-

import sys
import getopt

from methods import *
from ebook import *

def erroMsg():
	print "GKBG <Book Title> <Autor> <Options>\n \
\tOptions: \n \
\t\t-d <Directory> default: 'Contents/<Title>' \n \
\t\t-c <Color {#HEX or colorize}> default: #000000 \n \
\t\t-l <Language> default: pt-BR \n \
\t\t-u <UUID> default: will be generate \n \
\t\t-o <Orietation> default: landscape \n \
\t\t-t <Book Type> default: comic \n \
\t\t-w <Writing Mode> default: horizontal-lr"

def main(argv):	

	if argv != None and len(argv) > 0:
		ebook = Ebook(argv[0], argv[1])
	else:
		#erroMsg()
		#sys.exit(2)
		ebook = Ebook("Historias da Terra", "Sinergia")
		

	if len(argv) > 2:
		try:
			opts, args = getopt.getopt(argv[2:], "d:c:l:u:o:t:w:")
	   	except getopt.GetoptError:
	   		erroMsg()
	    	sys.exit(2)

		ebook.defineAtributes(opts)
		
	generateEbook(ebook)

if __name__ == '__main__':
	main(sys.argv[1:])	
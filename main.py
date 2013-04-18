# -*- coding: latin1 -*-

import sys
import glob

from methods import *


def main(argv):
	print glob.glob("*");
		

if __name__ == '__main__':
	main(sys.argv[1:])	
# -*- coding: latin1 -*-	

import os
from datetime import datetime

class Ebook:
	title = ""
	autor = ""
	directory = "Contents/"
	color = "#000000"
	lang = "pt-BR"
	orietation = "portrait"
	bookType = "comic"
	writingMode = "vertical-lr"
	uuid = "urn:uuid:4f5ec5d8-d29d-4d73-9826-d1a78ee98e6b"
	date = "2013-04-19"

	width = 0
	heigth = 0

	roles = {}

	indices = []
	indicesCont = 0

	imgs = {}
	imgsCont = 0

	def __init__(self, title, autor):
		self.title = "Historias da Terra" #title
		self.autor = "Sinergia" #autor

		self.writingMode = "horizontal-lr" #remove this
		self.orietation = "landscape" #remove this
		self.width = 1280 #remove this
		self.heigth = 750 #remove this

		self.directory = "Contents/" + title

		now = datetime.now()
		self.date = now.strftime("%Y-%m-%d")

	def defineAtributes(self, opts):
		"""
		ABRIR AQUIVO RULES E ADD NEW RULES E DADOS
		"""
		for opt, arg in opts:
	   		if opt == '-d':
	   			self.directory = arg
	   		elif opt == '-c':
	   			self.color = arg
	   		elif opt == '-l':
	   			self.lang = arg
	   		elif opt == '-u':
	   			self.uuid = arg
	   		elif opt == '-o':
	   			self.orietation = arg
	   		elif opt == '-t':
	   			self.bookType = arg
	   		elif opt == '-w':
	   			self.writingMode = arg
		pass

	def addIndice(self, name, directory):
		self.indicesCont += 1
		self.indices.append({"name": name, "directory": os.path.join(self.directory, directory), "number": str(self.indicesCont)})

		return self.indicesCont

	def addImg(self, img):
		self.imgsCont += 1
		self.imgs[img] = "%05d" % self.imgsCont

		return self.imgs[img]

	@staticmethod
	def GetACSSClass(number):
		return "div.q" + number + "{background-image: url('images/" + number + ".jpg');}"

	@staticmethod
	def GetAImgManifest(number):
		return "<item href='images/" + number + ".jpg' id='img" + number + "' media-type='image/jpeg'/>"

	@staticmethod
	def GetAPageManifest(number):
		return "<item href='frames/" + number + ".xhtml' id='q" + number + ".xhtml' media-type='application/xhtml+xml' />"

	@staticmethod
	def GetASpine(number):
		return "<itemref idref='q" + number + ".xhtml' />"

	@staticmethod
	def GetAIndice(name, numPage, numIndice):
		return "<navPoint id='nav-" + numIndice + "' playOrder='" + numIndice + "'>\n\
      <navLabel>\n\
        <text>" + name + "</text>\n\
      </navLabel>\n\
      <content src='frames/" + numPage + ".xhtml' />\n\
    </navPoint>"



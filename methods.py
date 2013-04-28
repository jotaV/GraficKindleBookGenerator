# -*- coding: latin1 -*-

import re
import os
import shutil
import zipfile

from ebook import *

contentFile = None
tocFile = None
styleFile = None

def generateEbook(ebook):

	if os.path.exists("Temp/"):
		shutil.rmtree("Temp/")

	os.makedirs("Temp/")
	os.makedirs("Temp/OEBPS/")
	os.makedirs("Temp/OEBPS/images")
	os.makedirs("Temp/OEBPS/frames")

	configureContentFile(ebook)
	configureTocFile(ebook)
	configureCSS(ebook)

	configureExtraRoles(ebook)

	getAndSetImages(ebook)

	finishing(ebook)

def configureContentFile(ebook):
	global contentFile

	contentFile = str((open("Base/content.opf")).read())

	contentFile = contentFile.replace("{{TITLE}}", ebook.title)
	contentFile = contentFile.replace("{{LANGUAGE}}", ebook.lang)
	contentFile = contentFile.replace("{{DATE}}", ebook.date)
	contentFile = contentFile.replace("{{AUTOR}}", ebook.autor)
	contentFile = contentFile.replace("{{UUID}}", ebook.uuid)
	contentFile = contentFile.replace("{{ORIENTATION}}", ebook.orietation)
	contentFile = contentFile.replace("{{WRITINGMODE}}", ebook.writingMode)
	contentFile = contentFile.replace("{{BOOKTYPE}}", ebook.bookType)

def configureTocFile(ebook):
	global tocFile

	tocFile = str((open("Base/toc.ncx")).read())

	tocFile = tocFile.replace("{{TITLE}}", ebook.title)
	tocFile = tocFile.replace("{{UUID}}", ebook.uuid)

def configureCSS(ebook):
	global styleFile
	
	styleFile = (open("Base/style.css")).read()

	if(ebook.color != "colorize"):
		styleFile = styleFile.replace("{{BACKGROUND}}", "body {background-color: " + ebook.color + ";}")
	else:
		styleFile = styleFile.replace("{{BACKGROUND}}", "")

def configureExtraRoles(ebook):
	global contentFile

	"""
	NÃO ESTAR DEVIDAMENTE CONFIGURADO
	"""
	contentFile = contentFile.replace("{{ADDROLE}}", "")

def getAndSetImages(ebook):

	#Get list of indices in the book
	for direct in os.listdir(ebook.directory):
		if os.path.isdir(os.path.join(ebook.directory, direct)):
			ind = re.sub(r"^(\d)*(\.|)( )*", "", direct)
			ebook.addIndice(ind, direct)

	for ind in ebook.indices:
		imgs = []

		for i in os.listdir(ind["directory"]):
			if os.path.isfile(os.path.join(ind["directory"], i)) and re.search(r"(.jpg)|(.jpeg)", str(i)) != None:#re.search(r"(.jpg)|(.jpeg)|(.img)", str(i)) != None:
				imgs.append({"name": i, "directory": os.path.join(ind["directory"], i)})

		if len(imgs) > 0:
			for img in imgs:
				setImgs(ebook, img)
			addMenu(ebook, imgs[0], ind)

def addMenu(ebook, img, indice):
	global tocFile

	numberPage = ebook.imgs[img["directory"]]
	numberIndice = indice["number"]

	tocFile = tocFile.replace("{{ADDMAPOBJECT}}", Ebook.GetAIndice(indice["name"], numberPage, numberIndice) + "\n      {{ADDMAPOBJECT}}");

def setImgs(ebook, img):
	global styleFile, contentFile

	number = ebook.addImg(img["directory"])

	#####################################################
	#copy image to the folder images
	#####################################################
	"""
	DEVE TER UMA COVERÇÃO DA QUALIDADE DA IMAGEM AQUI
	"""

	shutil.copyfile(img["directory"], "Temp/OEBPS/images/" + number + ".jpg")

	#####################################################
	#creating the class on css File
	#####################################################
	
	styleFile += Ebook.GetACSSClass(number) + "\n"

	#####################################################
	#creating the page in xhtml
	#####################################################

	frame = open("Temp/OEBPS/frames/" + number + ".xhtml", "w+")
	base = (open("Base/page.xhtml")).read()
	
	base = base.replace("{{CLASS}}", "q" + number)

	if(ebook.color != "colorize"):
		base = base.replace("{{BACKGROUND}}", "")
	else:
		pass

	frame.write(base)
	frame.close()

	#####################################################
	#add image on content.opf file 
	#####################################################

	contentFile = contentFile.replace("{{ADDIMAGE}}", Ebook.GetAImgManifest(number) + "\n    {{ADDIMAGE}}")

	#####################################################
	#add page on content.opf file
	#####################################################
	
	contentFile = contentFile.replace("{{ADDPAGE}}", Ebook.GetAPageManifest(number) + "\n    {{ADDPAGE}}")

	#####################################################
	#add page on spine in content.opf file
	#####################################################

	contentFile = contentFile.replace("{{ADDSPINE}}", Ebook.GetASpine(number) + "\n      {{ADDSPINE}}")

def finishing(ebook):
	global styleFile, tocFile, contentFile

	tocFile = tocFile.replace("{{ADDMAPOBJECT}}", "")

	newFile = open("Temp/OEBPS/toc.ncx", "w+")
	newFile.write(tocFile)
	newFile.close()

	contentFile = contentFile.replace("{{ADDIMAGE}}", "")
	contentFile = contentFile.replace("{{ADDPAGE}}", "")
	contentFile = contentFile.replace("{{ADDSPINE}}", "")
	contentFile = contentFile.replace("{{RESOLUTION}}", str(ebook.width) + "x" + str(ebook.heigth))

	newFile = open("Temp/OEBPS/content.opf", "w+")
	newFile.write(contentFile)
	newFile.close()

	styleFile = styleFile.replace("{{WIDTH}}", str(ebook.width))
	styleFile = styleFile.replace("{{HEIGTH}}", str(ebook.heigth))

	newFile = open("Temp/OEBPS/style.css", "w+")
	newFile.write(styleFile)
	newFile.close()	

	newFile = open("Temp/mimetype", "w+")
	newFile.write((open("Base/mimetype")).read())
	newFile.close()

	os.makedirs("Temp/META-INF/")
	newFile = open("Temp/META-INF/container.xml", "w+")
	newFile.write((open("Base/container.xml")).read())
	newFile.close()

	zf = zipfile.ZipFile(os.path.join(os.path.dirname(ebook.directory), ebook.title + ".epub"), "w", zipfile.ZIP_STORED)
	zipFolder(zf)
	zf.close()

	shutil.rmtree("Temp/")

def zipFolder(zFile):

	for root, dirs, files in os.walk("Temp/"):
		for f in files:
			dirname = os.path.join(root, f)
			zFile.write(dirname, re.sub(r"^Temp(/|\\)", "", dirname))
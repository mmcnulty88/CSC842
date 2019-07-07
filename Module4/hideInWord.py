	#Simple program to hide data into the file structure of a .docx word document while allowing the document to still function correctly.
	#Will also allow the hidden data to be extracted from a document.
	#The program takes advantage of the fact that a .docx document is a zip archive of files with standardized locations and names
	#	to be able to change the first image located in a file and/or be able to add a secret into a specific xml file that is also
	#	part of the structure.
	#The input document must be specified, then optionally an image, a secret file containing the secret you want to hide, and the output
	#	destination may be specified as needed.
	#For extracting, the input document is still required. Optionally, you can add file names for an image or text secret to be extracted to.
import zipfile
import shutil
import os
import tempfile
import argparse

	#Use argParse to define arguments that can be used with the program.
	#The filename of the .docx file is a positional and is required.
	#The -i or --image flag allows an image to be defined to replace the first image from the .docx file.
	#	If extracting, this may be used to set the name of the file that the image should be saved to.
	#The -s or --secret flag allows a file containing a secret to be specified and then that will be added to the .docx file.
	#	If extracting, this may be used to set the name of the file the extracted secret should be saved to.
	#The -o or --output flag allows a filename for the output to be specified. Otherwise a default of output.docx will be used.
	#Since all of the arguments are filenames, they should be strings and so their type is defined as such to add in a little extra checking.
	#	Note that this doesn't cause a problem with files that are only numbered since the file extension should be included making it a string.
	#Additionally, if no flag is set, the original document will simply be copied as it is.
argParse = argparse.ArgumentParser()
argParse.add_argument('filename', help='Name of the .docx file to add your secrets into.', type=str)
argParse.add_argument('-i', '--image', help='Image you would like to embed into the document or filename for an extracted image. Must be a jpeg image.', type=str)
argParse.add_argument('-s', '--secret', help='Secret file that you would like to read from and embed into a file in the document or filename for an extracted secret.', type=str)
argParse.add_argument('-o', '--output', help='The filename that the output should be saved to.', type=str, default='output.docx')
argParse.add_argument('-e', '--extractAll', help='Extract the image and xml file from the given document.', action='store_true')
argParse.add_argument('-ei', '--extractImage', help='Extract just the image file from the given document.', action='store_true')
argParse.add_argument('-es', '--extractSecret', help='Extract just the xml file from the given document.', action='store_true')
args = argParse.parse_args()
	
	#Name of the file we want to add secrets to or extract them from.
fileName = args.filename

	#Location of the first image in the docx structure.
image = 'word/media/image1.jpeg'

	#Location of one of the xml files in the docx structure.
contentTypes = '[Content_Types].xml'

	#Check to see if we should be extracting from the given document or not.
	#If we are extracting from the document, then we can open our file and then see what we should be extracting.
if args.extractAll or args.extractImage or args.extractSecret:

		#Create a ZipFile object for our document to extract files from.
	readDoc = zipfile.ZipFile(fileName, 'r')
	
		#Check to see if we should be extracting the image from the document.
	if args.extractAll or args.extractImage:
	
		#Extract the image from our document, copy it into the base directory, and finally clean up.
		readDoc.extract(image)
		
			#If an image name was specified, use that for our output filename otherwise use a default.
		if args.image != None:
			shutil.copy(image, args.image)
		else:
			shutil.copy(image, 'extractedImage.jpeg')
		shutil.rmtree('word')
		
		#Check to see if we should be extracting the xml file holding the secret.
	if args.extractAll or args.extractSecret:
	
		#Extract the xml file
		readDoc.extract(contentTypes)
		
			#If a secret file name was specified, use that to store our secret, otherwise use a default.
		if args.secret != None:
			secret = open(args.secret, 'w')
		else:
			secret = open('extractedSecret.txt','w')
		CTFile = open(contentTypes,'r')
		foundSecret = False
			#Start looking for our secret, which will be surrounded by comments.
			#When we find a comment line, start writing the secret from the xml file to our text file.
			#When we reach the end of the comments, stop writing.
			#We don't include the comment symbols as part of our secret.
		for line in CTFile:
			if line.rstrip() == '<!--':
				foundSecret = True
			elif foundSecret:
				if line.rstrip() == '-->':
					foundSecret = False
				else:
					secret.write(line)
		
			#Clean up our open files and original xml file.
		CTFile.close()
		secret.close()
		os.remove(contentTypes)
		
	#If we extracted from the given document, we are done here.
		
	#If we arent' extracting, then we can start the process of adding our secrets.
else:
		#Create a temporary directory to hold our files while we work.
	tempdir = tempfile.mkdtemp()

		#Temporary location for our zip file.
	tempZip = os.path.join(tempdir, 'newDoc.docx')	

		#Create a ZipFile object for our document to extract files from.
	readDoc = zipfile.ZipFile(fileName, 'r')

		#List to exclude the files we will edit from being copied from the original later.
		#	We will add to it based on our arguments.
	exclude = []

		#Add the file(s) we are editing to our exclude list.
		#Extract just the files we are editing and then edit them.
		#First we check if an image was included in our arguments.
	if args.image != None:
		exclude.append(image)
		readDoc.extract(image)
		
			#Copy the modified image over the original image.
		shutil.copy(args.image, image)
		
		#Now we check if a secret file was included in the arguments.
	if args.secret != None:
		exclude.append(contentTypes)
		readDoc.extract(contentTypes)
		
			#Add our secret as a comment in the xml file.
			#Opening the file in append mode to add our edits to the
			#	end of the file as xml comments.
			#	<!-- opens and --> closes a comment block in xml, so we wrap them around our secret.
			#	Since its inserted as a comment, it makes no changes to the actual document.
		CTFile = open(contentTypes, 'a')
		secret =  open(args.secret)
		CTFile.write('\n<!--\n')
		for line in secret:
			CTFile.write(line)
		CTFile.write('\n-->\n')

			#Close the files.
		secret.close()
		CTFile.close()

		#Open a location to write to temporarily.
		#	Set to append mode so we can add our own file(s) in.
	writeDoc = zipfile.ZipFile(tempZip, 'a')

		#Need to read from the original document to get the files from item.
		#Then we need to write the files we find in our original document to our temporary one.
		#This is where we exclude the original versions of the files we have edited and add in
		#	our edited versions.
	with readDoc:
		with writeDoc:
			for item in readDoc.infolist():
				if item.filename not in exclude:
					data = readDoc.read(item.filename)
					writeDoc.writestr(item, data)
				elif item.filename == image:
					writeDoc.write(image, image)
				elif item.filename == contentTypes:
					writeDoc.write(contentTypes, contentTypes)

		#Move the new docx from the temporary file to the local
		#	directory with the given filename.
	shutil.move(tempZip,args.output)

		#Remove the temporary directory created.
	shutil.rmtree(tempdir)
		#If we used it, remove the word directory (image location).
	if args.image != None:
		shutil.rmtree('word')
		#If we used it, remove the contentTypes xml file.
	if args.secret != None:
		os.remove(contentTypes)


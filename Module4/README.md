# Module 4 - hideInWord

Simple program to hide data into the file structure of a .docx word document while allowing the document to still function correctly.
Will also allow the hidden data to be extracted from a document.
The program takes advantage of the fact that a .docx document is a zip archive of files with standardized locations and names
	to be able to change the first image located in a file and/or be able to add a secret into a specific xml file that is also
	part of the structure.

## Tested With:

- Python 2 and 3
- Windows 10 OS
- Microsoft Word .docx type documents.

## Requirements:

- The image being inserted must be a jpeg.
- There must be at least one image in the document to modify if using the image flag.

## Usage:

```bash
python hideInWord.py [-h] [-i IMAGE] [-s SECRET] [-o OUTPUT] [-e] [-ei] [-es] filename
```
- "filename" is the input .docx document and must be specified for inserting and extracting.
- For inserting the image and secret flags are optional, you can choose to use one, both, or none.
- The output .docx file name may be specified with the output flag or a default of output.docx is used.
- For extracting the image and secret flags are used for output destination names for the respective extracted files. If not specified, then default names of extractedImage.jpeg and extractedSecret.txt are used.
- The flag e or extractAll will extract both an image and a secret.
- The flag ei or extractImage will extract only an image.
- The flag es or extractSecret will extract only a secret.

## Current Limitations:

- Images are specific to the .docx documents, though the secret works for other types such as an excel file.
- Only the first image is used.
- A specific file is always used to insert the secret into.
- Encrypt the secret instead of inserting it as it is directly from the file.

## Future Work:

- Randomize or allow a choice of which image to be replaced.
- Randomize or allow a choice of which file to insert the secret into.

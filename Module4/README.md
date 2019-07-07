# Module 3 - hideInWord

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
- There must be at least one image in the document to work

## Usage:

```bash
python hideInWord.py [-h] [-i IMAGE] [-s SECRET] [-o OUTPUT] [-e] [-ei] [-es] filename
```
- "filename" is the input .docx document and must be specified for inserting and extracting.
- For inserting the image and secret flags are optional, you can choose to use one, both, or none.
- For extracting the image and secret flags are used for output destination names for the respective extracted files.
- The output file name may be specified with the output flag or a default of output.docx is used.

## Current Limitations:

- Images are specific to the .docx documents, though the secret insertion works for other types such as an excel file.
- Only the first image is used.
- A specific file is always used to insert the secret into.

## Future Work:

- Randomize or allow a choice of which image to be replaced.
- Randomize or allow a choice of which file to insert the secret into.

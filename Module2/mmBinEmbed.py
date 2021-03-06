#mmBinEmbed - python 2.7.16
#Converts a given bin file to bytes using the pveReadBin perl script by Peter Van Eeckhoutte
#It then adds the bytes into a character array and simple default C file that can be used
#   to call the converted bin file.
#If a source file and an output file are provided, then the output of pveReadBin can be added to any file.

import subprocess
import sys
import re
#import tempfile

if (len(sys.argv) < 2) or (len(sys.argv) > 4):
    print("Usage: python mmBinEmbed.py [bin file to embed] [Optional: source file to embed into] [Optional: output file name]")
    print("Note: Enter the full path to the bin and/or source file if it is not in the same folder as the script.")
    print("\tThe same should be done to save the output file in a different location.")
    print("If providing a source file, it must include a line \"char embed[] = \"\";\" to signify where the bin contents should be embedded.")
    exit()

binFile = sys.argv[1]
if len(sys.argv) == 3:
    outputFile = sys.argv[2]
elif len(sys.argv) == 4:
    inputFile = sys.argv[2]
    outputFile = sys.argv[3]
else:
    outputFile = "default.c"
perl = subprocess.Popen(["perl", "pveReadBin.pl", binFile], stdout=subprocess.PIPE)

    #default output. Simple C code written to default.c and only used when just a bin file is provied.
if outputFile == "default.c":
    f = open("default.c", "w")
    f.write("//Autogenerated shellcode tester. Use this to test your shellcode.\n")
    f.write("\n\n")
    f.write("char shellcode[] = ")
    data = perl.stdout.readline()
    while data:
        if(data[0] == "\""):
            f.write(data)
        elif(len(data) > 2):
            print(data)
        data = perl.stdout.readline()
    f.write("int main(int argc, char **argv){\n\n")
    f.write("\tint (*func)();\n\n")
    f.write("\tfunc = (int (*)()) shellcode;\n\n")
    f.write("\t(int)(*func)();\n\n")
    f.write("}")
    f.close()
    print("Finished writing default.c with embedded bytes.")

    #Placeholder for writing to the same file as read from. Reads then entire file then writes the file with the embedded
    # bin file information.
elif len(sys.argv) == 3:
    print("Reading and writing to the same source file is not currently implemented.\nPlease run again with a destination file also provided.")

    #Read and write using different files.  Will be used if an output file name is provided in addition to an input file.
    # Reads a line and then writes that line until the embed location is found.
    # Regular expression is used to match the embed location and then change that line to add in the bin information.
    # After the information is embedded, then it continues to read and write to finish out the file.
elif len(sys.argv) == 4:
    fr = open(inputFile, "r")
    fw = open(outputFile, "w")
    readData = fr.readline()
    while readData:
            #regular expresion to match char embed[] = ""; no matter how the spacing is done.
        if re.search(r'\s{0,}char\s{0,}embed\[]\s{0,}=\s{0,}""\s{0,};\s{0,}', readData, re.M|re.I):
            fw.write("char embed[] = ")
            data = perl.stdout.readline()
            while data:
                if(data[0] == "\""):
                    fw.write(data)
                elif(len(data) > 2):
                    print(data)
                data = perl.stdout.readline()
        else:
            fw.write(str(readData))
        readData = fr.readline()
    fr.close()
    fw.close()
    print("Finished writing to "+outputFile+" using the contents of "+inputFile+".")



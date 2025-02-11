import os
import glob
import re

fastq_path = "/Users/logan/Documents/SampleSheetGenerator/FASTQ/"

class SingleRead():
    def __init__(self, file_path, basename):
        self.file_path = file_path
        self.files = ["",""]
        self.AddFile(basename)

    def AddFile(self,file_path,basename):
        if file_path == self.file_path:
            if self.files[0] == "":
                self.files[0] = basename
            else:
                print("Duplicate File Found")
        else:
            print("Bad Path: {}".format(file_path))

    def GetReads(self):
        print(self.files)


class ReadPair(SingleRead):
    def __init__(self, file_path, basename, read_match):
        self.read_match = read_match[:-2]
        self.file_path = file_path
        self.files = ["",""]
        self.AddFile(file_path,basename,read_match)

    def AddFile(self, file_path, basename, read_match):
        if file_path == self.file_path:
            if re.match(read_match[:-2], self.read_match):
                read_number = int(read_match[-2:-1]) - 1
                if self.files[read_number] == "":
                    self.files[read_number] = basename
                else:
                    print("Duplicate File Found")
            else:
                print("Bad File")
        else:
            print("Bad Path: {}".format(file_path))

fastq_files = {}

# get a list of all files in the path with the given pattern 
for i in glob.glob(os.path.join(fastq_path,"lung*")):
    fastq_file = list(os.path.splitext(i))
    fastq_directory = os.path.dirname(i)

    # Checks if the file is zipped and expands the extension to add the file type.
    if fastq_file[1] == ".gz":
        temp_file = list(os.path.splitext(fastq_file[0]))
        temp_file[1] += ".gz"
        fastq_file = temp_file

    # Gets the basename of the file
    basename = os.path.basename(i)
    print(basename)
    
    # Finds the read number if one exists
    pattern = re.search(r"_[rR]?[12]\.",basename)
    if pattern:

        # Removes the read number (ex. _R1) from the sample name
        sample_name = basename.replace(pattern[0], pattern[0][:-2]+".")

        if sample_name in fastq_files:
            fastq_files[sample_name].AddFile(fastq_directory,basename,pattern[0])
        else:
            fastq_files[sample_name] = ReadPair(fastq_directory,basename,pattern[0])

    else:
        if sample_name in fastq_files:
            fastq_files[sample_name].AddFile(fastq_directory,basename)
        else:
            fastq_files[sample_name] = SingleRead(fastq_directory,basename)
        
for i in fastq_files:
    print(i)
    print(fastq_files[i].GetReads())



def CheckExtension(fastqFile):
    pass

def StripExtension(fastqFile):
    pass
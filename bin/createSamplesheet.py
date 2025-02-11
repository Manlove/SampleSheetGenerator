import os
import glob
import re

class SingleRead():
    def __init__(self, file_path, sample_name, basename):
        self.sample_name = sample_name
        self.file_path = file_path
        self.files = ["",""]
        self.AddFile(file_path, basename)

    def AddFile(self,file_path,basename):
        if file_path == self.file_path:
            if self.files[0] == "":
                self.files[0] = basename
            else:
                print("Duplicate File Found")
        else:
            print("Bad Path: {}".format(file_path))

    def GetReads(self):
        return self.files
    
    def GetName(self):
        return self.sample_name

class ReadPair(SingleRead):
    def __init__(self, file_path, sample_name, basename, read_match):
        self.sample_name = sample_name
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

def CreateSampleSheet(fastq_files, fastq_path):

    # get a list of all files in the path with the given pattern 
    for i in glob.glob(os.path.join(fastq_path,"*")):
        fastq_file = list(os.path.splitext(i))
        fastq_directory = os.path.dirname(i)
        
        # Checks if the file is zipped and expands the extension to add the file type.
        if fastq_file[1] == ".gz":
            temp_file = list(os.path.splitext(fastq_file[0]))
            temp_file[1] += ".gz"
            fastq_file = temp_file

        # Gets the basename of the file
        basename = os.path.basename(i)
        
        # Finds the read number if one exists
        pattern = re.search(r"_[rR]?[12]\.",basename)
        
        sample_name = re.sub(r"_?[rR]?[12]?\..*","",basename)

        if pattern:

            # Removes the read number (ex. _R1) from the sample name
            stripped_name = basename.replace(pattern[0], pattern[0][:-2]+".")

            if stripped_name in fastq_files:
                fastq_files[stripped_name].AddFile(fastq_directory,basename,pattern[0])
            else:
                fastq_files[stripped_name] = ReadPair(fastq_directory,sample_name,basename,pattern[0])

        else:

            if basename in fastq_files:
                fastq_files[basename].AddFile(fastq_directory,basename)
            else:
                fastq_files[basename] = SingleRead(fastq_directory,sample_name,basename)

def WriteSampleSheet(fastq_files):
    with open("samplesheet.csv","w") as out_file:
        out_file.write("sample,fastq1,fastq2")
        for sample in fastq_files:
            reads = fastq_files[sample].GetReads()
            sample_name = fastq_files[sample].GetName()
            out_file.write("\n{},{},{}".format(sample_name,reads[0],reads[1]))

if __name__ == "__main__":
    fastq_path = "/Users/logan/Documents/SampleSheetGenerator/FASTQ/"
    fastq_files = {}
    CreateSampleSheet(fastq_files, fastq_path)
    WriteSampleSheet(fastq_files)
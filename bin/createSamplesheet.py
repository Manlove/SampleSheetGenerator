import os
import glob
import re
from typing import List, Dict, Union

class SingleRead:
    def __init__(self, file_path: str, sample_name: str) -> None:
        self.sample_name = sample_name
        self.file_path = file_path
        self.files: List[str] = ["",""]

    def add_file(self, file_path: str, basename: str) -> None:
        if file_path == self.file_path:
            if self.files[0] == "":
                self.files[0] = basename
            else:
                print("Duplicate File Found")
        else:
            print("Bad Path: {}".format(file_path))

    def get_reads(self) -> List[str]:
        return self.files
    
    def get_name(self) -> str:
        return self.sample_name

class ReadPair(SingleRead):
    def __init__(self, file_path: str, sample_name: str, read_match: str) -> None:
        super().__init__(file_path, sample_name) 
        self.read_match = read_match[:-2]

    def add_file(self, file_path: str, basename: str, read_match: str) -> None:
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

def create_sample_sheet(fastq_files: Dict[str, Union[SingleRead, ReadPair]], fastq_path: str) -> None:

    # get a list of all files in the path with the given pattern 
    for i in glob.glob(os.path.join(fastq_path, "*")):
        fastq_file = list(os.path.splitext(i))
        fastq_directory = os.path.dirname(i)
        
        # Checks if the file is zipped and expands the extension to add the file type.
        if fastq_file[1] == ".gz":
            temp_file = list(os.path.splitext(fastq_file[0]))
            temp_file[1] += ".gz"
            fastq_file  = temp_file

        # Gets the basename of the file
        basename = os.path.basename(i)
        
        # Finds the read number if one exists
        pattern = re.search(r"_[rR]?[12]\.", basename)
        
        sample_name = re.sub(r"_?[rR]?[12]?\..*", "", basename)

        if pattern:

            # Removes the read number (ex. _R1) from the sample name
            stripped_name = basename.replace(pattern[0], pattern[0][:-2] + ".")

            if stripped_name not in fastq_files:
                fastq_files[stripped_name] = ReadPair(fastq_directory, sample_name, pattern[0])

            fastq_files[stripped_name].add_file(fastq_directory, basename, pattern[0])

        else:

            if basename not in fastq_files:
                fastq_files[basename] = SingleRead(fastq_directory, sample_name)
            
            fastq_files[basename].add_file(fastq_directory, basename)
                
def write_sample_sheet(fastq_files: Dict[str, Union[SingleRead,ReadPair]]) -> None:
    with open("samplesheet.csv","w") as out_file:
        out_file.write("sample,fastq1,fastq2")
        for sample in fastq_files:
            reads = fastq_files[sample].get_reads()
            sample_name = fastq_files[sample].get_name()
            out_file.write("\n{},{},{}".format(sample_name, reads[0], reads[1]))

def main(fastq_path: str) -> None:
    fastq_files: Dict[str, Union[SingleRead, ReadPair]] = {}
    create_sample_sheet(fastq_files, fastq_path)
    write_sample_sheet(fastq_files)

if __name__ == "__main__":
    fastq_path = "/Users/logan/Documents/SampleSheetGenerator/FASTQ/"   
    main(fastq_path)
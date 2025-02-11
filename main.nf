
workflow {
	//switch (params.readtype){
	//	case "single":
	//		fastqPath = params.fastqdir + "*.fq"
	//		fastq_files = Channel.fromPath(fastqPath, checkIfExists: true)
	//		break
	//	case "paired":
	//		fastqPath = params.fastqdir + "*{1,2}.fq"
	//		fastq_files = Channel.fromFilePairs(fastqPath, checkIfExists: true)
	//		break
	//}
	//println fastqPath
	//fastq_files.view()

	import groovy.io.FileType

	def directory = new File('./FASTQ/')

	def fastqFiles = []
	directory.eachFileMatch(FileType.FILES, ~/.*\.fastq\.gz/) { file ->
    		fastqFiles << file.name
	}

	// Define a map to hold the results
	def filePairs = [:]

	// Check for paired files
	fastqFiles.each { file ->
    		def baseName = (file =~ /(.*)_[12]\.fastq\.gz/)[0][1]
    			if (!filePairs.containsKey(baseName)) {
        			def r1 = "${baseName}_R1.fastq.gz"
        			def r2 = "${baseName}_R2.fastq.gz"
        
        			if (fastqFiles.contains(r1) && fastqFiles.contains(r2)) {
            				// Paired-end files exist
				           filePairs[baseName] = [r1, r2]
        			} else if (fastqFiles.contains(file)) {
            				// Only single-end file exists
            				filePairs[baseName] = [file]
        			}
    			}
	}

	// Output results
	filePairs.each { sample, files ->
		if (files.size() == 2) {
        		println "Paired-end files for ${sample}: ${files[0]}, ${files[1]}"
		} else {
        		println "Single-end file for ${sample}: ${files[0]}"
    		}
	}

}

# PorePolish
**A tool for hands free, iterative pilon polishing of a fasta assembly using paired end Illumina reads.**

## Dependencies
- Python 3
- Pilon
- Samtools
- BWA

## Quick start
    porepolish.py -i /path/to/input.fasta -1 /path/to/illumina/R1.fastq -2 /path/to/illumina/R2.fastq -o /path/to/output_directory/
    
## Usage:     
    usage: porepolish.py [-h] -i INPUT -1 PE1 -2 PE2 -o OUTPUT

    Hands free MinION data processing using Porechop for barcode trimming/binning,
    and Unicycler for assembly

    optional arguments:
      -h, --help            show this help message and exit
      -i INPUT, --input INPUT
                            Runs unicycler in conservative mode
      -1 PE1, --pe1 PE1     Runs unicycler in bold mode
      -2 PE2, --pe2 PE2     Removes intermediate files
      -o OUTPUT, --output OUTPUT

## Why?
I use it to polish long read assemblies from something like Canu or Miniasm to correct for errors and misassemblies. The maximum number of Pilon rounds the script will attempt is 9, however if a previous round does not produce any changes the script will end early.

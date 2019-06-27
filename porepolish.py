#!/usr/bin/env python
import subprocess
import argparse
import os
import glob
import shutil
import sys
import re

# Version
_version_ = "0.1.2"

# Argparse argument setup
parser = argparse.ArgumentParser(description="Hands free iterative assembly polishing with Illumina reads using Pilon")
parser.add_argument("-i", "--input", required=True, help="FASTA file to be polished")
parser.add_argument("-1", "--pe1", required=True, help="Forwrd read to be used for polishing")
parser.add_argument("-2", "--pe2", required=True, help="Reverse read to be used for polishing")
parser.add_argument("-o", "--output", required=True, help="Output directory")
args = parser.parse_args()

# Colour set up
class colours:
    warning = '\033[91m'
    blue = '\033[94m'
    invoking = '\033[93m'
    bold = '\033[1m'
    term = '\033[0m'

# Welcome
print('')
print(colours.blue, colours.bold)
print('######################')
print('Welcome to PorePolish!')
print('######################',colours.term)

# Orientation
invoked_from = os.getcwd()
if not os.path.exists(args.output):
    os.mkdir(args.output)
    print('Output directory created.')
    print('')
os.chdir(args.output)
output = os.getcwd()
os.chdir(invoked_from)

# Variable set up
fasta_in = args.input
read_1 = args.pe1
read_2 = args.pe2
outdir = output + '/'
prefix = os.path.basename(fasta_in).replace('.fasta','')
round_one = outdir + prefix + '_R1'
round_two = outdir + prefix + '_R2'
round_three = outdir + prefix + '_R3'
round_four = outdir + prefix + '_R4'
round_five = outdir + prefix + '_R5'
round_six = outdir + prefix + '_R6'
round_seven = outdir + prefix + '_R7'
round_eight = outdir + prefix + '_R8'
final_round = outdir + prefix + '_final'
fasta_one = round_one + '.fasta'
fasta_two = round_two + '.fasta'
fasta_three = round_three + '.fasta'
fasta_four = round_four + '.fasta'
fasta_five = round_five + '.fasta'
fasta_six = round_six + '.fasta'
fasta_seven = round_seven + '.fasta'
fasta_eight = round_eight + '.fasta'
fasta_final = final_round + '.fasta'
changes_one = round_one + '.changes'
changes_two = round_two + '.changes'
changes_three = round_three + '.changes'
changes_four = round_four + '.changes'
changes_five = round_five + '.changes'
changes_six = round_six + '.changes'
changes_seven = round_seven + '.changes'
changes_eight = round_eight + '.changes'
changes_final = final_round + '.changes'
intermediates = ['index.amb', 'index.ann', 'index.bwt', 'index.pac', 'index.sa', 'mapped.sam', 'mapped.bam', 'mapped.bam.bai']
removal = [invoked_from + '/' + x for x in intermediates]

#  Messages
def goodbye():
    print('Done!','\n')
    print('Author: www.github.com/stevenjdunn','\n','\n')
    print('')
    print('Want to remove the _pilon tags from assembly headers?')
    print('Use sed -i 's/_pilon//g' yourfile.fasta')
    print('')
    print(colours.bold)
    print('#########')
    print('Finished!')
    print('#########', colours.term)

def roundend():
    print(colours.bold)
    print('##############')
    print('Round Finished')
    print('##############', colours.term)
    print('')
    print('')
# Round One
print(colours.bold)
print('#########')
print('Round One')
print('#########', colours.term)
# Index, Map, Index
print('')
print(colours.invoking)
print('Indexing Fasta...', colours.term)
print('')
subprocess.call(['bwa','index', fasta_in, '-p', 'index'])
print('')
print(colours.bold, colours.blue,'Done!', colours.term)
print('')
print(colours.invoking,'Mapping reads to assembly...',colours.term)
subprocess.call(['bwa','mem', 'index', read_1, read_2,'-o','mapped.sam'])
print('')
print(colours.bold, colours.blue,'Done!', colours.term)
print('')
print(colours.invoking, 'Sorting SAM file...', colours.term)
subprocess.call(['samtools','sort', 'mapped.sam', '-o', 'mapped.bam'])
print('')
print(colours.bold, colours.blue,'Done!', colours.term)
print('')
print('Polishing assembly with Pilon...')
subprocess.call(['samtools','index','mapped.bam'])

# Pilon
subprocess.call(['pilon','--genome', fasta_in, '--frags', 'mapped.bam', '--output', round_one, '--changes'])
print('')
print(colours.bold, colours.blue,'Done!', colours.term)
print('')
print('')
# Remove temp files
for item in removal:
    os.remove(item)
roundend()

# Round Two
# Check if changes were made on previous round and continue
if os.path.getsize(changes_one) > 0:
    print(colours.bold)
    print('#########')
    print('Round Two')
    print('#########', colours.term)
    # Index, Map, Index
    print('')
    print(colours.invoking, 'Indexing Fasta...', colours.term)
    subprocess.call(['bwa','index', fasta_one, '-p', 'index'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Mapping reads to assembly...')
    subprocess.call(['bwa','mem', 'index', read_1, read_2,'-o','mapped.sam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Sorting SAM file...')
    subprocess.call(['samtools','sort', 'mapped.sam', '-o', 'mapped.bam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Polishing assembly with Pilon...')
    subprocess.call(['samtools','index','mapped.bam'])

    # Pilon
    subprocess.call(['pilon','--genome', fasta_one, '--frags', 'mapped.bam', '--output', round_two, '--changes'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('')
    # Remove temp files
    for item in removal:
        os.remove(item)
    roundend()
else:
    print('No changes were made on the last round.')
    goodbye()
    sys.exit(1)

# Round Three
# Check if changes were made on previous round and continue
if os.path.getsize(changes_two) > 0:
    print(colours.bold)
    print('###########')
    print('Round Three')
    print('###########', colours.term)
    # Index, Map, Index
    print('')
    print(colours.invoking, 'Indexing Fasta...', colours.term)
    subprocess.call(['bwa','index', fasta_two, '-p', 'index'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Mapping reads to assembly...')
    subprocess.call(['bwa','mem', 'index', read_1, read_2,'-o','mapped.sam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Sorting SAM file...')
    subprocess.call(['samtools','sort', 'mapped.sam', '-o', 'mapped.bam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Polishing assembly with Pilon...')
    subprocess.call(['samtools','index','mapped.bam'])

    # Pilon
    subprocess.call(['pilon','--genome', fasta_two, '--frags', 'mapped.bam', '--output', round_three, '--changes'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('')
    # Remove temp files
    for item in removal:
        os.remove(item)
    roundend()
else:
    print('No changes were made on the last round.')
    goodbye()
    sys.exit(1)

# Round Four
# Check if changes were made on previous round and continue
if os.path.getsize(changes_three) > 0:
    print(colours.bold)
    print('#########')
    print('Round Four')
    print('#########', colours.term)
    # Index, Map, Index
    print('')
    print(colours.invoking, 'Indexing Fasta...', colours.term)
    subprocess.call(['bwa','index', fasta_three, '-p', 'index'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Mapping reads to assembly...')
    subprocess.call(['bwa','mem', 'index', read_1, read_2,'-o','mapped.sam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Sorting SAM file...')
    subprocess.call(['samtools','sort', 'mapped.sam', '-o', 'mapped.bam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Polishing assembly with Pilon...')
    subprocess.call(['samtools','index','mapped.bam'])

    # Pilon
    subprocess.call(['pilon','--genome', fasta_three, '--frags', 'mapped.bam', '--output', round_four, '--changes'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('')
    # Remove temp files
    for item in removal:
        os.remove(item)
    roundend()
else:
    print('No changes were made on the last round.')
    goodbye()
    sys.exit(1)

# Round Five
# Check if changes were made on previous round and continue
if os.path.getsize(changes_four) > 0:
    print(colours.bold)
    print('##########')
    print('Round Five')
    print('##########', colours.term)
    # Index, Map, Index
    print('')
    print(colours.invoking, 'Indexing Fasta...', colours.term)
    subprocess.call(['bwa','index', fasta_four, '-p', 'index'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Mapping reads to assembly...')
    subprocess.call(['bwa','mem', 'index', read_1, read_2,'-o','mapped.sam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Sorting SAM file...')
    subprocess.call(['samtools','sort', 'mapped.sam', '-o', 'mapped.bam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Polishing assembly with Pilon...')
    subprocess.call(['samtools','index','mapped.bam'])

    # Pilon
    subprocess.call(['pilon','--genome', fasta_four, '--frags', 'mapped.bam', '--output', round_five, '--changes'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('')
    # Remove temp files
    for item in removal:
        os.remove(item)
    roundend()
else:
    print('No changes were made on the last round.')
    goodbye()
    sys.exit(1)

# Round Six
# Check if changes were made on previous round and continue
if os.path.getsize(changes_five) > 0:
    print(colours.bold)
    print('#########')
    print('Round Six')
    print('#########', colours.term)
    # Index, Map, Index
    print('')
    print(colours.invoking, 'Indexing Fasta...', colours.term)
    subprocess.call(['bwa','index', fasta_five, '-p', 'index'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Mapping reads to assembly...')
    subprocess.call(['bwa','mem', 'index', read_1, read_2,'-o','mapped.sam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Sorting SAM file...')
    subprocess.call(['samtools','sort', 'mapped.sam', '-o', 'mapped.bam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Polishing assembly with Pilon...')
    subprocess.call(['samtools','index','mapped.bam'])

    # Pilon
    subprocess.call(['pilon','--genome', fasta_five, '--frags', 'mapped.bam', '--output', round_six, '--changes'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('')
    # Remove temp files
    for item in removal:
        os.remove(item)
    roundend()
else:
    print('No changes were made on the last round.')
    goodbye()
    sys.exit(1)

# Round Seven
# Check if changes were made on previous round and continue
if os.path.getsize(changes_six) > 0:
    print(colours.bold)
    print('###########')
    print('Round Seven')
    print('###########', colours.term)
    # Index, Map, Index
    print('')
    print(colours.invoking, 'Indexing Fasta...', colours.term)
    subprocess.call(['bwa','index', fasta_six, '-p', 'index'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Mapping reads to assembly...')
    subprocess.call(['bwa','mem', 'index', read_1, read_2,'-o','mapped.sam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Sorting SAM file...')
    subprocess.call(['samtools','sort', 'mapped.sam', '-o', 'mapped.bam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Polishing assembly with Pilon...')
    subprocess.call(['samtools','index','mapped.bam'])

    # Pilon
    subprocess.call(['pilon','--genome', fasta_six, '--frags', 'mapped.bam', '--output', round_seven, '--changes'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('')
    # Remove temp files
    for item in removal:
        os.remove(item)
    roundend()
else:
    print('No changes were made on the last round.')
    goodbye()
    sys.exit(1)

# Round Eight
# Check if changes were made on previous round and continue
if os.path.getsize(changes_seven) > 0:
    print(colours.bold)
    print('###########')
    print('Round Eight')
    print('###########', colours.term)
    # Index, Map, Index
    print('')
    print(colours.invoking, 'Indexing Fasta...', colours.term)
    subprocess.call(['bwa','index', fasta_seven, '-p', 'index'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Mapping reads to assembly...')
    subprocess.call(['bwa','mem', 'index', read_1, read_2,'-o','mapped.sam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Sorting SAM file...')
    subprocess.call(['samtools','sort', 'mapped.sam', '-o', 'mapped.bam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Polishing assembly with Pilon...')
    subprocess.call(['samtools','index','mapped.bam'])

    # Pilon
    subprocess.call(['pilon','--genome', fasta_seven, '--frags', 'mapped.bam', '--output', round_eight, '--changes'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('')
    # Remove temp files
    for item in removal:
        os.remove(item)
    roundend()
else:
    print('No changes were made on the last round.')
    goodbye()
    sys.exit(1)

# Round Nine
# Check if changes were made on previous round and continue
if os.path.getsize(changes_eight) > 0:
    print(colours.bold)
    print('##########')
    print('Final Round')
    print('###########', colours.term)
    # Index, Map, Index
    print('')
    print(colours.invoking, 'Indexing Fasta...', colours.term)
    subprocess.call(['bwa','index', fasta_eight, '-p', 'index'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Mapping reads to assembly...')
    subprocess.call(['bwa','mem', 'index', read_1, read_2,'-o','mapped.sam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Sorting SAM file...')
    subprocess.call(['samtools','sort', 'mapped.sam', '-o', 'mapped.bam'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('Polishing assembly with Pilon...')
    subprocess.call(['samtools','index','mapped.bam'])

    # Pilon
    subprocess.call(['pilon','--genome', fasta_eight, '--frags', 'mapped.bam', '--output', final_round, '--changes'])
    print('')
    print(colours.bold, colours.blue,'Done!', colours.term)
    print('')
    print('')
    # Remove temp files
    for item in removal:
        os.remove(item)
    roundend()
    #END
    if os.path.getsize(changes_final) >0:
        print('Changes were made in the final round.')
        print('You may want to run an additional round of Pilon.')
        print('')
        goodbye()
    else:
        print('No changes were made on the last round.')
        goodbye()
        sys.exit(1)
else:
    print('No changes were made on the last round.')
    goodbye()
    sys.exit(1)

# Variant Annotation Tool
This program is used to annotate each variant in the provided vcf file. The program is written in python 3.6, please make sure you have the right version installed.

## To run the code.
On the command line run the following scripts.

`python3 Annotate.py -i ExampleInput.vcf -o ExampleOutput.csv`

## Input file
Variant Call Format (VCF) file

## Output file.
A comma separated values with the following annotations for each variant
1. Type of variation.
2. Depth of sequence coverage at the site of variation.
3. Number of reads supporting the variant.
4. Percentage of reads supporting the variant versus those supporting reference reads.
5. Allele frequency of variant.

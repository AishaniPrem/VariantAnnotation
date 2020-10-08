#!usr/bin/python3.6
__author__= 'Aishani Prem'
__email__='aishaniprem@gmail.com'
import re
import argparse
import requests

#---Command Line Arguments----
parser=argparse.ArgumentParser(
      description="This script uses python3. Please make sure you have the correct version installed. This program is used to annotate each variant in the provided vcf file", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('-i','--input', help = "Input vcf file", required = True)
parser.add_argument('-o','--output', help = "Output(csv) file with variant annotation", required = True)

args = parser.parse_args()


####READ THE INPUT VCF FILE
VCFfile = open(args.input, 'r')
VCFfile = VCFfile.readlines()

####Open and write the header for the output file
fout = open(args.output, "w")
fout.write(f"""Chrom,Pos,ID,Type,Depth,NumOfReads,ReadPercent,AlleleFreq\n""")


for line in VCFfile:
	#Skip Headers
	if line.startswith("#"):
		pass
	else:
		#Work with data for each variant
		var = line.split('\t')
		Chrom = var[0]
		Pos = var[1]
		ID = var[2]
		Ref = var[3]
		Alt = var[4]
		Info = var[7].split(";")
		
		#Make dictionary of the info column for each variant
		InfoDict = dict([x.split('=') for x in Info])
		
		#Get data from the information dictionary for variant type, depth and number of reads
		Type = InfoDict['TYPE']
		if re.search('complex',Type):
			Type = 'complex'
		elif re.search('del',Type):
			Type = 'del'
		else:
			Type = Type.split(',')[0]

		#Get the depth of sequence coverage at the site of variation
		Depth = InfoDict["DP"]
		
		#Get the number of reads supporting the varian
		NumOfReads = InfoDict["AO"]
		try: 
			ReadPercent  = round(float(InfoDict["AO"]) / float(InfoDict["RO"]) * 100, 4)

		except:
			ReadPercent = "NA"
		
		#Get Allele frequency data of variant from ExAC API
		data = requests.get(f"http://exac.hms.harvard.edu/rest/variant/variant/{Chrom}-{Pos}-{Ref}-{Alt}")
		data = data.json()
		try:
			AlleleFreq = round(data["allele_freq"], 4)

		except: 
			AlleleFreq = "NA"

		fout.write(f"""{Chrom},{Pos},{ID},{Type},{Depth},{NumOfReads},{ReadPercent},{AlleleFreq}\n""")


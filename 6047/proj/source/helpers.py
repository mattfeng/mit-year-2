import sys


# returns proportion of genes that are in the interactome
def findGenes(genes, gene_dict):
	count = 0
	for g in genes:
		if g in gene_dict:
			count += 1
	return count / float(len(genes))


def readInteractome(interactome_file):
	gene_dict = {}
	file = open(interactome_file, 'r')
	for line in file:
		if not line.startswith('#'):
			split_line = line.split()
			gene1 = split_line[0]
			gene2 = split_line[1]
			if gene1 not in gene_dict:
				gene_dict[gene1] = 0
			if gene2 not in gene_dict:
				gene_dict[gene2] = 0
			gene_dict[gene1] += 1
			gene_dict[gene2] += 1
	return gene_dict

def readGenes(gene_file):
	gene_list = []
	file = open(gene_file, 'r')
	for line in file:
		gene_list.append(line.strip())
	return gene_list


# def convertGeneFile(gene_file):
# 	gene_list = []
# 	file = open(gene_file, 'r')
# 	gene_list = file.readline().strip().split(';')
# 	file.close()

# 	with open(gene_file, 'w') as f:
# 		for gene in gene_list:
# 			f.write(gene + '\n')

# 	return gene_list


def main():
	interactome_file = 'interactome.tsv'
	gene_file = sys.argv[1]

	gene_dict = readInteractome(interactome_file)
	gene_list = readGenes(gene_file)   # use this for line separated gene file (schiz, bipolar, autism)

	# gene_list = convertGeneFile(gene_file)  # use this for semicolon separate gene file (heart disease, diabetes)

	print len(gene_list)

	print findGenes(gene_list, gene_dict)

	
if __name__ == '__main__':
    main()
import sys

def read_fasta_sequences(fasta_file):
    """
    从基因组序列文件中读取序列名列表
    """
    genome_sequence_names = []
    with open(fasta_file, 'r') as fasta:
        for line in fasta:
            if line.startswith('>'):
                genome_sequence_names.append(line.strip()[1:])
    return genome_sequence_names

def filter_gff_by_fasta(gff_file, genome_sequence_names):
    """
    根据基因组序列名列表过滤注释文件，并输出到新文件中
    """
    output_file = "filtered_" + gff_file
    with open(gff_file, 'r') as gff, open(output_file, 'w') as filtered:
        for line in gff:
            if line.startswith('#'):
                filtered.write(line)
                continue
            
            columns = line.strip().split('\t')
            if len(columns) < 1:
                continue
            
            chromosome_name = columns[0]
            if chromosome_name in genome_sequence_names:
                filtered.write(line)
    
    print(f"Filtered GFF file written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test.py <fasta_file> <gff_file>")
        sys.exit(1)
    
    fasta_file = sys.argv[1]
    gff_file = sys.argv[2]
    
    try:
        genome_sequence_names = read_fasta_sequences(fasta_file)
        filter_gff_by_fasta(gff_file, genome_sequence_names)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)


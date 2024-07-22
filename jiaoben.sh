
genome=$1
annotation=$2

genome_prefix=$(echo "${genome}" | sed 's/\_genome\.fasta//')

#awk '$1 ~ /^chr/' ${annotation} > ${genome_prefix}.gff

gffread $2 -T -o ${genome_prefix}.gtf

awk '$3=="transcript"' ${genome_prefix}.gtf | awk '{print $1"\t"$4"\t"$5"\t"$10"\t"$7}' | sed 's/"//g'| sed 's/;//' > ${genome_prefix}.bed


gffread ${genome_prefix}.gtf -g ${genome} -x ${genome_prefix}_CDS.fasta


gffread ${genome_prefix}.gtf -g ${genome} -w ${genome_prefix}_mRNA.fasta


gffread ${genome_prefix}.gtf -g ${genome} -y ${genome_prefix}_protein.fasta

sed '/^>/! s/[^A-Za-z]/X/g' ${genome_prefix}_protein.fasta > ${genome_prefix}_cleaned_protein.fasta


python ~/20240505/Apple_pangenome_GDR_NCBI_20240423/extract_gene_sequence20240521.py --genome_file ${genome} --gene_bedfile ${genome_prefix}.bed --output_file_prefix ${genome_prefix}

python /data/changchuanjun/extract_promoter.py --genome_file ${genome} --gene_bedfile ${genome_prefix}.bed --promoter_range 2000 --output_file_prefix ${genome_prefix}


cp *_gene_sequence.fasta /home/changchuanjun/apple_pan-genefamily_GDR_NCBI_20240619/database_all_genome/gene_sequence/
cp *.bed /home/changchuanjun/apple_pan-genefamily_GDR_NCBI_20240619/database_all_genome/gene_bed/
cp *_CDS.fasta /home/changchuanjun/apple_pan-genefamily_GDR_NCBI_20240619/database_all_genome/CDS/
cp *_cleaned_protein.fasta /home/changchuanjun/apple_pan-genefamily_GDR_NCBI_20240619/database_all_genome/protein/
cp *_mRNA.fasta /home/changchuanjun/apple_pan-genefamily_GDR_NCBI_20240619/database_all_genome/mRNA/
cp *_promoter_sequence.fasta /home/changchuanjun/apple_pan-genefamily_GDR_NCBI_20240619/database_all_genome/promoter/

#/home/changchuanjun/apple_pan-genefamily_GDR_NCBI_20240619/database_all_genome/

from Bio import SeqIO
from Bio.Seq import Seq
import logging
import argparse
import warnings
import datetime

warnings.simplefilter(action="ignore", category=RuntimeWarning)
warnings.simplefilter(action="ignore", category=PendingDeprecationWarning)

log = logging.getLogger(__name__)


parser = argparse.ArgumentParser(add_help=False,description='extract promoter sequence using genome file and gene position bed file ')

parserRequired = parser.add_argument_group('Required arguments')
# define the arguments
parserRequired.add_argument('--genome_file', '-genome',help='genome_fasta_file',required=True)

parserRequired.add_argument('--gene_bedfile', '-bed',help='gene_position_bed_file',required=True)

parserRequired.add_argument('--promoter_range', '-pro',help='promoter_range,generally2000',required=True)

parserRequired.add_argument('--output_file_prefix', '-out',help='output_promoter_sequence_file',required=True)

current_time = datetime.datetime.now()


formatted_time = current_time.strftime("%Y_%m_%d")

args = parser.parse_args()  # 解析参数


input_genome=args.genome_file
input_genebedfile=args.gene_bedfile
input_promoterrange=int(args.promoter_range)
output_result=str(args.output_file_prefix)+"-"+formatted_time+"_promoter_sequence.fasta"
promoter_position_bed_file_result=str(args.output_file_prefix)+"-"+formatted_time+"_promoter_position.bed"

#def extract_promoters(bed_file, genome_fasta, upstream_length=input_promoterrange, output_file=output_result,bed_output=promoter_position_bed_file_result):

def extract_promoters(bed_file, genome_fasta, upstream_length=input_promoterrange, output_file=output_result, bed_output=promoter_position_bed_file_result):
    # 读取基因组 fasta 文件
    genome_sequences = SeqIO.to_dict(SeqIO.parse(genome_fasta, "fasta"))

    # 打开输出文件准备写入启动子序列
    with open(output_file, "w") as output:
        # 打开 BED 输出文件准备写入启动子坐标信息
        with open(bed_output, "w") as bed_output_file:
            # 遍历 bed 文件
            with open(bed_file, "r") as bed:
                for line in bed:
                    fields = line.strip().split("\t")
                    chrom, start, end, name, strand = fields[:5]

                    # 确定启动子区域的起始和结束位置
                    start = int(start)
                    end = int(end)
                    if strand == "+":
                        promoter_start = max(0, start - upstream_length-1)
                        promoter_end = start-1
                        promoter_seq = genome_sequences[chrom][promoter_start:promoter_end].seq
                    elif strand == "-":
                        promoter_start = max(0, end)
                        promoter_end = min(len(genome_sequences[chrom]), end + upstream_length)
                        promoter_seq = genome_sequences[chrom][promoter_start:promoter_end].seq.reverse_complement()
                    else:
                        print("Unknown strand:", strand)
                        continue

                    # 输出启动子序列到文件中
                    output.write(">{}_promoter\n".format(name))
                    output.write(str(promoter_seq) + "\n")

                    # 输出启动子坐标信息到 BED 文件中
                    bed_output_file.write("{}\t{}\t{}\t{}_promoter\t{}\n".format(chrom, promoter_start, promoter_end, name, strand))




# 调用函数提取启动子序列，并将结果保存到指定文件中
extract_promoters(input_genebedfile, input_genome, upstream_length=input_promoterrange, output_file=output_result,bed_output=promoter_position_bed_file_result)


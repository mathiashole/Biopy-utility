import os
import subprocess
from Bio import SeqIO

# 设置输入和输出文件夹路径
input_folder = './Single_Copy_Orthologue_Sequences'  # 存放包含基因序列的文件夹路径
output_folder = './orthofinder_result-2-concatenated_sequences__output_folder'  # 存放比对结果和保守位点序列的文件夹路径
concatenated_output_file1 = os.path.join(output_folder, 'concatenated_sequences_no-trimal.fasta')  # 存放串联后的保守位点序列的文件路径
concatenated_output_file2 = os.path.join(output_folder, 'concatenated_sequences_trimaled.fasta')  # 存放串联后的保守位点序列的文件路径

# 创建输出文件夹（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 存储每个物种的序列
species_sequences1 = {}
species_sequences2 = {}

def run_command(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Command failed: {cmd}")
        exit(1)

# Step 1: 对每个文件进行muscle比对并使用trimal保留保守位点
for filename in os.listdir(input_folder):
    if filename.endswith('.fa'):  # 假设文件格式为FASTA格式
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, f'{filename}_aligned.fasta')
        muscle_cmd = f"muscle -align {input_file} -output {output_file}"
        run_command(muscle_cmd)

        trimmed_output_file = os.path.join(output_folder, f'{filename}_trimmed.fasta')
        trimal_cmd = f"trimal -in {output_file} -out {trimmed_output_file} -automated1"
        run_command(trimal_cmd)

        # 检查文件是否为空
        if os.stat(output_file).st_size == 0:
            continue
        if os.stat(trimmed_output_file).st_size == 0:
            continue

        # 读取保守位点序列，并将相同物种的序列进行串联
        for record in SeqIO.parse(output_file, 'fasta'):
            species = record.id.split('|')[0]  # 假设物种名称在序列ID中以"|"分隔并位于第一个部分
            if species not in species_sequences1:
                species_sequences1[species] = ''
            species_sequences1[species] += str(record.seq)

        for record in SeqIO.parse(trimmed_output_file, 'fasta'):
            species = record.id.split('|')[0]  # 假设物种名称在序列ID中以"|"分隔并位于第一个部分
            if species not in species_sequences2:
                species_sequences2[species] = ''
            species_sequences2[species] += str(record.seq)

# Step 2: 将每个物种的保守位点串联起来并存放在一个文本文件中
with open(concatenated_output_file1, 'w') as f:
    for species, sequence in species_sequences1.items():
        f.write(f'>{species}\n{sequence}\n')

with open(concatenated_output_file2, 'w') as f:
    for species, sequence in species_sequences2.items():
        f.write(f'>{species}\n{sequence}\n')

# Step 3: 再次muscle比对并使用trimal保留保守位点
def muscle_and_trimal(input_file, output_file_prefix):
    output_file = os.path.join(output_folder, f'{output_file_prefix}.fasta')
    muscle_cmd = f"muscle -align {input_file} -output {output_file}"
    run_command(muscle_cmd)
    
    trimmed_output_file = os.path.join(output_folder, f'{output_file_prefix}_then_trimmed.fasta')
    trimal_cmd = f"trimal -in {output_file} -out {trimmed_output_file} -automated1"
    run_command(trimal_cmd)

muscle_and_trimal(concatenated_output_file1, 'C.S_no-trimal-again-muscle')
muscle_and_trimal(concatenated_output_file2, 'C.S_trimaled-again-muscle')


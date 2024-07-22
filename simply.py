import sys
import re
import shutil

def process_fasta(input_file):
    # 根据输入文件名生成临时文件名
    output_file = f"{input_file}.modify.fasta"

    try:

        # 打开输入文件和临时输出文件
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                if re.match(r'^>', line):
                    #line = line.replace('>', '')
                    fields = line.split()
                    if len(fields) >= 6:
                        fields[5] = fields[5].replace(',', '')
                        outfile.write('>'+fields[5] + '\n')
                    else:
                        outfile.write(line)
                else:
                    outfile.write(line)

        print(f"Processing of {input_file} completed successfully.")
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_fasta.py <input_file>")
    else:
        input_file = sys.argv[1]
        process_fasta(input_file)


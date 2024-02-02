import sys
import os
import json
import glob

if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <qcdir>")
    sys.exit(1)

qcdir = sys.argv[1]

# 获取 fastp qc 文件的路径列表
files = glob.glob(os.path.join(qcdir, "*.json"))
assert len(files) > 0, f"failed to find fastp json files in dir: {qcdir}"

result_file=qcdir+"/"+"all_sample_fastp_result.txt"
# 打开输出文件，并使用 with 语句确保文件的正确关闭
with open(result_file, "w") as outfile:
    # 向输出文件写入一行表头，包含了一些列名信息
    outfile.write("SampleID\trawDataReads\tcleanDataReads\trawDataBase\tcleanDataBase\tQ20\tQ30\tGC\n")

    # 遍历所有 fastp qc 文件
    for i in sorted(files):
        samplename = os.path.splitext(os.path.basename(i))[0]

        with open(i, "r") as f:
            qcjs = json.load(f)

            # 获取各项统计值
            rawDataReads = format(qcjs["summary"]["before_filtering"]["total_reads"], ",")
            rawDataBase = format(qcjs["summary"]["before_filtering"]["total_bases"], ",")
            cleanDataReads = format(qcjs["summary"]["after_filtering"]["total_reads"], ",")
            cleanDataBase = format(qcjs["summary"]["after_filtering"]["total_bases"], ",")
            Q20 = format(qcjs["summary"]["after_filtering"]["q20_rate"] * 100, '0.2f')
            Q30 = format(qcjs["summary"]["after_filtering"]["q30_rate"] * 100, '0.2f')
            GC = format(qcjs["summary"]["after_filtering"]["gc_content"] * 100, '0.2f')

            # 写入输出文件
            outfile.write("\t".join([samplename, rawDataReads, cleanDataReads, rawDataBase, cleanDataBase, Q20, Q30, GC]) + "\n")

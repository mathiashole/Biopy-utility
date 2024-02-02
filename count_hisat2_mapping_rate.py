import os
import logging
import argparse
import warnings
import datetime

warnings.simplefilter(action="ignore", category=RuntimeWarning)
warnings.simplefilter(action="ignore", category=PendingDeprecationWarning)

log = logging.getLogger(__name__)


parser = argparse.ArgumentParser(add_help=False,description='Counts a summary of every samples hisat2_mapping rate ')

parserRequired = parser.add_argument_group('Required arguments')

# define the arguments
parserRequired.add_argument('--the_input_location_of_mapping_log', '-input',help='Location of the mapping log to detect.',required=True)

#parserRequired.add_argument('--outFileName', '-out',help='File name to save the result.',type=writableFile,required=True)
parserRequired.add_argument('--outFileName', '-out',help='File name to save the result.',required=True)

#parserOpt = parser.add_argument_group('Optional arguments')
#parserOpt.add_argument('--result_file_name', '-outputname',help='Resul_file_tname.',default="hisat2_mapping.txt")

current_time = datetime.datetime.now()

#parsed_time = datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S.%f")

formatted_time = current_time.strftime("%Y_%m_%d_%H_%M_%S")
#formatted_time = parsed_time.strftime("%Y_%m_%d_%H_%M_%S")
#args = parse_arguments().parse_args(args)
#args = parse_arguments()

args = parser.parse_args()  # 解析参数


file_directory=args.the_input_location_of_mapping_log
save_path=args.outFileName



log.debug("Program starts to execute")

yp_name=[]
yp_content=[]


log_file=[]
tem_file=os.listdir(file_directory)
for i in tem_file:
    if i.endswith("log"):
        log_file.append(i)

log_file=sorted(log_file)
media_connect="/"

def huizong_write():
    rate_sum=open(save_path+media_connect+"hisat2_mapping_rate"+formatted_time+".txt","w")
    for i in log_file:
        log_file_path=file_directory+media_connect+i
        yp_name.append(i)
        for line in open(log_file_path):
            if line[1:8]=="Overall":
                yp_content.append(line.split("\t")[-1])
    if len(yp_name)==len(yp_content):
        for i in range(len(yp_name)):
            rate_sum.write(yp_name[i]+"\t"+yp_content[i])
    rate_sum.close()

def delete_log_huoqu():
    delete_wj=[]
    for i in log_file:
        if i.endswith("log"):
            delete_wj.append(file_directory+media_connect+i)
    return delete_wj

def delete_log():
    delete_file=delete_log_huoqu()
    for i in delete_file:
        os.remove(i)

#mapping_sum_exists()
huizong_write()
delete_log_huoqu()
#delete_log()

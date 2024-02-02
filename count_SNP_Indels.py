import os

yp_name=[]
yp_content=[]
yp_indels=[]
route_path="./"
log_file=[]
tem_file=os.listdir(route_path)
for i in tem_file:
    if i.endswith("log"):
        log_file.append(i)

log_file=sorted(log_file)
media_connect=""
def mapping_sum_exists():
    if os.path.exists(route_path+media_connect+"mapping_sum.txt"):
        os.remove(route_path+media_connect+"mapping_sum.txt")
    else:
        pass

def huizong_write():
    rate_sum=open(route_path+media_connect+"mapping_sum.txt","w")
    for i in log_file:
        log_file_path=route_path+media_connect+i
        yp_name.append(i)
        for line in open(log_file_path):
            if line[0:14]=="Number of SNPs":
                yp_content.append(line.split("\t")[-1])
            if line[0:16]=="Number of INDELs":
                yp_indels.append(line.split("\t")[-1])
    if len(yp_name)==len(yp_content)==len(yp_indels):
        for i in range(len(yp_name)):
            rate_sum.write(yp_name[i]+"\t"+yp_content[i].replace("\n","")+"\t"+yp_indels[i])
    rate_sum.close()

def delete_log_huoqu():
    delete_wj=[]
    for i in log_file:
        if i.endswith("log"):
            delete_wj.append(route_path+media_connect+i)
    return delete_wj

def delete_log():
    delete_file=delete_log_huoqu()
    for i in delete_file:
        os.remove(i)

mapping_sum_exists()
huizong_write()

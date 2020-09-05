f=open("Segment.txt","r",encoding="gb18030",errors="ignore")
out1=open("train.txt","w+")
out2=open("test.txt","w+")
cnt=0
total=len(f.readlines())
f.seek(0)#回到文件开头
for line in f.readlines():
    cnt+=1
    if cnt>=round(total*0.9):#10作为测试集
        try:
            out2.writelines(line)
        except UnicodeEncodeError:
            continue
    else:
        try:
            out1.writelines(line)#90%作为训练集
        except UnicodeEncodeError:
            continue


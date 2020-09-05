f=open("Segment.txt","r",encoding="gb18030",errors="ignore")
max_length=0
for line in f:
    word_list=line.strip().split(" ")
    for word in word_list:
        if len(word)>max_length:
            max_length=len(word)
print("最大词长度:",max_length)
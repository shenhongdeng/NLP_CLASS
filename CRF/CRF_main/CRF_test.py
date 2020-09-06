with open("result.txt","r",encoding="utf8") as f:
    total_cnt = 0
    correct_cnt = 0
    total_cnt_test=0
    for line in f:
        line = line.strip()
        if line == '': continue
        word, r, p = line.split()
        if p=='S'or p=='E':
            total_cnt+=1
            if r==p:
                correct_cnt+=1
        if r=='S'or r=='E':
            total_cnt_test+=1
    precision=correct_cnt/total_cnt
    recall=correct_cnt/total_cnt_test
    F1=2*precision*recall/(recall+precision)
    print("Precision:",precision)
    print("Recall:",recall)
    print("F1:",F1)
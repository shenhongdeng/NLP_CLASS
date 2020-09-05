import json
def get_word_reverse_list():#把语料里的所有词读入并反转
    IN = open("train.txt", "r", encoding="gb18030",errors='ignore')
    word_list = []
    for line in IN:
        single_sen = line.strip()
        if not single_sen:
            continue
        else:
            single_sen = single_sen.split(" ")
        for word in single_sen:
            word_list.append(word[::-1])#把字符串反转过来填入
    return list(set(word_list))
def create_single_tree(flag,cur_dict,word,cur_word,cur_num,length_of_word):#这里flag就是判断当前词是不是在词典树里面建好了，cur_dict就是当前到的树的那一层的结点，word就是当前在填充的词，cur_word就是这个词里面当前在建的字,cur_num就是层数，length_of_word就是词的长度
    if  flag == 0:
        return
    if not cur_dict.get(cur_word):
        cur_dict[cur_word]={}
    cur_num+=1
    if cur_num==length_of_word:
        flag=0
        return
    return create_single_tree(flag,cur_dict[cur_word],word,word[cur_num],cur_num,length_of_word)#递归建树

def create_whole_dict_tree(dict_tree,word_list):#就是把语料里的所有的词都读入，然后每个词去调用create_single_tree来把每个词填充到树里面
    for word in word_list:
        try:
            create_single_tree(1,dict_tree,word,word[0],0,len(word))
        except IndexError:
            continue
    return dict_tree

def dump_dict_back_tree():#把树存储成json文件
    word_list=get_word_reverse_list()
    # word_list=['人国中','间中','打','鼠地']
    # print("假设的反向词表:",word_list)
    dict_tree={}
    dict_tree=create_whole_dict_tree(dict_tree, word_list)
    # print("假设的词表的dict树形结构:",dict_tree)
    # sen="中国人会打地鼠"
    # print("测试语句:",sen)
    # ans_list = split_sen_by_back(sen, dict_tree)
    # print("分词结果:", ans_list)
    out=open("dict_back_tree.json","w+")
    json.dump(dict_tree,out)
    out.close()
dump_dict_back_tree()

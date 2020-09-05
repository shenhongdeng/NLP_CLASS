import json
#这里的代码注释和反向的一样就不再赘述了
def get_word_list():
    IN = open("train.txt", "r", encoding="gb18030",errors='ignore')
    word_list = []
    for line in IN:
        single_sen = line.strip()
        if not single_sen:
            continue
        else:
            single_sen = single_sen.split(" ")
        for word in single_sen:
            word_list.append(word)
    return list(set(word_list))
def create_single_tree(flag,cur_dict,word,cur_word,cur_num,length_of_word):
    if  flag == 0:
        return
    if not cur_dict.get(cur_word):
        cur_dict[cur_word]={}
    cur_num+=1
    if cur_num==length_of_word:
        flag=0
        return
    return create_single_tree(flag,cur_dict[cur_word],word,word[cur_num],cur_num,length_of_word)

def create_whole_dict_tree(dict_tree,word_list):
    for word in word_list:
        try:
            create_single_tree(1,dict_tree,word,word[0],0,len(word))
        except IndexError:
            continue
    return dict_tree


def dump_dict_forward_tree():
    word_list=get_word_list()
    # word_list=['中国人大','中间','打','地鼠']
    # print("假设的词表:",word_list)
    dict_tree={}
    dict_tree=create_whole_dict_tree(dict_tree, word_list)
    # print("假设的词表的dict树形结构:",dict_tree)
    # sen="中国人会打地鼠"
    # print("测试语句:",sen)
    # ans_list = split_sen(sen, dict_tree)
    # print("分词结果:", ans_list)
    out=open("dict_forward_tree.json","w+")
    json.dump(dict_tree,out)
    out.close()
# dump_dict_forward_tree()

# word_list=['中国人','中间','打','地鼠']
# word_list_reverse=[]
# for word in word_list:
#     word_list_reverse.append(word[::-1])
#
#
# print(word_list_reverse)

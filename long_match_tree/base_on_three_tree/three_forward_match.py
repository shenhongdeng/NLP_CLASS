import json
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
# word_list=get_word_list()
def create_three_forward_tree(word_list):
    first_word_set=set()
    transit_dict_list=list(dict() for i in range(32))
    for word in word_list:
        try:
            first_word=word[0]
            first_word_set.add(first_word)
            for i in range(len(word)-1):
                if word[0:i+1] not in transit_dict_list[i].keys():
                    transit_dict_list[i][word[0:i+1]]=set()
                transit_dict_list[i][word[0:i+1]].add(word[i+1])
        except IndexError:
            continue
    first_word_list_sorted=sorted(list(first_word_set))
    for single_dict in transit_dict_list:
        for key,value in single_dict.items():
            single_dict[key]=sorted(list(value))
    return first_word_list_sorted,transit_dict_list

def dump_three_forward_tree():
    word_list=get_word_list()
    first_word_list_sorted,transit_dict_list=create_three_forward_tree(word_list)
    f1=open("three_dict_forward_tree.json","w+")
    json.dump(transit_dict_list,f1)
    f2=open("first_word_list_sorted.json","w+")
    json.dump(first_word_list_sorted,f2)

def binary_search(word_list, target):
    low = 0  # 最小数下标
    high = len(word_list) - 1  # 最大数的下标
    while low <= high:
        mid = (low + high) // 2  # 取中间值
        if word_list[mid] == target:
            return word_list[mid]
        elif word_list[mid] > target:
            high = mid - 1  # 如果中间值比目标值大,则在mid左半边找
        else:
            low = mid + 1  # 如果中间值比目标值小,则在mid右半边找
    return False#没找到


def search(sen,transit_dict_list,first_word_list_sorted):
    cur_word=binary_search(first_word_list_sorted,sen[0])
    if cur_word==False or len(sen)==1:#只有一个字的，和第一个字就找不到的
        return 0
    for i in range(len(sen)-1):
        # if cur_word not in transit_dict_list[i].keys():#单字词的情况
        #     return i
        next_list=transit_dict_list[i][cur_word]
        temp_word=binary_search(next_list,sen[i+1])
        if temp_word==False:
            return i#返回最后一个字的下标
        else:cur_word+=temp_word
        if cur_word not in transit_dict_list[i+1].keys() or len(cur_word)==len(sen):
            return i+1

def split_sen_by_forward(sen,transit_dict_list,first_word_list_sorted):
    ans_list=[]
    origin_sen=sen
    while True:
        cut_place=search(sen,transit_dict_list,first_word_list_sorted)
        ans_list.append(sen[:cut_place+1])
        if "".join(ans_list)==origin_sen:
            break
        else:sen=sen[cut_place+1:]
    return ans_list
def test_small_word_list():
    test_sen = "中国人会打地鼠"
    word_list = ['中国人', '中间', '打', '地鼠']
    first_word_list_sorted,transit_dict_list=create_three_forward_tree(word_list)
    print("假设的词表:",word_list)
    print("假设词表的所有词的第一个字的排序序列:",first_word_list_sorted)
    print("基于假设的词表建出来的树结构:",transit_dict_list)
    print("测试语句:",test_sen)
    print("测试分词结果:",split_sen_by_forward(test_sen,transit_dict_list,first_word_list_sorted))

# dump_three_forward_tree()
def test():
    In1=open("three_dict_forward_tree.json","r")
    transit_dict_list=json.load(In1)
    In2=open("first_word_list_sorted.json","r")
    first_word_list_sorted=json.load(In2)
    while True:
        sen = input("plz input a sentence (input q to quit):")
        if sen == 'q':
            break
        ans_list = split_sen_by_forward(sen,transit_dict_list,first_word_list_sorted)
        print("分词结果:", ans_list)

test()
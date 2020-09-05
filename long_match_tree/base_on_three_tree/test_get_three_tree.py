words = ['as', 'at', 'be', 'he', 'by', 'in', 'of', 'is', 'it','on', 'or', 'to']
tree = []
first_alpha=set()
second_alpha={}

def create_tree(cur_tree,start,end,first_alpha):#先基于单词的第一个字母建树
    if end-start<1:return
    cur_tree.append(first_alpha[int((start+end)/2)])
    cur_tree.append([])
    cur_tree.append([])
    create_tree(cur_tree[1],start,int((start+end)/2),first_alpha)
    create_tree(cur_tree[2],int((start+end)/2)+1,end,first_alpha)

def add_tree(tree,char,alpha):#然后把单词的第二个字母添加到树当中去
    if len(tree)==0:
        return 0
    if char>tree[0]:
        return add_tree(tree[2],char,alpha)
    elif char<tree[0]:
        return add_tree(tree[1],char,alpha)
    else:
        tree.append([])
        create_tree(tree[3],0,len(alpha),alpha)#列表的三号元素插入下一个字母的二叉树
        return 1

for word in words:
    first_alpha.add(word[0])
    if not second_alpha.get(word[0]):
        second_alpha[word[0]]=set()
    second_alpha[word[0]].add(word[1])

first_alpha=sorted(first_alpha,key=lambda x:x)#排序
print("第一个字母集合:",first_alpha)
for k in second_alpha.keys():
    second_alpha[k]=sorted(second_alpha[k],key=lambda x:x)
    print("字母",k,"后对应的字母集合:",second_alpha[k])

create_tree(tree,0,len(first_alpha),first_alpha)#建首字母的二叉树
for k,v in second_alpha.items():#加入第二个字母
    add_tree(tree,k,v)
print("词典树结构:",tree)

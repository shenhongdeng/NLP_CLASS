import re
import struct
from functools import cmp_to_key

class Idx():
	HZIdx=[0 for i in range(0x10000)]#0x10000其实就是65535,也就是中文的码表的最大范围，可以包含所有的汉字，这里把个数都
	#都初始化为0，HZIdx就是倒排索引表(接上一行)
	CMP_LEN=10
	PosIdx=[]
	FTXDat=[]
	TotalNum=0
	def MergeFilesUnicode(self,FileList,DatFile):#DatFile对应的是正排表
		Out=open(DatFile,"wb")
		for i in range(len(FileList)):#把list下的所有文件的所有字符都编码成GBK然后存到Out当中(这里刚好只有一个文件)
			Inp=open(FileList[i],"r")
			DatBuf=Inp.read()#read()相当于是把文件当成一整个字符串读进来
			Inp.close()#关闭当前文件
			self.TotalNum+=len(DatBuf)#把字符串的长度加到total上
			self.WriteData(DatBuf,Out)#把文件的每一个字符编码成GBK然后写到Out当中去，并且在HZIdx中把字对应的GBK编码变成数组下标
			#然后在数组上统计各个字的频率(接上一行)

			print("Processing ",FileList[i])
		Out.close()
		return True

	def	CreateIdx(self,FileList,DatFile,HZIdxFile,PosIdxFile):
		if not self.MergeFilesUnicode(FileList,DatFile):#把FileList下的所有文件的字符都编码成GBK然后存到DatFile中，(判断语句也是会执行里面的函数的)
			return False
		if not self.PosInfoFill(DatFile):#就是把倒排文件表建好了，并且还恢复了一下HZIdx表
			return False

		if not self.WriteHZ(HZIdxFile):#把倒排索引表写入文件存储起来
			return False

		if not self.WriteIdx(PosIdxFile):#把倒排文件表写入文件存储起来
			return False
		return True


	def WriteData(self,DatBuf,Out):
		for i in range(len(DatBuf)):#遍历文件中的每个字符
			GB=DatBuf[i].encode("gbk")#把它都编码成GBK的编码
			if len(GB) == 1:#如果是一个字节的话,一些符号是一个字节的
				ID=struct.unpack("B",GB)#一个字节长度的对应用B去unpack
			else:#两个字节，汉字都是两个字节的
				ID=struct.unpack("H",GB)#两个字节长度的对应用H去unpack
			self.HZIdx[ID[0]]+=1#unpack的结果其实是一个元组比如"我"encode完以后再unpack的结果就是(53966,)，要ID[0]把数字取出来
			#然后这里其实就是先统计各个字的词频(接上一行)
			Out.write(GB)#这里就是把每个字的GBK编码都写入到Out对应的文件中(正排表)
		return True	


	def GetReadyHZ(self):
		for i in range(0x10000):#遍历倒排索引表
			self.HZIdx[i]+=self.HZIdx[i-1]#数组原先装的是各个字的词频，现在把它变成倒排文件对应的该字的起始编号

	def RecoveryHZ(self):#HZIdx中的内容全部后推一个元素，使得HZIdx[i]为内码是0到i-1的汉字的总个数
		for i in range(0x10000-1,0,-1):
			self.HZIdx[i]=self.HZIdx[i-1]
		self.HZIdx[0]=0

	def cmp(self,X1,X2):
		if X1+self.CMP_LEN < self.TotalNum  and X2+self.CMP_LEN < self.TotalNum:#首先看下搜索区域有没有超出文本总长度
			Str1=self.FTXDat[X1:X1+self.CMP_LEN]#就只要求出这个字后面10个长度的字符出来就可以
			Str2=self.FTXDat[X2:X2+self.CMP_LEN]
			if Str1 < Str2:#这其实就相当于字符串的字典序排序
				return -1
			elif Str1 > Str2:
				return 1
		return 0
		
	def SortWrite(self,Out):
		for i in range(0x10000-1):
			BlockBuff=self.PosIdx[self.HZIdx[i]:self.HZIdx[i+1]]#通过倒排索引表找到倒排文件表对应字的聚集区域，然后把它切出来
			BlockBuff=sorted(BlockBuff,key=cmp_to_key(self.cmp))#这边这个cmp_to_key是一个从python 2升级过来的cmp参数函数，它可以把cmp参数转化成key 参数，因为python3的sorted函数
			#没有cmp参数，只有key函数，这里实现对聚集区域的内容进行排序(接上一行)

			for j in range(len(BlockBuff)):
				Num=struct.pack("I",BlockBuff[j])#把排好序的倒排文件聚集区域pack一下成两个字节长度的字节流
				Out.write(Num)#写入文件
	def PosInfoFill(self,DatFile):#建好倒排文件表
		self.GetReadyHZ()#把倒排索引表建好，数组的值对应的是该字在倒排文件中的序号ID

		Inp=open(DatFile,"r")#读入各个字符对应的GBK编码的这个文件(正排表)
		self.FTXDat=Inp.read()#以字符串的形式赋值给FTXDat
		Inp.close()#关闭文件
		self.PosIdx=[0 for i in range(len(self.FTXDat))]#倒排文件数组的元素个数和正排文件元素个数(字符个数)一样

		for i in range(len(self.FTXDat)):
			GB=self.FTXDat[i].encode("gbk")#因为读进来的时候是r的方式，所以还要再把文件的每个字符编码成GBK
			if len(GB) == 1:#符号的那些就是一个字节长度
				ID=struct.unpack("B",GB)#得到字符对应的数字编码
			else:#汉字是两个字节长度
				ID=struct.unpack("H",GB)#得到字符对应的数字编码
		
			self.PosIdx[self.HZIdx[ID[0]-1]]=i#ID[0]才是真正的对应的数值ID,减一是上一个字的结尾的位置，是个开区间
			#然后i对应的是该字在正排表的编号(接上一行)

			self.HZIdx[ID[0]-1]+=1#该字倒排索引上的结尾区间的数字加1，其实就是表示个数，老师上课说这个其实可以两个字的
			#起始位置相减就可以得到个数(接上一行)

		self.RecoveryHZ()#HZIdx中的内容全部后推一个元素，使得HZIdx[i]为内码是0到i-1的汉字的总个数
		return True

	def WriteHZ(self,HZIdxFile):
		Out=open(HZIdxFile,"wb")
		for i in range(len(self.HZIdx)):#遍历倒排索引表
			Num=struct.pack("I",self.HZIdx[i])#把倒排索引表的值(倒排文件的序号ID)pack成字节流，I对应的是Unsigned int
			Out.write(Num)#把转换好的倒排文件序号ID写入文件中(就是把倒排索引数组的值存储起来)
		Out.close()
		return True	

	def WriteIdx(self,PosIdxFile):
		Out=open(PosIdxFile,"wb")
		Num=struct.pack("I",self.TotalNum)#把总的字符个数先写入文件中
		Out.write(Num)
		self.SortWrite(Out)#把倒排文件中每个字对应的聚集区域排序，并写入文件
		Out.close()#关闭文件
		return True	


class FTR:
	HZIdx=[]#用来存储倒排索引
	PosIdx=[]#用来存储倒排文件
	FTXDat=[]#用来存储正排表
	TotalNum=0#整个大文档的字符的数量
	CMP_MAXLEN=10#比较字符串时候取的字符串长度

	def FTRInit(self,HZIdxFile,DatFile,psIdx):
		Inp=open(HZIdxFile,"rb")#以字节流的方式读入倒排索引
		self.HZIdx=[0 for i in range(0x10000)]#初始化倒排索引表
		for i in range(0x10000):
			NumByte=Inp.read(4)#也就是读2个字节长度的数据出来
			Num=struct.unpack("I",NumByte)#转化成数值ID
			self.HZIdx[i]=Num[0]#把之前存储好的HZIdx的信息都赋值过来
		Inp.close()


		Inp=open(psIdx,"rb")#以字节流的方式读入倒排文件
		NumByte=Inp.read(4)#读2个字节长度的数据出来
		Num=struct.unpack("I",NumByte)#转化成数值ID
		self.TotalNum=Num[0]#第一个读进来的对应的是在大文档的字符的数量
		self.PosIdx=[0 for i in range(self.TotalNum)]#先初始化为0
		for i in range(self.TotalNum):
			NumByte=Inp.read(4)#读2个字节长度的数据出来
			Num=struct.unpack("I",NumByte)#转化成数值ID
			self.PosIdx[i]=Num[0]#把之前存储好的PosIdx的信息都赋值过来
		Inp.close()


		Inp=open(DatFile,"r")#读入正排表
		self.FTXDat=Inp.read()#以整个字符串的方式读入
		Inp.close()


	def bSearchLow(self,Start, End , Query):
		CompRes = 0#用于存放字符串的比较结果
		mid  = 0#同于二分查找更新区间
		if Start >= End:#如果区域的起点大于终点就是错误的
			return -1   

		nLen=len(Query)#查询的关键字的字符串的长度
		if nLen > self.CMP_MAXLEN:#如果查询的字符串长度超过10
			nLen = self.CMP_MAXLEN#就只把查询的字符串的长度就定为10
		CmpStr=self.FTXDat[self.PosIdx[Start]:self.PosIdx[Start]+nLen]#把对应区间的倒排文件对应的正文的内容取nlen个出来
		if CmpStr > Query:#取出来的内容的字典序比用户查询的内容来的大
			CompRes=1
		elif CmpStr < Query:#取出来的内容的字典序比用户查询的内容来的小
			CompRes=-1
			
		if CompRes == 0:#取出来的内容和用户查询的内容一致
			return Start
		
		if End - Start == 1:#字的对应在倒排文件中的聚集区域的个数只有1个
			return -1  
		
		if CompRes > 0:#如果取出来的内容的字典序比用户查询的内容来的大，那么在这个聚集区域里面就肯定不存在和用户输入匹配的字符串了
			return -1   
		
		mid = int((Start + End)/2)#二分查找，这里就是要缩小搜索区间
		Ret = self.bSearchLow( Start , mid , Query)#抽取出左边区域，然后继续进行二分查找
		if Ret == -1:#如果没找到可以匹配query的数据
			return self.bSearchLow( mid, End , Query) #抽取出右边区域，然后继续进行二分查找
		return Ret#如果有找到，返回的是对应倒排文件表的最开始的编号，没找到就是-1


	def bSearchHigh(self,Start, End ,Query):
		CompRes = 0#用于存放字符串的比较结果
		mid  = 0#同于二分查找更新区间
		Ret= 0
		if Start >= End:#如果区域的起点大于终点就是错误的
			return -1   
			
		nLen=len(Query)#用户查询的关键字的字符串长度
		if  nLen > self.CMP_MAXLEN:#如果超过10
			nLen = self.CMP_MAXLEN#就把它改为10

		CmpStr=self.FTXDat[self.PosIdx[End-1]:self.PosIdx[End-1]+nLen]#从该字在倒排文件中的位置取其对应在正文的位置，然后截取nlen长度的字符串出来进行比较
		if CmpStr > Query:#取出来的内容的字典序比用户查询的内容来的大
			CompRes=1
		elif CmpStr < Query:#取出来的内容的字典序比用户查询的内容来的小
			CompRes=-1

		if CompRes == 0:#取出来的内容和用户查询的内容一致
			return End  

		if End - Start == 1:#字的对应在倒排文件中的聚集区域的个数只有1个
			return -1

		if CompRes < 0:#如果取出来的内容的字典序比用户查询的内容来的小，那么在这个聚集区域里面就肯定不存在和用户输入匹配的字符串了
			return -1  

		mid = int(( Start + End)/2)   #二分查找，这里就是要缩小搜索区间
		Ret = self.bSearchHigh( mid , End , Query)  #抽取出右边的区域，然后继续进行二分查找
		if  Ret == -1:#如果没找到可以匹配query的数据
			return self.bSearchHigh( Start, mid , Query) #就抽取出左边的区域，然后继续进行二分查找
		return Ret#如果有找到，返回的是对应倒排文件表的最后的编号，没找到就是-1


	def SearchFTR(self,Start, End,Query,FTSRet,WindowSize,RetNum):
		nPosLow=self.bSearchLow(Start,End,Query)#从该字聚集区域的开始点和结束点(也就是倒排文件的编号开始和结束的位置)进行二分查找，找到区间的下界
		if  nPosLow == -1:#看有没有找到
			return False

		nPosHigh=self.bSearchHigh(Start,End,Query)#从该字聚集区域的开始点和结束点(也就是倒排文件的编号开始和结束的位置)进行二分查找，找到区间的上界
		
		for i in range(nPosLow,nPosHigh):#遍历查找出来符合用户query的区间上下界区域
			if self.PosIdx[i] < WindowSize:#windowsize是20，如果查找出来的关键字对应的正排表的位置小于20
				nFirst=0#它其实就是要显示符合用户输入的文档的字符串的起始截取位置
			else:#否则
				nFirst=self.PosIdx[i]-WindowSize#就减去20


			if self.PosIdx[i]+len(Query)+WindowSize > self.TotalNum:#如果对应的正排表的位置+用户搜索的字符串的长度以后再加上20超过整个文档的长度的话
				nLast=self.TotalNum#它其实就是要显示符合用户输入的文档的字符串的尾截取位置
			else:#否则
				nLast=self.PosIdx[i]+len(Query)+WindowSize
			Ret=self.FTXDat[nFirst:nLast]#就是从文档中截取用户输入的关键词左边20个字符和右边20个字符来作为输出
			Ret=re.sub("\s","##",Ret)#替换内容
			FTSRet.append(Ret)#然后把每篇文档的截取部分存入到FTSRet当中
			if RetNum < len(FTSRet):#每次最多返回100个符合用户输入的文档
				break
		
	def Search(self,psInp,FTSRet,WindowSize,RetNum):
		GB=psInp[0].encode("gbk")#把查询关键字序列的第一个字编码成gbk
		if len(GB) == 1:#看下是不是字符
			ID=struct.unpack("B",GB)
		else:	#还是汉字
			ID=struct.unpack("H",GB)
		#然后unpack出来GBK字节流对应的ID
		self.SearchFTR(self.HZIdx[ID[0]-1],self.HZIdx[ID[0]],psInp,FTSRet,WindowSize,RetNum)#进行查找，通过倒排索引表找到该字在倒排文件表中的的聚集范围

def IdxMain():
	ObjIdx=Idx()#实例化一个Idx的对象
	FileList=["train.001"]
	DatFile="FTR.dat"#正排表
	HZIdxFile="Unit.dat"#倒排索引
	PosIdxFile="Offset.dat"#倒排文件
	ObjIdx.CreateIdx(FileList,DatFile,HZIdxFile,PosIdxFile)#把正排表，倒排索引和倒排文件分别得出并存储起来
	
def FTSMain():
	ObjFTR=FTR()#实例化一个FTR的对象
	DatFile="FTR.dat"#指定正排表的文件名
	HZIdxFile="Unit.dat"#指定倒排索引表的文件名
	psIdx="Offset.dat"#指定倒排文件表的文件名
	ObjFTR.FTRInit(HZIdxFile,DatFile,psIdx)#然后用已经存储好的各个表的信息来赋值到对应的数据结构当中
	FTSRet=[]#用来存储每次查找出来的信息
	WindowSize=20#输出的结果是关键字前后的20个字符
	RetNum=100#一次最多返回100个查询结果
	while 1:
		Query=input("Pls:")#输入你要查询的关键字
		if Query == 'q':
			break
		FTSRet.clear()#每一次都要把存储查询结果的List清除一下
		ObjFTR.Search(Query,FTSRet,WindowSize,RetNum)#进行查找
		for i in range(len(FTSRet)):#把结果一一打印出来
			print(FTSRet[i])
#IdxMain()
FTSMain()

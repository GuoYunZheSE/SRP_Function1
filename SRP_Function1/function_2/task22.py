
import numpy as np 
import re
import random
import pandas as pd 
import time
def get_all_roi(fr,way):
	listRoi=[]
	newGraph=False
	for line in fr.readlines():
		if line.startswith('-------'):
			feature=[]
			listRoiSmall=[]
			newGraph=True
		if newGraph:
			if line.startswith('lbl'):
				group1=line.split(' ')
				#feature={}
				feature=dict([word.strip('\n').split('=') for word in group1])
				#print(feature)
			if line.startswith('pos '):
				line=line[6:-4]
				group2=line.split(';')
				position=[roiP.strip().split(' ') for roiP in group2]
			if line.startswith('occl'):
				line=line[6:-3]
				group3=line.split(' ')
				ID_file=way.split('.')
				ID=ID_file[0].split('/')
				listRoiSmall=[[feature['lbl'],position[index],roio,ID[0]+'_'+ID[1]+'_'+str(int(feature['str'])+index)] for index,roio in enumerate(group3)]
				listRoi.extend(listRoiSmall)
		if line.startswith('\n'):
			newGraph=False
	return listRoi
def get_one_roi(fr,zhen_shu,way):
	listRoi=[]
	newGraph=False
	for line in fr.readlines():
		if line.startswith('-------'):
			feature=[]
			listRoiSmall=[]
			newGraph=True
		if newGraph:
			if line.startswith('lbl'):
				group1=line.split(' ')
				#feature={}
				feature=dict([word.strip('\n').split('=') for word in group1])
				if int(zhen_shu)>=int(feature['str']) and int(zhen_shu)<=int(feature['end']):
					continue
				else:
					newGraph=False
				#print(feature)
			if line.startswith('pos '):
				line=line[6:-4]
				group2=line.split(';')
				position=[roiP.strip().split(' ') for roiP in group2]
			if line.startswith('occl'):
				line=line[6:-3]
				group3=line.split(' ')
				ID_file=way.split('.')
				ID=ID_file[0].split('/')
				#listRoiSmall=[[feature['lbl'],position[index],roio,ID[0]+'_'+ID[1]+'_'+str(int(feature['str'])+index)] for index,roio in enumerate(group3)]
				listRoiSmall=[feature['lbl'],position[zhen_shu-int(feature['str'])],group3[zhen_shu-int(feature['str'])],ID[0]+'_'+ID[1]+'_'+str(zhen_shu)]
				listRoi.append(listRoiSmall)
		if line.startswith('\n'):
			newGraph=False
	return listRoi

def get_roi():
	ID=input("请输入你想查找的范围：")
	ID=ID.split('_')
	df=[]
	if len(ID)==1:
		print("这个数据集的全部roi信息如下：")
		tick1=time.time()
		num=0
		while num<100:
			way=ID[0]+'/V00'+str(num)+'.txt'
			num=num+1
			fr=open(way)
			#lis=['label','position','hide','ID']
			#name=input("Please input ID:")
			listRoi=get_all_roi(fr,way)
			#df_roi=pd.DataFrame(listRoi,columns=lis)
			if num==1:
				df=listRoi
			else:
				df.extend(listRoi)
				#df.append(df_roi)
			#print(df_roi)
		tick2=time.time()
		print(tick2-tick1)
		#print(df)
	if len(ID)==2:
		print("这个视频集得全部roi信息如下：")
		way=ID[0]+'/'+ID[1]+'.txt'
		fr=open(way)
		lis=['label','position','hide','ID']
		listRoi=get_all_roi(fr,way)
		df_roi=pd.DataFrame(listRoi,columns=lis)
		print(df_roi)
	if len(ID)==3:
		print("这一帧的全部roi的信息如下：")
		way=ID[0]+'/'+ID[1]+'.txt'
		fr=open(way)
		zhen_shu=int(ID[2])
		lis=get_one_roi(fr,zhen_shu,way)
		print(lis)
if __name__ == '__main__':
	get_roi()		

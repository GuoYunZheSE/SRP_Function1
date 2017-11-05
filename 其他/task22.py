
import numpy as np 
import re
import random
import pandas as pd 
import time
def get_roi(fr):
	listRoi=[]
	#listRoi=np.array([[]])
	newGraph=False
	for line in fr.readlines():

		if line.startswith('-------'):
			feature=[]
			listRoiSmall=[]
			newGraph=True
		# if line.startswith('\n'):
		# 	listRoi.append(listRoiSmall)
		# 	#listRoi.concatenate(listRoiSmall)
		# 	newGraph=False
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
				#listRoi.extend(listRoiSmall)
				#print(listRoiSmall)
				#print(position)
			if line.startswith('occl'):
				line=line[6:-3]
				group3=line.split(' ')
				listRoiSmall=[[feature['lbl'],position[index],roio] for index,roio in enumerate(group3)]
				listRoi.extend(listRoiSmall)
		if line.startswith('\n'):
			#print(np.array(listRoiSmall))
			#listRoi.append(listRoiSmall)
			#listRoi.concatenate(listRoiSmall)
			newGraph=False
	return listRoi


if __name__ == '__main__':
	num=0
	tick1=time.time()
	while num<100:
		way='Data-srp/V00'+str(num)+'.txt'
		num=num+1
		#name='v000_'+str(random.randint(610,2224))
		fr=open(way) 
		lis=['label','position','hide']
			#name=input("Please input ID:")
		listRoi=get_roi(fr)
        #print(listRoi)
        #print(pd.DataFrame(listRoi,columns=lis))
	tick2=time.time()
	print("总耗时：",tick2-tick1)
		#print("这一帧图片的全部物体的位置：",name,np.array(poition))
		#print("这一帧图片的物体遮挡信息：", np.array(hide))
		# a=np.array(content)
		# print(a)

from numpy import *
import re
import os
import sys
import numpy as np
import time
import glob

def get_roi_by_id_frame(id_set,id_video,id_frame):
	for parent,dirnames,files in os.walk('%s/%s_tmp' % (id_set,id_video)):
		num = len(files)
	mat_pos = mat(ones((num,4))*-1).astype(int).astype(str)
	mat_lbl = mat(ones((num,1))*-1).astype(int).astype(str)
	mat_occl = mat(ones((num,1))*-1).astype(int).astype(str)

	for filename in files:
		list_fn = re.split('_|,|\.',filename)
		if list_fn[0]== id_video:
			ind = int(list_fn[1]) 
			start = int(list_fn[2])
			end = int(list_fn[3])
			if id_frame >= start and id_frame <= end:
				with open(('%s/%s_tmp/' + filename )% (id_set,id_video),'r') as f3:
					lines = f3.readlines()
				list_line = re.split(' |=|\'',lines[0])
				lbl = list_line[2]
				pos = re.split('\[|\]',lines[1])[1].split('; ')[id_frame-start]
				x = pos.split(' ')[0]
				y = pos.split(' ')[1]
				w = pos.split(' ')[2]
				h = pos.split(' ')[3]
				occl = re.split('\[|\]',lines[3])[1].split(' ')[id_frame-start]
				ind -= 1
				mat_lbl[ind] = np.mat([lbl])
				mat_pos[ind] = np.mat([x,y,w,h])
				mat_occl[ind] = np.mat([occl])
	extract_roi_from_roilist(mat_pos,mat_lbl,mat_occl)

def get_roi_by_id_video(id_set,id_video):
	with open('%s/%s.txt' % (id_set,id_video),'r') as f:
		lines = f.readlines()
	frame = int(re.split(' |=',lines[1])[1])
	num = int(re.split(' |=',lines[1])[3])

	global min_start, max_end,batch_size
	min_start = frame
	max_end = 1
	
	batch_size = int(140000/num)
	batch_num = int(frame/batch_size + 1)

	global mat_lbl,mat_pos,mat_occl
	if batch_num > 1:
		for k in range(0,batch_num-1):
			mat_pos = mat(ones((num*batch_size,4))*-1).astype(int).astype(str)
			mat_lbl = mat(ones((num*batch_size,1))*-1).astype(int).astype(str)
			mat_occl = mat(ones((num*batch_size,1))*-1).astype(int).astype(str)
			read_roi(k*batch_size+1,(k+1)*batch_size+1,lines,num)
			extract_roi_from_roilist(mat_pos,mat_lbl,mat_occl)

	mat_pos = mat(ones((frame%batch_size*num,4))*-1).astype(int).astype(str)
	mat_lbl = mat(ones((frame%batch_size*num,1))*-1).astype(int).astype(str)
	mat_occl = mat(ones((frame%batch_size*num,1))*-1).astype(int).astype(str)
	read_roi((batch_num-1)*batch_size+1,frame+1,lines,num)
	extract_roi_from_roilist(mat_pos,mat_lbl,mat_occl)

def read_roi(begin,final,lines,num):
	global min_start, max_end, batch_size
	for id_frame in range(begin,final):
		head = 5
		if id_frame > 1 and ( id_frame <= min_start or id_frame >= max_end):
			continue;
		for i in range(0,num):
			list = re.split(' |=',lines[head])
			start = int(list[3])
			end = int(list[5])
			if id_frame == 1:
				if start < min_start:
					min_start = start
				if end > max_end:
					max_end = end
			if id_frame >= start and id_frame <= end:
				lbl = re.split(' |=|\'',lines[head])[2]
				pos = re.split('\[|\]',lines[head+1])[1].split('; ')[id_frame-start]
				x = pos.split(' ')[0]
				y = pos.split(' ')[1]
				w = pos.split(' ')[2]
				h = pos.split(' ')[3]
				occl = re.split('\[|\]',lines[head+3])[1].split(' ')[id_frame-start]
				global mat_lbl,mat_pos,mat_occl
				mat_lbl[(id_frame%batch_size-1)*num+i] = np.mat([lbl])
				mat_pos[(id_frame%batch_size-1)*num+i] = np.mat([x,y,w,h])
				mat_occl[(id_frame%batch_size-1)*num+i] = np.mat([occl])
			head += 7

def extract_roi_from_roilist(mat_pos,mat_lbl,mat_occl):
	global result
	for i in range(shape(mat_lbl)[0]):
		if callable_fun(mat_lbl[i],mat_pos[i],mat_occl[i]):
			roi = np.hstack((mat_lbl[i],mat_pos[i],mat_occl[i]))
			roi = array(res)[0]
			result.append(roi)

def callable_fun(roi_a,roi_b,roi_c):
	return False

def generate_tmp(id_set,id_video):
	os.mkdir('%s/%s_tmp' % (id_set, id_video))
	with open('%s/%s.txt' % (id_set, id_video),'r') as f:
		lines = f.readlines()
	num = int(re.split(' |=',lines[1])[3])
	head = 5
	for i in range(0,num):
		list = re.split(' |=',lines[head])
		start = list[3]
		end = list[5]
		with open('%s/%s_tmp/%s_%d_%s,%s.txt' % (id_set,id_video,id_video,i+1,start,end),'w') as f2:
			for i in lines[head : head+5]:
				f2.write(i)
		head += 7



def find():
	while 1:
		id_input = input("Please enter an set ID/video ID/image ID:")
		global result
		result = []
		if len(id_input.split('_')) == 1:
			start_time = time.clock()
			id_set = id_input.split('_')[0]
			for filename in glob.glob('%s/*.txt' % id_set):
				id_video = filename.split('.')[0].split('\\')[1]
				get_roi_by_id_video(id_set,id_video)
			
			end_time = time.clock()
			print(end_time-start_time)
		elif len(id_input.split('_')) == 2:
			start_time = time.clock()
			
			id_set = id_input.split('_')[0]
			id_video = id_input.split('_')[1]
			get_roi_by_id_video(id_set,id_video)
			
			end_time = time.clock()
			print(end_time-start_time)
		elif len(id_input.split('_')) == 3:
			start_time = time.clock()
			
			id_set = id_input.split('_')[0]
			id_video = id_input.split('_')[1]
			id_frame = int(id_input.split('_')[2])
			if not os.path.exists('%s/%s_tmp' % (id_set, id_video)):
				generate_tmp(id_set,id_video)
			get_roi_by_id_frame(id_set,id_video,id_frame)
			
			end_time = time.clock()
			print(end_time-start_time)
		else:
			print("输入值无效")
			continue

find()



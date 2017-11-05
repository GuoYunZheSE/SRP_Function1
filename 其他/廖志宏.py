import os
import time
import numpy as np
'''
this file should be placed in the root directory of dataset
'''
'''
deal_with_txt return four list:LABELn_1,ROIn_4,HIDEn_1 of one image
txt_file->txt_path
image_id->frame
'''
def pre_deal_txt(path):
    with open(path, 'r') as f:
        txt_content = f.read()
    txt_content = txt_content.split('-----------------------------------')
    head = txt_content.pop(0)
    frame = head.split('nFrame=')[1].split(' n=')[0]
    return frame

def deal_with_txt(path,image_id):
    LABELn_1 = []
    ROIn_4 = []
    HIDEn_1 = []
    flag1 = '-----------------------------------'
    flag2 = 'lbl='
    flag3 = 'pos ='
    flag4 = '; '
    cur_frame = int(image_id)

    with open(path, 'r') as f:
        txt_content = f.read()

    txt_content = txt_content.split(flag1)
    '''
    txt head process
    '''
    txt_head = txt_content.pop(0)
    vbb_version = txt_head.split('vbb version=')[1].split('nFrame=')[0]
    
    max_frame = txt_head.split('nFrame=')[1].split(' n=')[0]
    
    if cur_frame > int(max_frame) :
        print 'error by image ID input.'
        return
        '''
        unknow content process
        '''
    n = txt_head.split(' n=')[1].split('log=')[0]
    
    unknow_content = txt_head.split('log=')[1]
    '''
    txt label content process
    '''
    LABELn_1 = ['' for n in range(len(txt_content))]
    ROIn_4 = [[-1,-1,-1,-1] for n in range(len(txt_content))]
    HIDEn_1 = [0 for n in range(len(txt_content))]
    i = len(txt_content)-1
    while len(txt_content) > 0 :
        cur_txt = txt_content.pop(0)
        label_name = cur_txt.split('lbl=\'')[1].split('\' str=')[0]
        start_frame = int(cur_txt.split('str=')[1].split(' end=')[0])
        end_frame = int(cur_txt.split('end=')[1].split(' hide=')[0])
        hide = cur_txt.split('hide=')[1].split('pos =')[0]
        LABELn_1[i-len(txt_content)] = label_name
        HIDEn_1[i-len(txt_content)] = int(hide)
        if cur_frame < start_frame or cur_frame > end_frame :
            '''ROIn_4[i-len(txt_content)] = [-1,-1,-1,-1]'''
            continue
        roi_content = cur_txt.split('pos =[')[1].split(' ]posv=')[0]
        roi_content = roi_content.split('; ')
        d = len(roi_content)-1
        while len(roi_content)>0 :
            cur_roi = roi_content.pop(0)
            if cur_frame != start_frame + (d-len(roi_content)):
                continue
            cur_roi1 = float(cur_roi.split(' ')[0])
            cur_roi2 = float(cur_roi.split(' ')[1])
            cur_roi3 = float(cur_roi.split(' ')[2])
            cur_roi4 = float(cur_roi.split(' ')[3])
            ROIn_4[i-len(txt_content)] = [cur_roi1,cur_roi2,cur_roi3,cur_roi4] 

    '''LABELn_1 = np.array(LABELn_1)
    ROIn_4 = np.array(ROIn_4)
    HIDEn_1 = np.array(HIDEn_1)
    '''
    return LABELn_1,ROIn_4,HIDEn_1

'''
external_query_fn is required to deal with the value [roi,label,hide]
'''
dataset_flag = 'set'
video_flag = 'V'
image_flag = ''

def external_query_fn(input1,input2,input3):
    return 1

def query_image_ROI(external_query_fn,path,image_id):
    ROI_list = []
    LABELn_1,ROIn_4,HIDEn_1 =  deal_with_txt(path,image_id)
    while len(LABELn_1)>0:
        ROI = ROIn_4.pop(0)
        LABEL = LABELn_1.pop(0)
        HIDE = HIDEn_1.pop(0)
        if external_query_fn(ROI,LABEL,HIDE):
            ROI_list.append([ROI,LABEL,HIDE])    
    return ROI_list

def query_video_ROI(external_query_fn,path):
    ROI_list = []
    frame = int(pre_deal_txt(path))
    for image_id in range(0,frame):
        ROI_list.append(query_image_ROI(external_query_fn,path,image_id))
    return ROI_list

def query_dataset_ROI(external_query_fn,path):
    ROI_list = []
    '''
    read all file name in the path
    then call query_video_ROI(external_query_fn,path)
    ''' 
    for files in os.walk(path):
         for i in range(len(files[2])):
             path1 = os.path.join(path,files[2][i])
             print path1
             ROI_list.append(query_video_ROI(external_query_fn,path1))
    return ROI_list
    
def query_all_ROI(external_query_fn,path):
    ROI_list = []
    for dirs in os.walk(path):
         for i in range(len(dirs[1])):
             path1 = os.path.join(path,dirs[1][i])
             print path1
             '''ROI_list.append(query_dataset_ROI(external_query_fn,path1))
             '''
    return ROI_list


def query_ROI_fn(external_query_fn,query_range):
    print 'start time:'
    print time.strftime('%H-%M-%S',time.localtime(time.time()))
    '''
    function input:
    '''
    ROI_list = []

    path = os.path.abspath('.')  
    '''
    query_range include:
    1.dataset query
    2.video query
    3.image query
    format: [dataset index , video index , image index]
    index = '' mean query all element under this range
    '''
    DATASET_RANGE = 0
    VIDEO_RANGE = 1
    IMAGE_RANGE = 2
    if query_range[DATASET_RANGE] != '':
        if dataset_flag not in query_range[DATASET_RANGE]:
            print 'unexpected dataset index'
            return
        path = os.path.join(path,query_range[DATASET_RANGE])

        if query_range[VIDEO_RANGE] != '':
            if video_flag not in query_range[VIDEO_RANGE]:
                print 'unexpected video index'
                return
            if '.txt' not in query_range[VIDEO_RANGE]:
                print 'video index need .txt suffix'
                return
            path = os.path.join(path, query_range[VIDEO_RANGE])
            if query_range[IMAGE_RANGE] != '':
               print query_image_ROI(external_query_fn,path,query_range[IMAGE_RANGE])
            else:
                '''query all image in one video '''
                query_video_ROI(external_query_fn,path)
        else:
            '''query all video in one dataset '''
            query_dataset_ROI(external_query_fn,path)
    else:
        query_all_ROI(external_query_fn,path)

    print 'end time:'
    print time.strftime('%H-%M-%S',time.localtime(time.time()))
    return ROI_list

query_ROI_fn(external_query_fn,['','',''])
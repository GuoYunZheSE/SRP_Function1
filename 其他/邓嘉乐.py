import os
import numpy as np
import glob

class LABELs:
    def __init__(self,label,rois,hide):
        self.LABEL=label
        self.ROIs=rois
        self.HIDE=hide
   
def get_roi_frame(file,image_id,dir = os.path.abspath('')):
    t1 = file.split('.')[0]
    t2 = image_id.split('_')[0]

    if cmp(t1,t2) != 0 :
        print 'error by txt name or image ID input.'
        return

    flag1 = '-----------------------------------'
    cur_frame = int(image_id.split('_')[1])

    path = os.path.join(dir,file)
    with open(path, 'r') as f:
        txt_content = f.read()
    #f.close()

    txt_content = txt_content.split(flag1)
    '''
    txt head process
    '''
    txt_head = txt_content.pop(0)
    vbb_version = txt_head.split('vbb version=')[1].split('nFrame=')[0]
    #print 'vbb_version = '+vbb_version
    max_frame = txt_head.split('nFrame=')[1].split(' n=')[0]
    #print 'nFrame = '+max_frame
    if cur_frame > int(max_frame) :
        print 'error by image ID input.'
        return
        '''
        unknow content process
        '''
    n = txt_head.split(' n=')[1].split('log=')[0]
    #print 'n = '+n
    unknow_content = txt_head.split('log=')[1]
    '''
    txt label content process
    '''

    #initial
    lbs=[]

    i = len(txt_content)-1
    while len(txt_content) > 0 :
        cur_txt = txt_content.pop(0)
        label_name = cur_txt.split('lbl=\'')[1].split('\' str=')[0]
        start_frame = int(cur_txt.split('str=')[1].split(' end=')[0])
        end_frame = int(cur_txt.split('end=')[1].split(' hide=')[0])
        if start_frame>end_frame:
            continue
        hide = int(cur_txt.split('hide=')[1].split('pos =')[0])

        if cur_frame < start_frame or cur_frame> end_frame :
            if cur_frame!=-1 :
                continue
            '''ROIn_4[i-len(txt_content)] = [-1,-1,-1,-1]'''
        
        roi_content = cur_txt.split('pos =[')[1].split(' ]\nposv=')[0]
        roi_content = roi_content.split('; ')
        d = len(roi_content)-1

        tROI=[] 
        while len(roi_content)>0 :
            cur_roi = roi_content.pop(0)
            frame = start_frame + (d-len(roi_content))
            if cur_frame != frame:
                if cur_frame!=-1 :
                    continue
            
            cur_roi=cur_roi.split(';')[0]
            cur_roi1 = float(cur_roi.split(' ')[0])
            cur_roi2 = float(cur_roi.split(' ')[1])
            cur_roi3 = float(cur_roi.split(' ')[2])
            cur_roi4 = float(cur_roi.split(' ')[3])
            tROI.append([frame,cur_roi1,cur_roi2,cur_roi3,cur_roi4] )

        lbs.append(LABELs(label_name,tROI,hide))
 

    lbs = np.array(lbs)

    '''
    for i in lbs :
        print i.LABEL
        print i.ROIs
        print i.HIDE
    '''

    return lbs


def get_roi_video(file,dir = os.path.abspath('')):
    t1 = file.split('.')[0]
    return get_roi_frame(file,t1+'_-1',dir)


def get_roi_ds(dir = os.path.abspath('')+'\\annotations\\',filetpye = '.txt'):
    ds=[]
    files=glob.glob(dir+'*\\*'+filetpye)
    for i in files:
    #    print os.path.split(i)[1],os.path.split(i)[0]
        ds.append(get_roi_video(os.path.split(i)[1],os.path.split(i)[0]))
    return ds

@profile
def find(range,callable_func):
    result=[]
    if range == '-1':
        roilist=[]
        ds=get_roi_ds()
        for i in ds:
            for j in i:
                roilist.append(j)
    else:
        if range.find('_')==-1:
            roilist=get_roi_video(range)
        else:
            roilist=get_roi_frame(range)

    for roi in roilist:
        if callable_func(roi):
            result.append(roi)


    '''
    for i in result :
        print i.LABEL
        print i.ROIs
        print i.HIDE
    '''

    return result


def callable_func(roi):
    if roi.LABEL == 'ride_person':
     return True
    return False;


#get_roi_frame('V002.txt','V002_-1')
#get_roi_video('V000.txt')
#get_roi_ds()

find('-1',callable_func)
#roilist=get_roi_video('V000.txt')
#print roilist


import time
import os
import pandas as pd
import glob
import re

def find_(range,callable_func):
    roilist = get_roi(range)
    return callable_func(roilist)

def callable_func(roilist):
    return False

def get_roi(range):
    tick1 = time.time()
    if len(range.split('_')) == 1:
        set_id = range.split('_')[0]
        get_roi_by_set(set_id)
        tick2 = time.time()
        print("Total: ", tick2 - tick1)
    elif len(range.split('_')) == 2:
        set_id = range.split('_')[0]
        video_id = range.split('_')[1]
        get_roi_by_video(set_id, video_id)
        tick2 = time.time()
        print("Total: ", tick2 - tick1)
    else:
        set_id = range.split('_')[0]
        video_id = range.split('_')[1]
        frame_id = int(range.split('_')[2])
        get_roi_by_frame(set_id, video_id, frame_id)
        tick2 = time.time()
        print("Total: ", tick2 - tick1)


def get_roi_by_set(set_id):
    for filename in glob.glob('%s/*.txt' % set_id):
        video_id = filename.split('.')[0].split('\\')[1]
        get_roi_by_video(set_id, video_id)

def get_roi_by_video(set_id, video_id):
    with open('%s/%s.txt' % (set_id, video_id), 'r') as f:
        flag = 0
        roilist = []
        for line in f.readlines():
            if line.startswith('-------'):
                flag = 1
            if flag:
                if line.startswith('lbl'):
                    lblset = line.split(' ')
                    feature = dict([word.strip('\n').split('=') for word in lblset])
                    # print(feature)
                if line.startswith('pos '):
                    line = line[6:-4]
                    roiset = line.split(';')
                    target = [[feature['lbl'], feature['hide'], roiP.strip().split(' ')] for roiP in roiset]
                    roilist.extend(target)
            if line.startswith('\n'):
                flag = 0
        features = ['label', 'hide', 'position']
        print (pd.DataFrame(roilist, columns=features))
        return roilist


def get_roi_by_frame(set_id, video_id,frame_id):
    cur_path = os.path.abspath('')
    def pre_deal_frame(set_id, video_id, frame_id):
        with open('%s/%s.txt' % (set_id, video_id), 'r') as pre_video:
            fnew = open('_new.txt', 'w+')
            for line in pre_video.readlines():
                data = line.strip()
                if len(data) != 0:
                    if data != '-----------------------------------':
                        fnew.write(data)
                        fnew.write('\n')
            pre_video.close()
            fnew.close()
            goal_path = cur_path + '\\' + set_id + '\\' + video_id.encode('gb2312')
            if os.path.isdir(goal_path):
                print("")
            else:
                os.mkdir(goal_path)
            file2 = open(goal_path + '\\' + video_id + "_1.txt", "w")
            content = ""
            fnew = open('_new.txt', 'r')
            text = fnew.readlines()
            for i in range(4, len(text)):
                if ((i - 3) % 5 != 0):
                    content += text[i - 1]
                else:
                    content += text[i - 1]
                    file2.write(''.join(content))
                    destination = goal_path + '\\' + video_id + "_" + str((i) / 5 + 1) + ".txt"
                    file2 = open(destination, "w")
                    content = ""
            content += text[i]
            file2.write(''.join(content))
            file2.close()
            fnew.close()

    pre_deal_frame(set_id, video_id, frame_id)
    text = open('%s/%s.txt' % (set_id, video_id)).read()
    num1 = re.findall("str=(\d+)", text)
    num2 = re.findall("end=(\d+)", text)
    num1 = [int(n) for n in num1]
    num2 = [int(n) for n in num2]
    nnroi = ''
    nnoccl = ' '
    nnlbl = ' '
    for i in range(0, len(num1)):
        if (frame_id >= num1[i] and frame_id <= num2[i]):
            t = open(cur_path + '\\' + set_id + '\\' + video_id +'\\' + video_id+ "_" + str(i + 1) + '.txt').readlines()
            lbl = re.compile("lbl='(.*)'").findall(t[0])
            lbl = ''.join(lbl)
            nnlbl += (lbl + ";")
            bias = frame_id - num1[i]
            roi = t[1]
            occl = t[3]
            occl = occl[6:]
            nroi = roi[6:]
            nroi = nroi.split(';')
            occl = occl.split(' ')
            nnroi += (nroi[bias] + ";")
            nnoccl += (occl[bias] + ";")
    print(" The imformation about the position of all the people in this frame is:\n" + nnroi)
    print(" The imformation about the occl of all the people in this frame is:\n" + nnoccl)
    print(" The imformation about the label of all the things in this frame is:\n" + nnlbl)

find_('set06',callable_func)
find_('set06_V000',callable_func)
find_('set06_V000_154',callable_func)
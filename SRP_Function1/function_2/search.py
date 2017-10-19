import  os
import numpy
import re
import time
import requests
import multiprocessing 
from Identify import Identify

def search_all(node_number,begin,end,allinstance):
    t=time.time()
    Temp=numpy.empty(shape=(0,4))
    for instance in allinstance[begin:end]:
        for i in range(2,len(instance)):
            Temp1=[instance[i].Lable,instance[i].Begin,instance[i].End,instance[i].Hide]
            Temp1=numpy.array(Temp1).transpose()
            if len(instance[i].ROI) != 1:
                Temp2=numpy.array(instance[i].ROI)
            else:
                Temp2=numpy.empty(shape=(0,4))
            Temp3=numpy.vstack((Temp1,Temp2))
            Temp=numpy.vstack((Temp,Temp3))
    print("Node%d Search All Complete"%(node_number),time.time()-t)
    '''
    Preloading...
Loading Complete time used: 3.3614439964294434
Search Frame set00 V000 751 Complete 0.0010027885437011719
[["'people'" '707' '766' '0']
 ['55.667476' '201.605382' '44.196755' '74.895553']
 ["'ride_person'" '707' '1714' '0']
 ['411.709416' '171.665254' '68.369048' '139.474576']]
Search Video set00 V000 Complete 0.04463553428649902
[["'ride_person'" '610' '682' '0']
 ['545.380383' '213.129787' '20.669856' '37.991489']
 ['540.381378' '208.22766' '20.445873' '42.238649']
 ...,
 ['24.847205' '164.180052' '38.127042' '116.25198']
 ['15.076292' '163.723255' '36.498334' '118.148998']
 ['5.349445' '163.375264' '34.801902' '119.94926']]
Search DataSet set00 Complete 0.8321986198425293
[["'ride_person'" '610' '682' '0']
 ['545.380383' '213.129787' '20.669856' '37.991489']
 ['540.381378' '208.22766' '20.445873' '42.238649']
 ...,
 ['683.701268' '165.201903' '20.538827' '76.718816']
 ['685.127575' '163.070825' '19.397781' '78.849894']
 ['686.553883' '160.939746' '18.256735' '80.980973']]
Search All Complete 482.2505006790161
[["'ride_person'" '610' '682' '0']
 ['545.380383' '213.129787' '20.669856' '37.991489']
 ['540.381378' '208.22766' '20.445873' '42.238649']
 ...,
 ['672.290808' '226.394292' '15.213946' '45.260042']
 ['679.422345' '226.242072' '15.023772' '45.767442']
 ['686.553883' '226.089852' '14.833597' '46.274841']]
    '''
    return Temp

def search_dataset(dataset_name,allinstance):
    t=time.time()
    Temp=numpy.empty(shape=(0,4))
    for instance in allinstance:
        if instance[1]==dataset_name:
            for i in range(2,len(instance)):
                Temp1=[instance[i].Lable,instance[i].Begin,instance[i].End,instance[i].Hide]
                Temp1=numpy.array(Temp1).transpose()
                if len(instance[i].ROI) != 1:
                    Temp2=numpy.array(instance[i].ROI)
                else:
                    Temp2=numpy.empty(shape=(0,4))
                Temp3=numpy.vstack((Temp1,Temp2))
                Temp=numpy.vstack((Temp,Temp3))
        else:
            continue
    print("Search DataSet %s Complete"%(dataset_name),time.time()-t)
    return Temp

def search_video(dataset_name,video_name,allinstance):
    t=time.time()
    Temp=numpy.empty(shape=(0,4))
    for instance in allinstance:
        if instance[1]==dataset_name:
            if instance[0]==video_name:
                for i in range(2,len(instance)):
                    Temp1=[instance[i].Lable,instance[i].Begin,instance[i].End,instance[i].Hide]
                    Temp1=numpy.array(Temp1).transpose()
                    if len(instance[i].ROI) != 1:
                        Temp2=numpy.array(instance[i].ROI)
                    else:
                        Temp2=numpy.empty(shape=(0,4))
                    Temp3=numpy.vstack((Temp1,Temp2))
                    Temp=numpy.vstack((Temp,Temp3))
            else:
                continue
        else:
            continue
    print("Search Video %s %s Complete"%(dataset_name,video_name),time.time()-t)
    return Temp

def search_frame(dataset_name,video_name,frame_id,allinstance):
    t=time.time()
    Temp=numpy.empty(shape=(0,4))
    for instance in allinstance:
        if instance[1]==dataset_name:
            if instance[0]==video_name:
                for i in range(2,len(instance)):
                    if int(instance[i].Begin)<=frame_id and int(instance[i].End)>=frame_id:
                        Temp1=[instance[i].Lable,instance[i].Begin,instance[i].End,instance[i].Hide]
                        Temp1=numpy.array(Temp1).transpose()
                        if len(instance[i].ROI) != 1:
                            Temp2=numpy.array(instance[i].ROI[frame_id-int(instance[i].Begin)])
                        else:
                            Temp2=numpy.empty(shape=(0,4))
                        Temp3=numpy.vstack((Temp1,Temp2))
                        Temp=numpy.vstack((Temp,Temp3))
                    else:
                        continue
            else:
                continue
        else:
            continue
    print("Search Frame %s %s %d Complete"%(dataset_name,video_name,frame_id),time.time()-t)
    return Temp

def search_all_multiprocess(allinstance,count):
    Nodes=[]
    Assign=count/20
    t=time.time()
    pool=multiprocessing.Pool(processes=4)
    for node in range(count):
        pool.apply_async(search_all,(node,node*Assign,(node+1)*Assign,allinstance))
    pool.close()
    pool.join()
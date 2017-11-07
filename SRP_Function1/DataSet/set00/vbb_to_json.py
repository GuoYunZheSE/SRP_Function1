import os
import glob
import json
import re



# parse files
img_id = 0
ann_id = 0
obj_id = 0
cat_list = ['background', 'person', 'people', 'person-fa', 'person?']


#Find the path of sets
for dir_name in sorted(glob.glob('G:\\SRP_Function1\\SRP_Function1\\DataSet\\set*')):
    #for each set we find the txt files there
    for ann_fn in sorted(glob.glob('{}/*.txt'.format(dir_name))):
        
        # open files
        vbb_file = open(ann_fn)
        #If ann_fn is V000.txt then ann_fn becomes V000
        ann_fn = ann_fn.strip('.txt')
        #jason_file becomes V000.json
        json_file = open('{}.json'.format(ann_fn), 'w')
        # json_data
        json_data = {'info':{}, 'images':[], 'annotations':[]}

        json_data['info'] = {
            'description': 'This is a json version label of the Caltech Pedestrian dataset, converted from vbb version.',
            'version': '1.0',
            'vbb_version': '1.4',
            'cat_list': ['background', 'person', 'people', 'person-fa', 'person?']
        }


        lines = vbb_file.readlines()

        for line_n in range(len(lines)):
            line = lines[line_n]
            line_n = line_n + 1
            vbb_data = dict(re.findall(r'([A-Za-z]*)=[\']*(\[.*\]|[^\[\]\s\']*)[\']*',line))

            if 'nFrame' in vbb_data:
                nFrame = int(vbb_data['nFrame'])


            if 'lbl' in vbb_data:
                category = vbb_data['lbl']
                
                if category not in cat_list:
                    cat_list.append(category)

                cat_id = cat_list.index(category)

                start = int(vbb_data['str']) - 1
                end = int(vbb_data['end']) - 1
                hide = int(vbb_data['hide'])
                
                
                line = lines[line_n]
                line_n = line_n + 1
                pos = re.findall(r'([0-9\.]+)',line)

                
                line = lines[line_n]
                line_n = line_n + 1
                posv = re.findall(r'([0-9\.]+)',line)

                line = lines[line_n]
                line_n = line_n + 1
                occl = re.findall(r'([0-9\.]+)',line)

                for i in range(start,end+1):
                    ann = {}
                    ann['ann_id'] = ann_id
                    ann_id = ann_id+1
                    ann['obj_id'] = obj_id
                    ann['img_id'] = img_id+i
                    ann['bbox'] = [float(pos[(i-start)*4]), float(pos[(i-start)*4+1]), float(pos[(i-start)*4+2]), float(pos[(i-start)*4+3])]
                    ann['bbox_v'] = [float(posv[(i-start)*4]), float(posv[(i-start)*4+1]), float(posv[(i-start)*4+2]), float(posv[(i-start)*4+3])]
                    ann['is_hard'] = int(occl[i-start])
                    ann['cat_id'] = cat_id
                    json_data['annotations'].append(ann)

                obj_id = obj_id+1

        
        for i in range(nFrame):
            json_data['images'].append({'id':img_id, 'file_name': '{}_{}_{}.jpg'.format(os.path.basename(dir_name),os.path.basename(ann_fn),i)})
            img_id = img_id + 1

        json.dump(json_data, json_file)

        json_file.close()
        vbb_file.close()




















































import os
import glob
import json
import re


# parse files
img_id = 0
ann_id = 0
obj_id = 0
cat_list = ['background', 'person', 'people', 'person-fa', 'person?']

cat_list = ['background',]


# json_data
json_data = {'info':{}, 'images':[], 'annotations':[]}

json_data['info'] = {
    'description': 'This is a json version label of the Caltech Pedestrian dataset, converted from vbb version.',
    'version': '1.0',
    'vbb_version': '1.4',
    'cat_list': ['background', 'person', 'people', 'person-fa', 'person?']
}


json_file = open('annotations_caltech_pedestrian_train.json', 'w')

dir_list = sorted(glob.glob('G:\\SRP_Function1\\SRP_Function1\\DataSet\\set*'))
for dir_num in range(6):
    dir_name = dir_list[dir_num]
    for ann_fn in sorted(glob.glob('{}/*.txt'.format(dir_name))):
        
        # open files
        vbb_file = open(ann_fn)

        ann_fn = ann_fn.strip('.txt')

        lines = vbb_file.readlines()

        for line_n in range(len(lines)):
            line = lines[line_n]
            line_n = line_n + 1
            vbb_data = dict(re.findall(r'([A-Za-z]*)=[\']*(\[.*\]|[^\[\]\s\']*)[\']*',line))

            if 'nFrame' in vbb_data:
                nFrame = int(vbb_data['nFrame'])


            if 'lbl' in vbb_data:
                category = vbb_data['lbl']
                
                if category not in cat_list:
                    cat_list.append(category)

                cat_id = cat_list.index(category)

                start = int(vbb_data['str']) - 1
                end = int(vbb_data['end']) - 1
                hide = int(vbb_data['hide'])
                
                
                line = lines[line_n]
                line_n = line_n + 1
                pos = re.findall(r'([0-9\.]+)',line)

                
                line = lines[line_n]
                line_n = line_n + 1
                posv = re.findall(r'([0-9\.]+)',line)

                line = lines[line_n]
                line_n = line_n + 1
                occl = re.findall(r'([0-9\.]+)',line)

                for i in range(start,end+1):
                    ann = {}
                    ann['ann_id'] = ann_id
                    ann_id = ann_id+1
                    ann['obj_id'] = obj_id
                    ann['img_id'] = img_id+i
                    ann['bbox'] = [float(pos[(i-start)*4]), float(pos[(i-start)*4+1]), float(pos[(i-start)*4+2]), float(pos[(i-start)*4+3])]
                    ann['bbox_v'] = [float(posv[(i-start)*4]), float(posv[(i-start)*4+1]), float(posv[(i-start)*4+2]), float(posv[(i-start)*4+3])]
                    ann['is_hard'] = int(occl[i-start])
                    ann['cat_id'] = cat_id
                    json_data['annotations'].append(ann)

                obj_id = obj_id+1

        for i in range(nFrame):
            json_data['images'].append({'id':img_id, 'file_name': '{}_{}_{}.jpg'.format(os.path.basename(dir_name),os.path.basename(ann_fn),i)})
            img_id = img_id + 1

        
        vbb_file.close()  


json.dump(json_data, json_file)

json_file.close()
        






# json_data
json_data = {'info':{}, 'images':[], 'annotations':[]}

json_data['info'] = {
    'description': 'This is a json version label of the Caltech Pedestrian dataset, converted from vbb version.',
    'version': '1.0',
    'vbb_version': '1.4',
    'cat_list': ['background', 'person', 'people', 'person-fa', 'person?']
}


json_file = open('annotations_caltech_pedestrian_test.json', 'w')

dir_list = sorted(glob.glob('G:\\SRP_Function1\\SRP_Function1\\DataSet\\set*'))
for dir_num in range(6,11):
    dir_name = dir_list[dir_num]
    for ann_fn in sorted(glob.glob('{}/*.txt'.format(dir_name))):
        
        # open files
        vbb_file = open(ann_fn)

        ann_fn = ann_fn.strip('.txt')

        lines = vbb_file.readlines()

        for line_n in range(len(lines)):
            line = lines[line_n]
            line_n = line_n + 1
            vbb_data = dict(re.findall(r'([A-Za-z]*)=[\']*(\[.*\]|[^\[\]\s\']*)[\']*',line))

            if 'nFrame' in vbb_data:
                nFrame = int(vbb_data['nFrame'])


            if 'lbl' in vbb_data:
                category = vbb_data['lbl']
                
                if category not in cat_list:
                    cat_list.append(category)

                cat_id = cat_list.index(category)

                start = int(vbb_data['str']) - 1
                end = int(vbb_data['end']) - 1
                hide = int(vbb_data['hide'])
                
                
                line = lines[line_n]
                line_n = line_n + 1
                pos = re.findall(r'([0-9\.]+)',line)

                
                line = lines[line_n]
                line_n = line_n + 1
                posv = re.findall(r'([0-9\.]+)',line)

                line = lines[line_n]
                line_n = line_n + 1
                occl = re.findall(r'([0-9\.]+)',line)

                for i in range(start,end+1):
                    ann = {}
                    ann['ann_id'] = ann_id
                    ann_id = ann_id+1
                    ann['obj_id'] = obj_id
                    ann['img_id'] = img_id+i
                    ann['bbox'] = [float(pos[(i-start)*4]), float(pos[(i-start)*4+1]), float(pos[(i-start)*4+2]), float(pos[(i-start)*4+3])]
                    ann['bbox_v'] = [float(posv[(i-start)*4]), float(posv[(i-start)*4+1]), float(posv[(i-start)*4+2]), float(posv[(i-start)*4+3])]
                    ann['is_hard'] = int(occl[i-start])
                    ann['cat_id'] = cat_id
                    json_data['annotations'].append(ann)

                obj_id = obj_id+1
                
        for i in range(nFrame):
            json_data['images'].append({'id':img_id, 'file_name': '{}_{}_{}.jpg'.format(os.path.basename(dir_name),os.path.basename(ann_fn),i)})
            img_id = img_id + 1

        
        vbb_file.close()  


json.dump(json_data, json_file)

json_file.close()
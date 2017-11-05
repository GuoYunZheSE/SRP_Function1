
def search(file,name):
    positionSum=[]
    hideSum=[]
    video,Frame=name.split('_')
    for line in file.readlines():
        if line.startswith ('lbl'):
            group2=line.split(' ')
            feature={}
            for lis in group2:
                keyValue=lis.strip('\n').split('=')
                feature[keyValue[0]]=keyValue[1]
            if int(Frame)>=int(feature['str']) and int (Frame)<=int(feature['end']):
                hideSum.append(list(feature['hide']))
                insideHudje=True
            else:
                hideSum.append(list(feature['hide']))
                positionSum.append([-1,-1,-1,-1])
        if line.startswith('pos '):
            line=line[6:-4]
            group1=line.split(';')
            position=[]
            for lis in group1:
                groupList=[float(num) for num in lis.strip().split(' ')]
                position.append(groupList)
            if int(Frame)>=int(feature['str']) and int (Frame)<=int(feature['end']):
                positionSum.append(position[int(Frame)-int(feature['str'])])
    return positionSum,hideSum


def func(range, defined_func):
    f=[]
    f=open('annotations\set00\V002.txt','r')
    positionSum=search(f,range)
    result=[]
    for lis in positionSum:
        if defined_func(lis):
            result.append(lis)
    return result

def _func(lis):
    if lis=='0':
        return 'True'
    else: return 'False'



print(func('as_8888',_func))
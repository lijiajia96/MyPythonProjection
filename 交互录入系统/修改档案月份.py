import os
path=r"Z:\Service Operations\9-Technical Support-manage\SO-Technical Training\13 技术培训档案\2020\培训档案\2020.5月培训档案\城市公司"
file_name=os.listdir(path)

for name in file_name:

    oldname=os.path.join(path,name)
    new=name.replace("Jan","May")
    print(new)
    newname=os.path.join(path,new)
    print(newname)
    os.rename(oldname,newname)




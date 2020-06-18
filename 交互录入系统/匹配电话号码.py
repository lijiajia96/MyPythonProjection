import pandas as pd
path = r'Z:\Service Operations\9-Technical Support-manage\SO-Technical Training\13 技术培训档案\交接参考附件（技术）\4-培训签到表\2019\2019.12\12月签到总表.xlsx'
data = pd.DataFrame(pd.read_excel(path))#读取数据,设置None可以生成一个字典，字典中的key值即为sheet名字，此时不用使用DataFram，会报错
print(data.index)#获取行的索引名称
print(data.columns)#获取列的索引名称
print(data['学员姓名'])#获取列名为姓名这一列的内容
print(data.loc[0])#获取行名为0这一行的内容

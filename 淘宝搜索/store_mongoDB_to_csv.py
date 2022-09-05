import pymongo
import csv

def main(colname,dbname):
    client=pymongo.MongoClient('localhost')
    db=client[dbname]
    if colname in db.collection_names():
        col=db[colname]
        dic=[]
        for i in col.find({},{'_id':0}):
            dic.append(i)
        header=list(dic[0].keys())
        with open('{}.csv'.format(colname),'w',encoding='utf-8') as f:
            writer=csv.DictWriter(f,header)
            writer.writeheader()
            writer.writerows(dic)
    else:
        print('"{}"这个集合不在数据库"{}"中'.format(colname,dbname))

if __name__=="__main__":
    main('手机','taobao')

import pymongo
import json

def main(colname,dbname):
    client=pymongo.MongoClient('localhost')
    db=client[dbname]
    if colname in db.collection_names():
        col=db[colname]
        dic=[]
        for i in col.find({},{'_id':0}):
            dic.append(i)
        with open('{}.json'.format(colname),'w',encoding='utf-8') as f:
            json.dump(dic,f,ensure_ascii=False,indent=4)
    else:
        print('"{}"这个集合不在数据库"{}"中'.format(colname,dbname))

if __name__=="__main__":
    main('充气娃娃','taobao')

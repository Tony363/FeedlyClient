import pandas as pd
import opml as ol
import listparser as lp
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

def OPML():
    outline = ol.parse(
        './feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-28.opml')
    print("title: ", outline.title)
    outline_methods = [method_name for method_name in dir(outline)
                       if callable(getattr(outline, method_name))]
    print(outline_methods)
    for i in range(len(outline)):
        print(outline[0].text)
    print()

def Lparser(rssfile='./feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-28.opml'):
    d = lp.parse(rssfile)
    d_methods = [method_name for method_name in dir(d)
                 if callable(getattr(d, method_name))]
    print(d_methods,'\n')
    feeds = d.feeds
    dic = {feed:[feeds[0][feed]] for feed in feeds[0]}
    keys = dic.keys()
    for line in range(1,len(d.feeds)):
        """
        print(d.feeds[line])
        print(feeds[line].title)
        print(feeds[line].categories)
        print(feeds[line].url)
        print(feeds[line].tags)
        """
        for key in keys:
            dic[key].append(feeds[line][key])
    return dic

def mergeDict(dic1,dic2):
    keys = dic1.keys()
    for key,val in dic2.items():
        if key not in keys:
            dic1[key] = val
        else:
            dic1[key] += val
    return dic1

def RSSmultiple(*args,source='url'):
    fdic = {}
    for file in args:
        dic = Lparser(file)
        fdic = mergeDict(fdic, dic)
    df = pd.DataFrame(fdic)
    df.sort_values(by=source,inplace=True)
    df.set_index(source,inplace=True)
    return df,fdic

def to_xml(dic):
    xml = dicttoxml(dic,attr_type=False,item_func=lambda x:x)
    xml_decode = xml.decode()
    xmlfile = open("FeedlyRSS.xml","w")
    xmlfile.write(xml_decode)
    xmlfile.close()
    return parseString(xml)


if __name__ == '__main__':
    print(pd.__version__)
    df,fdic = RSSmultiple(
        './feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-28.opml',
        './feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-29.opml',
        './feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-29(1).opml'
        )
    dom = to_xml(fdic)
    print(dom.toprettyxml())
    df.to_csv("feedlyRSS.csv")
    
    

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

def Lparser(rssfile='./feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-28.opml',to_csv=False):
    d = lp.parse(rssfile)
    d_methods = [method_name for method_name in dir(d)
                 if callable(getattr(d, method_name))]
    print(d_methods,'\n')
    feeds = d.feeds
    f = open('rssfeeds.txt','w')
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
    df = pd.DataFrame(dic)
    print(df)
    if to_csv: df.to_csv('feedlyRSS.csv')
    return df

def RSSmultiple(*args,source='url'):
    df = pd.DataFrame()
    for file in args:
        df = pd.concat([df,Lparser(file)],axis=0)
    df.sort_values(by=source,inplace=True)
    df.set_index(source,inplace=True)
    return df

def to_xml(df,orient='list'):
    xml = dicttoxml(df.to_dict(orient=orient),attr_type=False,item_func=lambda x:x)
    xml_decode = xml.decode()
    xmlfile = open("FeedlyRSS.xml","w")
    xmlfile.write(xml_decode)
    xmlfile.close()
    return parseString(xml)


if __name__ == '__main__':
    print(pd.__version__)
    df = RSSmultiple(
        './feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-28.opml',
        './feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-28.opml',
        './feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-28.opml'
        )
    dom = to_xml(df)
    print(dom.toprettyxml())
    df.to_csv("feedlyRSS.csv")
    pass
    

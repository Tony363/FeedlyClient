import os
import pandas as pd
import opml as ol
import listparser as lp
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from xml.etree import ElementTree

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


def unwrap(lst):
    if isinstance(lst,list):
        lst = unwrap(lst[0])
    return lst

def mergeDict(dic1,dic2):
    keys = dic1.keys()
    for key,val in dic2.items():
        if key not in keys:
            dic1[key] = val
        else:
            dic1[key] += val
    return dic1

def Lparser(rssfile='./feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-28.opml'):
    d = lp.parse(rssfile)
    d_methods = [method_name for method_name in dir(d)
                 if callable(getattr(d, method_name))]
    print(d_methods,'\n')
    feeds = d.feeds
    keys = feeds[0].keys()
    dic = {}
    for line in range(len(feeds)):
        for key in keys:
            if isinstance(feeds[line][key],list):
                feeds[line][key] = unwrap(feeds[line][key]) 
        dic[f"RssFeed {line}"] = feeds[line]        
    return dic

def RSSmultiple(*args):
    fdic = {}
    for file in args:
        dic = Lparser("./In/"+file)
        fdic = {**fdic,**dic}
    return fdic

def to_xml(dic):
    xml = dicttoxml(dic,attr_type=False,item_func=lambda x:x)
    xml_decode = xml.decode()
    xmlfile = open("./Out/FeedlyRSS.xml","w")
    xmlfile.write(xml_decode)
    xmlfile.close()
    return parseString(xml)

def to_csv(dic,source='categories'):
    df = pd.DataFrame(dic).transpose()
    df.sort_values(by=source,inplace=True)
    df.to_csv("Out/FeedlyRSS.csv")
    return df


def extract_rss_urls_from_opml(filename):
    urls = []
    with open(filename, 'rt') as f:
        tree = ElementTree.parse(f)
    for node in tree.findall('.//outline'):
        url = node.attrib.get('xmlUrl')
        if url:
            urls.append(url)
    return urls

if __name__ == '__main__':
    print(pd.__version__)
    print(*os.listdir('./In'))
    fdic = RSSmultiple(*os.listdir('./In'))
    # fdic = RSSmultiple(
    #     './In/feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-28.opml',
    #     './In/feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-29.opml',
    #     './In/feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-29(1).opml'
    #     )
    dom = to_xml(fdic)
    df = to_csv(fdic)
    print(dom.toprettyxml())
    urls = extract_rss_urls_from_opml('./In/feedly-e42affb2-52f5-4889-8901-992e3a3e35de-2021-06-28.opml')
    print(urls)

    

import requests,uvicorn,io
import pandas as pd
from fastapi import Depends,FastAPI
from fastapi.responses import StreamingResponse
from deta import Deta

app = FastAPI(title="api rate limiter")
project_key = "c0v7erzu_UMHnYtbdHmMAz4A1uzdbKhiZ7nvS2Ds5"

@app.get("/get_data/{query}")
async def store_data(query:str,deta = Deta(f"{project_key}")):
    db = deta.Base("simple.db")
    return db.get(str(query))

@app.get("/to_csv/")
async def to_CSV(
    deta=Deta(f"{project_key}"),
    content={'key':[],'應修系級':[],'開課系所':[]},
    stream=io.StringIO(),
    entries=0,
    ):
    db = deta.Base("simple.db")
    query = db.get(str(entries))
    if not query:
        return {"msg":"no items in db"}
    while query:
        query = db.get(str(entries))
        content['key'].append(query['key'])
        content['應修系級'].append(query['應修系級'])
        content['開課系所'].append(query['開課系所'])
        entries += 1
        query = db.get(str(entries))
    pd.DataFrame(content).to_csv(stream,index=False)
    response = StreamingResponse(iter([stream.getvalue()]),media_type="text/csv")
    response.headers['Content-Disposition'] = "attachment; filename=export.csv"
    return response


@app.get("/store_data/")
async def get_csv(
    deta = Deta(f"{project_key}"),
    url='https://sea.cc.ntpu.edu.tw/pls/dev_stud/course_query_all.queryByAllConditions?seq1=A&qCollege=%AAk%AB%DF%BE%C7%B0%7C&qYear=109&qTerm=2'
    ):
    db = deta.Base("simple.db")
    r = requests.get(url)
    df = pd.read_html(r.text)
    courses = df[0][['開課系所','應修系級']]
    for i in range(len(courses)):
        db.put({"開課系所":courses.iloc[i,0],"應修系級": courses.iloc[i,1],'key':str(i)})
    return {"status":"ok"}

def test():
    url='https://sea.cc.ntpu.edu.tw/pls/dev_stud/course_query_all.queryByAllConditions?seq1=A&qCollege=%AAk%AB%DF%BE%C7%B0%7C&qYear=109&qTerm=2'
    r = requests.get(url)
    df = pd.read_html(r.text)
    courses = df[0][['開課系所','應修系級']]
    # print(courses)
    for i in range(len(courses)):
        print(courses.iloc[i,0],courses.iloc[i,1])
        

if __name__ == "__main__":
    """
    leaking bucket algorithm - standart rate response
    token bucket algorithm - with burst
    """
    uvicorn.run("main:app", debug=True, reload=True)
    # test()


   
    
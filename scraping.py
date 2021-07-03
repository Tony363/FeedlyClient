import requests,ast,json
from client import FeedlyClient
from pathlib import Path
from feedly.api_client.session import FeedlySession

FEEDLY_REDIRECT_URI = "http://fabreadly.com/auth_callback"
FEEDLY_CLIENT_ID="e42affb2-52f5-4889-8901-992e3a3e35de"
FEEDLY_CLIENT_SECRET="secret"
FEEDLY_TOKEN = 'A9eehjuM3ZcADztI5JahBdjx0Pl8yZFO2lC1_-IwdC5im1U5j7n55ikt-BikLIRalu_KDrhdPjdA827XMlM5jEier6m0p98AgfPgepnm5sz9f7g0t_87ETZvZvoxGIJnWt2EXEpt4OBjdwsTli3bNszT0M1xiGZxKSDrVZ_iBxp69oQUaDqXmWqAGdQltVbUoFkPMQMc4Cx4BYkeWwO6huAc_o485Nu6LiuOwqZOzIPh18A:feedly'

if __name__ == '__main__':
    # sess = FeedlySession(FEEDLY_TOKEN)
    # print("session instantiated")
    # call = sess.do_api_request('/v3/feeds/feed%2Fhttp%3A%2F%2Fblog.feedly.com%2Ffeed%2F')
    # print("test call:\n",call)
    # user_categories = sess.user.get_categories('politics')
    # print("test user categories:\n",user_categories)
    url = 'https://cloud.feedly.com/v3/streams/contents?streamId=feed%2Fhttp%3A%2F%2Fwww.readwriteweb.com%2Frss.xml&count=20'
    headers = {'Authorization':'Bearer '+FEEDLY_TOKEN}
    r = requests.get(url=url,headers=headers)
    if r.status_code == 200:
        # print(type(r.content))
        # info_str = r.content.decode("UTF-8")
        # print(info_str)
        # data = ast.literal_eval(str(info_str))
        dic = json.loads(r.content)
        print(type(dic))
        print(dic.keys())
        print(dic['items'][0].keys())
        print(dic['items'][0]['content']['content'])
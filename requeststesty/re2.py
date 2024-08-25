import requests


url = 'https://movie.douban.com/j/chart/top_list'

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    'Accept-Language': 'en-US,en;q=0.9',  # 设置接受的语言
}

params = {
 'type' : '5',
 'interval_id' : '100:90' ,
 'action' : '',
 'start' : '0',
 'limit' : '10'
 }

response = requests.get(url=url, headers=headers, params=params)
xcd = response.json()


id = 1
for mv in xcd:
    mvname = mv['title']
    mvsc = mv['score']
    print(id , mvname, mvsc)
    id +=1

#
# for i in xcd:
#     print(i['title'])
#     print(i['release_date'])
#     print(i['rating'])
#     print(i['actors'])





import requests
import webbrowser
import time

url = 'http://music.vaiwan.com/music/list?'
query = input('请输入要下载的歌曲：')
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
}
params = (
    ('key', query),
    ('pageNo', '1'),
    ('pageSize', '20'),
)
response = requests.get(url=url, headers=headers, params=params)
list_data = response.json()

for i in range(0, 10):
    print(str(i + 1) + '.' + list_data['data']['list'][i]['name'] + '-------' + list_data['data']['list'][i]['artist'])

select = input("请输入序号来选择想要下载的歌曲：")
data = {
    'name': list_data['data']['list'][int(select) - 1]['name'],
    'artist': list_data['data']['list'][int(select) - 1]['artist']
}
response = requests.post('http://music.vaiwan.com/music/save', headers=headers, data=data)
down_url = response.json()
down_url = down_url['data']
if down_url == '':
    print("很抱歉，没有找到下载链接")
else:
    print(down_url + '\n2秒后会调用浏览器打开链接')
    time.sleep(2)
    webbrowser.open_new_tab(down_url)

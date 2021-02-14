import requests
import webbrowser
import time
import json

url = 'http://music.vaiwan.com/music/list?'
query = input('请输入要下载的歌曲：')
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
}

params = (
    ('limit', '20'),
    ('modelTypes', r'App\Artist,App\Album,App\Track,App\User,App\Playlist'),
    ('query', query),
)

cookies = {
    'cookies': '_ga=GA1.1.2141880371.1613289230; _ga_RWV44BMN28=GS1.1.1613289230.1.1.1613289254.0; theme=light; _ga_JTH5TBMPQD=GS1.1.1613289256.1.1.1613289342.0; XSRF-TOKEN=eyJpdiI6Im5SaE5JckFkU2xSeFo3NE12a1hOV3c9PSIsInZhbHVlIjoiRFJ5cHowYnBHVXBMNEI4czdyK0ZQMVNMTkhwdXpxQVhoV0lweXI1RDNwTS9LRFlnVXlSZE9CWlAranhUSmljK0UxVjlLUjkvcThZWjZ2djBKRTdHT0xWaWZKOHppRE1MWkpvT1VyNFlGa0F3R3haTUdmY1MyVHF3dXpQSi91MFkiLCJtYWMiOiJiY2M3Yzg0NzgyNWUxM2M2YmE1Y2UwNjYxNTRmZjQ3NjdhNWVjMGIzODI2MzhiMDQzYjdmNjUyMmNkNzQ4ZDg2In0=; myfreemp3_session=eyJpdiI6ImpHTWVlb1cxZ01jNlRBbEtoUiszSlE9PSIsInZhbHVlIjoiN1JxczczQzFhRE1GL2lyaTZUVFhpbGU3V1I5UjVaM3JwK0RPdW9kWXZqdnVGQWpudWM2blJka1VTdkNHYTNDQ3NGQk1QWTZuRldkNGhRMlE2OG1NMWxPN1hUeVMxcXE4NFFPczR6UnNiSHdBRzRhck5zOHJGclp0dTh0YWtnNTAiLCJtYWMiOiJmZTE4YmU5ODI4OTRhMzIwZGFjMzZlY2ZjMTZiNGJkNmZhYjdiNDFhMzE3OGFmYzNiZTY2OWNmNTcwNzQ4ODFkIn0='
}

response = requests.get('https://music.liumingye.cn/secure/search', headers=headers, params=params)

list_data = json.loads(response.text)
page = 1


def print_info(page_in):
    try:
        for i in range(10 * (page_in - 1), 10 * page_in):
            print(str(i + 1) + '.' + str(list_data['results']['tracks'][i]["name"]) + '-------' + str(
                list_data['results']['tracks'][i]['artists'][0]['name']))
    except IndexError:
        for i in range(10 * (page_in - 1), len(list_data['results']['tracks'])):
            print(str(i + 1) + '.' + str(list_data['results']['tracks'][i]["name"]) + '-------' + str(
                list_data['results']['tracks'][i]['artists'][0]['name']))
            print('后面没有了，不要再翻页啦！')

    global page

    select = input("请输入序号来选择想要下载的歌曲：（如果本页没有你想要的歌曲，输入*来翻页！）")

    if select == '*':
        page += 1
        print_info(page)
    else:
        down_url = list_data['results']['tracks'][int(select) - 1]['url']

        if '/link/' in down_url:
            down_url = 'https://music.liumingye.cn' + down_url

        print(down_url)
        if down_url == '':
            print("很抱歉，没有找到下载链接")
        else:
            print('2秒后会调用浏览器打开链接')
        time.sleep(2)
        webbrowser.open_new_tab(down_url)


print_info(1)

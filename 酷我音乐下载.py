import requests
import os
import time
import json

page = 1
query = input('请输入要下载的歌曲：')
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
}


def print_info(page_in):  # 打印搜索结果，并获取歌曲rid和名称
    params = (
        ('limit', '20'),
        ('offset', page_in),
        ('keyWord', query),
    )
    response = requests.get('http://yz.8848mv.com/api/v1/search?', headers=headers, params=params)
    list_data = json.loads(response.text)
    xuhao = (page_in - 1) * 19 + 1
    for i in range(0, 19):
        print(str(xuhao) + '.' + str(list_data['data']['data']['list'][i]["name"]) + '-------' + str(
            list_data['data']['data']['list'][i]['artist']))
        xuhao += 1
    select = input("请输入序号来选择想要下载的歌曲：（如果本页没有你想要的歌曲，输入*来翻页！）")
    global page
    if select == '*':
        page += 1
        print_info(page)
    else:
        music_id = list_data['data']['data']['list'][int(select) - 1]['rid']
        file_Name = str(list_data['data']['data']['list'][int(select) - 1]["name"]) + '-' + str(
            list_data['data']['data']['list'][int(select) - 1]['artist'])
        return music_id, file_Name


def get_print_url(rid, size_in):  # 根据rid，获取下载链接
    data = (
        ('br', 'flac'),
        ('rid', rid),
    )
    data2 = (
        ('br', '320k'),
        ('rid', rid),
    )

    if size_in == '1':
        response2 = requests.get('http://yz.8848mv.com/api/v1/getURl?', headers=headers, params=data)
    else:
        response2 = requests.get('http://yz.8848mv.com/api/v1/getURl?', headers=headers, params=data2)

    list_data2 = json.loads(response2.text)
    down_url = list_data2['data']['url']['url']
    print(down_url)
    if down_url == '':
        print("很抱歉，没有找到下载链接")
    else:
        print('2秒后会自动下载')

    time.sleep(2)
    return down_url


def down(file_Name, url_in):  # 访问下载链接，保存文件
    response2 = requests.get(url_in)
    if 'flac' in url_in:
        file_Name = file_Name + '.flac'
    elif 'mp3' in url_in:
        file_Name = file_Name + '.mp3'
    else:
        exit()

    if not os.path.exists('song'):
        os.mkdir('song')
    with open('./song/' + file_Name, 'wb') as ff:
        ff.write(response2.content)


if __name__ == '__main__':
    musicrid, name = print_info(page)
    size = input('选择需要下载的歌曲品质：    1.flac    2.320k\t')
    url = get_print_url(musicrid, size)
    down(name, url)

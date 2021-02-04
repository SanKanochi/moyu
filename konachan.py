# -*- coding: utf-8 -*-
# @Author  : xyz
# @Time    : 2021/2/4 10:02
# @Function: 利用API接口爬取Konachan的图片

"""
Konachan对API接口的说明
"""
# List
# The base URL is /post.xml.
#
# limit How many posts you want to retrieve. There is a hard limit of 100 posts per request.
# page The page number.
# tags The tags to search for. Any tag combination that works on the web site will work here. This includes all the meta-tags.
import os
import requests
import xmltodict
import multiprocessing

# konachan 提供的 API
API = r"https://konachan.com/post.xml"
# 图片保存路径
SAVE_PATH = r"C:\Users\KANOCHI\Pictures\konachan"
# 每次请求的图片数量
LIMIT = multiprocessing.cpu_count()
PAGE_LIMIT = 10


def process_post(para):
    post = para[0]
    tags = para[1]
    log_path = para[2]
    img_url = post['@file_url']
    format = img_url.split('.')[-1]
    id = post['@id']
    file_name = tags + "_" + id + '.' + format
    file_path = SAVE_PATH + "\\" + tags + "\\" + file_name
    img_r = requests.get(img_url)
    with open(file_path, 'wb') as f:
        f.write(img_r.content)
        print(str(id) + "已下载")
    with open(log_path, 'a') as log:
        log.write(str(id) + "已下载\n")


def start(tags: str):
    """
    主函数
    :param tags: 需要爬取的标签
    :param api: API接口
    :return:
    """
    page = 1    # 起始为1
    if not os.path.exists(SAVE_PATH + "\\" + tags):
        os.mkdir(SAVE_PATH + "\\" + tags)
    while(True):
        url = API + "?limit=" + str(LIMIT) + "&tags=" + tags + "&page=" + str(page)
        r = requests.get(url)
        response = r.text
        posts = xmltodict.parse(response, "utf-8")['posts']
        log_path = SAVE_PATH + "\\" + tags + "\\" + "log.txt"
        with open(log_path, 'a') as log:
            log.write("现在工作在第" + str(page) + "页\n")
        print("现在工作在第" + str(page) + "页")
        if 'post' not in list(posts.keys()):
            break
        else:
            post = posts['post']
            para = [[post[i], tags, log_path] for i in range(len(post))]
            pool = multiprocessing.Pool(LIMIT)
            pool.map(process_post, para)
            pool.close()
            pool.join()
            page += 1
            if page > PAGE_LIMIT:
                with open(log_path, 'a') as log:
                    log.write("本次工作已结束\n")
                break


if __name__ == "__main__":
    # start("genshin_impact")
    # start("uncensored")
    # start("pussy")
    # start("azur_lane")
    start("minato_aqua")
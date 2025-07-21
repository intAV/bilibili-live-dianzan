import requests
import time
import execjs
import re

#房间id
roomid = "31255806"
cookie = ""


def get_w_rid(arg1,wts):
    with open("w_rid.js", "r", encoding="utf-8") as file:
        js_code = file.read()
    ctx = execjs.compile(js_code)
    result = ctx.call("js_encrypt", arg1,wts)
    return result

def like():
    hh = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    }
    res = requests.get(f"https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomBaseInfo?room_ids={roomid}&req_biz=video",headers=hh,timeout=5)
    data = res.json()
    anchor_id = data.get('data').get('by_room_ids').get(roomid).get('uid')
    user_id = re.findall("DedeUserID=(.*?);",cookie)[0]
    csrf = re.findall("bili_jct=(.*?);",cookie)[0]
    
    headers = {
            "referer": "https://live.bilibili.com/{}?live_from=85001&spm_id_from=333.1365.live_users.item.click".format(roomid),
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
            "cookie":cookie
    }
    url = "https://api.live.bilibili.com/xlive/app-ucenter/v1/like_info_v3/like/likeReportV3"

    wts = str(round(time.time()))
    params = {
        "click_time": 1000,
        "room_id": roomid,
        "uid": user_id,
        "anchor_id": anchor_id,
        "web_location": "444.8",
        "csrf": csrf,
        "wts": wts,
    }

    w_rid_str = get_w_rid(params,wts)

    params["w_rid"] = w_rid_str.get("w_rid")
    print(f"anchor_id:{anchor_id},user_id:{user_id},csrf:{csrf},w_rid_str:{w_rid_str.get("w_rid")}")

    response = requests.post(url=url, headers=headers, params=params,timeout=5)
    print(response.text)


if __name__ == "__main__":
    like()

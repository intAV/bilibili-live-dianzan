import requests
import time
import execjs

#房间id
roomid = "31255806"
#房主user id 
anchor_id = "702013828"
#user id
uid = ""
#csrf=cookie的bili_jct值
csrf = ""
cookie = ""


with open("w_rid.js", "r", encoding="utf-8") as file:
    js_code = file.read()

ctx = execjs.compile(js_code)

def get_w_rid(arg1,wts):
    result = ctx.call("js_encrypt", arg1,wts)
    return result


def like():
    headers = {
        "referer": "https://live.bilibili.com/{}?live_from=85001&spm_id_from=333.1365.live_users.item.click".format(roomid),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
        "cookie":cookie
    }
    url = "https://api.live.bilibili.com/xlive/app-ucenter/v1/like_info_v3/like/likeReportV3"

    wts = str(round(time.time()))
    arg1 = {
        "click_time": 1000,
        "room_id": roomid,
        "uid": uid,
        "anchor_id": anchor_id,
        "web_location": "444.8",
        "csrf": csrf,
        "wts": wts,
    }

    w_rid_str = get_w_rid(arg1,wts)

    params = {
        "click_time": 1000,
        "room_id": roomid,
        "uid": uid,
        "anchor_id": anchor_id,
        "web_location": "444.8",
        "csrf": csrf,
        "w_rid": w_rid_str.get("w_rid"),
        "wts": w_rid_str.get("wts"),
    }
    # print(params)
    response = requests.post(url=url, headers=headers, params=params)

    print(response.status_code,response.text)
    time.sleep(5)



if __name__ == "__main__":
    like()
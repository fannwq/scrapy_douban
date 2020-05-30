# -*- coding: utf-8 -*- 
import json
from flask import Flask
from flask import render_template
from flask import request

from chart import *
from info import *

app = Flask(__name__)

# the last fetch time
LAST_FETCH_TIMESTAMP = time.time()
# expire time
EXPIRE_TIME = 1
# fetch result
RESULT = []
# the info crawl class
INFO_INSTANCE = InfoClas()
RECENTLY_DATA_LENGTH = 2000


def update():
    global RESULT, INFO_INSTANCE, LAST_FETCH_TIMESTAMP
    print "[fetch data]------>begin"
    result_new = INFO_INSTANCE.fetch()
    print "[fetch data]------>data length:" + str(len(RESULT))
    print "[fetch data]------>end"
    LAST_FETCH_TIMESTAMP = time.time()

    print "[DB operation]------>DB data length:" + str(len(RESULT))
    # 与新数据对比并且筛选
    for new_item in result_new:
        flag = False
        for old_item in RESULT:
            if new_item["id"] == old_item["id"]:
                flag = True
                break
        if flag == False:
            RESULT.append(new_item)
    RESULT = sorted(RESULT, key=lambda x: x['id'], reverse=True)
    print "[DB operation]------>merge data length:" + str(len(RESULT))

    # 只保留1000条数据
    if len(RESULT) > 1000:
        RESULT = RESULT[:1000]


update()


def isExpire():
    global LAST_FETCH_TIMESTAMP
    cur_time = time.time();
    time_span = cur_time - LAST_FETCH_TIMESTAMP;
    print "[time span]------>span:" + str(time_span)
    if time_span > EXPIRE_TIME:
        return True
    else:
        return False


def search(keywords):
    global RESULT, RESULT_BACKUP
    result = [];
    total = RESULT[:RECENTLY_DATA_LENGTH]
    for item in total:
        title = item["title"]
        for word in keywords:
            if word in title:
                result.append(item)
                total.remove(item)
                break
    result = sorted(result, key=lambda x: x['id'], reverse=True)
    return result


@app.route('/refresh')
def refresh():
    # if the data haven't update more than ten minutes
    # 因为部署在平台上，只能使用单线程更新，只有更新完才能相应用户
    if isExpire():
        update()
    return json.dumps({
        'status': 'ok'
    })


@app.route('/force')
def force_refresh():
    global RESULT
    update()
    return json.dumps({
        'status': 'ok',
        'data': len(RESULT)
    })


@app.route('/')
def welcome():
    global RESULT
    return render_template('index.html', data_length=len(RESULT), data=RESULT[:RECENTLY_DATA_LENGTH])


@app.route('/analysis')
def analysis():
    global RESULT
    instance = ChartClas()
    result = instance.analysis(RESULT)
    return json.dumps(result)


@app.route('/data')
def dataLength():
    global RESULT
    return json.dumps({
        'status': 'ok',
        'data': len(RESULT)
    })


@app.route('/fetch')
def fetch():
    global RESULT, LAST_FETCH_TIMESTAMP
    keywords = request.args["param"].split("&")
    for item in keywords:
        print(item)
    result = search(keywords);
    return json.dumps({
        'status': 'ok',
        'data': result
    })


@app.errorhandler(404)
def page_not_found(error):
    return "wrong"


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, use_reloader=True)

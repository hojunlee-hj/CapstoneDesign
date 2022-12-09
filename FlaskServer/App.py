from flask import Flask, request, jsonify, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text
import yaml
from SlackPath import SlackPath
import requests, json

app = Flask(__name__)

slackPath = SlackPath()

# 일반적인 라우트 방식입니다.
@app.route('/board')
def board():
    return "그냥 보드"

# URL 에 매개변수를 받아 진행하는 방식입니다.
@app.route('/board/<article_idx>')
def board_view(article_idx):
    return article_idx

# 위에 있는것이 Endpoint 역활을 해줍니다.
@app.route('/boards',defaults={'page':'index'})
@app.route('/boards/<page>')
def boards(page):
    return page+"페이지입니다."

@app.route('/slack', methods=['POST'])
def createSlackAlarm():
    print(request.is_json)
    param = request.get_json()
    print(param)
    print(slackPath)
    print('-----')
    print(slackPath.getPath(0))
    
    sendToSlack(param['classNum'], param['originText']);
    return jsonify({"param": "OARA"})

@app.route('/testDB', methods=['GET'])
def DBTest():
    user = current_app.database.execute(text("""
        SELECT 
            id,
            name,
            email,
            profile
        FROM users
        WHERE id = :user_id
    """), {
        'user_id' : 1
    }).fetchone()

    return {
        'id'      : user['id'],
        'name'    : user['name'],
        'email'   : user['email'],
        'profile' : user['profile']
    } if user else None
    

def sendToSlack(classNum, originText):
    print(classNum)
    print(originText)
    print(slackPath.getPath(classNum))
    path = slackPath.getPath(classNum)
    param1 = makeJsonString(classNum, originText)
    # json_object = json.loads(param1)
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    print(param1)
    response = requests.post(url=path, headers=headers, json=param1)
    print(response.content)




def makeJsonString(classNum, originText):

    className = slackPath.getClassName(classNum)

    ret = {
    "username" : "동국죠스 이슈 분류 시스템",
    "icon_url" : "https://github.com/hojunlee-hj/CapstoneDesignNLP/blob/main/Webhook/donggukJaws.png?raw=true",
    "blocks": [
    	{
    		"type": "section",
    		"text": {
    			"type": "mrkdwn",
    			"text": "*기술적 문제* : 앱 클라이언트 기능 문제"
    		}
    	},
    	{
    		"type": "section",
    		"block_id": "section567",
    		"text": {
    			"type": "mrkdwn",
    			"text": "*담당 부서* : {}".format(className)
    		}
    	},
        {
    		"type": "section",
    		"text": {
    			"type": "mrkdwn",
    			"text": "*기능 태그* : #업데이트 #재생"
    		}
    	},
        {
            "type": "section",
    		"text": {
    			"type": "mrkdwn",
    			"text": "*주요 이슈*\n```진짜 어플이 너무 느립니다 다른 어플로 갈아타고 싶을 정도에요...```"
    		}
        },
    	{
    		"type": "section",
    		"block_id": "section789",
    		"fields": [
    			{
    				"type": "mrkdwn",
    				"text": "*전체 리뷰 내용*\n>{}".format(originText) 
    			}
    		]
    	}
    ]
}

    return ret

app.config.from_pyfile("config.py")

database = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
app.database = database


app.run(host="localhost",port=5000)


import requests
from DonggukJaws.util.slack.SlackPath import SlackPath
import time

def sendToSlack(classNum, originText, techIssue, issueSentence):
	slackPath = SlackPath()
	path = slackPath.getPath(classNum)
	param1 = makeJsonString(classNum, originText, techIssue, issueSentence)
	print(path)
	print(param1)
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	response = requests.post(url=path, headers=headers, json=param1)
	print(response)
	print(response.content)




def makeJsonString(classNum, originText, techIssue, issueSentence):
	slackPath = SlackPath()
	className = slackPath.getClassName(classNum)
	ret = {
    "username" : "동국죠스 사용자 이슈 분류 시스템",
    "icon_url" : "https://github.com/hojunlee-hj/CapstoneDesignNLP/blob/main/Webhook/donggukJaws.png?raw=true",
    "blocks": [
    	{
    		"type": "section",
    		"text": {
    			"type": "mrkdwn",
    			"text": "*기술적 문제* : {}".format(techIssue)
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
    			"text": "*주요 이슈*\n```{}```".format(issueSentence)
    		}
        }
    ],
    "attachments": [
        {
    		"color": "#2eb886",
            "pretext": "*전체 리뷰 내용*",
    		"text": "{}".format(originText),
			"image_url": "http://my-website.com/path/to/image.jpg",
            "thumb_url": "http://example.com/path/to/thumb.png",
            "footer": "Google Playstore",
            "footer_icon": "https://github.com/hojunlee-hj/CapstoneDesignNLP/blob/main/Webhook/google-play-png-logo.png?raw=true",
            "ts": int(time.time())
    	}
    ]
}
	return ret
import requests
from DonggukJaws.util.slack.SlackPath import SlackPath
import time
import operator

def sendToSlack(classNum, originText, techIssue, issueSentence, techTags):
	slackPath = SlackPath()
	path = slackPath.getPath(classNum)
	param1 = makeJsonString(classNum, originText, techIssue, issueSentence, techTags)
	print(path)
	print(param1)
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	response = requests.post(url=path, headers=headers, json=param1)
	print(response)
	print(response.content)




def makeJsonString(classNum, originText, techIssue, issueSentence, techTags):
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
    			"text": "*기능 태그* : {}".format(techTags)
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


def processTag(classNum, originalText, okt):
	'''
    어간 추출
    분류된 클래스에 따른 키워드들을 가져온다.
    가져온 키워드들을 for문 돌려서 가져오게 한다. - 어간 추출 사용?
    없으면 기본값이 있어야 한다.
    중요도 * 나온 빈도수로?
    '''

	d1 = {'애플워치': 2, '안드로이드 오토': 2, '오토': 2, '아이폰': 2, '갤럭시': 2, '플레이리스트': 2, '재생 목록': 2, '싱크': 2, '캐시': 2, '꺼진다': 2,
		  '버튼': 2, '위젯': 2, '잠금화면': 2, '재생': 2}
	d2 = {'렉': 2, '끊겨요': 2, '느려요': 2, '사라졌어요': 2, '계정': 2, '로그인': 2, '결제': 2, '서버': 2, '불안정': 2, '로딩': 2, '요금': 2,
		  '연결': 2}
	d3 = {'해주세요': 2, 'UX': 2, 'UI': 2, '상단바': 2, "어려워요": 2, '어딨는지': 2, '앨범': 2, '디자인': 2}
	d4 = {'가사': 2, '음질': 2, '추가': 2, '음원': 2, '팝송': 2, '권리사': 2, '일본어': 2, '일본': 2}
	d5 = {'네트워크': 2, '와이파이': 2, '와이 파이': 2, '셀룰러': 2, '데이터': 2, '연결': 2}

	baseTag = ['앱 오류', '서버 오류', '기획 오류', '컨텐츠 운영 오류', '네트워크 오류']

	tagInfo = [d1, d2, d3, d4, d5]
	selectedTag = tagInfo[classNum - 1]
	score = {}
	for key, value in selectedTag.items():
		score[key] = 0

	stem = okt.morphs(originalText, stem=True)

	for word in stem:
		for key, value in selectedTag.items():
			if (word == key):
				print(key)
				score[key] += value

	score = sorted(score.items(), key=operator.itemgetter(1), reverse=True)

	ret = []
	for key in score:
		if (key[1] != 0 and len(ret) < 3):
			ret.append(key[0])

	if (len(ret) < 3):
		ret.append(baseTag[classNum - 1])

	print(ret)

	return ret

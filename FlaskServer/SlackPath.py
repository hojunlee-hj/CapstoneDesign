import yaml

class SlackPath:
    def __init__(self):
        with open('properties.yaml') as f:
            files = yaml.load(f,Loader=yaml.FullLoader)
            print(files)
            self.slackPaths = files['app']
    
    def getPath(self, classNum):
        return self.slackPaths['class'][classNum]
    
    def getClassName(self, classNum):
        return self.slackPaths['className'][classNum]
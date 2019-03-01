import math
import utils
def getPrior(train, confidence=0.95):
	result = {}
	mean = train['target'].mean()
	#h = 1.96*(confidence*1.96/2)*(train["target"].std()/math.sqrt(len(train['target'])))
	h = 1.96*math.sqrt((mean)*(1-mean)/len(train["target"]))
	print(len(train["target"]))
	result['estimation'] = mean
	result['min5pourcent'] = mean-h
	result['max5pourcent'] = mean+h
	return result

class APrioriClassifier(utils.AbstractClassifier):
	def __init__(self):
		print("classeur initialise")

	def estimClass(self, attr):
		return 1

	def statsOnDF(self, df):
		result = {}
		vp = 0
		vn = 0
		fp = 0
		fn = 0
		for t in df.itertuples():
			dic = t._asdict()
			temoin = self.estimClass(dic)
			if(temoin == 1):
				if(temoin == dic['target']):
					vp += 1
				else:
					fp += 1
			else:
				if(temoin == dict['target']):
					vn += 1
				else:
					fp += 1
		result['vp'] = vp
		result['vn'] = vn
		result['fp'] = fp
		result['fn'] = fn
		return result
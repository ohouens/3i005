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
		result['precision'] = vp*1.0/(vp+fp)
		result['vp'] = vp
		result['vn'] = vn
		result['fp'] = fp
		result['fn'] = fn
		result['rappel'] = 1.0
		return result

def P2D_l(df, attr):
	result = {}
	result[0] = {}
	result[1] = {}
	malade = 0
	sain = 0
	for t in df.itertuples():

		dic = t._asdict()
		if dic['target'] == 1:
			malade += 1
			if dic[attr] in result[1].keys():
				result[1][dic[attr]] += 1
			else:
				result[1][dic[attr]] = 1
		else :
			sain += 1
			if dic[attr] in result[0].keys():
				result[0][dic[attr]] += 1
			else:
				result[0][dic[attr]] = 1

	for i in result[0].keys():
		result[0][i] = result[0][i]*1.0/sain
	for i in result[1].keys():
		result[1][i] = result[1][i]*1.0/malade
	
	return result

def P2D_p(df, attr):
	result = {}
	for t in df.itertuples():
		dic = t._asdict()
		if(dic[attr] not in result.keys()):
			result[dic[attr]] = {}
			result[dic[attr]][0] = 0
			result[dic[attr]][1] = 0
			result[dic[attr]]['cpt'] = 0
		result[dic[attr]]['cpt'] += 1
		if(dic['target'] == 1):
			result[dic[attr]][1] += 1
		else:
			result[dic[attr]][0] += 1

	for i in result.keys():
		result[i][0] = result[i][0]*1.0/result[i]['cpt']
		result[i][1] = result[i][1]*1.0/result[i]['cpt']
		result[i].pop('cpt', None)
	return result
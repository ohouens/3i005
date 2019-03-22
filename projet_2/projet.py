import math
import utils

def conversion(entier, L=[0,0,0,0]):
	
	i = 3
	while i >= 0 :
		L[i] = entier//(1024**i)
		entier = entier%(1024**i)
		i -= 1
	return L



def getPrior(train, confidence=0.95):
	result = {}
	mean = train['target'].mean()
	#h = 1.96*(confidence*1.96/2)*(train["target"].std()/math.sqrt(len(train['target'])))
	h = 1.96*math.sqrt((mean)*(1-mean)/len(train["target"]))
	#print(len(train["target"]))
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
				if(temoin == dic['target']):
					vn += 1
				else:
					fn += 1
		result['precision'] = vp*1.0/(vp+fp)
		result['vp'] = vp
		result['vn'] = vn
		result['fp'] = fp
		result['fn'] = fn
		result['rappel'] = vp*1.0/(vp+fn)
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

class ML2DClassifier(APrioriClassifier):
	def __init__(self, df, attr):
		print("classeur ML2D initialise")
		self.df = df
		self.attr = attr
		self.inter = P2D_l(self.df, self.attr)
	
	def estimClass(self, personne):
		if(self.inter[0][personne['thal']] >= self.inter[1][personne['thal']]):
			return 0
		else:
			return 1

class MAP2DClassifier(APrioriClassifier):
	def __init__(self, df, attr):
		print("classeur MAP2D initialise")
		self.df = df
		self.attr = attr
		self.inter = P2D_p(self.df, self.attr)
	
	def estimClass(self, personne):
		if(self.inter[personne['thal']][0] >= self.inter[personne['thal']][1]):
			return 0
		else:
			return 1

def nbParams(df, attrs=None):
	result = 1
	units = ["o","Ko","Mo","Go"]
	if(attrs == None):
		attrs = utils.getNthDict(df,0).keys()
	for i in attrs:
		result *= len(P2D_p(df, i))
	result *= 8
	string = str(len(attrs))+" variable(s) : " + str(result) + " octets"
	if result >= 1024:
		string += " ="
		conver = conversion(result)
		i = len(conver) - 1
		while i >= 0:
			while i > 0 and conver[i] == 0:
				i -= 1
			string = string +" "+str(conver[i])+units[i]
			i -= 1
	print(string)


def nbParamsIndep(df, attrs=None):
	result = 0
	if(attrs == None):
		attrs = utils.getNthDict(df,0).keys()
	for i in attrs:
		result += len(P2D_p(df, i))
	result *= 8
	string = str(len(attrs))+" variable(s) : " + str(result) + " octets"
	if(result > 1024):
		quotient = result//1024
		reste = result%1024
		string = string + " = "+str(quotient)+"ko "+str(reste)+"o"
	print(string)

def drawNaiveBayes(df, attr):
	result = ""
	for i in utils.getNthDict(df,0).keys():
		if(i != attr):
			result += attr+"->"+i+";"
	return utils.drawGraph(result)

def nbParamsNaiveBayes(df, attribut, liste_attributs=None):
	valAttr = len(P2D_p(df, attribut))
	result = 0
	units = ["o","Ko","Mo","Go"]
	if(liste_attributs == None):
		liste_attributs = utils.getNthDict(df,0).keys()
	for i in liste_attributs:
		if i == attribut:
			result += 1
		else:
			result += len(P2D_p(df, i))
	if(result != 0):
		result *= 8*valAttr
	else:
		result = 8*valAttr
	string = str(len(liste_attributs))+" variable(s) : " + str(result) + " octets"
	if result >= 1024:
		string += " ="
		conver = conversion(result)
		i = len(conver) - 1
		while i >= 0:
			while i > 0 and conver[i] == 0:
				i -= 1
			string = string +" "+str(conver[i])+units[i]
			i -= 1
	print(string)

class MAPNaiveBayesClassifier(APrioriClassifier):
	def __init__(self, df, attr):
		print("classeur ML2D initialise")
		self.df = df
		self.attr = attr
		self.inter = P2D_l(self.df, self.attr)

	def estimClass(self, personne):
		if(self.inter[0][personne['thal']] >= self.inter[1][personne['thal']]):
			return 0
		else:
			return 1

	def estimProbas():
		pass
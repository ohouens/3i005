import math
import utils
import numpy as np
import pandas as pd
import pydotplus
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats



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
		"""
		VP : nombre d'individus avec target = 1 et classe prévue = 1
		VN : nombre d'individus avec target = 0 et classe prévue = 0
		FP : nombre d'individus avec target = 0 et classe prévue = 1
		FN : nombre d'individus avec target = 1 et classe prévue = 0"""
		vrai_positif = 0
		vrai_negatif = 0
		faux_positif = 0
		faux_negatif = 0
		"""calcul des différentes statistiques:
			témoin représente l'estimation de la classe de la personne et 
			dic['target'] sa classe réelle """
		for t in df.itertuples():
			dic = t._asdict()
			temoin = self.estimClass(dic)
			if(temoin == 1):
				if(temoin == dic['target']):
					vrai_positif += 1
				else:
					faux_positif += 1
			else:
				if(temoin == dic['target']):
					vrai_negatif += 1
				else:
					faux_negatif += 1
		result['precision'] = vrai_positif*1.0/(vrai_positif+faux_positif)
		result['vp'] = vrai_positif
		result['vn'] = vrai_negatif		
		result['fp'] = faux_positif
		result['fn'] = faux_negatif
		result['rappel'] = vrai_positif*1.0/(vrai_positif+faux_negatif)
		return result

def P2D_l(df, attr):
	"""
	P2D_l(df, attr) calcule dans le dataframe la probabilité P(attr|target) sous 
	la forme d'un dictionnaire asssociant à la valeur T
	un dictionnaire associant à la valeur A la probabilité P(attr=A|target=T)"""
	result = {}
	result[0] = {}
	result[1] = {}
	malade = 0
	sain = 0

	for t in df.itertuples():

		dic = t._asdict()
		A = dic[attr]
		if dic['target'] == 1:
			malade += 1

			if A in result[1].keys():
				result[1][A] += 1
			else:
				result[1][A] = 1
		else :
			sain += 1
			if A in result[0].keys():
				result[0][A] += 1
			else:
				result[0][A] = 1

	for i in result[0].keys():
		result[0][i] = result[0][i]*1.0/sain
	for i in result[1].keys():
		result[1][i] = result[1][i]*1.0/malade

	return result

def P2D_p(df, attr):
	"""
	P2D_p(df, attr) calcule dans le dataframe la probabilité P(target|attr)
	sous la forme d'un dictionnaire associant à la valeur A
	un dictionnaire associant à la valeur T la probabilité P(target=T|attr=A)"""
	result = {}
	for t in df.itertuples():
		dic = t._asdict()
		A = dic[attr]
		if(A not in result.keys()):
			result[A] = {}
			result[A][0] = 0
			result[A][1] = 0
			result[A]['cpt'] = 0
		result[A]['cpt'] += 1
		if(dic['target'] == 1):
			result[A][1] += 1
		else:
			result[A][0] += 1

	for i in result.keys():
		result[i][0] = result[i][0]*1.0/result[i]['cpt']
		result[i][1] = result[i][1]*1.0/result[i]['cpt']
		result[i].pop('cpt', None)
	return result

class ML2DClassifier(APrioriClassifier):
	def __init__(self, df, attr):
		"""self.inter est un dictionnaire P2D_l (dictionnaire associant à la valeur T
	un dictionnaire associant à la valeur A la probabilité P(attr=A|target=T))"""
		print("classeur ML2D initialise")

		self.df = df
		self.attr = attr
		self.inter = P2D_l(self.df, self.attr)

	def estimClass(self, personne):
		""" le classifier retourne :
		0 si P(A|0) > P(A|1)
		1 sinon"""
		if(self.inter[0][personne[self.attr]] >= self.inter[1][personne[self.attr]]):
			return 0
		else:
			return 1

class MAP2DClassifier(APrioriClassifier):
	def __init__(self, df, attr):
		"""self.inter est un dictionnaire P2D_p (dictionnaire associant à la valeur A
	un dictionnaire associant à la valeur T la probabilité P(target=T|attr=A))"""
		print("classeur MAP2D initialise")
		self.df = df
		self.attr = attr
		self.inter = P2D_p(self.df, self.attr)

	def estimClass(self, personne):
		""" le classifier retourne :
		0 si P(0|A) > P(1|A)
		1 sinon"""
		if(self.inter[personne[self.attr]][0] >= self.inter[personne[self.attr]][1]):
			return 0
		else:
			return 1

def nbParams(df, attrs=None):
	"""nbParams calcule la taille mémoire des tables $P(target|attr_1,..,attr_k)$
	étant donné un dataframe et la liste $[target,attr_1,...,attr_l]$
	 en supposant qu'un float est représenté sur 8octets"""
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


def conversion(entier, L=[0,0,0,0]):
	""" conversion prend en entrée un nombre d'octets 
	et retourne le nombre sous la form  d'une liste 
	[o, Ko, Mo, Go]
	ex : conversion(10000000000) -> [0, 761, 320, 9]"""
	i = 3
	while i >= 0 :
		L[i] = entier//(1024**i)
		entier = entier%(1024**i)
		i -= 1
	return L


def nbParamsIndep(df, attrs=None):
	"""calcule la taille mémoire nécessaire pour représenter les tables de probabilité
	étant donné un dataframe, en supposant qu'un float est représenté sur 8octets
	et en supposant l'indépendance des variables """
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




class MLNaiveBayesClassifier(APrioriClassifier):
	def __init__(self, df):
		self.df = df
		self.liste_attributs = utils.getNthDict(df,0).keys()
		self.proba = {}
		for attribut in self.liste_attributs:
			self.proba[attribut] = P2D_l(self.df, attribut)


	def estimClass(self, personne):
		sain, malade = self.estimProbas(personne)
		if malade > sain:
			return 1
		else:
			return 0


	def estimProbas(self,dictionnaire):
		proba_sain   = 1
		proba_malade = 1
		for attribut in self.proba:
			if attribut != 'target':
				inter = self.proba[attribut]
				if dictionnaire[attribut] in inter[0] and dictionnaire[attribut] in inter[1] :

					proba_sain *= inter[0][dictionnaire[attribut]]
					proba_malade *= inter[1][dictionnaire[attribut]]
	 

		return (proba_sain, proba_malade)


class MAPNaiveBayesClassifier(APrioriClassifier):
	def __init__(self, df):
		self.df = df
		self.liste_attributs = list(utils.getNthDict(df,0).keys())
		self.liste_attributs.remove('target')
		self.proba = {}
		for i in self.liste_attributs:
			self.proba[i] = P2D_l(self.df, i)


	def estimClass(self, personne):
		sain, malade = self.estimProbas(personne)
		if malade > sain:
			return 1
		else:
			return 0


	def estimProbas(self,dictionnaire):
		proba_sain   = self.df["target"].mean()
		proba_malade = 1-self.df["target"].mean()
		for attribut in self.proba:
			inter = self.proba[attribut]
			if dictionnaire[attribut] in inter[0] and dictionnaire[attribut] in inter[1] :

				proba_sain *= inter[0][dictionnaire[attribut]]
				proba_malade *= inter[1][dictionnaire[attribut]]

		return (proba_sain/(proba_sain+proba_malade), proba_malade/(proba_sain+proba_malade))


def isIndepFromTarget(df, attribut, seuil):
	""" Matrice va stocker la matrice de contingence.
		Pour la construire on a besoin des différentes valeurs
		de l'attribut passé en paramètre."""
	valeurs = np.unique(df[attribut].values)
	matrice = np.zeros((2, len(valeurs)),dtype=int)

	for index, row in df.iterrows():
		matrice[row["target"], np.where(valeurs==row[attribut])] += 1

	chi2, p, dof, ex = scipy.stats.chi2_contingency(matrice)
	return p > seuil




class ReducedMLNaiveBayesClassifier(APrioriClassifier):
	def __init__(self, df, seuil):
		self.df = df
		self.liste_attributs = utils.getNthDict(df,0).keys()
		self.proba = {}
		for attribut in self.liste_attributs:
			if not isIndepFromTarget(df, attribut, seuil):
				self.proba[attribut] = P2D_l(self.df, attribut)


	def estimClass(self, personne):
		sain, malade = self.estimProbas(personne)
		if malade > sain:
			return 1
		else:
			return 0


	def estimProbas(self,dictionnaire):
		proba_sain   = 1
		proba_malade = 1
		for attribut in self.proba:
			inter = self.proba[attribut]
			if dictionnaire[attribut] in inter[0] and dictionnaire[attribut] in inter[1] :
				proba_sain *= inter[0][dictionnaire[attribut]]
				proba_malade *= inter[1][dictionnaire[attribut]]

		return (proba_sain, proba_malade)

	def draw(self):
		result = ""
		for i in self.proba.keys():
			if(i != 'target'):
				result += "target"+"->"+i+";"
		return utils.drawGraph(result)



class ReducedMAPNaiveBayesClassifier(APrioriClassifier):
	def __init__(self, df, seuil):
		self.df = df
		self.liste_attributs = utils.getNthDict(df,0).keys()
		self.proba = {}
		for attribut in self.liste_attributs:
			if not isIndepFromTarget(df, attribut, seuil):
				self.proba[attribut] = P2D_l(self.df, attribut)



	def estimClass(self, personne):
		sain, malade = self.estimProbas(personne)
		if malade > sain:
			return 1
		else:
			return 0


	def estimProbas(self,dictionnaire):
		proba_sain   = self.df["target"].mean()
		proba_malade = 1-self.df["target"].mean()
		for attribut in self.proba:
			inter = self.proba[attribut]
			if dictionnaire[attribut] in inter[0] and dictionnaire[attribut] in inter[1] :

				proba_sain *= inter[0][dictionnaire[attribut]]
				proba_malade *= inter[1][dictionnaire[attribut]]

		return (proba_sain/(proba_sain+proba_malade), proba_malade/(proba_sain+proba_malade))

	def draw(self):
		result = ""
		for i in self.proba.keys():
			if(i != 'target'):
				result += "target"+"->"+i+";"
		return utils.drawGraph(result)

def mapClassifiers(dic, df):
	precision = []
	rappel = []
	nom = []
	for k, v in dic.items():
		inter = v.statsOnDF(df)
		nom.append(k)
		precision.append(inter['precision'])
		rappel.append(inter['rappel'])
	plt.scatter(precision, rappel, color="r", marker="x")
	for i, txt in enumerate(nom):
		plt.annotate(txt, (precision[i], rappel[i]))

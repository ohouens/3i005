import io
import math
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import seaborn as sns
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#Définition des nucléotides
nucleotide = {'A':0,'C':1,'G':2,'T':3}
nucleotide_inverse = {0:'A',1:'C',2:'G',3:'T'}
nucleotide_indetermine = {'A':0,'C':1,'G':2,'T':3,'N':-1}

def decode_sequence(sequence):
    inv_nucleotide = {v:k for k, v in nucleotide_indetermine.items()}
    to_str = ""
    for i in sequence:
        if(i in inv_nucleotide):
            to_str += inv_nucleotide[i]
        else:
            to_str += 'N'
    return to_str


def encode_sequence(string):
    to_list = []
    for base in string:
        if(base in nucleotide_indetermine):
            to_list.append(nucleotide_indetermine[base])
    return to_list

def read_fasta(fasta_filepath):
    fasta_file = io.open(fasta_filepath, 'r')
    current_sequence = ""
    sequences_dict = {}
    for line in fasta_file.readlines():
        if(line[0] == '>'):
            current_sequence = line
            sequences_dict[line] = []
        else:
            for nucl in line:
                if(nucl in nucleotide_indetermine):
                    sequences_dict[current_sequence].append(nucleotide_indetermine[nucl])


    return sequences_dict

def listToString(liste):
    return "".join(str(j) for j in liste)

def nucleotide_count(sequence):
    count = [0 for k in nucleotide]
    for nucl in sequence:
        if(nucl >= 0):
            count[nucl] += 1
    return count

def nucleotide_frequency(sequence):
    count = [0 for k in nucleotide]
    n_nucl = 0.
    for nucl in sequence:
        if(nucl >= 0):
            count[nucl] += 1
            n_nucl += 1.
    return count/(np.sum(count))

def log_proba_sequence(liste_freq):
    proba = 1
    for i in liste_freq:
        proba *= i
    return math.log(proba)

def code(m,k):
    indice = k-1
    res = 0
    for i in m:
        res += nucleotide[i]*(4**indice)
        indice -= 1
    return res

def inverse(indice ,k):
    res = ""
    reste = 0
    index = k-1
    temoin = indice
    for i in range(k):
        res += nucleotide_inverse[temoin//(4**(index))]
        temoin = temoin%4**(index)
        index -= 1
    return res

def genereMots(k):
    res = {}
    for i in range(4**k):
        res[inverse(i, k)] = 0
    return res

def count_word(k, sequence):
    res = genereMots(k)
    for i in range(len(sequence)-k+1):
        mot = sequence[i:i+k]
        string = ""
        for s in mot:
            string += nucleotide_inverse[s]
        res[string] += 1

    return res

def comptage_attendu(frequences, k, l):
    """comptage attendu renvoie le comptage théorique des différents
     nucléotides dans la séquence"""
    result = {}
    mots = genereMots(k)
    for mot in mots:
        inter = 1
        for lettre in mot:
            inter *= frequences[nucleotide[lettre]]
        result[mot] = inter*l
    return result

def graphique(k, sequence):

    frequences = nucleotide_frequency(sequence)
    abscisse   = comptage_attendu(frequences, k, len(sequence))
    ordonnee   = count_word(k, sequence)
    x = []
    y = []
    for cle in ordonnee.keys():
        y.append(ordonnee[cle])
        x.append(abscisse[cle])
    plt.title( "Comparaison des occurences, k = "+str(k))
    plt.scatter(x, y, edgecolor='black')
    plt.plot([min(min(x),min(y)),max(max(x),max(y))],[min(min(x),min(y)),max(max(x),max(y))], 'r-', lw=2,label="x=y")
    plt.xlabel("Nombre d'occurences attendues")
    plt.ylabel("Nombre d'occurences observées")
    plt.legend()
    plt.show()

def simule_sequence(lg, m):
    """simule séquence renvoie une séquence de 
    longueur Lg dont :
    la proportion en A est de m[0], 
    la propotrion en C est de m[1],
    la propotrion en G est de m[2],
    la propotrion en T est de m[3].
    On rappelle que 0 représente le nucléotide A,
    1 le nucléotide C,
    2 le nucléotide G,
    3 le nucléotide T,
     """

    seq =[]
    for i in range(lg):
        a = random.random()
        if a < m[0]:
            seq.append(0)
        elif a < m[0]+m[1]:
            seq.append(1)
        elif a < m[0]+m[1]+m[2]:
            seq.append(2)
        else:
            seq.append(3)
    return seq

def compare(k, sequence):
    """la fonction compare renvoie la valeur absolue 
    de la différence entre le comptage observé et le comptage attendu.
    Plus ce nombre est proche de zéro plus les comptages sont similaires."""
    frequences = nucleotide_frequency(sequence)
    abscisse = comptage_attendu(frequences, k, len(sequence))
    ordonnee = count_word(k, sequence)
    x = []
    y = []
    for cle in ordonnee.keys():
        y.append(ordonnee[cle])
        x.append(abscisse[cle])
    return math.fabs(np.mean([y])-np.mean([x]))

def probaempirique(mot,n,K):
    res = 0
    sequences = []
    for i in range(K):
        sequences.append(simule_sequence(1000,[0.25,0.25,0.25,0.25]))
    for i in sequences:
        dico = count_word(len(mot), i)
        if mot in dico.keys() :
            res += 1
    if res >= n:
        return res*1.0/len(sequences)
    else :
        return 0
def creationhisto(motifs,x,K):
    proba = {}
    for i in motifs:
        proba[i]=[]
        for j in range(x):
            proba[i].append(probaempirique(i,j,K))

    return proba


def histogramme(proba,motifs,o):
    liste=[]
   
    # bins = []
    # bins=np.arange(4)
    # color = ['yellow', 'green','brown','blue']
    for i in range(len(motifs)):
    #     plt.bar(proba[motifs[i]],bins+i/4.0,color[i])
        liste.append(proba[motifs[i]])
    # #plt.hist([liste[0],liste[1],liste[2],liste[3]], bins = bins, color = ['yellow', 'green','brown','blue'],
    # #   edgecolor = 'red', hatch = '/', label = [motif for motif in motifs]) # bar est le defaut
    # plt.ylabel('probabilités')
    # plt.xlabel('occurences minimale par séquence')
    # plt.title('')
    # plt.legend()
    #
    a = tuple(liste[0])
    b = tuple(liste[1])
    c = tuple(liste[2])
    d = tuple(liste[3])

    fig, ax = plt.subplots()

    index = np.arange(o)
    bar_width = 0.2
    opacity = 0.6
    
    rects1 = ax.bar(index-bar_width, a, bar_width,
                    alpha=opacity, color='blue',label=motifs[0])
    rects2 = ax.bar(index, b, bar_width,
                    alpha=opacity, color='red',label=motifs[1])
    rects3 = ax.bar(index +bar_width, c, bar_width,
                    alpha=opacity, color='yellow',label=motifs[2])
    rects3 = ax.bar(index + 2*bar_width, d, bar_width,
                    alpha=opacity, color='green',label=motifs[3])
    ax.set_xlabel('occurences minimales du motif ')
    ax.set_ylabel('probabilités')
    ax.set_title("")
    ax.set_xticks(index + bar_width / 4)
    ax.set_xticklabels(('1', '2', '3', '4', '5'))
    ax.legend()

    plt.show() 

def histogramme2(motifs,N):

    dico = creationhisto(motifs,N,10)
    x = list(dico.values())
    print(x)
    sns.distplot(x)

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
        result[mot] = inter*(l-k+1)
    return result

def graphique(k, sequence):
    """Trace le graphique avec en abscisse le comptage attendu
    et en ordonnée le comptage observé"""
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
    """la boucle suivante affiche les motifs dont le nombre d'occurences 
    réel est nettement supérieur au nombre d'occurences attendu
    dans la séquence"""
    dico={}
    dico["Motifs"]=[]
    for cle in ordonnee.keys():
        if(ordonnee[cle]>10*(abscisse[cle]+1)):
            dico["Motifs"].append(cle)
    print(dico)

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


def probaempirique(mot,  frequences,l=10000, boucles=1000):
    """Renvoie un dictionnaire dont les clés sont les occurences n,
    les valeurs sont la probabilité d'avoir le mot n fois"""
    probas = {}
    for i in range(boucles):
        seq = simule_sequence(l, frequences)
        mots = count_word(len(mot), seq)
        cpt = mots[mot]
        if cpt in probas:
            probas[cpt] += 1
        else:
            probas[cpt] = 1
    return {key : value/boucles for key,value in probas.items()}


def histogramme(mot, frequences):
    probas = probaempirique(mot,frequences)
    fig, ax = plt.subplots(figsize=(7,5))
    ax.bar(probas.keys(), probas.values())
    ax.set_title("Distribution du comptage de "+mot)
    ax.set_xlabel("Occurrences")
    ax.set_ylabel("Probabilités")


def estimMatrice(sequence):
    """Renvoie la matrice de transition calculée à partir
    du comptage de mots de longueur 2"""
    dico = count_word(2,sequence)
    matrice = np.zeros((4,4),dtype=float)
    
    for i in range(4):
        denominateur = 0
        for j in range(4):
            matrice[i][j] = dico[nucleotide_inverse[i]+nucleotide_inverse[j]]
            denominateur += dico[nucleotide_inverse[i]+nucleotide_inverse[j]]
        matrice[i,:]= matrice[i,:]*1.0 / denominateur

    return matrice


def simule_markov(lg, matrice, frequences=[0.25,0.25,0.25,0.25]):
    """simule _markov renvoie une séquence de 
    longueur Lg dont les proportions en nucléotide
    suivent le modèle de dinucléotides"""
    sequence = ""
    #calcul du premier nucléotide
    a = random.random()
    if a < frequences[0]:
        sequence += str(0)
    elif a < frequences[0]+frequences[1]:
        sequence += str(1)
    elif a < frequences[0]+frequences[1]+frequences[2]:
        sequence += str(2)
    else:
        sequence += str(3)
    #estimation des lg-1 nucléotides suivant
    for i in range(1,lg):
        a = random.random()
        if a < matrice[int(sequence[i-1])][0]:
            sequence += str(0)
        elif a < matrice[int(sequence[i-1])][0]+matrice[int(sequence[i-1])][1]:
            sequence += str(1)
        elif a < matrice[int(sequence[i-1])][0]+matrice[int(sequence[i-1])][1]+matrice[int(sequence[i-1])][2]:
            sequence += str(2)
        else:
            sequence += str(3) 



    return sequence


def proba_apparition(mot, M, frequence=[0.25,0.25,0.25,0.25]):
    """proba_apparition calcule la probabilité d'apparition 
    du mot à l'aide du vecteur frequence (pour le 1er nucleotide)
    et de la matrice M pour les nucléotides suivant"""
    p = frequence[nucleotide[mot[0]]]

    for i in range(1,len(mot)):
        p = p*M[nucleotide[mot[i-1]]][nucleotide[mot[i]]]

    return p

def nbr_occurences( M, k, l, frequence=[0.25,0.25,0.25,0.25]):
    """nbr occurences renvoie le nombre supposé
    d'occurences des mot de taille k, dans une séquence de taille lg à
    partir du vecteur frequence et de la matrice M"""
    result = {}
    mots = genereMots(k)
    for mot in mots.keys():
        
        result[mot] = (l-k+1)*proba_apparition(mot,M,frequence=frequence)

    return result
import io
import math
import numpy as np
import matplotlib.pyplot as plt
import random

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
    res = {}

    for i in range(len(sequence)-k+1):
        mot = sequence[i:i+k]
        string = ""
        for s in mot:
            string += nucleotide_inverse[s]
        if string in res.keys():
            res[string] += 1
        else:
            res[string] = 1

    return res

def comptage_attendu(frequences, k, l):
    #UTILISER LOGPROBA
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
    abscisse = comptage_attendu(frequences, k, len(sequence))
    ordonnee = count_word(k, sequence)
    x = []
    y = []
    for cle in ordonnee.keys():
        y.append(ordonnee[cle])
        x.append(abscisse[cle])
    plt.scatter(x, y, edgecolor='black')
    plt.show()

def simule_sequence(lg, m):
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
    frequences = nucleotide_frequency(sequence)
    abscisse = comptage_attendu(frequences, k, len(sequence))
    ordonnee = count_word(k, sequence)
    x = []
    y = []
    for cle in ordonnee.keys():
        y.append(ordonnee[cle])
        x.append(abscisse[cle])
    return math.fabs(np.mean([y])-np.mean([x]))

def probaempirique(sequences,mot,n):
    res = 0

    for i in sequences.values():
        dico = count_word(len(mot), i)
        if mot in dico.keys() and dico[mot] >= n:
            res += 1
    return res*1.0/len(sequences)

# Forestas Yan
#Projet: Compression de donnÃ©es par codage Huffman
import time as time
ASCII = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '\n', '\x1a']
HEXA =  ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
#Determination_alphabet("/Users/forestay/Travaux/PROJ_631/alice.txt")



         

#This programm takes a path and return the text of the .txt file associated with this path
def Recuperer_texte(emplacement):
    with open(emplacement,'r') as f:
        texte = f.read()
    return texte

#This programm takes a path and return the text of the .bin file associated with this path
def Recuperer_texte_bin(emplacement):
    with open(emplacement,'rb') as f:
        texte = f.read()
    return texte




#The point of this program is to determine wich caracter are used in a text and how many times
#We will present the result as a list of lists, each list contains the caracter and its frequency

#The programm takes 0.25s for Alice.txt
def Determination_alphabet(emplacement):
    #We get the text
    texte = Recuperer_texte(emplacement)
    liste_frequence = []
    
    #For each caracter of the text, we check if it is already in the list
    for k in range(len(texte)):
        i = recherche_liste(liste_frequence, texte[k])
        #If it is not, we add it
        if i == -1:
            liste_frequence.append([texte[k], 1])       
        #If it is, we add one to its frequency
        else:
            liste_frequence[i][1] +=1
    
    #We sort the list by frequency and ASCII order
    liste_frequence = tri_ASCII(liste_frequence)
    return liste_frequence



#It return the spot of a caracter in a list
#It return -1 if it is not in the list
def recherche_liste(liste, caractere):
    for k in range(len(liste)):
        if caractere == liste[k][0]:
            return k
    return -1

#Gives the order of the caracter in ASCII (' '=0, '!'=1, ...)
#It does that by searching the caracter in the list ASCII at the begining of the code
def tri_ASCII_aux(caractere):
    for k in range(len(ASCII)):
        if ASCII[k] == caractere:
            return k

#Finds the Z-th smallest element of a list
#(liste_ordonnee is the sorted version of liste)
def z_eme_plus_petit(z,liste, liste_ordonnee):
    for k in range(len(liste)):
        if liste[k] == liste_ordonnee[z]:
            return k
    
#Used in the function "Determination_alphabet" 
def tri_ASCII(liste_frequence):
    liste_val_ascii = []
    liste_triee = []
    #gets the ASCII value of every caracter in the list
    for k in range (len(liste_frequence)):
        liste_val_ascii += [tri_ASCII_aux(liste_frequence[k][0])]
    
    liste_ordonnee = liste_val_ascii[:]
    liste_ordonnee.sort()
    #This function sorts every caracter by their ASCII value
    #It searches the smallest value, then the second smallest,...
    for z in range(len(liste_val_ascii)):
        ind = z_eme_plus_petit(z,liste_val_ascii, liste_ordonnee)
        liste_triee.append(liste_frequence[ind])

    liste_triee_finale = [liste_triee[0]]
    #This sorts the previously sorted list by frequency
    #It does this while respecting the ASCII order between caracters with the same frequency
    for k in range(1,len(liste_triee)):
        for z in range(len(liste_triee_finale)):
            if liste_triee[k][1] < liste_triee_finale[z][1]:
                liste_triee_finale.insert(z, liste_triee[k])
                break
            elif z == (len(liste_triee_finale)-1):
                liste_triee_finale.append(liste_triee[k])
    #The programm returns the list sorted by frequency and ASCII order
    return liste_triee_finale
            
         












#A tree is defined as having a label, two sons and a frequence
class Arbre:
    def __init__(self, label, fg, fd, freq):
        self.label = label
        self.fg = fg
        self.fd = fd
        self.freq = freq

#Takes a list of lists of labels and frequences and creates a forest (its trees are leaves) with these labels and frequences
def creer_foret(liste):
        Foret =[]
        for k in range(len(liste)):
            Foret.append(Arbre(liste[k][0],None,None,liste[k][1]))
        return Foret
    
# This programm creates the tree in Step 2
#Thanks to "tri_ASCII" and the way the forest is made, the trees are sorted by frequence
def creer_arbre(Foret):
    while len(Foret)>1:
        #We therefore don't have to search which frequences are the smallest, we just take the first two trees
        t1,t2 = Foret[0], Foret[1]
        del Foret[0]
        del Foret[0]
        arb = Arbre(None,t1,t2, t1.freq + t2.freq)
        
        #We just have to make sure that the new tree is put in the right spot in the forest
        k = 0
        while k<len(Foret) and Foret[k].freq < arb.freq:
            k+=1
        Foret.insert(k,arb)
    return Foret[0]
           
#This function creates the dictionnary we will use to encode every letter of the text
#It will browse the tree and return a dictionnary with every caracter in the text and their binary code
#Gros_cara does not nead to be a specific caracter, it just needs to be represented with more than 8bits
#Gros_cara will be useful later
def Codage(Arbre):
    dico, gros_cara = Codage_aux(Arbre, "")
    return dico, gros_cara
def Codage_aux(Arbre, code):
    dico = {}
    gros_cara = None
    #If the root has a label, it's a leaf, therefore it has no sons and its label and code are added to the dictionnary
    if Arbre.label != None:
        dico[Arbre.label] = code
        if len(code)>8:
            gros_cara = code
    
    #If it has no label, it's not a leaf, and the function will call itself for it's two sons
    #It will also add a 0 or 1 (depending on which son it is) to the code of the caracter
    else:
        dico_aux, gros_cara_aux = Codage_aux(Arbre.fg, code+"0")
        dico = dict(list(zip(dico.keys(), dico.values())) + list(zip(dico_aux.keys(), dico_aux.values())))
        if gros_cara_aux != None:
            gros_cara = gros_cara_aux
        dico_aux, gros_cara_aux = Codage_aux(Arbre.fd, code+"1")
        dico = dict(list(zip(dico.keys(), dico.values())) + list(zip(dico_aux.keys(), dico_aux.values())))
        if gros_cara_aux != None:
            gros_cara = gros_cara_aux
    return dico,gros_cara













#This function takes the path of a .txt files (<name>.txt)
#It will return (<name>nom_fin),   nom_fin being "_comp.bin", "_freq.txt" or "_decomp.txt"
def sortie(emplacement, nom_fin):
    for k in range(len(emplacement)):
        if emplacement[-k-1] == '.':
            return emplacement[:len(emplacement)-k-1] + nom_fin

#This function creates the frequency file
def txt_freq(emplacement, liste):
    #We get the path of the soon to be created _freq file
    emplacement_ecrit = sortie(emplacement, "_freq.txt")
    with open(emplacement_ecrit,'w') as f:
        #We write how many caracters there are
        f.write(str(len(liste)) + "\n")
        #prints every lines of the txt
        for k in range(len(liste)):
            #A line is the caracter in question (liste[k][0]), a space and the frequency (str(liste[k][1])
            txt = liste[k][0] + " " + str(liste[k][1]) + "\n"
            f.write(txt)

#This function is the main one, it will compress the .txt
#On polytech's computers, we can encode ~165Ko of text per second
def compression(emplacement):
    #We get the text
    texte = Recuperer_texte(emplacement)
    #We create the Dictionnary
    liste = Determination_alphabet(emplacement)
    For = creer_foret(liste)
    arb = creer_arbre(For)
    Dico, gros_cara = Codage(arb)
    
    code = ""  
    if gros_cara == None:
        gros_cara = "00000000"
    #We convert every caracter of the text in binary accordind to their value in the dictionnary
    for lettre in texte:
        code += Dico[lettre]
    #If the code's number of bits isn't a multiple of 8, we add the begining of gros_cara to code
    #The idea is that we will add at maximum 7 caracters
    #Due to the ways we create our tree, it's not possible for a caracter's code to contain the entirety code of an other caracter
    #So if we add the beging of gros_cara (which has at least 8bits) we are sure that the programm will not recognise any caracter and will just ignore the end
    #If there are no caracters with more than 7 bits, we will just add zeros at the end of the code, but it may add a random caracter at the end of the decompressed file
    if len(code)%8 != 0:
        code += gros_cara[:(8-(len(code)%8))]
        
    #We create are chain of bytes (it initialy has a space in it)
    code_hexa = bytes([0])
    for k in range(len(code)//8):
        val_deci = 0
        #We cut the code in groups of 8 caracters, calculates the decimal value of this group of 8 bits, and add the caracter corresponding to this value to the chain of bytes
        for z in range(8):
            val_deci += (code[k*8 + z] == '1')* 2**(7-z)
        code_hexa += bytes([val_deci])
    emplacement_ecrit = sortie(emplacement, "_comp.bin")
    
    #We write in the .bin file (we put 'wb' instead of 'w' because it's a .bin file)
    with open(emplacement_ecrit,'wb') as f:
        f.write(code_hexa)
    txt_freq(emplacement, liste)
    return 


#In the files, one caracter is one byte, so the volume of the file (in bytes) in the number of caracters of the file
#Alice.txt is a 149Ko file, the file the programm returns weights 83Ko
#The compression rate of this algorithm is 56%
def taux_compression(emplacement):
    emplacement_encode = sortie(emplacement, "_comp.bin")
    texte = Recuperer_texte(emplacement)
    texte_encode = Recuperer_texte_bin(emplacement_encode)
    return len(texte_encode)/len(texte)


#For alice.txt, the average number of bits is 9394
def Nb_bits_moyen(emplacement_comp, emplacement_freq):
    #We use the _freq file to get the amount of different caracters
    txt = Recuperer_texte(emplacement_freq)
    k = 0
    while txt[k] != '/n':
        k +=1
    nb_cara = int(txt[:k])
    
    #The total number of bits if the amount of caracters (one caracter) times 8
    texte = Recuperer_texte_bin(emplacement_comp)
    a = 8*len(texte)
    return a/nb_cara








#Starting from now, this is for decoding Huffman


#This function takes the _freq file and creates a list of list like what Determination_alphabet returns
#This is because we will be able to use the functions above to create the tree and the dictionnary
def recup_liste(emplacement):
    #For this function, we can't do a "for line in texte:" because of the '/n' caracter that the programm takes into account
    texte = Recuperer_texte(emplacement)
    liste = []
    k=0
    #We remove the first line
    while texte[k] != "\n":
        k += 1
    texte = texte [k+1:]
    
    liste_lignes = []
    while len(texte) > 0:
        #We add the first caracter of the line (we do this because after we will serach for '/n', and is prevents the programm to consider the caracter '/n' and an enter key)
        texte_aux = texte[0]
        k = 1
        #We serach for '/n' which are enter keys
        while texte[k] != "\n":
            k += 1
        texte_aux += texte[1:k]
        liste_lignes.append(texte_aux)
        texte = texte[(k+1):]
        
    #We transform our list of lines in a list of lists
    for ligne in liste_lignes:
        liste.append([ligne[0], int( ligne[2:] )])
        
    return liste


#This function reverses the key and value of every element the dictionnary
def inverse_dico(Dico):
    nouveau_dico = {}
    for cle in Dico:
        nouveau_dico[Dico[cle]] = cle
    return nouveau_dico
    



#This function decompresses the compressed file
def decompression(emplacement_comp, emplacement_freq):
    liste = recup_liste(emplacement_freq)
    For = creer_foret(liste)
    arb = creer_arbre(For)
    Dico, gros_cara = Codage(arb)
    
    texte = Recuperer_texte_bin(emplacement_comp)
    txt_bin = ""
    
    for k in range(len(texte)):
        binaire = bin(texte[k])[2:]
        binaire = "0"* (8- len(binaire)) + binaire
        txt_bin += binaire
    txt_bin = txt_bin[8:]
    
    Dico = inverse_dico(Dico)
    txt = ""
    txt_restant = txt_bin[:]
    txt_aux = ""
    while len(txt_restant) != 0:
        txt_aux += txt_restant[0]
        txt_restant = txt_restant[1:]
        for cle in Dico:
            if cle == txt_aux:
                txt += Dico[cle]
                txt_aux = ""
                break
    
    emplacement_ecrit = sortie(emplacement_comp, "_decomp.txt")
    with open(emplacement_ecrit,'w') as f:
        f.write(txt)

"""      
a = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~\n"      
def b(a):
      print(len(a))
      l = []
      for k in range(len(a)):
          l += a[k]
      return l"""

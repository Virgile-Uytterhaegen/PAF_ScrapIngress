# En-tete

import os
os.chdir("/cal/homes/arenault/workspace/PAF_ScrapIngress")
import csv


# Recuperation des coordonnees d'un portail a partir de son id et de l'id d'un joueur a partir de son pseudo

def portalFinder(ficIn,portalId):
    with open(ficIn,'r') as fic:
        csv_reader = csv.reader(fic,delimiter = ';')
        for line in csv_reader:
            if (int(line[1]) == portalId):
                return line[0].split(',')              # On extrait les coordonnees du portail 
        return []                                      # si le portail n'est pas trouvé on renvoie une liste vide

def playerFinder(ficIn,pseudo):
    with open(ficIn,'r') as fic:
        csv_reader = csv.reader(fic,delimiter = ';')
        for line in csv_reader:
            if line[0] == pseudo:
                return line[1]                         # On extrait l'id du joueur 
        return -1                                      # si le joueur n'est pas trouve on renvoie -1



# Recuperation de la liste des points visités par un joueur

''' La periode est donnee en jour et sera convertie en secondes par la fonction.
    Repetition est le nombre de periode que l'on veut analyser. Par exemple playerVisitedLocations(1,7,4) va creer 
    4 fichiers (un par periode de 7 jours) comportant les coordoonees auquelles le joueur s'est rendu'''


def playerVisitedLocations(joueurId,period,repetition):
    period = period*24*3600                                  #le timestamp fonctionne en seconde
    with open('Actions_triees_par_joueur/'+str(joueurId)+'.csv','r') as to_read:
        csv_reader = csv.reader(to_read,delimiter = ';')
        visitedLocations = {}
        first_line = True
        for line in csv_reader:
            if first_line:                                   #traitement particulier de la premiere ligne
                initial_timestamp = int(line[0])             #on compte les periodes a partir de l'heure de depart
                final_timestamp = initial_timestamp + period 
                first_line = False
            if repetition:
                if (final_timestamp < int(line[0])):         #on atteint la fin de la periode, on sauvegarde et on réinitialise
                    save('j'+str(joueurId)+'_week'+str(repetition)+'.csv',visitedLocations)
                    repetition -= 1
                    final_timestamp += period
                    visitedLocations = {}
        
                currentLocations = [line[4]]                 #traitement generique des portails: 
                if (len(line)==6):                           #on ajoute le portail au dictionnaire s'il n'y est pas
                    currentLocations.append(line[5])         #on compte egalement le nombre de fois qu'un joueur a visiter un portail
                for loc in currentLocations:
                    if not loc in visitedLocations:
                        visitedLocations[loc] = (line[0],1)
                    else:
                        visitedLocations[loc] = (visitedLocations[loc][0],visitedLocations[loc][1]+1)
  

''' Amelioration: on donne maintenant le pseudo du joueur et non plus son id.'''

def playerVisitedLocations2(pseudo,period,repetition):
    playerId = playerFinder('names.csv',pseudo)
    playerVisitedLocations(playerId,period,pseudo)
    

# Sauvegarde

'''Cette fonction sert dans playerVisitedLocations.
   fic est le fichier de sortie et data le dictionnaire des localisations.'''

def save(fic,data):
    with open(fic,'w') as to_write:
        csv_writer = csv.writer(to_write,delimiter=';')
        for x in data:
            coord = portalFinder('portails.csv',int(x))
            csv_writer.writerow([coord[0],coord[1]])

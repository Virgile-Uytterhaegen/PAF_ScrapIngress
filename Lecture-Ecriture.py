# En-tête: bibliothèques à importer, etc

import os
os.chdir("/cal/homes/arenault/workspace/PAF_ScrapIngress")
import csv


# Recopiage d'un bout de fichier, utile pour la generation de fichiers tests

def copy(ficIn,ficOut,nb_lignes_toCopy):
    with open(ficIn, 'r') as to_read:
        with open(ficOut,'w') as to_write:
            csv_writer = csv.writer(to_write, delimiter = ';')
            csv_reader = csv.reader(to_read, delimiter = ';')
            k = nb_lignes_toCopy
            for line in csv_reader:
                csv_writer.writerow(line)
                if (k==1):
                    break
                k -= 1



# Conversion html vers csv


''' La fonction prend en entree le fichier html, le fichier dans lequel ecrire en sortie et le nombre d'informations qu'il faut ecrire
    sur chaque ligne'''

def htmlToCSV(ficIn,ficOut,nb_info_par_ligne):
    with open(ficIn,'r') as to_read:
        with open(ficOut,'a') as to_write:
            txt = to_read.read()
            tab = [x[4:] for x in txt.split('</tr>')[:-1]]    # On supprime les composantes <tr> et </tr>. On recupere un tableau 
                                                              # 2D dont les lignes sont les infos d'un portail. Le [:-1] sert a eliminer la liste vide en fin de tableau
            tab = [y.split('</td>')[:-1] for y in tab]        # Pour chaque portail on sépare les informations délimitées par </td>
            tab = [tab[i][j][4:] for i in range(len(tab)) for j in range(nb_info_par_ligne)] # On supprime l'en-tete <td>
            csv_writer = csv.writer(to_write, delimiter=';')
            for k in range(0,len(tab),nb_info_par_ligne):
                csv_writer.writerow(tab[k:k+nb_info_par_ligne])
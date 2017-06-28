import matplotlib.pyplot as plt
import matplotlib.cm
import csv
import os
os.chdir('C:\Users\oburg\workspace\PAF_ScrapIngress')

 
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize



fig, ax = plt.subplots(figsize=(30,50)) #initialisation des dimensions de la carte

#                       'lat_0'; 'lon_0' latitude et longitude 0 de la carte
#    llcrnrlat latitude du coin en bas à gauche,llcrnrlon longitude du coin en bas à gauche
#    'urcrnrlat' latitude du coin en bas à droite, 'urcrnrlon' longitude du coin en bas à droite
#                                       \/ \/ \/ \/ \/
m = Basemap(resolution='h', # crude, low , intermediate, high or full
            lat_0=49.6, lon_0=-4.36,llcrnrlon=-5.14,llcrnrlat=42.13 , urcrnrlon=8.53, urcrnrlat=51.26)#initialisation de la zone géographique à cartographier.
            


m.drawmapboundary(fill_color = 'aqua') #choix de la couleur des océans, ici bleu clair
m.fillcontinents(color= 'green',lake_color = 'aqua')# choix de la couleur des continents et des lacs
m.drawcoastlines()

#Fonction permettant de séparer en deux les données (latitude et longitude) de la première colonne du csv contenant les coordonnées du portail.
with open('.\portails.csv', 'r') as to_read:
     csv_reader = csv.reader(to_read , delimiter= ';')
     tab = []
     k=100
     for line in csv_reader:
         if not (k):
            break 
         temp = line[0].split(',')
         temp.append(line[1])
         tab.append(temp) 
         k = k-1
         
         #print(temp)
         
n = len(tab)

print(n)

# Cette boucle va permettre de dessiner les 100 premiers portails avec leurs label sur la carte m
for i in range (100):
    lab = str(tab[i][2]) # On prends pour label l'ordre d'apparitions des portails dans le .csv
    tmp_long  =float(tab[i][0])#on va chercher la latitude du portail ( 1 ere colonne du .csv)
    tmp_lat =float(tab[i][1])  #on va chercher la longitude du portail (2eme colonne du .csv)
    x,y = m(tmp_lat, tmp_long) # on retranscrit les infos précédentes en coordonnées de la carte m
    m.plot(y,x , color = 'yellow', marker = 'D', label = 'lab') #Cette ligne permet de dessiner un point pour chaque portail.
  #print(lab)
  



# print(tab)
plt.show()




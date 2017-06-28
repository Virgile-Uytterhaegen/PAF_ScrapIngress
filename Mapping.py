import matplotlib.pyplot as plt
import matplotlib.cm
import csv
import os
os.chdir('C:\Users\oburg\workspace\PAF_ScrapIngress')

 
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize

fig, ax = plt.subplots(figsize=(10,20)) #initialisation des dimensions de la carte

#                       'lat_0'; 'lon_0' latitude et longitude 0 de la carte
#    llcrnrlat latitude du coin en bas à gauche,llcrnrlon longitude du coin en bas à gauche
#    'urcrnrlat' latitude du coin en bas à droite, 'urcrnrlon' longitude du coin en bas à droite
#                                       \/ \/ \/ \/ \/
m = Basemap(resolution='c', # crude, low , intermediate, high or full
            projection='merc',lat_0=49.6, lon_0=-4.36,llcrnrlon=-5.14,llcrnrlat=42.13 , urcrnrlon=8.53, urcrnrlat=51.26)#initialisation de la zone géographique à cartographier.
            


m.drawmapboundary(fill_color = 'aqua') #choix de la couleur des océans, ici bleu clair
m.fillcontinents(color= 'coral',lake_color = 'aqua')# choix de la couleur des continents et des lacs
m.drawcoastlines()

#Fonction permettant de séparer en deux les données (latitude et longitude) de la première colonne du csv contenant les coordonnées du portail.
with open('.\portails.csv', 'r') as to_read:
     csv_reader = csv.reader(to_read , delimiter= ';')
     tab = []
     for line in csv_reader:
         temp = line[0].split(',')
         temp.append(line[1])
         tab.append(temp) 
         
         # print(temp)
         
         
n = len(tab)

print(n)
for i in range (n):
    m.plot (tab[i][0] , tab[i][1] )# Cette ligne permet de dessiner un point pour chaque portail.
        

print(tab)
plt.show()




# En-tete

import os
os.chdir("/cal/homes/arenault/workspace/PAF_ScrapIngress")
import csv
import math as m
import numpy as np
import cv2

''' coordonnees gps de la France: 42, -5, 8, 52
    Si l'on veut creer des zones de 1km² sur la France il faut entrer:
    id_geographique('portails.csv', 42.0, -5.0, 8.0, 52.0, 1)'''


# Dichotomie 2D

# La fonction prend en entree les limites de la zone initiale, la longueur de la zone finale, les coordonnées [x,y] du portail.
# Elle renvoie l'ID de la zone dans laquelle se trouve le portail; -1 si le portail n'est pas dans la zone scrappee.

def dichotomie2D(xmin,xmax,ymin,ymax,precision,portail):
    xp,yp = portail[0],portail[1]
    ID = 0
    xc,yc = (xmax-xmin)/2+xmin,(ymax-ymin)/2+ymin 
    if (xp > xmax or xp < xmin or yp > ymax or yp < ymin):       # Le portail est hors limite, on renvoie donc -1
        return -1
    while (ymax-ymin > precision and xmax-xmin > precision):     # Le portail etant dans les limites, on effectue une dichotomie
        if (xp <= xc and yp >= yc):                              # Portail est dans la zone superieure gauche
            ID = 10*ID+1
            xmax,ymin = xc,yc
            xc,yc = xc-(xmax-xmin)/2,yc+(ymax-ymin)/2
        elif (xp > xc and yp > yc):                              # Portail est dans la zone superieure droite
            ID = 10*ID+2
            xmin,ymin = xc,yc
            xc,yc = xc+(xmax-xmin)/2,yc+(ymax-ymin)/2
        elif (xp < xc and yp < yc):                              # Portail est dans la zone inferieure gauche
            ID = 10*ID+3
            xmax,ymax = xc,yc
            xc,yc = xc-(xmax-xmin)/2,yc-(ymax-ymin)/2
        elif (xp >= xc and yp <= yc):                            # Portail est dans la zone inferieure droite
            ID = 10*ID+4
            xmin,ymax = xc,yc
            xc,yc = xc+(xmax-xmin)/2,yc-(ymax-ymin)/2
    return ID


''' Test dichotomie2D:

xmin,xmax,ymin,ymax = 0,4,0,4
precision = 1
portails = [[i+0.5,j+0.5] for i in range(4) for j in range(4)]
portails.append([0,7])

[dichotomie2D(xmin,xmax,ymin,ymax,precision,p) for p in portails]'''


# Conversion de la latitude, longitude en coordonnées cartésiennes

# La fonction prend en entree latitude et longitude d'un point de référence (l'origine de notre repère) ainsi que la
# latitude et la longitude du point qui nous interesse.
# En sortie on obtient les coordonnees (x,y) de ce point par rapport à l'origine en entrée.
# on utilise la formule "Haversine"

# Rq: la latitude correspond au y et la longitude au x du repere cartesien.

def degreToRad(deg):
    return deg*m.pi/180

def conversion(origin_lat,origin_long,latitude,longitude):
    origin_lat,origin_long = degreToRad(origin_lat),degreToRad(origin_long) 
    latitude, longitude = degreToRad(latitude),degreToRad(longitude) 
    dlat = latitude-origin_lat
    dlong = longitude-origin_long
    a = m.sin(dlat/2)**2 + m.cos(origin_lat)*m.cos(latitude)*m.sin(dlong/2)**2
    c = 2*m.asin(a**(0.5))
    radius = 6371   #rayon de la Terre en km
    if (latitude < origin_lat or longitude < origin_long):  #certaines distances sont negatives par rapport a notre origine
        return -c*radius
    return c*radius


# ajout de l'id geographique dans le fichier ficIn


''' La fonction prend en entree un fichier contenant une liste de portail, les coordonnees GPS du point origine,
    les coordonnees GPS extremes en x et en y, la precision (en km).
    Elle reecrit la liste des portails en adjoignant l'id geographique dans le fichier portails_IdGeo.csv'''


def id_geographique(fichier, o_lat,o_lon,x_lon,y_lat,precision):
    xmin = 0                                                            #xmin et ymin sont l'origine, c'est systematiquement (0,0)
    xmax = conversion(o_lat,o_lon,o_lat,x_lon)                          #on extrait des coordonnees gps les coordonnes cartesiennes
    ymin = 0                                                            #de la zone a cartographier (sert pour la dichotomie)
    ymax = conversion(o_lat,o_lon,y_lat,o_lon)
    with open('portails_IdGeo.csv','w') as fic:
        with open(fichier, 'r') as to_read:
            csv_reader = csv.reader(to_read, delimiter = ';')
            csv_writer = csv.writer(fic, delimiter = ';')
            for line in csv_reader:          
                portal = line[0].split(',')                            # portal[lat,lon]
                x,y = conversion(o_lat,o_lon,o_lat,float(portal[1])),conversion(o_lat,o_lon,float(portal[0]),o_lon)
                portal[0],portal[1] = x,y                              # portal[x,y]
                ID = dichotomie2D(xmin,xmax,ymin,ymax,precision,portal)
                csv_writer.writerow(line + [ID])



# Visualisation des résultats dans la console
    
def visualisation():
    with open('portails_IdGeo.csv', 'r') as to_read:
        csv_r = csv.reader(to_read, delimiter = ';')
        nb_par_zone = {}
        for line in csv_r:
            zone = line[4][:]                       #la precision actuelle donne une zone de 1km² a chaque chiffre tronqué on multiplie par 4 la surface
            if not zone in nb_par_zone:
                nb_par_zone[zone] = (line[0], 1)    #on range dans le dictionnaire une paire de coordonnees representatives
            else:                                   #de la zone et le nombre de portails dans la zone
                nb_par_zone[zone] = (nb_par_zone[zone][0], nb_par_zone[zone][1]+1)
    
    temp = nb_par_zone.values()
    temp.sort(key=lambda zone : zone[1], reverse = True)
    temp[:100]                                      #on peut faire le choix de n'afficher que les 100 zones les plus denses par exemple



# Visualisation sur une carte (ne fonctionne pas pour le moment)

img = cv2.imread('carte_paris.png')
[w,h,p] = np.shape(img)

def visu():
    areas = zones()
    for i in range(w):
        for j in range(h):
            if (img[i,j][0] <= 10 and img[i,j][1] <= 10 and img[i,j][2] <= 10):
                img[i,j] = portalToColour(areas[i,j])
    cv2.imwrite('visu.jpg', img)

def pxInParis():
    nb_px = 0
    for k in range(w):
        for l in range(h):
            if (img[k,l][0] != 132 and img[k,l][1] != 132 and img[k,l][2] != 132):
                nb_px += 1
    return nb_px

nb_px = pxInParis()

km_px = 105.4/nb_px
km_px = m.sqrt(km_px)

arc_de_triomphe = [48.873673, 2.295001]
adt = [137,186]

def gpsTopx(lat,lon):
    dx = conversion(arc_de_triomphe[0],arc_de_triomphe[1],arc_de_triomphe[0],lon)
    dy = conversion(arc_de_triomphe[0],arc_de_triomphe[1],lat,arc_de_triomphe[1])
    px_x,px_y = dx//km_px,dy//km_px
    return adt[0]+px_x,adt[1]-px_y

def poids():
    poids = np.zeros([w,h])
    with open('portails.csv','r') as to_read:
        csv_reader = csv.reader(to_read, delimiter = ';')
        for line in csv_reader:
            lat,lon = float(line[0].split(',')[0]),float(line[0].split(',')[1])
            x,y = gpsTopx(lat,lon)
            if (0<=x<w and 0<=y<h):
                poids[x,y] += 1
    return poids

def zones():
    weight = poids()
    zones = np.ones([w,h])
    for i in range(15):          # l'image fait 500*500px et 1km² = 33px*33px. On cree donc 500/33 = 15 zones par cote
        for j in range(15):
            current_zone = weight[33*i:33*(i+1),33*j:33*(j+1)]
            n,p = np.shape(current_zone)[0],np.shape(current_zone)[1]
            nb_portals = 0
            for k in range(n):
                for l in range(p):
                    nb_portals += current_zone[k,l]
            nb_portals*zones[33*i:33*(i+1),33*j:33*(j+1)]
    return zones

def portalToColour(nb):
    if (nb<5):
        return [0, 0, 50]
    if (nb<10):
        return [0, 0, 100]
    if (nb<15): 
        return [0, 0, 150]
    if (nb<20):
        return [0, 0, 200]
    return [0,0,250]

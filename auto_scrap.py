# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 10:09:43 2017

@author: uytterhaegen

Ce script permet d'automatiser le scrapping grâce à ingrex.
Il lance plusieurs scripts en parallèle 

entrez vos latitudes et longitudes qui definissent la zone que vous voulez scrapper
ces coordonnees se calculent avec les coordonnees decimales * 10^6
    
si vous obtenez l'erreur   self.version = re.findall(r'gen_dashboard_(\w*)\.js', request.text)[0]
                           IndexError: list index out of range
    
mettez a jour le fichier cookies avec les cookies dispo sur Ingress Intel
"""

import os
import ingrex_lib
import comm

os.chdir(os.getcwd())
print(os.getcwd())

coord = ('chemin d acces au fichier de coordonnes en txt')


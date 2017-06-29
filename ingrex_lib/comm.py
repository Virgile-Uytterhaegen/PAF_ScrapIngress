"COMM monitor"
import ingrex
import time
import csv
import os
import sys
os.chdir(os.getcwd())

def main(coordfile):
    "main function"
    
    coordinates = open(coordfile,'r')
    
    minLngE6 = int(coordinates.readline())
    minLatE6 = int(coordinates.readline())
    maxLngE6 = int(coordinates.readline())
    maxLatE6 = int(coordinates.readline())

    field = {
        'minLngE6':minLngE6,
        'minLatE6':minLatE6,
        'maxLngE6':maxLngE6,
        'maxLatE6':maxLatE6,

    }
    
    with open('cookies') as cookies:
        cookies = cookies.read().strip()

    mints = -1

    while True:
        intel = ingrex.Intel(cookies, field)
        result = intel.fetch_msg(mints)
        if result:
            mints = result[0][1] + 1
        with open ('./logs.csv','wb') as csvfile:
           logswriter = csv.writer(csvfile, delimiter=";")
           logswriter.writerow(['Timestamp']+['Player']+['Faction']+['Action']+['Portail1']+['Coordonnees']+['Portail2']+['Coordonnees'])
           origin = time.gmtime()
           while(abs(time.gmtime()[5]-origin[5])<10):
               for item in result[::-1]:
                   msg = ingrex.Message(item)
                   compteur = time.gmtime()
                   print('Time {} Message {} Compteur{}{}{}'.format(msg.time,msg.text,abs(compteur[3]-origin[3]),abs(compteur[4]-origin[4]),abs(compteur[5]-origin[5])))
                   
                   if (msg.action == 'l' or msg.action == 'dl'):
                       logswriter.writerow([msg.timestamp]+[msg.player]+[msg.team]+[msg.action]+[msg.portail1]+[msg.coord1]+[msg.portail2]+[msg.coord2])
                   else :
                       logswriter.writerow([msg.timestamp]+[msg.player]+[]+[msg.team]+[msg.action]+[msg.portail]+[msg.coord])
                                      
           sys.exit("Le csv a atteint le nombre de lignes maximum")
              

if __name__ == '__main__':
    main('coordinates.txt')

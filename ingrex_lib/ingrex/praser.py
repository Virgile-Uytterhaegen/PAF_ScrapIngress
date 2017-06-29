"Ingrex praser deal with message"
from datetime import datetime, timedelta

class Message(object):
    "Message object"
    def __init__(self, raw_msg):
        self.raw = raw_msg
        self.guid = raw_msg[0]
        self.timestamp = raw_msg[1]
        seconds, millis = divmod(raw_msg[1], 1000)
        time = datetime.fromtimestamp(seconds) + timedelta(milliseconds=millis)
        self.time = time.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]
        self.text = raw_msg[2]['plext']['text']
        self.type = raw_msg[2]['plext']['plextType']
        self.team = raw_msg[2]['plext']['team']
        self.coord = (raw_msg[2]['plext']['markup'][2][1]['latE6'],raw_msg[2]['plext']['markup'][2][1]['lngE6'])
        self.player= raw_msg[2]['plext']['markup'][0][1]['plain']
        self.portail = raw_msg[2]['plext']['markup'][2][1]['plain']
        
        self.info = raw_msg[2]['plext']['text'].split(" ")
        
        if (self.info[1] == 'destroyed'):
            if(self.info[3] == 'Resonator'):
                self.action = 'dr'
            elif(self.info[3] == 'Control'):
                self.action = 'dcf'
            else: self.action = 'dl'
            
        if (self.info[1] == 'deployed'):
            self.action = 'dep'
            
        if(self.info[1] == 'apply'):
            self.action = 'app'
            
        if(self.info[1]=='established'):
            self.action = 'est'
        
        if(self.info[1] == 'completed'):
            self.action = 'comp'
        
        if(self.info[1] ==  'upgraded'):
            self.action = 'up'
            
        if(self.info[1] == 'placed'):
            self.action = 'pl'
        
        if(self.info[1] == 'recharged'):
            self.action = 'rch'
            
        if(self.info[1] == 'hacked'):
            self.action = 'hck'
            
        if(self.info[1]=='captured'):
            self.action='ca'
                
        if(self.info[1]=='created'):
            self.action='cr'
            
        if (self.info[1] == 'linked'):
            self.action = 'l'
            
        if (self.action == 'l' or self.action == 'dl'):
            self.portail1 = raw_msg[2]['plext']['markup'][2][1]['plain']
            self.portail2 = raw_msg[2]['plext']['markup'][4][1]['plain']
            self.coord1 = (raw_msg[2]['plext']['markup'][2][1]['latE6'],raw_msg[2]['plext']['markup'][2][1]['lngE6'])
            self.coord2 = (raw_msg[2]['plext']['markup'][4][1]['latE6'],raw_msg[2]['plext']['markup'][4][1]['lngE6'])
        
        
        

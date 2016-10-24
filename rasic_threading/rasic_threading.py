__author__ = 'Rasic Benjamin'
__version__ = 1.0

import threading, math

class Encrypt(threading.Thread):
    """"Diese Klasse soll mehrere Threads dazu verwendne
    eine Nachricht zu verschlüsseln und dan wieder zu entschlüsseln
    """
    msg = ""
    tc = 0
    msg = input("Geben Sie die zu Verschlüsselnde Nachricht ein:")
    tc = int(input("Wieviele Threads sollen verwendet werden? (integer)"))

    def __init__(self,thread_number,msgpart):
        """
        Init mit thread nummer un dem nachrichten part
        :param thread_number:
        :param msgpart:
        :return:
        """
        threading.Thread.__init__(self)
        self.thread_count = thread_number
        self.msgpart = msgpart

    def run(self):
        """
        Soll den ihm zugeweißen Teil der Nachricht Verschlüsseln und Printen
        und die Verschlüsselte Nachricht wird dann wieder Entschlüsselt und in Großbuchstaben printen
        :return:
        """
        checkabc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        cc = {"A":"B", "B":"C", "C":"D", "D":"E", "E":"F", "F":"G", "G":"H", "H":"I", "I":"J", "J":"K", "K":"L", "L":"M", "M":"N", "N":"O", "O":"P", "P":"Q", "Q":"R", "R":"S", "S":"T", "T":"U", "U":"V", "V":"W", "W":"X", "X":"Y", "Y":"Z", "Z":"A"}
        eingang = self.msgpart.upper()
        newmsg = ""
        for x in eingang: #Verschlüsselt die eingegebene Nachricht
            if x in checkabc:
                newmsg = newmsg + cc[x]
            elif x == " ":
                newmsg = newmsg + " "
            else:
                print("Please only use spaces and the abc! Unsuported Symbol!")
        print( "Enrypted Messagepart : " + newmsg )

        dc = {"B":"A", "C":"B", "D":"C", "E":"D", "F":"E", "G":"F", "H":"G", "I":"H", "J":"I", "K":"J", "L":"K", "M":"L", "N":"M", "O":"N", "P":"O", "Q":"P", "R":"Q", "S":"R", "T":"S", "U":"T", "V":"U", "W":"V", "X":"W", "Y":"X", "Z":"Y", "A":"Z"}
        oldmsg = ""
        for x in newmsg: #Entschlüsselt das verschlüsselte wort
            if x in checkabc:
                oldmsg = oldmsg + dc[x]
            elif x == " ":
                oldmsg = oldmsg + " "
            else:
                print("Please only use spaces and the abc! Unsuported Symbol!")
        print( "Decrypted Messagepart : " + oldmsg )



threads = []
start = []
end = []

#Berechnet und fügt die indexe durch die die nachricht geteilt werden soll in zwei listen
for cc in range(0, Encrypt.tc): #
    start.append(int(cc * math.ceil(len(Encrypt.msg) / Encrypt.tc)))
    end.append(int(start[cc] + math.ceil(len(Encrypt.msg) / Encrypt.tc)))

#Startet die vom user input eingegebene anzahl an threads
for i in range(0, Encrypt.tc):
    thread = Encrypt(i,Encrypt.msg[start[i]:end[i]])
    threads += [thread]
    thread.start()


#Wartet auf thread terminisierung
for x in threads:
    x.join()






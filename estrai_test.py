#!/usr/bin/python
# coding: utf-8

import re

# INIZIO - Parametri da inserire PRIMA DI ESEGUIRE LO SCRIPT

path = './dati/LINGUE_STRANIERE_830/A245_TXT/A245_003/'  # imposta il percorso alla cartella corrente
nome_file = 'A245_003_fra_30_TEST' # nome del file
est = 'txt'  # estensione del file
sep = '\t' # separatore nel file risultato cioè in nome_file_RIS.est
classe = nome_file[:4]

# Pattern regex per intercettare Domanda e Risposta
inizio_dom = re.compile('\d+. ')  # 1 o più cifre numeriche seguite da "." e " "
inizio_risp = re.compile('\([A-E]\) ')  # '(A) ', '(B) ', '(C) ', '(D) ', '(E) '
#inizio_risp = re.compile('[a-e]. ')  # 'a. ', 'b. ','c. ','d. ','e. '

scelta_risp = ['(A)','(B)','(C)','(D)','(E)']  # lista delle possibili scelte nelle risposte
# FINE - Parametri da inserire PRIMA DI ESEGUIRE LO SCRIPT


righe = []  # lista delle righe del file per successiva elaborazione
diz_dom = {}  # dizionario con le domande
diz_risp = {} # dizionario con le risposte
risp = {} # dizionario temporaneo per ogni risposta 


f = open(path+nome_file+'.'+est,'r')  # apre il file nome_file in lettura

for riga in f:
  r = riga.strip()  # elimina gli spazi davanti e dietro la riga
  if len(r) > 0:  # elimino le righe vuote
    righe.append(r) # metto la riga nella lista righe

f.close() # chiude il file


# INIZIO - CICLO PER ESTRARRE DOMANDE E RISPOSTE
print
print 'Estrazione domande/risposte dal file '+nome_file+'.'+est

tmp = ''
c = 0  # conta righe
i = 0  # conta domande
flag_dom = False
flag_risp = False

while c < len(righe):
  d = inizio_dom.match(righe[c])  # match dom
  if d <> None:
    flag_dom = True
    flag_risp = False
    i += 1
    key_dom = classe+'_'+'%03d'%(i)
    #print 'key_dom in diz_dom: ',key_dom,
    diz_dom[key_dom] = ''
    righe[c] = righe[c][d.end():].lstrip()

    if risp <> []:
      #print 'key_dom in diz_risp: ',key_dom   
      diz_risp[classe+'_'+'%03d'%(i-1)]= risp  # alimento diz_risp      
      risp = {}

  r = inizio_risp.match(righe[c]) # match risp
  if r <> None:
    flag_dom = False
    flag_risp = True
    key_risp = r.group()[:3]
    
    risp[key_risp] = ''
    righe[c] = righe[c][r.end():].lstrip()     # prendo la prima riga della risposta tagliando la lettera


  if flag_dom == True and flag_risp == False:
    diz_dom[key_dom]+= righe[c] + ' '

  if flag_risp == True and flag_dom == False:
    risp[key_risp] += righe[c] + ' '

  #print c,righe[c]
  c += 1
  if c == len(righe):
    break

print 'Sono state trovate '+str(i)+' domande/risposte.'

# FINE - CICLO PER ESTRARRE DOMANDE E RISPOSTE



# Assegno al diz_risp le risposte dell'ultima domanda del file
if risp <> {}:
  diz_risp[key_dom]=risp  # alimento diz_risp
  risp = {}



etichette = diz_dom.keys() # prendo le chiavi del dizionario domande
#etichette = diz_risp.keys() 
etichette.sort()  # ordino le chiavi in ordine alfabetico
#print etichette

# ciclo per stampare domande e risposte
for e in etichette:
  d = diz_dom[e]
  r = diz_risp[e]
  print e,d
  print e,r
  print


# INIZIO SCRITTURA FILE RISULTATO


print
print 'Scrittura sul file '+nome_file[:-5]+'_RIS'+'.'+est

f = open(path+nome_file[:-5]+'_RIS'+'.'+est,'w')

# Costruzione testata del file risultato
testata = 'classe'+sep+'indice'+sep+'domanda'+sep
for scelta in scelta_risp:
  testata += scelta + sep


f.write(testata+'\n');

for r in etichette:
  c,i = r.split('_') # separa l'etichetta in c=classe, i=indice
  if diz_risp.has_key(r):
    et_risp = diz_risp[r].keys()
    et_risp.sort()
    risp = ''
    for e in et_risp:
      risp += diz_risp[r][e]+sep
    f.write(c+sep+i+sep+diz_dom[r]+sep+risp+'\n');

f.close()

print 'Operazione completata'
# FINE SCRITTURA FILE RISULTATO


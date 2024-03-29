#!/usr/bin/python

import csv
import platform

def csv_read(path,filename,sep):
  f_input = open(path+filename,'rb')
  csvreader = csv.DictReader(f_input,delimiter=sep)
  nomi = csvreader.fieldnames
  diz_curr = []

  for row in csvreader:
    #print row
    diz_curr.append(row)

  nomi.sort()	
  nrec = len(diz_curr)

  return nomi, nrec, diz_curr


def csv_writer(path,filename,sep,fieldnames,rows,flag_header):

  f_output = open(path+filename,'wb')
  csvwriter = csv.DictWriter(f_output, delimiter=sep, fieldnames=fieldnames)

  # Creo l'header con fieldnames e lo scrivo nel file
  if flag_header == True:
    diz_header = {}

    for e in fieldnames:
	  diz_header[e] = e
    csvwriter.writerow(diz_header)

  for row in rows:
    csvwriter.writerow(row)
  
  f_output.close


if __name__ == '__main__':
  

  riga_dom = {}
  riga_risp = {}
  righe_dom = []
  righe_risp = []
  righe_sql = []
  tmp_campi = ''
  
  sistema = platform.system()
  
  # INIZIO - Parametri da inserire PRIMA DI ESEGUIRE LO SCRIPT

  # modificare il path in base al sistema operativo usato
  if sistema == 'Linux':
    path = './dati/LINGUE_STRANIERE_830/A245_TXT/A245_003/'
    fine_riga = '\n'
  if sistema == 'Windows':
    path = 'dati\\LINGUE_STRANIERE_830\\A245_TXT\\A245_003\\'
    fine_riga = '\r\n'

  filename = 'A245_003_fra_30'

  est = '.txt'
  sep = '\t'
  nome_tabella = 'question'
  campi_dom = ['id','languagecode','category','type','question','explanation','freeTextAnswer','severity']
  campi_risp = ['id','question','answer','correct','sort']

  prog_dom = 20  # partenza progressivo 'id' nella tabella 'question'
  prog_risp = 1 # partenza progressivo 'id' nella tabella 'answer'
  
  # FINE - Parametri da inserire PRIMA DI ESEGUIRE LO SCRIPT
  
  nr_file = filename[5:8]
  
  # davanti alla domanda ci metto progressivo file es '(001.001) '


  # Carico il diz delle soluzioni
  f_sol = open(path+filename+'_SOL.txt','r')
  diz_sol = {}
  list_sol = []
  for riga in f_sol:
    valore = riga.replace(fine_riga,'')	# elimina i caratteri fine riga e ritorno di windows
    list_sol.append('('+valore+')')

  f_sol.close
  
  etichette,nrec,diz_curr = csv_read(path,filename+'_RIS'+est,sep)
  
  id_sol = 0
  for diz in diz_curr:
    riga_dom['id'] = prog_dom
    riga_dom['languagecode'] = 'it'
    riga_dom['category'] = filename[:4]
    riga_dom['type'] = 0
    #riga_dom['question'] = '('+ filename[:4]+'.'+str('%03d'%prog_dom)+') '+diz['domanda']
    riga_dom['question'] = diz['domanda']
    riga_dom['explanation'] = 'Spiegazione della risposta esatta'
    riga_dom['freeTextAnswer'] = ''
    riga_dom['severity'] = 1

    diz_sol[prog_dom]=list_sol[id_sol] # riempie il diz delle soluzioni
    #print str(prog_dom),diz_sol[prog_dom]
    id_sol += 1

    i = 0
    for l in ['(A)','(B)','(C)','(D)','(E)']:
      riga_risp['id'] = prog_risp
      riga_risp['question'] =riga_dom['id']
      riga_risp['answer']=diz[l]
      
      if diz_sol[prog_dom] == l:
        riga_risp['correct'] = 1
      else:
        riga_risp['correct'] = 0

      riga_risp['sort']= i
      i += 1
      prog_risp += 1 
      righe_risp.append(riga_risp)
      riga_risp = {}

    
    prog_dom += 1 
    righe_dom.append(riga_dom)
    riga_dom = {}

csv_writer(path,filename+'_question.txt',sep,campi_dom,righe_dom,False)
csv_writer(path,filename+'_answer.txt',sep,campi_risp,righe_risp,False)


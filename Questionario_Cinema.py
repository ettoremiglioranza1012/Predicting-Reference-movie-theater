import pandas as pd 
import matplotlib.pyplot as plt  
import plotly.express as px
import numpy as np

file_csv = "C:/Users/ettor/OneDrive/Documenti/UNITN - TRIENNALE/CORSI/3 anno, 1 SEM/Marketing/LL/LL_3_Session/Input/QUESTIONARIO_Cinema.csv"
ds_cin = pd.read_csv(file_csv, encoding='latin-1')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def genere(valore):
    if valore == 0:
        valore = 'Femmina'
        return valore
    else:
        valore = 'Maschio'
        return valore 

nuova_colonna = ds_cin['M'].apply(genere)
ds_cin.insert(1, 'Genere', nuova_colonna)

def aggiungi(valore):
    
    if valore == '50':
        return '50' + valore 
    else:
        return valore

def calcola_media(valori):
    
    valore_splitted = valori.split(',')
    valore1 = float(valore_splitted[0])
    valore2 = float(valore_splitted[1])
    media = (valore1 + valore2) / 2
    
    return media


ds_cin = ds_cin.drop('F', axis = 1)
for i in ds_cin.columns[1:]:
    
    ds_cin[i] = ds_cin[i].str.replace(r'[^a-zA-Z0-9]', ' ', regex = True)

ds_cin = ds_cin.dropna()
ds_cin['Fascia di eta'] = ds_cin['Fascia di eta'].str.replace(r'[^0-9]', '', regex = True)
ds_cin['Fascia di eta'] = ds_cin['Fascia di eta'].str[:2] + ',' + ds_cin['Fascia di eta'].str[2:]
nuova_colonna = ds_cin['Fascia di eta'].apply(calcola_media)
ds_cin.insert(2, 'Eta media', nuova_colonna)
ds_cin['Eta media'] = ds_cin['Eta media'].astype(str)
ds_cin = ds_cin.drop('Fascia di eta', axis = 1)
ds_cin['Numero dei componenti nucleo familiare'] = ds_cin['Numero dei componenti nucleo familiare'].str.replace('pi', 'Più', regex = True)
ds_cin['Numero medio di film visti al cinema ogni mese'] = ds_cin['Numero medio di film visti al cinema ogni mese'].str.replace('Pi', 'Più', regex = True)
ds_cin['Numero medio di libri letti in un anno'] = ds_cin['Numero medio di libri letti in un anno'].str.replace('Pi', 'Più', regex = True)
ds_cin['Numero medio di concerti visti in un anno'] = ds_cin['Numero medio di concerti visti in un anno'].str.replace('Pi', 'Più', regex = True)
ds_cin['Numero medio di mostre viste in un anno'] = ds_cin['Numero medio di mostre viste in un anno'].str.replace('Pi', 'Più', regex = True)
ds_cin['Numero medio di musei visitati in un anno'] = ds_cin['Numero medio di musei visitati in un anno'].str.replace('Pi', 'Più', regex = True)
ds_cin['Numero medio di rappresentazioni teatrali viste in un anno'] = ds_cin['Numero medio di rappresentazioni teatrali viste in un anno'].str.replace('Pi', 'Più', regex = True)
ds_cin_UCI = ds_cin[ds_cin['Sala cinematografica di riferimento'] == 'UCI']
ds_cin_TS = ds_cin[ds_cin['Sala cinematografica di riferimento'] == 'The Space']
ds_cin_other = ds_cin[ds_cin['Sala cinematografica di riferimento'] == 'Altra']
lista_cinema = [ds_cin_UCI, ds_cin_TS, ds_cin_other]

# algoritmo di ricerca delle stringhe: obiettivo ritornare una lista di lista, con una copia singola 
# delle stringhe di ogni colonna. 

ds_loop = ds_cin.drop(['M', 'Sala cinematografica di riferimento'], axis = 1)

stringa = ' '
lista_stringhe = []

for i, df in enumerate(ds_loop):
    
        lista_stringhe.append([])

        for cella in ds_cin[df]:
        
             if cella != stringa and cella not in lista_stringhe[i]:        
                
                stringa = cella 
                lista_stringhe[i].append(stringa) 

# flusso dati per visualizzare l'influenza delle caratteristiche dei consumatori sulla scelta del cinema 
# grafici statici;
for i, df in enumerate(lista_cinema):

    dm = df.drop(['M','Sala cinematografica di riferimento'], axis = 1)
    
    for n, lista_dentro_lista in enumerate(lista_stringhe[:-1]):
        
        lista_somme = []

        for stringax in lista_dentro_lista:
                
            conteggio = dm[dm.columns[n]].str.count(stringax).sum()
            lista_somme.append(conteggio)
        
        altezze = lista_somme
        categorie = lista_dentro_lista

        colori = [(0.6, 0.3, 0.3), (0.4, 0.6, 0.4), (0.4, 0.4, 0.8), (0.7, 0.5, 0.7)]
        titolo = (df['Sala cinematografica di riferimento'].iloc[0])
        
        plt.figure(figsize=(10,8))
        plt.bar(categorie, altezze, color=colori)
        plt.title('Sala cinematogafica di riferimento: %s' % titolo)
        plt.ylabel('%s' % dm.columns[n])
        plt.xticks(rotation=25)
        plt.tight_layout()
        
        plt.show()

# flusso dati per visualizzare l'influenza delle caratteristiche dei consumatori sulla scelta del cinema 
# grafici interattivi;
for i, df in enumerate(lista_cinema):

    dm = df.drop(['M', 'Sala cinematografica di riferimento'], axis = 1)
    
    for n, lista_dentro_lista in enumerate(lista_stringhe):
        
        lista_somme = []

        for stringax in lista_dentro_lista:
                
            conteggio = dm[dm.columns[n]].str.count(stringax).sum()
            lista_somme.append(conteggio)
        
        altezze = lista_somme
        categorie = lista_dentro_lista
        titolo = (df['Sala cinematografica di riferimento'].iloc[0])

        db = {
      
                "Categoria" : categorie,
      
            dm.columns[n] : altezze
      
        }
        
        data = pd.DataFrame(data = db, index = np.arange(1, len(altezze)+1))
        fig = px.bar(data, x="Categoria", y=dm.columns[n],
                     color = "Categoria", text_auto='.2s',
                     title = 'Sala cinematogafica di riferimento: %s' % titolo, height=700,width=800,
                     color_discrete_sequence=px.colors.qualitative.Set2, template='plotly_white')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, showlegend=False)
        fig.update_layout(yaxis_title = None, xaxis_title = dm.columns[n])
        fig.show()
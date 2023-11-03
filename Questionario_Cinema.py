#!/usr/bin/env python
import pandas as pd 
import matplotlib.pyplot as plt  
import plotly.express as px
import numpy as np

def genere(valore):
    if valore == 0:
        valore = 'Femmina'
        return valore
    else:
        valore = 'Maschio'
        return valore 

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

def pulizia_dati(ds_cin):
        
        ds_cin = ds_cin.drop('F', axis = 1)

        nuova_colonna = ds_cin['M'].apply(genere)
        ds_cin.insert(1, 'Genere', nuova_colonna)

        for i in ds_cin.columns[1:]:
            ds_cin[i] = ds_cin[i].str.replace(r'[^a-zA-Z0-9]', ' ', regex = True)
        
        ds_cin = ds_cin.dropna()
        ds_cin['Fascia di eta'] = ds_cin['Fascia di eta'].str.replace(r'[^0-9]', '', regex = True)
        ds_cin['Fascia di eta'] = ds_cin['Fascia di eta'].apply(aggiungi)
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

        return ds_cin

def categorizzazione(ds_cin):
        
        ds_cin_UCI = ds_cin[ds_cin['Sala cinematografica di riferimento'] == 'UCI']
        
        ds_cin_TS = ds_cin[ds_cin['Sala cinematografica di riferimento'] == 'The Space']
        
        ds_cin_other = ds_cin[ds_cin['Sala cinematografica di riferimento'] == 'Altra']
        
        lista_cinema = [ds_cin_UCI, ds_cin_TS, ds_cin_other]

        return lista_cinema

def lista_stringa(ds_cin):
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
    
    return lista_stringhe, ds_loop

def somma(lista_cinema, lista_stringhe, ds_loop):
    matrice_somme = []

    for i, df in enumerate(lista_cinema):
        matrice_somme.append([])

        for n, lista_dentro_lista in enumerate(lista_stringhe):
            matrice_somme[i].append([])

            for stringax in lista_dentro_lista:

                conteggio = df[ds_loop.columns[n]].str.count(stringax).sum()
                matrice_somme[i][n].append(conteggio)
    return matrice_somme

def name_titoli(lista_cinema):
    titoli = []
    
    for titolo in lista_cinema:
        titoli.append(titolo['Sala cinematografica di riferimento'].iloc[0])

    return titoli

def label(dm):
    lista_label = []
    
    for df_label in dm.columns:
        lista_label.append(df_label)
    
    return lista_label

def grafici_matplotlib_subplot(matrice_somme, lista_stringhe, lista_label, titoli):
    k= 0
    
    while k < len(matrice_somme[0]):
        z = 0
        fig, axs = plt.subplots(1, 3, figsize=(15,8))
        
        while z < len(matrice_somme):
            altezze = matrice_somme[z][k]
            categorie = lista_stringhe[k]
            colori = [(0.6, 0.3, 0.3), (0.4, 0.6, 0.4), (0.4, 0.4, 0.8), (0.7, 0.5, 0.7)]

            axs[z].bar(categorie, altezze, color = colori)
            axs[z].set_title('Sala: %s' % titoli[z])
            #axs[0].set_ylabel(lista_label[k])
            axs[z].tick_params(axis='x', labelrotation=75)

            z += 1

        k += 1
        plt.tight_layout()
        fig.suptitle(lista_label[k-1], fontsize=12, y = 1.05)
        plt.show()

def grafici_px_express(lista_stringhe, lista_cinema):
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

def grafici_matplotlib(lista_stringhe, lista_cinema):
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

def main():

    file_csv = "C:/Users/ettor/OneDrive/Documenti/UNITN - TRIENNALE/CORSI/3 anno, 1 SEM/Marketing/LL/LL_3_Session/Input/QUESTIONARIO_Cinema.csv"
    ds_cin = pd.read_csv(file_csv, encoding='latin-1')
    
    ds_cin = pulizia_dati(ds_cin)
    
    lista_cinema = categorizzazione(ds_cin)
    
    lista_stringhe, ds_loop = lista_stringa(ds_cin)

    matrice_somme = somma(lista_cinema, lista_stringhe, ds_loop)

    titoli = name_titoli(lista_cinema)

    lista_label = label(ds_loop)

    grafici_matplotlib_subplot(matrice_somme, lista_stringhe, lista_label, titoli)  # griglia sunplot confronto
    #grafici_px_express(lista_stringhe, lista_cinema)   # grafici singoli
    #grafici_matplotlib(lista_stringhe, lista_cinema)   # grafici interattivi px.express

if __name__ is '__main__':
    main()
    
    







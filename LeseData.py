import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd

#Valg av tidsvindu for plotting av data
vintertid = False

# import og laging av arrays
# Henter inn fila som en dataframe i pandas
# data = pd.read_csv('http://sensor.marin.ntnu.no/logs/noa.txt', delimiter=',')
data = pd.read_csv('noa.txt', delimiter=',')

epochTime = data["1715000796"].values # NB: Disse verdiene samsvarer med første kolonne i datafilen, du må endre til det som gjelder din fil
volt = data["4.16"].values
temp = data['11.2'].values
runTime = data['103306'].values/1000 # Gjør ms om til s

# Funksjon for å lage datetime-objeter fra epochTime
def epochToDatetime(x):
    liste=[]
    for i in range(len(x)):
        if vintertid:
            t=dt.datetime.utcfromtimestamp(x[i]) + dt.timedelta(hours=1)
        else:
            t=dt.datetime.utcfromtimestamp(x[i]) + dt.timedelta(hours=2)
            
        liste.append(t)
        
    return liste

timelist=epochToDatetime(epochTime)

plt.figure(1,figsize=(11,8)) # Angir figurnummer og figur størrelse (cm)
plt.plot(timelist,volt,'b.') # Plotter spenning som funk. av tid med blå 
plt.ylabel('Spenning[V]') # Angir tekst på den vertikale aksen
plt.xlabel('Tid') # Angir tekst på den horisontale aksen
plt.title('Spenning (1S3P 2500mah liPo)') # Angir figuroverskrift
plt.ylim(3.2,4.2) # Angir skalaen på den vertikale aksen
plt.grid() # Angir at det skal tegnes opp et rutenett
plt.show() # Viser plottet

plt.figure(2,figsize=(11,8))
plt.plot(timelist,temp,'b.')
plt.xlabel('Tid')
plt.ylabel('Temperatur')
plt.title('Temperaturmålinger')
plt.grid()
plt.show()

plt.figure(3,figsize=(11,8))
plt.plot(timelist,runTime,'b.')
plt.ylim(0,200)
plt.title('runTime')
plt.xlabel('Sendingsnr.')
plt.ylabel('RunTime for programmet [s]')
plt.grid()
plt.show()

# Regning av gjennomsnittlig intervall
interval=np.zeros(len(epochTime)-1) # Lager en array med nuller
for i in range(len(epochTime)-1):
    interval[i] = int((epochTime[i+1]-epochTime[i]))

interval_mean = np.mean(interval[0:len(interval)-1])
print('Gjennomsnittlig intervall mellom sendinger: ', interval_mean)

# Finner antall ganger intervall mellom sending er over 7 minutter (420 sek)
count = 1
for i in range (len(interval)):
    if interval[i] > 420: # 420 sek = 7 minutter pluss litt til = feilsending
        count+=1

print('Antall feilsendinger: ',count)

# Finner gjennomsnittstemperatur
temp_mean = np.mean(temp)
print('Gjennomsnittstemperatur: ',temp_mean)

# Finner høyeste og laveste temperatur
temp_max = np.max(temp)
temp_min = np.min(temp)
print('Høyeste temperatur: ',temp_max)
print('Laveste temperatur: ',temp_min)
print()

# Bruker pandas for å se på mellom annet standardavvik, gjennomsnitt og kvartiler
df = pd.DataFrame(data)
print(df.describe())
print()

# Bruker pandas for å se nærmere på termperturdata
print("Gjennomsnittstemperatur: ", df['24.2'].mean())
print("Makstemperatur: ", df['24.2'].max()) # Finner maksimumstemperatur
print("Minimumstemperatur: ", df['24.2'].min()) # Finner minimumstemperatur
print()
print("Antall ganger ullike temperaturer forekommer: ")
print(df['24.2'].value_counts()) # Teller antall ganger hver verdi forekommer
print()
print("Temperaturen som forekommer oftest: ", df['24.2'].value_counts().idxmax()) # Finner den mest forekommende verdien
print("Standardavvik: ", df['24.2'].std()) # Finner standardavvik
print("Median: ", df['24.2'].median()) # Finner median, altså midtverdien

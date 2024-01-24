import csv
import itertools
import hashlib
import time
import statistics
import pandas as pd



def yuval(legitMessage, ilegitMessage, h, m):
    dictTextHashes = {}
    for actualCombo in itertools.product(["0", "1"], repeat=m):
        actualCombo = bin(int(''.join(map(str, actualCombo)), 2))[2:].ljust(30, '0')
        combinedText = ""
        for index, value in enumerate(actualCombo):
            combinedText = f'{combinedText} {legitMessage[index][int(value)]}'

        dictTextHashes[hashlib.md5(combinedText.encode('utf-8')).hexdigest()[:h]] = actualCombo
        
    for actualCombo in itertools.product(["0", "1"], repeat=m):
        actualCombo = bin(int(''.join(map(str, actualCombo)), 2))[2:].ljust(30, '0')
        combinedText = ""
        for index, value in enumerate(actualCombo):
            combinedText = f'{combinedText} {ilegitMessage[index][int(value)]}'

        ilegitHash =  hashlib.md5(combinedText.encode('utf-8')).hexdigest()[:h]

        if ilegitHash in dictTextHashes: 
            legitCombo = dictTextHashes[ilegitHash] 
            return [str(legitCombo), str(actualCombo), str(ilegitHash)]
    
    return None


def messageLoad(file):
    with open(file, encoding='UTF-8') as f:
        reader = csv.reader(f)
        message = list(tuple(line) for line in reader)[1:]
    return message


def mainYuval(minHash, maxHash):
    legitMessage = messageLoad("Mensajes/mensajeLicito.csv")
    
    for hashValue in range(minHash,maxHash):
        times = []
        messageBits = hashValue*2
        colisions = 0
        df_print = pd.DataFrame()

        while colisions < 15:
            ilegitMessage = messageLoad('Mensajes/mensajeIlicito ' + str(colisions) + '.csv')
            start_time = time.time()
            result = yuval(legitMessage, ilegitMessage, hashValue, messageBits)
            total_time = time.time() - start_time
            if result != None:    
                times.append(total_time) 
                colisions += 1

                new_row = {
                    "Bits Mensaje": messageBits,
                    "Comb Binaria Lícita": result[0],
                    "Comb Binaria Ilícita": result[1],
                    "Hash": result[2],
                    "Tiempo (s)": round(total_time, 4)
                    }
                
                df_print = pd.concat([df_print, pd.DataFrame([new_row])], ignore_index=True)
                messageBits = hashValue*2

            else:
                messageBits += 1

        df_print.to_csv("Resultados Yuval/Hash " + str(hashValue) + " " + str(round(statistics.mean(times),4)) + ".csv", index=False)



 
legitMessage = messageLoad("Mensajes/mensajeLicito.csv")
ilegitMessage = messageLoad('Mensajes/mensajeIlicito 7.csv')
print("12 bits")
yuval(legitMessage, ilegitMessage, 6, 12)
print("\n")
print("14 bits")
yuval(legitMessage, ilegitMessage, 7, 14)
print("\n")
print("16 bits")
yuval(legitMessage, ilegitMessage, 8, 16)
print("\n")
print("18 bits")
yuval(legitMessage, ilegitMessage, 9, 18)
print("\n")
print("20 bits")
print(yuval(legitMessage, ilegitMessage, 10, 20))
print("\n")
print("22 bits")
yuval(legitMessage, ilegitMessage, 11, 22)
print("\n")
print("24 bits")
yuval(legitMessage, ilegitMessage, 12, 24)
print("\n")
















# -*- coding: cp1252 -*-
#Porpouse: This code will test ".docx" files,
# using LibreOffice 4.3.4.1 Writer
#Developed by: Denis Araujo da Silva
#Date: 18th November 2014
#Based on Charlie Miller Fuzzer - "Babysitting an army of mokeys"
##############################################################
#                     Configuration                          #

#List of files to use as initial seed
file_list=[
    "Files\EXECUÇÃO TRABALHISTA.docx",
    "Files\codigo_defesa_consumidor.docx",
    "Files\ctb_l9503.docx",
    "Files\CF1988.docx"
    ]

#App that is going to be tested - Libre Office
app = "C:\Program Files (x86)\LibreOffice 4\program\soffice.exe"

fuzz_output = "Files\Fuzz.docx"
FuzzFactor = 250
num_tests = 10000

##############################################################
import random
import math
import string
import subprocess
import time
import os
import signal

for i in range(num_tests):
    seq = []    
    seq.append("App: " + str(app) + "\n")

    file_choice = random.choice(file_list)
    seq.append("File: " + str(file_choice) + "\n")
    
    buf = bytearray(open(file_choice, 'rb').read())

    #Start Charlie Miller code
    numwrites = random.randrange(math.ceil((float(len(buf))/FuzzFactor)))+1

    seq.append("Number of writes: " + str(numwrites) + "\n")

    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        seq.append("Value before: " + str(buf[rn]) + "\n")
        buf[rn] = rbyte
        seq.append("Value after: " + str(buf[rn]) + "\n")

    #End Charlie Miller code

    #wait a little bit to kill the process
    time.sleep(2)
    open(fuzz_output, 'wb').write(buf)

    process = subprocess.Popen([app, fuzz_output],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processPID = process.pid
    
    print ('Waiting!')
    time.sleep(5)
    print ("Finished wait!")

    print ("Process ID:" + str(processPID))

    crashed = process.poll()
    if crashed:
        print ('Crashed! - Logging ...')
        log_file = open("logs\FuzzerTest" + str(i) + ".log",'w')
        log_file.writelines(seq)
        log_file.close()

    #forcing kill - not nice :(   
    subprocess.Popen("taskkill /F /T /PID %i"%process.pid , shell=True)

    #These two didn't work
    #os.kill(processPID,signal.SIGTERM)    
    #process.kill()

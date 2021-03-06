# -*- coding: utf-8 -*-
"""SIP Project Phon read label generate.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tsyeoVU3uH5Ji_yK_cy2aS_io0taTWoP
"""

import numpy as np
line = {}
start = {}
end = {}
phoneme = {}
store_len = {}
unvoiced = ['p','t','k','f','th','s', 'sh', 'pcl','tcl','kcl','pau','epi','h#']

file_no = 462
for j in [346, 347, 348, 349, 351, 352, 353]:#range(168):
    total_line = 0
    counter = 0
    for i in range(10):
        filename = 'newtrainphone/' + str(j+1) +'/' + str(i+1) + '.PHN'
        with open(filename) as file:
            line[i] = file.readlines()
            counter = counter + len(line[i])
            total_line = total_line + int(line[i][-1].split()[1])
            store_len[i] = len(line[i])
            if i == 0:
                st_conv = 0
                st_range = 0
                en_range = store_len[i]
            else:
                st_conv = end[en_range] + st_conv
                st_range = st_range + store_len[i-1] + 1
                en_range = en_range + store_len[i] + 1
            for (k,zk) in zip(line[i],range(st_range,en_range)):
                k = k.split()
                start[zk] = int(k[0]) + st_conv
                end[zk] = int(k[1]) + st_conv
                phoneme[zk] = k[2]
            start[en_range] = end[en_range-1]
            if i != 9:
                end[en_range] = end[en_range-1] + 4000
            phoneme[en_range] = 'h#'
    total_line = total_line + 36000

    n = int(np.ceil((total_line)/160))
    label = {}
    for i in range(n):
        if i == 0:
            st_loop = 0
        else:
            st_loop = i*160
        en_loop = st_loop + 400

        for k in range(en_range + 1):
            if st_loop < end[k] and en_loop < end[k]:  
                if phoneme[k] not in unvoiced:#unvoiced define karo
                    label[i] = 1
                else:
                    label[i] = -1
                break    
            if k != en_range:
                if st_loop < end[k] and en_loop > end[k]:
                    if ((phoneme[k] not in unvoiced) or (phoneme[k+1] not in unvoiced)):#unvoiced define karo
                        label[i] = 1
                    else:
                        label[i] = -1
                    break
                    
    #check MFCC length
    from python_speech_features import mfcc
    import scipy.io.wavfile as wav

    
    filename = "newtrainwithnoisep12\s" + str(j+1) + ".wav"
    (Fs,data) = wav.read(filename)
    Obs = mfcc(data,samplerate=Fs,winlen=0.025,winstep=0.01,numcep=13)
  
    if len(Obs) > len(label):
        append_n = len(Obs) - len(label)
        for i in range(append_n):
            label[n+i] = 0








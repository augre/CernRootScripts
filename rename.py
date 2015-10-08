#!/usr/bin/env python
import os
path = './'
for filename in os.listdir(path):
    try:
        prefix1, prefix2, num = filename[:-5].split('_')
        num = num.zfill(3)
        new_filename = prefix1+"_"+prefix2+ "_" + num + ".root"
        if prefix1=="Dosimetry" and prefix2=="Detector":
            print new_filename
            os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
        else:
            pass
    except:
        pass

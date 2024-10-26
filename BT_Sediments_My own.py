# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:57:15 2020

@author: Sabbir
"""

import pygimli as pg
import glob
import numpy as np
from pygimli.physics import SIPSpectrum 

with open('results.txt','w') as fid:
    fid.write('Filename,rhoCC,mCC,tauCC,cCC,mDD,tauDD\n')
    fmt=',{:.1f},{:.3f},{:.1e},{:.2f},{:.3f},{:.1e}\n'
  
  
#   for filename in glob.glob('*.txt'):
    for filename in glob.glob('D:/Thesis/Lab Measurement/Long measurement/Altered/Sediment/*.csv'):
        k=0.006138
        f,phi,amp=np.genfromtxt(filename, usecols=(2,4,5), unpack=True, skip_header=29, delimiter=',')
        
        SIP=SIPSpectrum(f=f, phi=-phi, amp=amp*k, onlydown=True, unify=True, basename=filename[:-4])
        SIP.cutF(0.01, down=True)
        SIP.removeEpsilonEffect()
#       SIP.phi = np.abs(SIP.phi)
#       schreibt die Rohdaten raus nach remove Epsilon
        re, im = SIP.realimag(cond=True)
        A=np.column_stack((SIP.f, SIP.amp, SIP.phi*1000, re, im))
        np.savetxt(SIP.basename+".out", A, header="f [Hz]\trho [Ohm*m]\tphi [mrad]\tSigmaReal [S/m]\tSigmaImag [S/m]")

        #SIP.showDataKK()
        #SIP.fitCCEM()
        SIP.fitDebyeModel()
        SIP.fitColeCole(taupar=(1e-4, 1e-6, 1))
        #SIP.fit2CCPhi()
#       SIP.fitColeCole(mstart=0.1, taupar=(1e-4, 1e-5, 1e4))
        mtot = sum(SIP.mDD) # total chageability
        lmtau = np.exp( np.sum( np.log(SIP.tau) * SIP.mDD )/mtot ) # log-mean tau

#       Export DD Data 
        tmDD = np.column_stack((SIP.tau, SIP.mDD))
        np.savetxt(SIP.basename+"_DD.out", tmDD, header="DDtau\tmDD")  
        
#       Export CC Data 
        # tmCC = np.column_stack((SIP.f, SIP.ampCC, SIP.phiCC))
        # np.savetxt(SIP.basename+"_CC.out",tmCC , header="f\tCCampl\tphiCC")  

    
        fig,ex=SIP.showAll()
        ex[0].set_title(filename[:-4])
        SIP.saveFigures()
    
        fid.write(filename[:-4]+fmt.format(*SIP.mCC,mtot,lmtau))


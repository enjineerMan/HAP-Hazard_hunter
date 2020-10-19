# -*- coding: utf-8 -*-
"""
Copyrights / Droit d'auteurs
(C) 2018 The HDF Group 
(C) 2020 Government of Canada

----
This example code was written for the Covid19 Space Apps Challenge  
of May 30-31, 2020

It illustrates how to access a MOPITT MOP02J version 8 
HDF-EOS5 Grid file in Python. and convert it into a csv file.

The HDF file must be in your current working directory.

----
Ce code d'exemple a été écris pour le Space Apps Challenge Covid19 
du 30-31 Mai 2020.

Il montre comment accéder à un fichier MOPITT MOP02J version 8
HDF_EOS5 en python et le convertir en fichier csv.
Le fichier HDF doit être dans le même dossier que le code .py . 

----
Tested under / Testé sous: Python 3.7
Last updated / Modifié le: 2020-05-13 
By / Par : Camille Roy, Canadian Space Agency / Agence Spatiale Canadienne 
"""

import os
import re
import h5py
import numpy as np

#Nom du fichier HDF à lire / Name of the HDF file to read
FILE_NAME = 'MOP02J-20200322-L2V18.0.3.he5'

with h5py.File(FILE_NAME, mode='r') as f:
    #Lecture des données hdf / reading hdf data
    #Pour voir toutes les variables dipsonible / to see all available data : 
    # print(f['/HDFEOS/SWATHS/MOP02/Data Fields'].keys())
    group = f['HDFEOS/SWATHS/MOP02/Data Fields'] #location of data 
    
    #RetrievedCOTotalColumn
    dsname1 = 'RetrievedCOTotalColumn'   
    data1 = group[dsname1][:].T 
    units1 = group[dsname1].attrs['units'].decode() #Units
    fillvalue1 = group[dsname1].attrs['_FillValue'] 
    data1[data1 == fillvalue1] = np.nan 
    
    #RetrievedCOMixingRatioProfile
    dsname2 = 'RetrievedCOSurfaceMixingRatio'  
    data2 = group[dsname2][:].T
    units2 = group[dsname2].attrs['units'].decode() #Units
    fillvalue2 = group[dsname2].attrs['_FillValue'] 
    data2[data2 == fillvalue2] = np.nan 
    
    #RetrievedCOSurfaceMixingRatio
    dsname3 = 'RetrievedCOMixingRatioProfile'      
    data3 = group[dsname3][:].T[0] 
    units3 = group[dsname3].attrs['units'].decode() #Units
    fillvalue3 = group[dsname3].attrs['_FillValue'] 
    data3[data3 == fillvalue3] = np.nan 
    
    #RetrievedCOSurfaceMixingRatio
    dsname4 = 'RetrievedSurfaceTemperature'      
    data4 = group[dsname4][:].T 
    units4 = group[dsname4].attrs['units'].decode() #Units
    fillvalue4 = group[dsname4].attrs['_FillValue'] 
    data4[data4 == fillvalue4] = np.nan 
    
    # Info de géolocalisation / Geolocalisation information at:
    # '/HDFEOS INFORMATION/StructMetadata.0' 
    lat = f['HDFEOS/SWATHS/MOP02/Geolocation Fields/Latitude'][()]
    long = f['HDFEOS/SWATHS/MOP02/Geolocation Fields/Longitude'][()]

    #FORMAT DES DONNÉES POUR METTRE EN CSV.
    #DATA FORMAT FOR CSV TABLE
    n = 14 #Nombre de colonnes / Number of columns
    Tab = np.zeros((lat.size,n)) #Tableau vide à remplir / Empty table to fill

    # Remplissage avec les données / Filling table with data
    Tab[:,0]=lat    #Latitude
    Tab[:,1]=long   #Longitude
    Tab[:,2]=data1[0] #COTotalColumn
    Tab[:,3]=data2[0] #RetrievedCOSurfaceMixingRatio
    for i in range(data3.shape[0]): #Loop on RetrievedCOMixingRatioProfile
        Tab[:,4+i]=data3[i]
        #End loop on RetrievedCOMixingRatioProfile
    Tab[:,13]=data4[0] #RetrievedSurfaceTemperature

    #Sauvegarde du fichier en type .csv / Save csv file 
    np.savetxt(FILE_NAME.replace('.he5','.csv'), Tab,delimiter=',',
               header='Latitude, Longitude, COTotalColumn,COMixingRatio surface,COMixingRatio 900hPa,COMixingRatio 800hPa,COMixingRatio 700hPa,COMixingRatio 600hPa, COMixingRatio 500hPa,COMixingRatio 400hPa,COMixingRatio 300hPa,COMixingRatio 200hPa,COMixingRatio 100hPa,RetrievedSurfaceTemperature ')

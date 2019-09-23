# This script reads in a Voyager import log and extracts IDs for duplicate bibs, as well as IDs for bibs, MFHDs, and items added. It then exports this information to a spreadsheet and cleans up the temporary files created as part of the script's functioning.
# I wrote this to quickly find all duplicates within an import log files since those need to be addressed after the import. I added the functionality to grab the other IDs because it would be useful if something went terribly awry and I needed to delete them all. The spreadsheet is just because I got caught up in scope creep - prettyLog.py will do the same thing but output to a text file.
# Modules required: re, openpyxl, os

def findDuplicates():
  duplicates = []
  fh = open(fname)
  fout = open("temp.txt", "w")
  # read through file, extract the line after the line starting with BibID & rank and write to temp file
  with fh as f:
    lines = f.readlines()
    n_lines = len(lines)
    for i, line in enumerate (lines) :
      line = line.rstrip()
      if line.startswith("	BibID & rank") and \
          n_lines > i + 2 and lines[i + 2].startswith("") :
          duplicates.append(lines[i+1])
    fout.write(str(duplicates))

def cleanFile():
    # read through temp file created by extractDuplicates(), extract only the ID numbers to temp file
    fh = open("temp.txt", 'r')
    fout = open("duplicates.txt", 'w')
    data = fh.read()
    ids = re.findall(r'[0-9]+\s', data)
    fout.write("Duplicate bibs:" + "\n")
    for id in ids:
        fout.write(id + '\n')

def extractIDs():
    # read through log file, extract IDs for added records to temp files
    fh = open(fname)
    fout1 = open("bibs.txt", "w")
    fout1.write("Bibs added\n")
    fout2 = open("mfhds.txt", "w")
    fout2.write("MDHDs added\n")
    fout3 = open("items.txt", "w")
    fout3.write("Items added\n")
    for line in fh :
        line = line.rstrip()
        if line.startswith("	Adding Bib") :
            line = re.findall(r'[0-9]+',line)
            for id in line:
              fout1.write(id + "\n")
        elif line.startswith("MFHD_ID ") :
            line = re.findall(r'[0-9]+',line)
            for id in line:
              fout2.write(id + "\n")
        elif line.startswith("ITEM_ID ") :
            line = re.findall(r'[0-9]+',line)
            for id in line:
                fout3.write(id + "\n")
        else :
            continue

def createSpreadsheet() :
    import openpyxl
    # create spreadsheet
    wb=openpyxl.Workbook()
    # open and name worksheets
    ws1=wb.active
    ws1.title = "Duplicate Bibs"
    ws2=wb.create_sheet("IDs added")
    # write the duplicate Bib IDs to the first sheet
    duplicates = open("duplicates.txt", "r")
    ids0 = duplicates.readlines()
    for r in range(0,len(ids0)):
        ws1.cell(row=r+1,column=1).value=ids0[r]
    # write the IDs for added bibs to the first column of the second sheet
    bibs = open("bibs.txt", "r")
    ids1 = bibs.readlines()
    for r in range(0,len(ids1)):
        ws2.cell(row=r+1,column=1).value=ids1[r]
    # write the IDs for added MFHDs to the second column of the second sheet
    mfhds = open("mfhds.txt", "r")
    ids2 = mfhds.readlines()
    for r in range(0,len(ids2)):
        ws2.cell(row=r+1,column=2).value=ids2[r]
    # write the IDs for added items to the third column of the second sheet
    items = open("items.txt", "r")
    ids3 = items.readlines()
    for r in range(0,len(ids3)):
        ws2.cell(row=r+1,column=3).value=ids3[r]
    # save spreadsheet with the name input by the user
    wb.save(outname + ".xlsx")

def deleteTempFiles() :
    # deletes the temp files created since this info is now in the spreadsheet
    import os
    os.remove("temp.txt")
    os.remove("duplicates.txt")
    os.remove("bibs.txt")
    os.remove("MFHDs.txt")
    os.remove("items.txt")

import re # doing this here since multiple functions need it
fname = input("Enter input file name (including extension): ")
outname = input("Enter output file name (without extension): ")
findDuplicates()
cleanFile()
extractIDs()
createSpreadsheet()
deleteTempFiles()

# ssLog
This script reads in a Voyager import log and extracts IDs for duplicate bibs, as well as IDs for bibs, MFHDs, and items added. It then exports this information to a spreadsheet and cleans up the temporary files created as part of the script's functioning.

I wrote this to quickly find all duplicates within an import log files since those need to be addressed after the import. I added the functionality to grab the other IDs because it would be useful if something went terribly awry and I needed to delete them all. The spreadsheet is just because I got caught up in scope creep - prettyLog.py will do the same thing but output to a text file.

Modules required: re, openpyxl, os

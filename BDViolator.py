#BlackDuck-Violator: Process BlackDuck component scan to mark components as "In Violation" or "Not In Violation"
#                   based upon designated list of license rules. This tool is intended for use as prep for import
#                   into DetectDojo for license risk management.

# Process: unzip BlackDuck component data, stream components.csv to new file replacing violation field based upon
#          matches within the RiskyLicenseList.csv file.

# RiskyLicenseList TIP: use the UID and License name from known BlackDuck scan results for exact match.
#                       If unknown, use a UID of '0' and text to match for a best guess approach.

import zipfile
import tempfile
import sys
import os
from tqdm import tqdm

def unpack( file,tmpdir ):
    print("Processing %s"%file)
    with zipfile.ZipFile(file) as zf:
        for member in tqdm(zf.infolist(), desc=' Extracting '):
            try:
                if member.filename[-1]  == "/":
                    continue
                member.filename  = os.path.basename(member.filename)
                zf.extract(member, tmpdir)
            except zipfile.error as e:
                print("Unzip error.")
                pass

def repack( file,tmpdir ):
    print(' Repackaging archive...')
    zipf = zipfile.ZipFile(file, 'w', zipfile.ZIP_DEFLATED)
    for folderName, subfolders, filenames in os.walk(tmpdir):
       for filename in filenames:
           #create complete filepath of file in directory
           filePath = os.path.join(folderName, filename)
           # Add file to zip
           zipf.write(filePath, filename)
    zipf.close()
    print(' Done. BlackDuck archive ready for DetectDojo import.')

def read_bad_list():
    print("Reading list of bad licenses...")
    bad_list = open("RiskyLicenseList.csv", "r")
    bad_items = []
    for line in bad_list:
        if "License ids, License" not in line:
            pos = 0
            for item in line.split(","):
                if item != "0":
                    bad_items.append(item.strip())
                    print("\tBad license: %s"%item.strip())
    return bad_items

def check_for_match( line,bad_list ):
    for bad in bad_list:
        if bad in line:
            #if "Sun" in line:
            #    print("Found Affero: %s"%line)
            return True
    return False

def process( directory,bad_list ):
    count = 0
    found = False
    for entry in os.scandir(directory):
        if "components" in entry.path:
            found = True
            print(" Found Component CSV.")
            file = open(entry.path, "r")
            fileout = open(entry.path+"2", "w")
            for line in file:
                if check_for_match( line,bad_list ):
                    #we have a bad license
                    fileout.write(line.replace("Not In Violation","In Violation"))
                    count += 1
                else:
                    #keep original but reset the violation line if needed
                    if "Not In Violation" not in line:
                        fileout.write(line.replace("In Violation","Not In Violation"))
                    else:
                        fileout.write(line)
            os.replace(entry.path+"2",entry.path)
    if found:
        print(" Processed Archive. Found %s component violations."%count)
        return count
    else:
        print(" Processed Archive. ***************ERROR: DID NOT FIND COMPONENT CSV.*******************")

def process_archive( filename ):
    #create a temp directory for processing
    total = 0
    with tempfile.TemporaryDirectory() as tmpdir:
        print("=============================================================================")
        print('Created temporary directory')
        #unpack zip file to tmp
        unpack( filename,tmpdir )
        #process the component file for violations
        total = process( tmpdir,bad_array )
        #repack the zip file baack to the original
        repack( filename,tmpdir )
    return total

#build list of licenses that should be marked as a violation.
bad_array = read_bad_list()

file=sys.argv[1] if len(sys.argv) > 1 else "./"
directory =  False
if not os.path.isfile(file):
    directory = True
    print("Processing directory for all zip archives.")
    total = 0
    for entry in os.scandir(file):
        if ".zip" in entry.path:
            total += process_archive( entry )
    print("=============================================================================")
    print("Total license violations found: %s"%total)
else:
    print("Single archive for processing %s"%file)
    process_archive( file )

################### AVAYA 1100 SERIES PHONE MAC CONFIG GENERATION SCRIPT ######################
## Script to Generate MAC address unique files with phone numbers for auto login.
## Input CSV with at least columns: MAC, Phone.
## The CSV must have header rows with "MAC" and "Phone" headers (without quotes)
## 
## Requires Python 3. For older linux versions with both, use "python3" to initiate script.
##
## USAGE: python cfg-generator.py [csv input file]
## EXAMPLE: python cfg-generator.py AS5300configfiles.csv
## 
## Version: 1.02
## Updated: 2022-02-12
## Author: Brett Barker - brett.barker@brbtechsolutions.com 
########################################BRB####################################################

import csv
import datetime
import os
import sys
from collections import defaultdict


def main():
    ## Check for proper amount of arguments
    if len(sys.argv) < 2:
        print('Error: Missing argument. Enter CSV file as argument.')
        return  
    inputfile = sys.argv[1]
    if len(sys.argv) > 2:
        print('Error: Too many arguments. The only argument should be the CSV file.')
        return
    
    
    defaultPassword = 123456  #  SET THE DEFAULT PASSWORD FOR THE PHONE ACCOUNTS TO LOGIN WITH HERE
    results_file_name = "cfg-results.txt"
    cwd = os.path.abspath(os.getcwd())
    now = datetime.datetime.now()
    numSuccess = 0
    numFailure = 0
    macDict = defaultdict(list)
    outputpath = "output_files"
    os.makedirs(outputpath, exist_ok = True) # Make output directory if it doesn't exist.

    results_file = open(results_file_name, 'a')
    file = open(inputfile,'r') # Open file in read only
    file_dict = csv.DictReader(file) # Read the CSV into a dictionary. Note: Header row of the CSV MUST contain MAC,Phone,

    ## Start results file
    results_file.write('\n-----\n' + now.strftime('%Y-%m-%d %H:%M') + ' Starting Config Generation\n')

    ## Check for correct header row with MAC and Phone fields in the input file.
    if not 'MAC' in file_dict.fieldnames or not 'Phone' in file_dict.fieldnames:
        print('Error: ' + inputfile + ' does not contain a header row with "MAC" and "Phone"\n')
        results_file.close() # Close results file before erroring out.
        file.close() # Close the input file before erroring out.
        return 0

    ## Change CSV dict into a dictionary with MAC address keys and add each phone number as value to a list and sort it.
    for row in file_dict:
        macDict[row['MAC']].append(row['Phone']) # Add the phone number to corresponding MAC address dictionary key.
        macDict[row['MAC']].sort() # Sort the list of phone numbers in ascending order.
        # if len(macDict[row['MAC']]) > 9:
        #    print(row['MAC'])
        #     print(macDict[row["MAC"]])

    ## Make the files. Loop through each MAC address in the dictionary.
    for mac, phonevalues in macDict.items():
        file_logins = []
        filename = "SIP" + mac.upper() + ".cfg" # Set output filename

        if os.path.exists(outputpath + '/' + filename):  # Check if file already exists. Don't write the file if it already exists.
           numFailure += 1 # Increment fail counter.
           results_file.write('FAIL - File already exists: ' + filename + '\n') 

        else: # If the file doesn't exist, create it.
            maxlogins = len(phonevalues) # set max_login parameter to the number of phone numbers that will be auto-logged in.
            file_contents = ['SLOW_START_200OK NO','ENABLE_LOCAL_ADMIN_UI NO','AUTO_UPDATE YES','AUTO_UPDATE_TIME 2200','MAX_LOGINS '+ str(maxlogins),'AUTOLOGIN_ENABLE 2']
            key = 1 # set initial line key number            
            for phonenumber in phonevalues:  # Loop through each phone number in the list for the given MAC and create auto login.
                file_logins = file_logins + ['AUTOLOGIN_ID_KEY' + str(key).zfill(2) + ' '  + phonenumber + '@uc.mil']
                file_logins = file_logins + ['AUTOLOGIN_PASSWD_KEY' + str(key).zfill(2) + ' ' + str(defaultPassword)]
                key += 1

            output = open(outputpath + '/' + filename, 'x') # Open Output file.
            results_file.write('SUCCESS - Writing File ' + filename + '\n')
            output.write("\n\n".join(file_contents)) # Write static data in the file.
            output.write("\n\n")
            output.write("\n\n".join(file_logins)) # Write the auto login data
            output.close() # Close the output file.
            numSuccess+=1 # Increment success counter.

    ## Post Results to Terminal
    print('\n---------- RESULTS ----------')
    print('Avaya 11xx Config files created from: ' + inputfile)
    print('Output files saved to: ' + cwd + '/' + outputpath)
    print('Successful files written: ' + str(numSuccess))
    print('Number of Failures: ' + str(numFailure))
    print('** More details in ' + results_file_name + '**')
    print('-----------------------------\n')

    ## Write Results to Results file
    results_file.write('\n---------- RESULTS FROM ' + now.strftime('%Y-%m-%d %H:%M') + ' ----------\n')
    results_file.write('Avaya 11xx Config files created from: ' + inputfile + '\n')
    results_file.write('Output files saved to: ' + cwd + '/' + outputpath + '\n')
    results_file.write('Successful files written: ' + str(numSuccess) + '\n')
    results_file.write('Number of Failures: ' + str(numFailure) + '\n')
    results_file.write('----------------------------------------------------------\n')

    results_file.close() # Close results file.
    file.close() # Close the input file.

    return

if __name__=="__main__":
    main()

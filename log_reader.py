#!/usr/bin/python


"""
Script to read in web server logs from LOG_DIR and count the occurances of each response code
per minute. Output the results to a csv in 'timestamp,response_code,count' format
"""

from datetime import datetime
import os
import re

LOG_DIR = '/Users/jeffvaleo/Desktop/tu/log-parser/logs/'

def process_log():
    """
    Parse a logfile, pull out timestamp without seconds, add the http response code
    and write it to a dict as a key with an initial value of 1
    For each other instance of timestamp + reponse_code in the log
    """
    storage_array = {}
    for log in os.listdir(LOG_DIR):
        log_path = os.path.join(LOG_DIR, log)
        if log.endswith('.log'):
            print('Processing Log: {0}'.format(log))
            with open(log_path) as log_file: # Maybe use readline to read into mem
                for line in log_file:
                    try:
                        timestamp = re.findall(r"\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}", line)[0]
                    except Exception as e:
                        print('Exception caught in locating timestamp')
                    response_code = line.split()[8] # Assume it's always here
                    if re.match(r"[1-4][0-9]{2}", response_code):
                        dict_key = timestamp[0:-3] + ':' + response_code # Remove the seconds field
                        if dict_key in storage_array.keys():
                            response_count = storage_array[dict_key] + 1
                            storage_array[dict_key] = response_count
                        else:
                            storage_array[dict_key] = 1
    return storage_array

def write_to_csv(array):
    """
    Take in a dict, split the date & time from the status code out of the key then
    write to a CSV
    """
    print 'Writing To CSV'
    today = str(datetime.now().date())
    out_file= today + '.out'
    with open(out_file, 'w') as file:
        file.write('timestamp,response_code,count\n') # Write header
        for key, value in array.iteritems():
            response_code = key.split(':')[3]
            time_stamp = key[0:-4]
            count = value
            file.write('{0},{1},{2}\n'.format(time_stamp,response_code,count)) # Not using csv as this is a lighter-weight solution
        file.close()
        print('CSV Output Complete @ {0}'.format(out_file))

if __name__ == '__main__':
    storage_array = process_log()
    write_to_csv(storage_array)


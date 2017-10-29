#!/usr/bin/env python
# encoding: utf-8
"""
@author: skyyao
@file: find_medianval_by_date.py
@time: 10/25/2017
"""
import sys
import os
import datetime
import heapq

"""
validate_date_str is to determine if the current line's date 
format is valid.
"""
def validate_date_str(date_str):
    try:
        datetime.datetime.strptime(date_str, '%m%d%Y')
        return True
    except ValueError:
        return False

"""
validate_zipcode_str is to determine if the current line's zipcode 
format is valid.
"""
def validate_zipcode_str(zipcode_str):
    if len(zipcode_str) == 5 and zipcode_str.isdigit():
        return True, zipcode_str
    if len(zipcode_str) == 9 and zipcode_str.isdigit():
        return True, zipcode_str[0:5]   
    else:
        return False, 0

"""
Use cmte_id and date as key, put the record as val in hash_by_date. 
"""    
def write_record_by_date(line, hashmap):
    key_by_date = line[0] + line[13]
    if key_by_date not in hashmap:
        record = Record()
        hashmap[key_by_date] = record
        record.cmte_id = line[0]
        record.tran_dt = line[13]
    else:
        record = hashmap[key_by_date]
    record.amt_list.append(int(line[14]))
    record.total_amt += int(line[14])
    record.total_trans += 1

"""
Use zipcode as key, put the record as val in hash_by_zipcode.
"""         
def write_record_by_zip(line, zipcode, hashmap):
    key_by_zip = zipcode
    if key_by_zip not in hashmap:
        record = Record()
        hashmap[key_by_zip] = record
        record.cmte_id = line[0]
        record.zip_code = zipcode
    else:
        record = hashmap[key_by_zip]
    cur_amt = int(line[14])    
    record.total_amt += cur_amt
    record.total_trans += 1
        
    if len(record.amt_max_heap) == len(record.amt_min_heap):
        heapq.heappush(record.amt_min_heap, -heapq.heappushpop(record.amt_max_heap, -cur_amt))
    else:
        heapq.heappush(record.amt_max_heap, -heapq.heappushpop(record.amt_min_heap, cur_amt))
    return record

"""
As stream data flow, only need the top values of record.amt_max_heap
and record.amt_min_heap to determine the median. 
"""  
def write_file_by_zip(file, record):
    if len(record.amt_min_heap) == len(record.amt_max_heap):
        cur_median = '%.0f' % ((record.amt_min_heap[0] - record.amt_max_heap[0]) / 2.0)
    else:
        cur_median = '%.0f' % record.amt_min_heap[0]
    file.write(record.cmte_id + '|' + record.zip_code +'|' + str(cur_median) + '|' + str(record.total_trans) 
                + '|' + str(record.total_amt) + '\n')


"""
Sort the hash_by_date by the key, then the output should be sorted as cmte_id first, then date.
Also sort the amt_list to determine the median for each output line.
"""          
def write_file_by_date(file, hashmap):
    with open(file, 'w') as output_file_by_date:
        sort_list = sorted(hashmap.items(), key = lambda d:d[0])
        for key, val in sort_list:
            val.amt_list.sort()
            if val.total_trans % 2 == 0:
                cur_median = '%.0f' % ((val.amt_list[int(val.total_trans / 2)] + 
                                    val.amt_list[int(val.total_trans / 2 - 1)]) / 2.0)
            else:
                cur_median = '%.0f' % val.amt_list[int(val.total_trans / 2)]
            output_file_by_date.write(val.cmte_id + '|' + val.tran_dt +'|' + str(cur_median) + '|' 
                                      + str(val.total_trans) + '|' + str(val.total_amt))
            output_file_by_date.write('\n')
               
"""
Genterate data structure Record to save useful data.
"""     
class Record:
    def __init__(self):
        self.cmte_id = None
        self.zip_code = None
        self.tran_dt = None
        self.total_trans = 0
        self.total_amt = 0
        self.amt_list = []
        self.amt_min_heap = []
        self.amt_max_heap = []
        
class Main(object):
    if not os.path.isfile(sys.argv[1]): #If the input file not exist, exit program with error message.
        sys.exit('Input file does not exist.')
    (basename, filename) = os.path.split(sys.argv[2])
    if not os.path.exists(basename): #If output directory not exist, make the directory.
        os.makedirs(basename)
    (basename, filename) = os.path.split(sys.argv[3])
    if not os.path.exists(basename): #If output directory not exist, make the directory.
        os.makedirs(basename)
        
    hash_by_date = {}
    hash_by_zip = {}
    output_file_by_zip = open(sys.argv[2], 'w')
    with open(sys.argv[1], 'r') as input_file:
        for line in input_file:
            cur_line = line.split('|')
            if cur_line[15] is not '' or cur_line[0] is '' or cur_line[14] is '': #Determine if the line is valid according to the cmte_id, tran_amt and other_id. 
                continue
            if validate_date_str(cur_line[13]):
                write_record_by_date(cur_line, hash_by_date)
                    
            zipcode_validate, zipcode = validate_zipcode_str(cur_line[10])
            if zipcode_validate is True:
                record = write_record_by_zip(cur_line, zipcode, hash_by_zip)
                write_file_by_zip(output_file_by_zip, record)
                
    output_file_by_zip.close()
    write_file_by_date(sys.argv[3], hash_by_date)
            

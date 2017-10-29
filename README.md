# InsightDataEngineering

This project is for Insight Date Engineering Program Selection.

The input file is FEC format, should be in input folder.
The output file is in output folder, named medianvals_by_zip.txt and medianvals_by_date.txt.

I write the input and output parts of code as if input file not exist, exit program with error message and
if output directory not exist, make the directory.

I genterate data structure 'Record' to save useful data. Including cmte_id, zipcode, date, total transactions numbers,
total transactions amounts and three special lists. One is amt_list, for medianvals_by_date.txt. The other amt_min_heap
and amt_max_heap are for medianvals_by_zip.txt.  

For the output file by date, since for each specific cmte_id + date, need to write a new line of data. Then I generate
hashtable that set cmte_id and date as key and connect this key to the record as val. These record has unique cmte_id + date, 
and when the new data read in which has the same key, then I put the new transaction amount into the record.amt_list, and 
accumulate the total transactions and total amounts.

After the input file is totally read in, I sort the hash_by_date by the key. Thus the output should be sorted as cmte_id first,
then date. And then for each key (specific cmte_id + date), sort the amt_list to determine the median for each key, and 
write cmte_id, date, median, total transactions, and total amounts to medianvals_by_date.txt.        


Similarly, I use zipcode as key, put the record as val in hash_by_zipcode since for each zipcode, we need to accumulate 
the result.

To consider the stream data flow, I don't use a list to keep all the amounts. Becasue when a new amounts put in, to sort the list and get the median will waste time (at least O(logn) for each new data], so I use two heap to save the amounts data. 
I use record.amt_max_heap save the left half of all transaction_amt, and the record.amt_min_heap save the right half 
of all transaction_amt. since there's no max top heap structure in Python, I use min top heap but saved the negative 
value inside as record.amt_max_heap. Then for each stream data line, only need the top values of this amt_max_heap
and amt_min_heap to determine the median, which save time (O(1) to get the median). 

Then to write cmte_id, zipcode, median, total transactions, and total amounts to medianvals_by_zip.txt for each new valid input line of data.

Finally, I want to thank the Insight Data Science to give me this opportunity to do this selection project.
Hope I can have honor to work as a member of you in future.

Best Regards,

Yao Yao 10/28/2017
 

  
                
   

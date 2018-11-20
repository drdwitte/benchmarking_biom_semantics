# coding: utf-8

from datetime import datetime
import re

c=0
print(str(datetime.now()))
with open('watdiv.1000M.nt', 'r') as watdiv_in, open('watdiv.80M_1.nt', 'w') as watdiv_out_1, open('watdiv.80M_2.nt', 'w') as watdiv_out_2, open('watdiv.80M_3.nt', 'w') as watdiv_out_3, open('watdiv.80M_4.nt', 'w') as watdiv_out_4, open('watdiv.80M_5.nt', 'w') as watdiv_out_5, open('watdiv.80M_6.nt', 'w') as watdiv_out_6, open('watdiv.80M_7.nt', 'w') as watdiv_out_7, open('watdiv.80M_8.nt', 'w') as watdiv_out_8, open('watdiv.80M_9.nt', 'w') as watdiv_out_9, open('watdiv.80M_10.nt', 'w') as watdiv_out_10, open('watdiv.80M_11.nt', 'w') as watdiv_out_11, open('watdiv.80M_12.nt', 'w') as watdiv_out_12:
        
        outputstreams = [watdiv_out_1, watdiv_out_2, watdiv_out_3, watdiv_out_4, watdiv_out_5, watdiv_out_6, watdiv_out_7, watdiv_out_8, watdiv_out_9, watdiv_out_10, watdiv_out_11, watdiv_out_12]

        
        for ntriple in watdiv_in:
            
            start = ntriple.find('<')
            stop = ntriple.find('>')
            subject = ntriple[start:stop+1]
            
            h = hash(subject) % 12

            outputstreams[h].write(ntriple )
            
            c+=1
            
            if c%1e6 == 0:
                print(c/1e6)

print(str(datetime.now()))





# coding: utf-8

from datetime import datetime
import re

c=0
print(str(datetime.now()))
with open('watdiv.100M.nt', 'r') as watdiv_in, open('watdiv.33M_1.nt', 'w') as watdiv_out_1, open('watdiv.33M_2.nt', 'w') as watdiv_out_2,     open('watdiv.33M_3.nt', 'w') as watdiv_out_3:
        
        outputstreams = [watdiv_out_1, watdiv_out_2, watdiv_out_3]
        
        for ntriple in watdiv_in:
            
            start = ntriple.find('<')
            stop = ntriple.find('>')
            subject = ntriple[start:stop+1]
            
            h = hash(subject) % 3

            outputstreams[h].write(ntriple )
            
            c+=1
            
            if c%1e6 == 0:
                print(c/1e6)

print(str(datetime.now()))





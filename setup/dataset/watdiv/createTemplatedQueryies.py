
# coding: utf-8

# In[19]:

import os
import subprocess


# #### Create dir ./templated for generated queries per template

# In[20]:

#TODO remove
#os.chdir('/home/ddewitte/Desktop/tempScriptSchrijven')

directory = 'templated'
if not os.path.exists(directory):
    os.makedirs(directory)
    


# #### Create bash file to generate queries in ./templated

# In[22]:

bash_script = open('queryscript.sh', "w")
bash_script.write('#!bin/bash')
bash_script.write('\n')

numQueriesPerTemplate = 100
numQueryRetries = 1

os.chdir('./testsuite')

for i in os.listdir(os.getcwd()):
    if i[-4:]=='.txt':
        bash_script.write('bin/Release/watdiv -q ./model/wsdbm-data-model.txt ./testsuite/'+i + ' '+str(numQueriesPerTemplate)+' '
                                                                                        +str(numQueryRetries)
                                                                                        +' > templated/'
                                                                                        +i[:-4]+'.sparql\n')
bash_script.close()
os.chdir('../')


# In[23]:

shellcmd = ["bash", "./queryscript.sh"]
p = subprocess.Popen(shellcmd, stdout=subprocess.PIPE)
output, err = p.communicate()
#print ("stdout: " + str(output))
#print ("stderr: " + str(err))


# #### First we now have to run the bash script generated in previous shell
# #### Get all .sparql files in the templated directory

# In[24]:

#os.getcwd()
os.chdir('./templated')

files = []

for i in os.listdir(os.getcwd()):
    if  i[-7:]=='.sparql':
        files.append(i)

print(files)


# #### Now we iterate over all templated/*.sparql files, 
# 
# 1. give them their own directory 
# 2. split to have one query per file
# 3. generate a .list file with all paths

# In[25]:

#function to extract a list of queries from a file of sparql queries
def extractQueries(filename):
    handle = open(filename, "r")
    queries = []
    lst = []
    for l in handle:
        l_tr = l.strip()
        if l_tr[:6] == 'SELECT':
            if len(lst)>0:
                q = " ".join(lst)
                queries.append(q)
                lst = None
                lst = []
                lst.append(l_tr)
            else:
                lst.append(l_tr)
            
        elif len(l_tr)==0: #newline
            pass

        else:
            lst.append(l_tr)

            
    if len(lst)>0:
        q = " ".join(lst)
        queries.append(q)
              
            
    return queries


# In[26]:

for f in files:
    query_list = extractQueries(f)
    
    f_prefix = f.split('.')[0]
    dirname = f_prefix
    
#1  #give them their own directory 
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        
    os.chdir(dirname)
    
    paths = []

#2 one query per file
    for i, query in enumerate(query_list):
        
        path = f_prefix+"_split"+str(i)+'.sparql'
        text_file = open(path, "w")
        text_file.write(query)
        text_file.close()
        paths.append(path)
   

    os.chdir('../')
    
#3 listfile    
    listfile = open (f_prefix+'.lst',"w")
    
    for p in paths:
        listfile.write('templated/'+f_prefix+'/'+p+"\n")
    
    listfile.close()


# In[ ]:




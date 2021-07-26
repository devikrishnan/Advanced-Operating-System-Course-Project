
from __future__ import print_function

import sys
import os
import argparse
import numpy as np

# DEFAULT NOT MENTIONED
parser = argparse.ArgumentParser(description='Summarises the size of each libraries and each object file in a map file.')
args = parser.parse_args()
args.combine = '--combine'

class SectionSize():
    code = 0
    data = 0  # Including metadata like import tables
    def total(self):
        return self.code + self.data
    def add_section(self, section, size):
        if section.startswith('.comment'):
            return
        if section.startswith('.debug'):
            return
        if section.startswith('.ARM.attributes'):
            return
        if section.startswith('.text'):
            self.code += size
        elif section != '.bss':
            self.data += size

size_of_source = {}

class FileOpen():
    def openFile( filename):
        lib_list = []
        print(filename)
        with open(filename) as f:
                lines = iter(f)
                for line in lines:
                    if line.strip() == "Linker script and memory map":
                         break

                current_section = None
                split_line = None
                for line in lines:
                     #print(line)
                    line = line.strip('\n')
                    if split_line:
            # Glue a line that was split in two back together
                        if line.startswith(' ' * 16):
                            line = split_line + line
                        else:  # Shouldn't happen
                            print("Warning: discarding line ", split_line)
                        split_line = None

                    if line.startswith((".", " .", " *fill*")):       #if line startswith any of the following strings given
                        pieces = line.split(None, 3)  # Don't split paths containing spaces   #takes in first variable , address, code size
                        if line.startswith("."):    
                # Note: this line might be wrapped, with the size of the section
                # on the next line, but we ignore the size anyway and will ignore that line
                            current_section = pieces[0]
                        elif len(pieces) == 1 and len(line) > 14:
                # ld splits the rest of this line onto the next if the section name is too long
                            split_line = line
                        elif len(pieces) >= 3 and "=" not in pieces and "before" not in pieces:
                            if pieces[0] == "*fill*":
                                source = pieces[0]    #source = *fill*  pieces[-1] = size
                                size = int(pieces[-1], 16)
                            else:
                                source = pieces[-1]                                            #last element of the pieces list = which is the path containing .a and .o
                                size = int(pieces[-2], 16)

                            if args.combine:
                                if '.a(' in source:
                        # path/to/archive.a(object.o)
                        #Just to get the list of libraries and object files associated with it
                                    if 'cm3' in source:
                                        libra=source[source.index('cm3')+4:source.index('.a')+2]   
                                        obj_file=source[source.index('.a')+3:source.index(')')]
                                        lib_list.append(libra)
                                        obj_list.append(obj_file)
                                    elif 'miosix' in source:
                                        libra=source[source.index('miosix')+7:source.index('.a')+2]
                                        obj_file=source[source.index('.a')+3:source.index(')')]
                                        lib_list.append(libra)
                                        obj_list.append(obj_file)

                #calculation of each source line and its associated size            
                            if source not in size_by_source:
                    #print(source) 
                                size_by_source[source] = SectionSize()
                
                #print(current_section)
                            size_by_source[source].add_section(current_section, size)



lib_list=set(lib_list)



sources = list(size_by_source.keys())
sources.sort(key = lambda x: size_by_source[x].total())

#print(sources)
pie={}

#listing size of overall lib and non lib 
sumtotal_lib=0
sumtotal_nonlib=0
for s in sources:
    #print(s)   
    if 'main.o' in s: #need to chnage this condition for non lib to consider only the text and data
        #print(s)
        size = size_by_source[s]
        sumtotal_nonlib += size.total()
    elif "*fill*" not in s and not s.endswith("boot.o"): 
        #print(s)                      #need to change 
        size = size_by_source[s]
        sumtotal_lib += size.total() 


pie={'pie1': {'lib':sumtotal_lib,'nonlib':sumtotal_nonlib}}
pie['lib']={}


for libs in lib_list:
    pie[libs]={}

#listing overall size of each lib 
for i in lib_list:
    libsize=0
    #print("********************************")
    for s in sources:
        if i in s:
            #print(s)
            size = size_by_source[s]
            libsize=libsize+size.total()
    pie['lib'].update({i:libsize})

#listing size of each object file inside each lib
for i in lib_list:
    for o in obj_list:
        for s in sources:
            #print(s)
            if i in s and o in s:
                size = size_by_source[s]
                objsize=size.total()
                pie[i].update({o:objsize})
                break

json_data={'map_file':{'library':{}}}
for i in lib_list:
    json_data['map_file']['library'][i]="obj_files"

        
        result = {}

            
        
        values = np.fromiter(pie['pie1'].values(), dtype=int)
        print(pie.keys())
        
        # print the numpy array
        '''print(values)
        print(type(values))
        total = sum(values)
        new = [value * 100. / total for value in values]
        print(new)'''
        return pie , json_data


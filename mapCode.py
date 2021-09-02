
from __future__ import print_function

import sys
import os
import argparse
import numpy as np

lib_list=[] #list of names of all library present
obj_list =[] #list to store the names of all object files associated with libraries
nl_list=[] #list to store the names of non-library object files
size_by_source = {}
pie={} #dictionary to store the size division 

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

#size_of_source = {}

class FileOpen():
    def openFile(filename):
        lib_list = []
        obj_list =[]
        sumtotal_lib=sumtotal_nonlib=0
        print(filename)
        size_by_source = {}
        with open(filename) as f:
            lines = iter(f)
            for line in lines:
                if line.strip() == "Linker script and memory map":
                    break
            current_section = None
            split_line = None
            for line in lines:
                line = line.strip('\n')
                if split_line:
                    # Glue a line that was split in two back together
                    if line.startswith(' ' * 16):
                        line = split_line + line
                    else:  # Shouldn't happen
                        print("Warning: discarding line ", split_line)
                    split_line = None
                if line.startswith((".", " .", " *fill*")):       #if line startswith any of the following strings given
                    pieces = line.split(None, 3)  # Don't split paths containing spaces   
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
                                    libra=source[source.rindex('/')+1:source.rindex('.a')+2]   
                                    obj_file=source[source.index('.a')+3:source.index(')')]
                                    lib_list.append(libra)
                                    obj_list.append(obj_file)
                                elif 'miosix' in source:
                                    libra=source[source.rindex('/')+1:source.rindex('.a')+2]
                                    obj_file=source[source.index('.a')+3:source.index(')')]
                                    lib_list.append(libra)
                                    obj_list.append(obj_file)
                    
                        if source not in size_by_source:
                            size_by_source[source] = SectionSize()
                        size_by_source[source].add_section(current_section, size)


            lib_list=set(lib_list)
            obj_list=set(obj_list)
            sources = list(size_by_source.keys())
            sources.sort(key = lambda x: size_by_source[x].total())


            #For calculating the size of non-library section of chart and getting the list of non-library object files
            for s in sources:   
                if '.o' in s and '.a(' not in s and not s.endswith("boot.o") and 'main.o' not in s:
                    nl_file=s[s.rindex('/')+1:s.rindex('.o')+2]
                    nl_list.append(nl_file)
                    size = size_by_source[s]
                    sumtotal_nonlib += size.total()
                elif "*fill*" not in s and not s.endswith("boot.o") and 'main.o' not in s:                      
                    size = size_by_source[s]
                    sumtotal_lib += size.total()

                elif 'main.o' in s:
                    nl_list.append('main.o')
                    size = size_by_source[s]
                    sumtotal_nonlib += size.total()

            #print(nl_list)

            pie={'map_file': {'lib':sumtotal_lib,'nonlib':sumtotal_nonlib}}
            pie['lib']={}
            pie['nonlib']={}

            #For calculating size of each non-library file
            for ofile in nl_list:
                ofilesize=0
                for s in sources:
                    if "/"+ofile in s:
                        size = size_by_source[s]
                        ofilesize=ofilesize+size.total()
                        pie['nonlib'].update({ofile:ofilesize})
                    elif ofile == 'main.o' and 'main.o' in s:
                        size = size_by_source[s]
                        ofilesize=ofilesize+size.total()
                        pie['nonlib'].update({ofile:ofilesize})


            for libs in lib_list:
                pie[libs]={}

            #For calculating size of each library
            for i in lib_list:
                libsize=0
                for s in sources: 
                    if i in s:
                        size = size_by_source[s]
                        libsize=libsize+size.total()
                pie['lib'].update({i:libsize})


            #For calculating size of each object file of each library 
            for i in lib_list:
                for o in obj_list:
                    objsize=0
                    for s in sources:
                        if i in s and ".a("+o in s:
                            size = size_by_source[s]
                            objsize=objsize+size.total()
                            pie[i].update({o:objsize})

        json_data={'map_file':{'lib':{},'nonlib':{}}}
        for i in lib_list:
            json_data['map_file']['lib'][i]="obj_files"

        for i in nl_list:
            json_data['map_file']['nonlib']="obj_files"

        
        result = {}

            
        
        values = np.fromiter(pie['map_file'].values(), dtype=int)
        print(pie['nonlib'])
        
        # print the numpy array
        return pie , json_data


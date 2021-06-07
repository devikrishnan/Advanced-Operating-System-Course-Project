
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
            #import IPython;IPython.embed()
            for line in lines:
                if line.strip() == "Linker script and memory map":
                    break

            current_section = None
            split_line = None
            for line in lines:
                line = line.strip('\n')
                if split_line:

                    if line.startswith(' ' * 16):
                        line = split_line + line
                    else:  # Shouldn't happen
                        print("Warning: discarding line ", split_line)
                    split_line = None

                if line.startswith((".", " .", " *fill*")):       #if line startswith any of the following strings given
                    pieces = line.split(None, 3)  
                    if line.startswith("."):    
                        current_section = pieces[0]
                    elif len(pieces) == 1 and len(line) > 14:
                        split_line = line
                    elif len(pieces) >= 3 and "=" not in pieces and "before" not in pieces:
                        if pieces[0] == "*fill*":
                            source = pieces[0]
                            size = int(pieces[-1], 16)
                        else:
                            source = pieces[-1]    #last element of the pieces list = which is the path containing .a and .o
                            size = int(pieces[-2], 16)

                        if args.combine:
                            if '.a(' in source:
                                source = source[:source.index('.a(') + 2]
                                if 'cm3' in source:
                                    libra=source[source.index('cm3')+4:source.index('.a')]
                                    lib_list.append(libra)
                                elif 'miosix' in source:
                                    #print(source)
                                    libra=source[source.index('miosix')+7:source.index('.a')]
                                    lib_list.append(libra)
                       


                        if source not in size_of_source:
                            size_of_source[source] = SectionSize()
                        size_of_source[source].add_section(current_section, size)

        lib_list=set(lib_list)
        #import IPython;IPython.embed() 
        #print(lib_list)
        sources = list(size_of_source.keys())
        #print (sources)
        #print("****************")
        sources.sort(key = lambda x: size_of_source[x].total())
        sumtotal = sumcode = sumdata = 0
        for source in sources:
            size = size_of_source[source]
            sumcode += size.code
            sumdata += size.data
            sumtotal += size.total()

        pie={}
        sumtotal_lib=sumtotal_nonlib=0
        for s in sources:   
            #print(os.path.normpath(source))
            if 'main.o' in s:
                size = size_of_source[s]
                sumtotal_nonlib += size.total()
                #part1['nonlib']=sumtotal_nonlib
            else:
                #print(os.path.normpath(s))
                size = size_of_source[s]
                sumtotal_lib += size.total()
                #part1['lib']=sumtotal_lib 
        pie={'pie1': {'lib':sumtotal_lib,'nonlib':sumtotal_nonlib}}
        pie['lib']={}
        for i in lib_list:
            libsize=0
            for s in sources:
                if i in s:
                    size = size_of_source[s]
                    libsize=libsize+size.total()
            pie['lib'].update({i:libsize})

        #print(pie)
        
        result = {}

            
        
        values = np.fromiter(pie['pie1'].values(), dtype=int)
        print(pie.keys())
        
        # print the numpy array
        '''print(values)
        print(type(values))
        total = sum(values)
        new = [value * 100. / total for value in values]
        print(new)'''
        return pie


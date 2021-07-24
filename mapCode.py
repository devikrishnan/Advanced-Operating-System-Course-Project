
from __future__ import print_function

import sys
import os
import argparse
import numpy as np

lib_list=[]
obj_list=[]

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
    def openFile(filename):
        lib_list = []
        print(filename)
        size_by_source = {}
        with open(filename) as f:
            lines = iter(f)
            #import IPython;IPython.embed()
            for line in lines:
                #import IPython;IPython.embed()
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
                    #print("%s" %line)
                    pieces = line.split(None, 3)  # Don't split paths containing spaces   #takes in first variable , address, code size
                    if line.startswith("."):    
                        # Note: this line might be wrapped, with the size of the section
                        # on the next line, but we ignore the size anyway and will ignore that line
                        current_section = pieces[0]
                    elif len(pieces) == 1 and len(line) > 14:
                        print(line)
                        # ld splits the rest of this line onto the next if the section name is too long
                        split_line = line
                    elif len(pieces) >= 3 and "=" not in pieces and "before" not in pieces:
                        if pieces[0] == "*fill*":
                            source = pieces[0]    #source = *fill*  pieces[-1] = size
                            #print()
                            size = int(pieces[-1], 16)
                        else:
                            source = pieces[-1]
                            #print(source)                                            #last element of the pieces list = which is the path containing .a and .o
                            size = int(pieces[-2], 16)

                        if args.combine:                                                   #Todo:understand the checking condition
                            if '.a(' in source:
                                # path/to/archive.a(object.o)
                                #source = source[:source.index('.a(') + 2]

                                #Just to get the list of libraries and object files associated with it
                                if 'cm3' in source:
                                    libra=source[source.index('cm3')+4:source.index('.a')]   
                                    obj_file=source[source.index('.a')+3:source.index(')')]
                                    lib_list.append(libra)
                                    obj_list.append(obj_file)
                                elif 'miosix' in source:
                                    libra=source[source.index('miosix')+7:source.index('.a')]
                                    obj_file=source[source.index('.a')+3:source.index(')')]
                                    lib_list.append(libra)
                                    obj_list.append(obj_file)

                            #elif source.endswith('.o'):
                            #    where = max(source.rfind('\\'), source.rfind('/')) 
                            #    if where:
                            #        source = source[:where + 1] + '*.o' #did not understand

                        #calculation of each source line and its associated size            
                        if source not in size_by_source:
                            size_by_source[source] = SectionSize()
                            size_by_source[source].add_section(current_section, size)


        #print(obj_list)
        #print(lib_list)
        lib_list=set(lib_list)
        
        
        sources = list(size_by_source.keys())
        sources.sort(key = lambda x: size_by_source[x].total())
        sumtotal = sumcode = sumdata = 0
        for source in sources:
            size = size_by_source[source]
            sumcode += size.code
            sumdata += size.data
            sumtotal += size.total()


        pie={}
        sumtotal_lib=sumtotal_nonlib=0
        for s in sources:   
            if 'main.o' in s:
                size = size_by_source[s]
                sumtotal_nonlib += size.total()
            else:
                size = size_by_source[s]
                sumtotal_lib += size.total() 
        
        
        
        pie={'pie1': {'lib':sumtotal_lib,'nonlib':sumtotal_nonlib}}
        pie['lib']={}
        
        
        for libs in lib_list:
            pie[libs]={}


        for i in lib_list:
            libsize=0
            for s in sources: 
                if i in s:
                    size = size_by_source[s]
                    libsize=libsize+size.total()
                    pie['lib'].update({i:libsize})

        for i in lib_list:
            for o in obj_list:
                for s in sources:
                    if i in s and o in s:
                        size = size_by_source[s]
                        objsize=size.total()
                        pie[i].update({o:objsize})
                        break

        print(pie)


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


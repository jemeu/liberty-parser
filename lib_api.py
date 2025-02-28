import re
import sys
import tracemalloc

# The plan here is to maybe set a chunk size of maybe 100 lines

class Group:
    '''
    Parent class
    '''
    def __init__(self):
        self.definition = None
        self.name = None

# Have a separate class for parsing the file from the library itself, don't know how to jfjfjfj
class Library(Group):
    '''
    This represents the file as a whole
    '''
    def __init__(self, lib_path:str, definition = None, name = None):
        self.lib_path = lib_path
        # self.definition = definition
        self.name = name

        # Don't know whether this should be a string or a list
        self.header_text = []

        self.readptr = None

        # REMEMBER TO CLOSE THE FILE AT SOME POINT
        self.file = open(self.lib_path,'r')

        # Puts the read pointer at the beginning of the file
        # Might be faster to just set it to 0
        self.readptr = self.file.tell()

        # Returns a Library Object with 'definition' as the header of the .lib file        
        # alternative loop using readline()
        line = self.file.readline()
        while line: 

            # Writes out header
            if re.search('\s*library\s*\(',line):
                self.header_text.append(line) 
                name_object = re.search(r'\((.*?)\)',line)
                self.name = name_object.group(1)
       
            # Writes out cells 
            elif re.search('\s*cell\s*\(',line):
                # don't update self.readptr, leaving it at the start of the line just read  
                break                
                
            else:
                self.header_text.append(line)
                         
            self.readptr = self.file.tell()        
            line = self.file.readline()
                
        # Removes any extra blank lines at the end of the file
        # (as blank lines will still have a newline character at the end, resulting in two lines being printed)                   
        # if self.header_text[-1].endswith("\n"):
        #     self.header_text = self.header_text[:-1]

        self.definition = self.header_text # Q) Why clone the header_text attribute?

    def __iter__(self):
        return self

    def __next__(self):
        # This needs to iterate to find each cell in chunks
        self.cell = "Something needs go here"
        # notes: 
        # 1. the file handle should already have been opened in __init__          
        # 2. self.readptr should be pointing to the start of the line *just read*
        myCell = None
        self.file.seek(self.readptr)
        line = self.file.readline() # readline) returns an empty string '' when end-of-file is reached         
        while line: 
            if re.search('^\s*cell\s*\(',line):
                if myCell == None:
                    # re-parse the line with a more complex regex to extract the cell name
                    match = re.match(r'^\s*cell\s*\("?([^")]+)"?\)', line)
                    if match:
                        myCell = Cell()
                        myCell.name = match.group(1)
                        print(f"| creating new Cell object: {myCell.name}")
                        myCell.definition.append(line)
                        myCell.library = self
                    else:
                        # the syntax of the line doesn't conform to Liberty specification
                        print(f"syntax error on line '{line}'")
                        self.close_file()
                        raise StopIteration
                else:
                    break
            else:
                # don't update self.readptr, leaving it at the start of the line just read  
                myCell.definition.append(line)
                
            self.readptr = self.file.tell()  
            line = self.file.readline()
        
        # either no more lines to read, or an entire cell has been located
        if line == "":
            if myCell == None:
                self.close_file()
                raise StopIteration             
            else:
                # DEAL WITH THE EXTRA CLOSE CURLY BRACE THAT WILL BE IN THE DESCRIPTION
                print("Popping extra curly brace")
                myCell.definition.pop()

                return myCell
        else:
            return myCell

    def close_file(self):
        self.file.close()

    # Rename this to strip?
    def export(self,path,exclude = None):
        with open(path,'w') as output_file:
            for line in self.header_text:
                output_file.write(line)
            for cell in self:
                if cell.name not in exclude:
                    for line in cell.definition:
                        output_file.write(line)
            output_file.write('}')


    def smash(self, exclude = None):
        if exclude == None:
            exclude = []
        for cell in self:
            if cell.name not in exclude:
                file = f'{cell.name}.debug.lib'
                cell.export(file)
    


class Cell():
    def __init__(self):
        self.definition = []
        pass 

    def export(self,file = None):
        with open (file, 'w') as writefile:
            for line in self.library.header_text:
                writefile.write(line)

            for line in self.definition:
                writefile.write(line)

            writefile.write('}')

class Pin():
    def __init__(self):
        pass   

def byte_conversion(byte_val):
    for potential_unit in ['B','KB','MB','GB','TB','PB','EB']:
        if byte_val < 1024.000:
            return f"{byte_val:.3f} {potential_unit}"
        else:
            byte_val /= 1024

# Test 
if len(sys.argv) > 1:
  input_file = sys.argv[1]
else:
  input_file = 'example2.txt'

tracemalloc.start()
myLibrary = Library(input_file)
# myLibrary.export('exported_library.txt',['INV_X8N_A9PP96CTL_C20','INV_X10N_A9PP96CTL_C20'])
myLibrary.smash()
current_memory,peak_memory = tracemalloc.get_traced_memory()
print(f"Current memory use: {byte_conversion(current_memory)}")
print(f"Peak memory use: {byte_conversion(peak_memory)}")

tracemalloc.stop()

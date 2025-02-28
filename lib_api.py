import re
import sys

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
        if self.header_text[-1].endswith("\n"):
            self.header_text = self.header_text[:-1]

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
            if re.search('\s*cell\s*\(',line):
                if myCell == None:
                    # re-parse the line with a more complex regex to extract the cell name
                    match = re.match(r'^\s*cell\s*\("?([^")]+)"?\)', line)
                    if match:
                        print(f"| creating new Cell object")
                        myCell = Cell()
                        myCell.name = match.group(1)
                        myCell.definition.append(line) 
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

    def export(self,path,cell):
        with open(path,'w') as output_file:
            # Write header 
            for i in self.header_text:
                output_file.write(i)
            # Write definition 
            for j in cell.definition:
                output_file.write(j)
            output_file.write('}')

class Cell():
    def __init__(self):
        self.definition = []
        pass 

class Pin():
    def __init__(self):
        pass   

if len(sys.argv) > 1:
  input_file=sys.argv[1]
else:
  input_file='../example2.txt'

# Test code
myLibrary = Library(input_file)
for cell in myLibrary:
  #print(f"Within for loop, found {cell.name}")
  my_output = f'{cell.name}.lib'
  myLibrary.export(my_output,cell)



#print(myLibrary.definition)
#for myCell in myLibrary:
#  print(f"|   found cell object called '{myCell.name}' (with {len(myCell.definition)}-byte definition)")
  # if myCell.name == "INV_X3N_A9PP96CTL_C20":
  #  print(f"{myLibrary.definition}")
  #  print(f"{myCell.definition}")




# Pattern for getting cell names
# repattern = r'cell\s*\((.*?)\)'
# patterntest2 = re.findall(repattern,'cell (a;lksdfjal;kdsfa;lsdjfa;dfaljfalf) { as}{  ]asds daadssas }  wfwfewf cell   cell(11111111)')
# print(patterntest2)

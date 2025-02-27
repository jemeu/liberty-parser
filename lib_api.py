import re


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
        self.header_text = ""

        self.readptr = None

        # REMEMBER TO CLOSE THE FILE AT SOME POINT
        self.file = open(self.lib_path,'r')

        # Puts the read pointer at the beginning of the file
        # Might be faster to just set it to 0
        self.readptr = self.file.tell()

        # Returns a Library Object with 'definition' as the header of the .lib file
        
#         for line in self.file:
#             # If not the first cell
#             if not re.search('\s*cell\s*\(',line):
#                 self.header_text += line
# 
#                 ## This attempts to move the readpointer
#                 #self.readptr = self.file.tell()
#                 #print(self.readptr)
#             else:
#                 break
                
        # alternative loop using readline()
        line = self.file.readline()
        while line:        
            if not re.search('\s*cell\s*\(',line):
                self.header_text += line

                # This attempts to move the readpointer
                self.readptr = self.file.tell()
                print(self.readptr)
            else:
                # don't update self.readptr, leaving it at the start of the line just read  
                break
            self.readptr = self.file.tell()        
            line = self.file.readline()
                
        # Removes any extra blank lines at the end of the file
        # (as blank lines will still have a newline character at the end, resulting in two lines being printed)                   
        if self.header_text.endswith("\n"):
            self.header_text = self.header_text[:-1]
        name_object = re.search(r'\((.*?)\)',self.header_text)       

        self.name = name_object.group(1)
        self.definition = self.header_text
        
        

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
                        myCell.definition += line
                    else:
                        # the syntax of the line doesn't conform to Liberty specification
                        print(f"syntax error on line '{line}'")
                        raise StopIteration
                else:
                    break
            else:
                # don't update self.readptr, leaving it at the start of the line just read  
                myCell.definition += line
            self.readptr = self.file.tell()  
            line = self.file.readline()
        
        # either no more lines to read, or an entire cell has been located
        if line == "":
            if myCell == None:
                raise StopIteration             
            else:
                # DEAL WITH THE EXTRA CLOSE CURLY BRACE THAT WILL BE IN THE DESCRIPTION
                return myCell
        else:
            return myCell
        
    # This is useless at the moment
    def get_cell(self,cell):
        '''
        Returns the names of the cells, the contents etc
        '''
        re_pattern = r'cell\s*\((.*?)\)'
        cell_names = re.findall(re_pattern,self)

    def close_file(self):
        self.file.close()


class Cell():
    def __init__(self):
        self.definition = ""
        pass 

class Pin():
    def __init__(self):
        pass   


# Test code
myLibrary = Library('example.lib')
print(myLibrary.name)
#print(myLibrary.definition)
for myCell in myLibrary:
  print(f"|   found cell object called '{myCell.name}' (with {len(myCell.definition)}-byte definition)")
  if myCell.name == "INV_X1N_A9PP96CTL_C20":
      print(f"{myLibrary.definition}")
      print(f"{myCell.definition}")

print(vars(myCell))

myLibrary.close_file()


# Pattern for getting cell names
# repattern = r'cell\s*\((.*?)\)'
# patterntest2 = re.findall(repattern,'cell (a;lksdfjal;kdsfa;lsdjfa;dfaljfalf) { as}{  ]asds daadssas }  wfwfewf cell   cell(11111111)')
# print(patterntest2)

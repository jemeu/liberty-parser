import re


# The plan here is to maybe set a chunk size of maybe 100 lines

class Library:
    def __init__(self,description):
        self.description = description
    
    # This is a test method to check if something is actually an object or not
    # REMEMBER THIS IS A TEST METHOD 
    def explode(self):
        print("EXPLODED")

class Cell(Library):
    def __init__(self):
        pass 


class Pin(Cell):
    def __init__(self):
        pass    


# Have a separate class for parsing the file from the library itself, don't know how to jfjfjfj
class LibertyParser:
    def __init__(self, lib_path:str):
        self.lib_path = lib_path

        # Don't know whether this should be a string or a list
        self.header_text = ""

        # REMEMBER TO CLOSE THE FILE AT SOME POINT
        self.file = open(self.lib_path,'r')

    def __iter__(self):
        return self

    def __next__(self):
        # This needs to iterate to find each cell in chunks
        self.cell = "Something needs to go here"
    
    def parse_header(self):
        '''
        Returns a Library Object with 'description' as the header of the .lib file
        '''
        for line in self.file:
            # If not the first cell
            if not re.search('\s*cell\s*\(',line):
                self.header_text += line
            else:
                break
        # Removes any extra blank lines at the end of the file
        # (as blank lines will still have a newline character at the end, resulting in two lines being printed)                   
        if self.header_text.endswith("\n"):
            self.header_text = self.header_text[:-1]

        return_object = Library(self.header_text)
        match_object = re.search(r'\((.*?)\)',return_object.description)        
        return_object.description = match_object.group(1)
        return return_object
    
    def get_cell(self,cell):
        '''
        Returns the names of the cells, the contents etc
        '''
        re_pattern = r'cell\s*\((.*?)\)'
        cell_names = re.findall(re_pattern,self)

    def close_file(self):
        self.file.close()

# Test code
myFile = LibertyParser('example.lib')
myObject = myFile.parse_header()
print(myObject.description)
myFile.close_file()


# Pattern for getting cell names
repattern = r'cell\s*\((.*?)\)'
patterntest2 = re.findall(repattern,'cell (a;lksdfjal;kdsfa;lsdjfa;dfaljfalf) { as}{  ]asds daadssas }  wfwfewf cell   cell(11111111)')
print(patterntest2)

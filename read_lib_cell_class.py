import re


# The plan here is to maybe set a chunk size of maybe 100 lines

class Library:
    def __init__(self):
        pass
            
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
        pass
    
    def parse_header(self,output_path = None):
        '''
        Either returns the header of a .lib file, or writes it to a user specified location using output_path
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

        # Allows for an optional argument that specifies where to store it
        if output_path:
            with open(output_path,"w") as file:
                file.write(self.header_text)
        else:
            return self.header_text
    def close_file(self):


        self.file.close()
myFile = LibertyParser('example.lib')
var1 =myFile.parse_header()
myFile.close_file()
    
import re


class LibProcessor():


    def __init__(self, file_path:str, cell_name):
        self.file_path = file_path
        self.cell_name = cell_name
    

    def process_lib(self):
        with open(self.file_path,'r') as file:
            lines_printed = 0
            printing = True

            for line in file:
                # Prints the header
                # Checks if there is 'cell' followed by one or more 'anything other than a new line', then an open bracket
                if re.search('cell\s*\(',line):
                    printing = False

                

                # Keeps track of number of lines printed
                if printing == True:
                    print(line)
                    lines_printed += 1

            print(f"Lines printed = {lines_printed}")


myprocessor = LibProcessor("example.lib","INV_X8N_A9PP96CTL_C20")
myprocessor.process_lib()

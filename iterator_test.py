class IteratorTest1():
    def __init__(self,start,end):
        self.counter_val = start    
        self.end = end


    def __iter__(self):
        return self
    
    def __next__(self):
        if self.counter_val <= self.end:
            self.counter_val += 20
            return self.counter_val - 20
        else:
            raise StopIteration
        
myiterator = IteratorTest1(0,1000)
for x in myiterator:
    print(x)

class String_Interval():
    def __init__(self,string,interval):
        self.string = string
        self.interval = interval
        self.str_pointer = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        output = ""
        if self.str_pointer < len(self.string):
            output = self.string[self.str_pointer]
            self.str_pointer += self.interval
            return output
        else:
            raise StopIteration

myseconditerator = String_Interval("keyboardAndMouse",1)
for x in myseconditerator:
    print(x)

#!/usr/bin/env python3

# module load python/pandas_py3.8.2/1.4.0
# module load python/numpy_py3.8.2/1.24.3
# module load python/python/3.8.2

# Syntax notes:
# - header appears to be #H (possibly on its own line) followed by <name>='<value>'
#   pairs with single-quoted values separated by whitespace and arbitrarily spread
#   over multiple lines, with possibly more than one (complete) pair per line

# API notes:
# - json package exports load(), dump() at file level
# - csv package uses iterables for reading, and write() for writing
# - yaml package also exports file-level methods load() and dump()
# - pandas offers read_csv(), read_json() and to_csv(), to_json() for dataframes

import pandas as pd
import re

# prototype iterable CSDFReader class
class CSDFReader:
  def __new__(cls, filepath):
    instance = super().__new__(cls)
    return instance

  def __init__(self, filepath): # read the header
    self.filepath=filepath
    self._text_file = None
    self._header=None
    self._node_names=None
    self.node_names=[]
    self._rdptr = None

    # allow blank lines between #H and #N blocks
    section=None
    with open(self.filepath) as self._text_file:
      self._rdptr = self._text_file.tell()
      line = self._text_file.readline()
      while line:
        if line.startswith('#H'): # header found
          section='#H'
          self._header=line.replace('\n', ' ')
        elif line.startswith('#N'): # node names found
          section='#N'
          self._node_names=line.replace('\n', ' ')
        elif line.startswith('#'):
          break
        elif re.match(f'^\s*$',line):
          if self._header != None and self._node_names != None:
            break
        else:
          if section=='#H':
            self._header+=line.replace('\n', ' ')
          elif section=='#N':
            self._node_names+=line.replace('\n', ' ')
        self._rdptr = self._text_file.tell()
        line = self._text_file.readline()

    # parse the header and dynamically create attribute-value pairs (with lowercase attribute names)
    name_value_pairs = re.findall(r"(\S+='[^']*')+",self._header)
    for name_value_pair in name_value_pairs:
      match = re.match(r"(?P<name>\S+)='\s*(?P<value>\S+)'", name_value_pair)
      if match:
        self.__dict__[match.groupdict()['name'].lower()]=match.groupdict()['value']
      else:
        pass # FIXME should generate an error

    # parse the node names list
    quoted_node_names = re.findall(r"('[^']+')+",self._node_names)
    for quoted_node_name in quoted_node_names:
      match = re.match(r"'(?P<node_name>[^']+)'", quoted_node_name)
      if match:
        self.node_names.append(match.groupdict()['node_name'].lower())
      else:
        pass # FIXME should generate an error

    return None

  def __iter__(self):
     return self

  def __next__(self):
    data=None
    with open(self.filepath) as self._text_file:
      self._text_file.seek(self._rdptr)
      line = self._text_file.readline()
      while line:
        if line.startswith('#C'): # ? definition
          if data != None:
            break
          else:
            data=line.replace('\n', ' ')
        elif line.startswith('#'):
          break
        elif re.match(f'^\s*$',line):
          if data != None:
            break
        else:
          data+=line.replace('\n', ' ')
        self._rdptr = self._text_file.tell()
        line = self._text_file.readline()

    # parse the data (FIXME some sanity-checking here would be useful)
    if data!=None:
      data.strip()
      elements=data.split()
      sweepvar_value=elements[1]
      node_values=elements[2]
      node_values=elements[3:]
      df = pd.DataFrame({'Node' : self.node_names, 'Values' : node_values})
      return df
    else:
      raise StopIteration

#def read_sw0(filepath):
#  pass


file="/home/stecol02/projects/izanagi/tasks/spice_spi_read_csdf/_default.sw0"

csdfReaderObj=CSDFReader(file)
#print(f"analysis: {csdfReaderObj.analysis}")
#print(f"temperature: {csdfReaderObj.temperature}")
#print(f"sweepvar: {csdfReaderObj.sweepvar}")
#print(f"xend: {csdfReaderObj.xend}")
#print(f"nodes: {csdfReaderObj.nodes}")
#print(f"len(node_names): {len(csdfReaderObj.node_names)}")

for chunk in csdfReaderObj:
  print(chunk)

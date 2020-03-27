from pinkeen import inifile
from pinkeen.ansible.filters import AbstractFilterModule

class IniModule(AbstractFilterModule):

  @staticmethod
  def from_ini(string):
    return inifile.parse_string(string)
  
  def to_ini(data):
    return inifile.encode_data(data)

"""
  Simple disassembly optimizer for 'cursed' code.
  Taken mostly from:
    - https://github.com/idapython/src/blob/master/examples/hexrays/vds3.py
"""

from logger import Logger
from parsing.lexer import Lexer
from ida_hexrays import init_hexrays_plugin, install_hexrays_callback
import idaapi

# Gotta get a new prefs system soon when I have the time
prefs = {
  'fix_arc': True,
  'enabled': False,
}



class DemonMain(Logger):

  custom_name = 'Main'

  def __init__(self):
      Logger.__init__(self)
      self.log('Loaded and initialized')

  def is_assignment(self, line):
    return ('=' in line)

  def callback_handler(self, event, *args):
    if event == idaapi.hxe_func_printed:
      current_function = args[0] # get source text
      pseudocode = current_function.get_pseudocode()
      raw_text = self.get_raw_text(pseudocode)
      lexed = Lexer(raw_text)
      # for token in lexed.tokens:
      #   self.log('Token type: %s, name: "%s", Value: %s' % (token.type, token.name, token.lexeme))
  def get_raw_text(self, psuedocode):
    raw_lines = []
    for sl in psuedocode:
      raw_lines.append(sl.line)
    # psuedocode.clear()
    return '\n'.join(raw_lines)


class DemonPlugin(idaapi.plugin_t, Logger):

  flags = idaapi.PLUGIN_HIDE
  wanted_name = 'Curse psuedocode'
  comment = 'Curse your psuedocode forever using demonize'
  help=''
  wanted_hotkey = ''
  custom_name = 'Plugin'

  def init(self):
    if init_hexrays_plugin():

      self.main = DemonMain()

      def callback_shim(event, *args):
        if prefs['enabled']:
          self.main.callback_handler(event, *args)
        return 0

      install_hexrays_callback(callback_shim)
      return idaapi.PLUGIN_KEEP

  def run(self, __arg):
    self.log('Curse you psuedocode... what else do you want from me lmao')
    pass
  
  def term(self):
    self.log('AHHHHH')
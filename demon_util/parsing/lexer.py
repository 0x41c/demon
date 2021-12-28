from ..logger import Logger
from ida_lines import tag_skipcode
from .token import Token
import inspect




class LexingError(Logger):
  custom_name = 'Lexing Error'
  description = ''
  start = 0
  end = 0
  line_number = 0
  slice = ''

  def __init__(self, description, line_number, start, end, slice):
      object.__init__(self)
      self.description = description
      self.line_number = line_number
      self.start = start
      self.end = end
      self.slice = slice
  
  def _log(self):
    pass #TODO: Implement error logs




class Lexer(Logger):

  custom_name = 'Lexer'
  tokens = []
  errors = []
  pointer = -1
  current_line = 1
  source = ''
  _caller_cache = {}
  _high_level_caller = None
  lim = 0

  double_map = [
    [Token.master_map[Token.bitwise_ones_compliment], Token.bitwise_ones_compliment],
    [Token.master_map[Token.punc_parentheses_open], Token.punc_parentheses_open],
    [Token.master_map[Token.punc_parentheses_close], Token.punc_parentheses_close],
    [Token.master_map[Token.punc_bracket_open], Token.punc_bracket_open],
    [Token.master_map[Token.punc_bracket_close], Token.punc_bracket_close],
    [Token.master_map[Token.punc_curly_brace_open], Token.punc_curly_brace_open],
    [Token.master_map[Token.punc_curly_brace_close], Token.punc_curly_brace_close],
    [Token.master_map[Token.punc_comma], Token.punc_comma],
    [Token.master_map[Token.punc_colon], Token.punc_colon],
    [Token.master_map[Token.punc_semicolon], Token.punc_semicolon]
  ]

  triple_map = [
    [Token.master_map[Token.multiplication], Token.assign_multiply, Token.multiplication],
    [Token.master_map[Token.modulus], Token.assign_modulus, Token.modulus],
    [Token.master_map[Token.addition], Token.assign_add, Token.addition],
    [Token.master_map[Token.subtration], Token.assign_subtract, Token.subtration],
    [Token.master_map[Token.logical_not], Token.not_equal, Token.logical_not],
    [Token.master_map[Token.bitwise_xor], Token.assign_exclusive_or, Token.bitwise_xor]
  ]

  quad_map = [
    [Token.master_map[Token.bitwise_and], Token.assign_and, Token.logical_and, Token.bitwise_and],
    [Token.master_map[Token.bitwise_or], Token.assign_inclusive_or, Token.logical_or, Token.bitwise_or]
  ],

  quint_map = [
    [Token.master_map[Token.greater_than], Token.greater_or_equal, Token.assign_rshift, Token.bitwise_rshift, Token.greater_than],
    [Token.master_map[Token.smaller_than], Token.smaller_or_equal, Token.assign_lshift, Token.bitwise_lshift, Token.smaller_than]
  ]

  def __init__(self, source_code):
    Logger.__init__(self)
    self.source = source_code
    while self.lex() != True and len(self.swap) != 0 and int(len(self.swap) - 1) != 0:
      continue
    self.add_token(Token(Token.end_of_file))

  
  @property
  def swap(self):
    return self.source[self.pointer:]


  @property
  def char(self):
    return self.swap[0]


  def inc(self, amount = 1):
    cacheName = self._get_caller()
    if cacheName not in self._caller_cache:
      self._caller_cache[cacheName] = {
        'startPointer': self.pointer,
        'currentPointer': self.pointer + amount
      }
    else:
      self._caller_cache[cacheName]['currentPointer'] += amount
    self.pointer += amount


  def dec(self, amount = 1): # nifty for when you need to backtrack
    self._high_level_caller = self._get_caller()
    self.inc(-amount)


  def done(self, retval = None):
    caller = self._get_caller()
    if caller in self._caller_cache:
      self._caller_cache.pop(caller)
    return retval
  

  def add_token(self, token, ret_val = None):
    self._high_level_caller = self._get_caller()
    self.tokens.append(token)

    if ret_val == 'token':
      return self.done(token)
    return self.done(ret_val)


  def push_error(self, description):
    callee = self.get_caller()
    cache = self._caller_cache[callee]
    start = cache['startPointer']
    end = cache['currentPointer']
    error = LexingError(
      description,
      self.current_line,
      start,
      end,
      self.source[start:end]
    )
    self.errors.append(error)

  def _get_caller(self):
    if self._high_level_caller != None:
      caller = self._high_level_caller
      self._high_level_caller = None
      return caller
    return inspect.stack()[2][3]


  def lex_string(self):
    if self.char == '"':
      buffer = self.char
      self.inc()
      while self.char != '"':
        if self.char == '\\':
          self.inc()
          if self.char == 'n':
            buffer += '\n'
          elif self.char == 't':
            buffer += '\t'
          elif self.char == 'r':
            buffer += '\r'
          elif self.char == 'v':
            buffer += '\v'
          elif self.char == '\\':
            buffer += '\\'
          elif self.char == '"':
            buffer += '"'
          else:
            buffer += self.char
        else:
          buffer += self.char
        self.inc()
      return self.done(Token(Token.decl_str, buffer + '"'))
    return self.done()


  def lex_number(self):
    if self.char.isdigit():
      buffer = self.char
      float = False
      while True:
        self.inc()
        if not self.char.isdigit():
          break
    
        if self.char == '.' and not float:
          float = True
          buffer += self.char
        elif self.char == '.' and float:
          self.push_error('Invalid float literal')
          return self.done()
        else:
          buffer += self.char

      if float:
        return self.done(Token(Token.decl_flt, buffer))
      return self.done(Token(Token.decl_int, buffer))
    return self.done()
          

  def lex_identifier(self):
    id = ''
    def truth():
      if id != '':
        return self.char.isalpha() or self.char == '_' or self.char.isdigit()
      return self.char.isalpha() or self.char == '_'
    if truth():
      id = self.char

      while truth():
        self.inc()
        if not truth():
          self.dec()
          break
        id += self.char
      
      if id in Token.keyword_map:
        return self.done(Token(Token.keyword_map[id], id))
      else:
        return self.done(Token(Token.decl_id, id))
    return self.done()


  def lex(self):
  
    self.inc()    
    # self.log('Current IDX: %s, Amount of file left: %s' % (self.pointer, len(self.swap)))

    new_idx = tag_skipcode(self.swap)
    if new_idx != 0:
      # self.log('Moving to new idx: %s' % str(self.pointer + int(new_idx)))
      self.tokens.append(Token(Token.color_code, self.swap[:new_idx]))
      self.inc(new_idx - 1)
      return self.done()

      
    
    if len(self.swap) == 0:
      return self.done(True)

    while self.char.isspace():
      if self.char == '\n':
        return self.add_token(Token(Token.new_line))
      self.pointer += 1
    
    functions = [
      self.lex_string,
      self.lex_number,
      self.lex_identifier
    ]

    for func in functions:
      token = func()
      if token != None:
        return self.add_token(token)
      
    if self.char == '/':
      self.inc()
      if self.char == '/':
        while self.char != '\n':
          self.inc()
        return self.done()
      elif self.char == '*':
        while True:
          self.inc()
          if self.char == '*':
            self.inc()
            if self.char == '/':
              return self.done()
      elif self.char == '=':
        return self.add_token(Token(Token.assign_divide))
      self.dec()
      return self.add_token(Token(Token.division))

    for set in self.double_map:
      if self.char == set[0]:
        if set[0] == '(':
          self.inc()
          token = self.lex_number()
          if token != None:
            if token.lexeme.startswith('0' * 13):
              return self.add_token(Token(Token.color_code, '\x01(%s' % token.lexeme))

        return self.add_token(Token(set[1]))

    for set in self.triple_map:
      if self.char == set[0]:
        self.inc()
        if self.char == '=':
          return self.add_token(Token(set[1]))
        self.dec()
        return self.add_token(Token(set[2]))

    for set in self.quad_map:
      if self.char == set[0]:
        self.inc()
        if self.char == '=':
          return self.add_token(Token(set[1]))
        elif self.char == set[0]:
          return self.add_token(Token(set[2]))
        self.dec()
        return self.add_token(Token(set[3]))
    
    for set in self.quint_map:
      if self.char == set[0]:
        self.inc()
        if self.char == '=':
          return self.add_token(Token(set[1]))
        elif self.char == set[0]:
          self.inc()
          if self.char == '=':
            return self.add_token(Token(set[2]))
          self.dec()
          return self.add_token(Token(set[3]))
        self.dec()
        return self.add_token(Token(set[4]))

    if len(self.swap) != 0:
      return self.done()
    
    return self.done(True)

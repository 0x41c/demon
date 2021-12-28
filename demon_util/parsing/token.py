from ..logger import Logger

__type_index = 0

def idx():
  global __type_index
  ret = __type_index
  __type_index += 1
  return ret



class Token(Logger):

  custom_name = 'Token'
  _calculated_named_data = False
  type = -1
  name = ''
  lexeme = ''


  """
    Arithmetic Operators
  """
  addition = idx()
  subtration = idx()
  multiplication = idx()
  division = idx()
  modulus = idx()
  increment = idx()
  decrement = idx()


  """
    Relational Operators (Usually within boolean expr)
  """
  equal = idx()
  not_equal = idx()
  greater_than = idx()
  smaller_than = idx()
  greater_or_equal = idx()
  smaller_or_equal = idx()


  """
    Logical Operators
  """
  logical_and = idx()
  logical_or = idx()
  logical_not = idx()


  """
    Bitwise Operators
  """
  bitwise_and = idx()
  bitwise_or = idx()
  bitwise_xor = idx()
  bitwise_ones_compliment = idx()
  bitwise_lshift = idx()
  bitwise_rshift = idx()


  """
    Assignment Operators
  """
  assign = idx()
  assign_add = idx()
  assign_subtract = idx()
  assign_multiply = idx()
  assign_divide = idx()
  assign_modulus = idx()
  assign_lshift = idx()
  assign_rshift = idx()
  assign_and = idx()
  assign_exclusive_or = idx()
  assign_inclusive_or = idx()


  """
    Declarations
  """
  decl_id = idx()
  decl_str = idx()
  decl_int = idx()
  decl_flt = idx()


  """
    Keywords
  """
  keyword_if = idx()
  keyword_else = idx()
  keyword_while = idx()
  keyword_for = idx()
  keyword_return = idx()
  keyword_break = idx()
  keyword_continue = idx()
  keyword_true = idx()
  keyword_false = idx()
  keyword_nil = idx()


  """
    Misc
  """
  # TODO: Get ternery expressions in
  color_code = idx()
  end_of_file = idx()
  new_line = idx()

  """
    Punctuation
  """
  punc_curly_brace_open = idx()
  punc_curly_brace_close = idx()
  punc_parentheses_open = idx()
  punc_parentheses_close = idx()
  punc_bracket_open = idx()
  punc_bracket_close = idx()
  punc_period = idx()
  punc_comma = idx()
  punc_colon = idx()
  punc_semicolon = idx()



  """
    Master-Map

    Contains all the keywords and operators
  """
  master_map = {
    addition: '+',
    subtration: '-',
    multiplication: '*',
    division: '/',
    modulus: '%',
    increment: '++',
    decrement: '--',
    equal: '=',
    not_equal: '!=',
    greater_than: '>',
    smaller_than: '<',
    greater_or_equal: '>=',
    smaller_or_equal: '<=',
    logical_and: '&&',
    logical_or: '||',
    logical_not: '!',
    bitwise_and: '&',
    bitwise_or: '|',
    bitwise_xor: '^',
    bitwise_ones_compliment: '~',
    bitwise_lshift: '<<',
    bitwise_rshift: '>>',
    assign: '=',
    assign_add: '+=',
    assign_subtract: '-=',
    assign_multiply: '*=',
    assign_divide: '/=',
    assign_modulus: '%=',
    assign_lshift: '<<=',
    assign_rshift: '>>=',
    assign_and: '&=',
    assign_exclusive_or: '^=',
    assign_inclusive_or: '|=',
    keyword_if: 'if',
    keyword_else: 'else',
    keyword_while: 'while',
    keyword_for: 'for',
    keyword_return: 'return',
    keyword_break: 'break',
    keyword_continue: 'continue',
    keyword_true: 'true',
    keyword_false: 'false',
    keyword_nil: 'nil',
    end_of_file: '',
    new_line: '\n',
    punc_curly_brace_open: '{',
    punc_curly_brace_close: '}',
    punc_parentheses_open: '(',
    punc_parentheses_close: ')',
    punc_bracket_open: '[',
    punc_bracket_close: ']',
    punc_period: '.',
    punc_comma: ',',
    punc_colon: ':',
    punc_semicolon: ';',
  }

  """
  Keyword Map
  """
  keyword_map = {
    master_map[keyword_if]: keyword_if,
    master_map[keyword_else]: keyword_else,
    master_map[keyword_while]: keyword_while,
    master_map[keyword_for]: keyword_for,
    master_map[keyword_return]: keyword_return,
    master_map[keyword_break]: keyword_break,
    master_map[keyword_continue]: keyword_continue,
    master_map[keyword_true]: keyword_true,
    master_map[keyword_false]: keyword_false,
    master_map[keyword_nil]: keyword_nil,
  }

  def __init__(self, type, lexeme = None):
    Logger.__init__(self)
    self.type = type
    self.name = Token.get_name(self.type)
    if lexeme == None:
      if type in self.master_map:
        self.lexeme = self.master_map[type]
      else:
        self.error('Token value not provided to initialization (token type: %s, name: %s)' % (type, self.name))
    else:
      self.lexeme = lexeme

  @staticmethod  
  def get_name(token_type):
    if token_type is Token.addition:
      return "add"
    elif token_type is Token.subtration:
      return "sub"
    elif token_type is Token.multiplication:
      return "mul"
    elif token_type is Token.division:
      return "div"
    elif token_type is Token.modulus:
      return "mod"
    elif token_type is Token.increment:
      return "inc"
    elif token_type is Token.decrement:
      return "dec"
    elif token_type is Token.equal:
      return "equ"
    elif token_type is Token.not_equal:
      return "not equ"
    elif token_type is Token.greater_than:
      return "greater than"
    elif token_type is Token.smaller_than:
      return "smaller than"
    elif token_type is Token.greater_or_equal:
      return "greater or equ"
    elif token_type is Token.smaller_or_equal:
      return "smaller or equ"
    elif token_type is Token.logical_and:
      return "log and"
    elif token_type is Token.logical_or:
      return "log or"
    elif token_type is Token.logical_not:
      return "log not"
    elif token_type is Token.bitwise_and:
      return "bit and"
    elif token_type is Token.bitwise_or:
      return "bit or"
    elif token_type is Token.bitwise_xor:
      return "bit xor"
    elif token_type is Token.bitwise_ones_compliment:
      return "bit ones comp"
    elif token_type is Token.bitwise_lshift:
      return "bit lshift"
    elif token_type is Token.bitwise_rshift:
      return "bit rshift"
    elif token_type is Token.assign:
      return "assign"
    elif token_type is Token.assign_add:
      return "assign add"
    elif token_type is Token.assign_subtract:
      return "assign sub"
    elif token_type is Token.assign_multiply:
      return "assign mul"
    elif token_type is Token.assign_divide:
      return "assign div"
    elif token_type is Token.assign_modulus:
      return "assign mod"
    elif token_type is Token.assign_lshift:
      return "assign lshift"
    elif token_type is Token.assign_rshift:
      return "assign rshift"
    elif token_type is Token.assign_and:
      return "assign and"
    elif token_type is Token.assign_exclusive_or:
      return "excl or"
    elif token_type is Token.assign_inclusive_or:
      return "incl or"
    elif token_type is Token.decl_id:
      return "identifier"
    elif token_type is Token.decl_str:
      return "string"
    elif token_type is Token.decl_int:
      return "int"
    elif token_type is Token.decl_flt:
      return "float"
    elif token_type is Token.color_code:
      return "color code"
    elif token_type is Token.end_of_file:
      return "EOF"
    elif token_type is Token.new_line:
      return "Newline"
    elif token_type is Token.punc_curly_brace_open:
      return "curly open"
    elif token_type is Token.punc_curly_brace_close:
      return "curly close"
    elif token_type is Token.punc_bracket_open:
      return "bracket open"
    elif token_type is Token.punc_bracket_close:
      return "bracket close"
    elif token_type is Token.punc_parentheses_open:
      return "parenthesese open"
    elif token_type is Token.punc_parentheses_close:
      return "parenthesese close"
    elif token_type is Token.punc_period:
      return "period"
    elif token_type is Token.punc_comma:
      return "comma"
    elif token_type is Token.punc_colon:
      return "colon"
    elif token_type is Token.punc_semicolon:
      return "semicolon"



  @staticmethod
  def token_is_op(token_type):
    if token_type is Token.unassigned or \
       token_type is Token.addition or \
       token_type is Token.subtration or \
       token_type is Token.multiplication or \
       token_type is Token.division or \
       token_type is Token.modulus or \
       token_type is Token.increment or \
       token_type is Token.decrement or \
       token_type is Token.equal or \
       token_type is Token.not_equal or \
       token_type is Token.greater_than or \
       token_type is Token.smaller_than or \
       token_type is Token.greater_or_equal or \
       token_type is Token.smaller_or_equal or \
       token_type is Token.logical_and or \
       token_type is Token.logical_or or \
       token_type is Token.logical_not or \
       token_type is Token.bitwise_and or \
       token_type is Token.bitwise_or or \
       token_type is Token.bitwise_xor or \
       token_type is Token.bitwise_ones_compliment or \
       token_type is Token.bitwise_lshift or \
       token_type is Token.bitwise_rshift or \
       token_type is Token.assign or \
       token_type is Token.assign_add or \
       token_type is Token.assign_subtract or \
       token_type is Token.assign_multiply or \
       token_type is Token.assign_divide or \
       token_type is Token.assign_modulus or \
       token_type is Token.assign_lshift or \
       token_type is Token.assign_rshift or \
       token_type is Token.assign_and or \
       token_type is Token.assign_exclusive_or or \
       token_type is Token.assign_inclusive_or:
      return True
    return False

  @staticmethod
  def token_is_relational_op(token_type):
    if token_type is Token.equal or\
       token_type is Token.not_equal or\
       token_type is Token.greater_than or\
       token_type is Token.smaller_than or\
       token_type is Token.greater_or_equal or\
       token_type is Token.smaller_or_equal:
      return True
    return False
  
  @staticmethod 
  def token_is_bitwise_op(token_type):
    if token_type is Token.bitwise_and or \
       token_type is Token.bitwise_or or \
       token_type is Token.bitwise_xor or \
       token_type is Token.bitwise_ones_compliment or \
       token_type is Token.bitwise_lshift or \
       token_type is Token.bitwise_rshift:
      return True
    return False

  @staticmethod
  def token_is_assignment_op(token_type):
    if token_type is Token.assign or \
       token_type is Token.assign_add or \
       token_type is Token.assign_subtract or \
       token_type is Token.assign_multiply or \
       token_type is Token.assign_divide or \
       token_type is Token.assign_modulus or \
       token_type is Token.assign_lshift or \
       token_type is Token.assign_rshift or \
       token_type is Token.assign_and or \
       token_type is Token.assign_exclusive_or or \
       token_type is Token.assign_inclusive_or:
      return True
    return False
from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def enterMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    pass

  def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for * or /: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
    pass

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    
    # Validamos concatenación de strings y Conflicto 1 (string + otro tipo)
    if ctx.op.text == '+':
        if isinstance(left_type, StringType) and isinstance(right_type, StringType):
            self.types[ctx] = StringType()
            return
        elif isinstance(left_type, StringType) or isinstance(right_type, StringType):
            self.errors.append(f"Conflicto 1: No se puede sumar {left_type} con {right_type}")
            self.types[ctx] = StringType() # Fallback para seguir analizando
            return

    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for {ctx.op.text}: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterEquality(self, ctx: SimpleLangParser.EqualityContext):
    pass

  def exitEquality(self, ctx: SimpleLangParser.EqualityContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    # Conflicto 2: Igualdad entre tipos distintos
    if type(left_type) != type(right_type):
      self.errors.append(f"Conflicto 2: No se puede comparar igualdad entre {left_type} y {right_type}")
    self.types[ctx] = BoolType()

  def enterLogical(self, ctx: SimpleLangParser.LogicalContext):
    pass

  def exitLogical(self, ctx: SimpleLangParser.LogicalContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    # Conflicto 3: Operaciones lógicas con tipos no booleanos
    if not isinstance(left_type, BoolType) or not isinstance(right_type, BoolType):
      self.errors.append(f"Conflicto 3: Operadores lógicos requieren booleanos, se recibió {left_type} y {right_type}")
    self.types[ctx] = BoolType()

  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def is_valid_arithmetic_operation(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False

from SimpleLangParser import SimpleLangParser
from SimpleLangVisitor import SimpleLangVisitor
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckVisitor(SimpleLangVisitor):

  def visitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    else:
        raise TypeError("Unsupported operand types for * or /: {} and {}".format(left_type, right_type))

  def visitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    
    # Validamos concatenación de strings y Conflicto 1 (string + otro tipo)
    if ctx.op.text == '+':
        if isinstance(left_type, StringType) and isinstance(right_type, StringType):
            return StringType()
        elif isinstance(left_type, StringType) or isinstance(right_type, StringType):
            raise TypeError("Conflicto 1: No se puede sumar {} con {}".format(left_type, right_type))

    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
        return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
    else:
        raise TypeError("Unsupported operand types for {} : {} and {}".format(ctx.op.text, left_type, right_type))

  def visitEquality(self, ctx: SimpleLangParser.EqualityContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    # Conflicto 2: Igualdad entre tipos distintos
    if type(left_type) != type(right_type):
        raise TypeError("Conflicto 2: No se puede comparar igualdad entre {} y {}".format(left_type, right_type))
    return BoolType()

  def visitLogical(self, ctx: SimpleLangParser.LogicalContext):
    left_type = self.visit(ctx.expr(0))
    right_type = self.visit(ctx.expr(1))
    # Conflicto 3: Operaciones lógicas con tipos no booleanos
    if not isinstance(left_type, BoolType) or not isinstance(right_type, BoolType):
        raise TypeError("Conflicto 3: Operadores lógicos requieren booleanos, se recibió {} y {}".format(left_type, right_type))
    return BoolType()
  
  def visitInt(self, ctx: SimpleLangParser.IntContext):
    return IntType()

  def visitFloat(self, ctx: SimpleLangParser.FloatContext):
    return FloatType()

  def visitString(self, ctx: SimpleLangParser.StringContext):
    return StringType()

  def visitBool(self, ctx: SimpleLangParser.BoolContext):
    return BoolType()

  def visitParens(self, ctx: SimpleLangParser.ParensContext):
    return self.visit(ctx.expr())

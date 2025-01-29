import os, sys
sys.path.append(os.getcwd())
from easy_formula_transformation_mgl import *


formula_file = open(f"./formulas.md", "r")
formula_lines = formula_file.readlines()

list_strings = []
for i,formula in enumerate(formula_lines):
  if i > 0:
    start_index = formula.find("$")
    list_strings.append(formula[start_index+3:-3])

class GetIndexes(EasyFormulaIndex):
  file_name = "quadratic"
  formula_list = [
    [
      Tex(list_strings[0]),
      Tex(list_strings[1])
    ],[
      Tex(list_strings[1]),
      Tex(list_strings[2])
    ],[
      Tex(list_strings[2]),
      Tex(list_strings[3])
    ],[
      Tex(list_strings[3]),
      Tex(list_strings[4])
    ],
  ]
  arrange_methods = [
    lambda grp: grp.arrange(DOWN,buff=1),
    lambda grp: grp.scale(2)
  ]

class MainScene(Scene):
  def construct(self):
    pass







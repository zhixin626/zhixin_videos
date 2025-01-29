from manimlib import *
from pyglet.window.key import (
    U as UNDO_KEY,                   # Undo
    _1 as USE_RADIUS_KEY,            # Use radius as hover method
    S as SHOW_FORM_KEY,              # Show formulas strings in terminal
    Z as SIZE_PRE_FORMULA_KEY,       # Change size pre formula with scroll
    X as SIZE_POS_FORMULA_KEY,       # Change size pos formula with scroll
    N as SHOW_INDEXES_KEY,           # Show indexes
    E as RESET_COLORS_KEY,           # Set color white pre/pos formula
    A as HIGHLIGHT_FORMULA_KEY,      # Highlight pre/pos formula
    Q as SHOW_HIGHLIGHT_INDEXES_KEY, # show indexes selected with A
    T as CHANGE_TRANSFORM_KEY,       # Change transform type
    V as MOVE_PRE_FORMULA_KEY,       # Move pre formula to cursor
    B as MOVE_POS_FORMULA_KEY,       # Move pos formula to cursor
    R as RESET_KEY,                  # Reset current formulas
    F as INCREASE_RUN_TIME_KEY,      # +0.5 run_time
    G as DECREASE_RUN_TIME_KEY,      # -0.5 run_time
    W as WRITE_KEY,                  # Write to file
    C as PRINT_KEY,                  # Print file
    ENTER as NEXT_FORMULAS_KEY,      # list formulas -1
    BACKSPACE as PREV_FORMULAS_KEY,  # list formulas +1
    SPACE as PREVIEW_KEY,            # Show preview animation
)


def GTO(pos, i):
  f = next(filter(lambda mob: mob[0] == i, pos.targets), None)
  if f is not None:
    return [pos.subindex, f[1]]

def index_animation(
  base,
  target,
  arr,
  start_shift=0,
  end_shift=0,
  **kwargs):
  anims = []
  for _b,_t in arr:
    b = int(_b[:-1])
    t = _b[-1]
    args = [base[b+start_shift],target[_t+end_shift]]
    anims.append(
      FadeTransform(*args, **kwargs)                   if t == "T" else
      FadeTransform(args[0].copy(), args[1], **kwargs) if t == "C" else
      FadeTransform(*args, **kwargs)                   if t == "F" else
      FadeTransform(args[0].copy(), args[1], **kwargs) if t == "K" else
      ValueError("No TCFK found")
    )
  return anims

def get_indexes_from_target(targets):
  return [t[0] for t in targets]

def get_subindexes(mob, d=UP, buff=0.05, scale=0.3):
  return VGroup(*[
    Text(f"{i}")
        .scale(scale)
        .next_to(m, d, buff=buff)
    for i,m in enumerate(mob)
  ])

def get_not_empty_formula(f):
  if len(f) == 1:
    return f[0]
  return f

list_strings = [
  "ABC1",
  "DEF2",
  "GHI3",
  "JKL4",
  "PQR5",
]

class EasyFormulaIndex(Scene):
  file_name = "index_file"
  formula_list = [
    [
        Text(list_strings[0]),
        TexText(list_strings[1])
    ],
    [
        Text(list_strings[1]),
        Text(list_strings[2])
    ],
    [
        Text(list_strings[2]),
        Text(list_strings[3])
    ],
    [
        Text(list_strings[3]),
        Text(list_strings[4])
    ],
  ]

  arrange_methods = [
    lambda grp: grp.scale(2)
  ]

  def __init__(self, *args, **kwargs):
    self.pre_text = get_not_empty_formula(self.formula_list[0][0]).copy()
    self.pos_text = get_not_empty_formula(self.formula_list[0][1]).copy()
    self.set_init_attrs()
    self.cursor_dot    = Dot(color=PINK)
    self.radius_circle = Dot(radius=0.5,color=GREEN).set_opacity(0.1)
    self.scroll_type = "radius"
    self.transform_classes = [
      Transform, FadeTransform, TransformFromCopy
    ]
    self.transform_letters = "TFC"
    self.transform_labels_scale = 0.5
    self.step_formula = 0
    self.indexes_file_name = self.file_name 
    self.transform_index  = 0
    self.index_label = self.get_index_label()
    self.origin_dot = LEFT * FRAME_X_RADIUS + DOWN * FRAME_Y_RADIUS
    super().__init__(*args, **kwargs)

  def set_init_attrs(self):
    self.selected_state = False
    self.selected_text  = None
    self.selected_index = None
    self.base_index     = None
    self.target_index   = None
    self.history_states = []
    self.use_radius     = False
    self.formula_selected = False
    self.index_progress   = []
    self.preview_index    = 0
    self.n_index = 0
    self.changing_size = False
    self.moving_formula = None
    self.anim_run_time  = 6

  def get_index_label(self):
    return Text(f"{self.step_formula+1} / {len(self.formula_list)}").to_corner(UR,buff=0.05)

  def setup(self):
    transform_label      = Text("Transform")
    fade_transform_label = Text("FadeTransform")
    transform_from_copy  = Text("TransformFromCopy")
    labels = VGroup(
      transform_label,
      fade_transform_label,
      transform_from_copy
    )
    for mob in labels:
      mob.scale(self.transform_labels_scale)
      mob.to_corner(DR,buff=0.1)
      mob.set_color(GREY)
    labels.set_opacity(0)
    labels[0].set_opacity(1)
    self.transform_labels = labels
    self.anim_run_time_label = self.get_anim_run_time_label()

  def add_init_mobs(self):
    self.add(self.index_label)
    self.add(self.transform_labels)
    self.add(self.cursor_dot, self.radius_circle)
    self.add(self.anim_run_time_label)

  def get_anim_run_time_label(self):
    return Text(
        "run_time=%g"%self.anim_run_time,
        font="Fira Code"
    ).scale(0.7).to_corner(UL,buff=0.1)

  def set_indexes(self, clear=False):
    if not clear:
      targets_saved       = [_t.targets.copy() for _t in self.pos_text]
      list_step_saved     = [_t.list_step for _t in self.pos_text]
      highlight_saved     = [_t.highlight for _t in self.pre_text]
      highlight_saved_pos = [_t.highlight for _t in self.pos_text]
      self.pre_indexes.become(get_subindexes(self.pre_text))
      self.pos_indexes.become(get_subindexes(self.pos_text))
    else:
      if hasattr(self, "pre_indexes"):
        self.remove(self.pre_indexes, self.pos_indexes)
        del self.pre_indexes
        del self.pos_indexes
      self.pre_indexes = get_subindexes(self.pre_text)
      self.pos_indexes = get_subindexes(self.pos_text)

    self.pre_indexes.set_opacity(0)
    self.pos_indexes.set_opacity(0)

    for i,t in enumerate(self.pre_text):
      t.subindex=i
      t.text_index=self.pre_indexes[i]
      t.highlight=highlight_saved[i] if not clear else False

    for i,t in enumerate(self.pos_text):
      t.targets    = targets_saved[i] if not clear else []
      t.subindex   = i
      t.list_step  = list_step_saved[i] if not clear else None
      t.text_index = self.pos_indexes[i]
      t.highlight  = highlight_saved_pos[i] if not clear else False

  def get_pre_and_pos_text_from_step(self, clear=False):
    i = self.step_formula
    pre_text = get_not_empty_formula(self.formula_list[i][0]).copy()
    pos_text = get_not_empty_formula(self.formula_list[i][1]).copy()

    if not clear:
      self.remove(self.pre_text, self.pos_text)
      self.remove(self.phantom_pre_text, self.phantom_pos_text)
      del self.pre_text
      del self.pos_text
      del self.phantom_pre_text

    self.pre_text = pre_text
    self.pos_text = pos_text

    grp = VGroup(
      self.pre_text,
      self.pos_text
    ).arrange(DOWN, buff=1.5)

    for am in self.arrange_methods: am(grp)

    self.pre_text.save_state()
    self.set_indexes(clear)

    self.phantom_pre_text = self.pre_text.copy()
    self.phantom_pos_text = self.pos_text.copy()
    self.phantom_pre_text.set_opacity(0)
    self.phantom_pre_text.set_color(YELLOW)
    self.phantom_pos_text.set_opacity(0)
    self.phantom_pos_text.set_color(YELLOW)

    self.add(self.pre_text, self.pos_text)
    self.add(self.pre_indexes, self.pos_indexes)
    self.add(self.phantom_pre_text, self.phantom_pos_text)

  def construct(self):
    self.get_pre_and_pos_text_from_step(True)
    self.add_init_mobs()
    # self.interactive_embed()
    self.wait(0.5)

  def is_hover(self, mob):
    mob_coord = mob.get_center()
    cursor    = self.cursor_dot.get_center()
    if not self.use_radius:
      x, y, _ = mob_coord
      cursor_x, cursor_y, _ = cursor
      max_width  = mob.get_width() / 2
      max_height = mob.get_height() / 2
      return abs(cursor_x - x) < max_width and abs(cursor_y - y) < max_height
    else:
      distance_to_cursor = np.linalg.norm(mob_coord - cursor)
      return distance_to_cursor < self.radius_circle.get_width() / 2

  def are_overlapping(self, base, target):
    base_coord = base.get_center()
    target_coord = target.get_center()
    if not self.use_radius:
      x1, y1, _ = base_coord
      x2, y2, _ = target_coord
      max_width  = target.get_width() / 2
      max_height = target.get_height() / 2
      return abs(x1 - x2) < max_width and abs(y1 - y2) < max_height
    else:
      distance_to_cursor = np.linalg.norm(base_coord - target_coord)
      return distance_to_cursor < self.radius_circle.get_width() / 2

  def highlight_pre_formula(self, point):
    self.pos_text.set_stroke(width=0,color=WHITE)
    self.base_index = None
    self.selected_index = None
    for t in self.pre_text:
      if self.is_hover(t):
        t.set_stroke(width=6, color=PINK)
        self.selected_index = t.subindex
        self.base_index     = t.subindex
      else:
        t.set_stroke(width=0,color=WHITE)

  def highlight_pos_formula(self, point):
    if self.selected_index is not None:
      self.pre_text[self.selected_index].move_to(point)
      for i,t in enumerate(self.pos_text):
        if self.is_hover(t):
          t.set_stroke(width=6, color=ORANGE)
          self.target_index = i
        else:
          t.set_stroke(width=0,color=WHITE)

  def highlight_targets_formulas(self, point):
    self.preview_index = None
    for i,t in enumerate(self.pos_text):
      if self.is_hover(t):
        t.set_stroke(width=5,color=ORANGE)
        self.preview_index = i
      else:
        t.set_stroke(width=0,color=WHITE)

  def check_target_ready(self):
    if self.selected_index is not None and self.target_index is not None:
      base = self.pre_text[self.selected_index]
      target = self.pos_text[self.target_index]
      if self.are_overlapping(base, target):
        self.formula_selected = True
      else:
        self.formula_selected = False

  def update_cursor(self, point):
    self.cursor_dot.move_to(point)
    self.radius_circle.move_to(self.cursor_dot)
    if not self.selected_state:
        self.highlight_pre_formula(self.cursor_dot.get_center())
        self.highlight_targets_formulas(self.cursor_dot.get_center())
    else:
        self.highlight_pos_formula(self.cursor_dot.get_center())
    if self.moving_formula is not None:
      self.moving_formula.move_to(self.cursor_dot.get_center())

  def on_mouse_motion(self, point, d_point):
    self.update_cursor(point)
    super().on_mouse_motion(point, d_point)

  def restore_pre_text(self):
    if len(self.history_states) > 0:
        self.pre_text.become(self.history_states[-1])
    else:
        self.pre_text.restore()

  def on_mouse_press(self, point, button, modifiers):
    self.check_target_ready()
    if self.formula_selected \
      and self.target_index is not None \
      and self.selected_index is not None:
      arr = get_indexes_from_target(self.pos_text[self.target_index].targets)
      if self.selected_index not in arr:
        if f"{self.pre_text[self.selected_index].get_color()}".upper() == f"{rgb_to_color(hex_to_rgb(RED))}".upper():
          print(f"Index {self.selected_index} is already added")
          self.pos_text[self.target_index].targets.append(
            [self.selected_index, "C" if self.transform_index == 0 or self.transform_index == 2 else "K"]
          )
        else:
          self.pos_text[self.target_index].targets.append(
            [self.selected_index, self.transform_letters[self.transform_index]]
          )
        self.index_progress.append([self.n_index, self.selected_index, self.target_index])
        self.restore_pre_text()
        self.pre_text[self.selected_index].set_color(RED)
        self.pos_text[self.target_index].list_step = self.n_index
        self.history_states.append(self.pre_text.copy())
        if self.target_index is not None:
          self.pos_text[self.target_index].set_color(PURPLE)
        self.selected_index = None
        self.target_index = None
        self.n_index += 1
      else:
        self.restore_pre_text()
    else:
      self.restore_pre_text()
    self.selected_state = not self.selected_state
    self.update_cursor(self.cursor_dot.get_center())
    if self.selected_state:
      self.cursor_dot.set_color("#00F")
    else:
      self.cursor_dot.set_color(PINK)

  def on_key_press(self, symbol, modifiers):
    global GTO
    if symbol == UNDO_KEY and len(self.history_states) > 0:
      self.restore_pre_text()
      if not self.changing_size:
        self.history_states.pop()
        last_index = self.index_progress[-1]
        nmob = list(filter(
          lambda mob: last_index[1] in get_indexes_from_target(mob.targets),
          self.pos_text
        ))
        n2mob = [(m.list_step, m.subindex, m) for m in nmob]
        n2mob.sort(key=lambda mob: mob[0])
        mob_with_index = n2mob[-1][-1]
        self.pre_text[last_index[1]].set_opacity(1)
        mob_with_index.targets.pop()
        if len(mob_with_index.targets) == 0:
          mob_with_index.set_color(WHITE)
        self.index_progress.pop()
        self.restore_pre_text()
        self.n_index -= 1
      self.changing_size = False
    if symbol == SHOW_FORM_KEY:
      print("*** *** *** ***")
      for t in self.pos_text:
        print(f"{t.subindex}: {t.targets}")
      print("=== === === ===")
      print("[")
      for i,t in enumerate(self.pre_text):
        f  = [ GTO(pos, i) for pos in self.pos_text ]
        f3 = [ f"{i}{_f[1]}" for _f in f if _f is not None ]
        f4 = [ _f[0] for _f in f if _f is not None ]
        if len(f3) > 0:
            print(f"  *zip({f3},{f4}),")
      print("]")
      print("*** *** *** ***")
    if symbol == CHANGE_TRANSFORM_KEY:
      self.transform_index = (self.transform_index + 1) % 3
      self.transform_labels.set_opacity(0)
      self.transform_labels[self.transform_index].set_opacity(1)
    if symbol == SHOW_INDEXES_KEY:
      self.pre_indexes.set_opacity(1)
      self.pos_indexes.set_opacity(1)
      if self.preview_index is not None:
        arr = get_indexes_from_target(self.pos_text[self.preview_index].targets)
        for el in arr:
          self.pre_indexes[el].set_color(YELLOW)
          self.phantom_pre_text[el].set_opacity(1)
      if self.base_index is not None:
        for i,t in enumerate(self.pre_text):
          f  = [ GTO(pos, i) for pos in self.pos_text ]
          f3 = [ f"{i}{_f[1]}" for _f in f if _f is not None ]
          f4 = [ _f[0] for _f in f if _f is not None ]
          if len(f4) > 0 and i == self.base_index:
            for i in f4:
              self.pos_indexes[i].set_color(YELLOW)
              self.phantom_pos_text[i].set_opacity(1)
    if symbol == RESET_COLORS_KEY:
      for t in [*self.pre_text, *self.pos_text]:
        t.set_color(WHITE)
        t.highlight = False
    if symbol == HIGHLIGHT_FORMULA_KEY:
      if self.selected_index is not None:
        self.pre_text[self.selected_index].set_color(GREEN)
        self.pre_text[self.selected_index].highlight = True
      for i,t in enumerate(self.pos_text):
        if self.is_hover(t):
          t.set_color(TEAL)
          t.highlight = True
    if symbol == SHOW_HIGHLIGHT_INDEXES_KEY:
      pre_arr = [t.subindex for t in self.pre_text if t.highlight == True]
      pos_arr = [t.subindex for t in self.pos_text if t.highlight == True]
      print(f"PRE_TEXT ~~~~")
      print(f"*[\n  Animation(mob[__i],)\n  for __i in {pre_arr}\n]\n")
      print(f"*[\n  Animation(mob[__i],)\n  for __i in {pos_arr}\n]\n")
      print(f"POS_TEXT ~~~~")
    if symbol == SIZE_POS_FORMULA_KEY:
      self.scroll_type = "pos"
    if symbol == SIZE_PRE_FORMULA_KEY:
      self.scroll_type = "pre"
    if symbol == MOVE_PRE_FORMULA_KEY:
      self.changing_size == True
      self.moving_formula = self.pre_text
    if symbol == MOVE_POS_FORMULA_KEY:
      self.changing_size == True
      self.moving_formula = self.pos_text
    if symbol == NEXT_FORMULAS_KEY:
      if self.step_formula < len(self.formula_list)-1:
        self.step_formula += 1
        self.reset_all()
        self.index_label.become(self.get_index_label())
    if symbol == PREV_FORMULAS_KEY:
      if self.step_formula > 0:
        self.step_formula -= 1
        self.reset_all()
        self.index_label.become(self.get_index_label())
    if symbol == RESET_KEY:
      self.reset_all()
    if symbol == PREVIEW_KEY:
      self.preview_animation()
    if symbol == INCREASE_RUN_TIME_KEY:
      self.anim_run_time += 0.5
      self.anim_run_time_label.become(self.get_anim_run_time_label())
    if symbol == DECREASE_RUN_TIME_KEY:
      self.anim_run_time -= 0.5
      self.anim_run_time_label.become(self.get_anim_run_time_label())
    if symbol == WRITE_KEY:
      self.write_indexes_to_file()
    if symbol == PRINT_KEY:
      self.print_indexes_file()
    if symbol == USE_RADIUS_KEY:
      self.use_radius = True

  def preview_animation(self):
    global GTO
    pre_text = self.pre_text.copy()
    pos_text = self.pos_text.copy()
    pre_text.set_color(WHITE)
    pos_text.set_color(WHITE)
    pos_text_phantom = pos_text.copy()
    pos_text_phantom.fade(0.9)
    self.pre_text.set_opacity(0)
    self.pos_text.set_opacity(0)
    self.add(pre_text, pos_text_phantom)
    arr = []

    for i,_ in enumerate(self.pre_text):
      f  = [ GTO(pos, i) for pos in self.pos_text ]
      f3 = [ f"{i}{_f[1]}" for _f in f if _f is not None ]
      f4 = [ _f[0] for _f in f if _f is not None ]
      if len(f3) > 0:
        sub_arr = zip(f3, f4)
        for _arr in sub_arr:
          arr.append(_arr)

    anims = index_animation(
        pre_text,
        pos_text,
        arr,
        run_time=self.anim_run_time
    )
    print("-- Running animation --")

    self.play(*anims)
    self.wait()

    self.pre_text.set_opacity(1)
    self.pos_text.set_opacity(1)
    self.remove(*pos_text)
    self.remove(pre_text, pos_text)
    self.remove(pos_text_phantom)
    del pre_text
    del pos_text

  def reset_all(self):
    self.remove(*self.mobjects)
    self.set_init_attrs()
    self.get_pre_and_pos_text_from_step(True)
    self.add_init_mobs()

  def change_size_pre_formula(self, scale=1.05):
    self.changing_size = True
    self.pre_text.scale(scale)
    self.phantom_pre_text.scale(scale)
    self.set_indexes()
    if len(self.history_states) > 0:
      for h in self.history_states:
        h.set_height(self.pre_text.get_height())
    else:
      self.pre_text.saved_state.set_height(self.pre_text.get_height())

  def change_size_pos_formula(self, scale=1.05):
      self.changing_size = True
      self.pos_text.scale(scale)
      self.phantom_pos_text.scale(scale)
      self.set_indexes()

  def on_key_release(self, symbol, modifiers):
    if symbol == MOVE_POS_FORMULA_KEY:
      self.phantom_pos_text.move_to(self.cursor_dot.get_center())
      self.pos_text.move_to(self.cursor_dot.get_center())
      self.set_indexes()
    if symbol == MOVE_PRE_FORMULA_KEY:
      self.pre_text.move_to(self.cursor_dot.get_center())
      self.phantom_pre_text.move_to(self.cursor_dot.get_center())
      self.set_indexes()
      if len(self.history_states) > 0:
        for h in self.history_states:
          h.move_to(self.pre_text)
      else:
        self.pre_text.saved_state.move_to(self.pre_text)
    if symbol == SHOW_INDEXES_KEY:
      self.pre_indexes.set_opacity(0)
      self.pos_indexes.set_opacity(0)
      self.pos_indexes.set_color(WHITE)
      self.pre_indexes.set_color(WHITE)
      self.phantom_pre_text.set_opacity(0)
      self.phantom_pos_text.set_opacity(0)
    if symbol in [SIZE_PRE_FORMULA_KEY, SIZE_POS_FORMULA_KEY]:
      self.scroll_type = "radius"
    if symbol == MOVE_PRE_FORMULA_KEY \
    or symbol == MOVE_POS_FORMULA_KEY:
      self.changing_size == False
      self.moving_formula = None
      self.scroll_type = "radius"
    if symbol == USE_RADIUS_KEY:
      self.use_radius = False

  def on_mouse_drag(self, *args):
    pass

  def on_mouse_scroll(self, *args):
    offset = args[1]
    dx = np.sign(offset[1])
    if self.scroll_type == "pre":
        self.change_size_pre_formula(1 + 0.05 * dx)
    elif self.scroll_type == "pos":
        self.change_size_pos_formula(1 + 0.05 * dx)
    elif self.scroll_type == "radius":
        self.radius_circle.scale(1 + 0.1 * dx)

  def write_indexes_to_file(self):
    index_file = f"{self.indexes_file_name}.md"
    f = open(index_file, "a")
    pre_arr = [t.subindex for t in self.pre_text if t.highlight == True]
    pos_arr = [t.subindex for t in self.pos_text if t.highlight == True]

    pre_text = self.pre_text
    pos_text = self.pos_text

    def get_instance_of_text(mob):
      if isinstance(mob, (Text, MarkupText)):
        return "text"
      elif isinstance(mob, StringMobject):
        return "tex_string"
      elif isinstance(mob, (Tex, TexText)):
        return "tex_strings"

    pre_string = getattr(pre_text, get_instance_of_text(pre_text))
    pos_string = getattr(pos_text, get_instance_of_text(pos_text))
    arr = []
    for i,_ in enumerate(self.pre_text):
      f1 = [ GTO(pos, i) for pos in self.pos_text ]
      f3 = [ f"{i}{_f[1]}" for _f in f1 if _f is not None ]
      f4 = [ _f[0] for _f in f1 if _f is not None ]
      if len(f3) > 0:
        arr_zipped = list(zip(f3, f4))
        for sub_arr_zipped in arr_zipped:
          arr.append(f"{sub_arr_zipped},")

    if len(arr) > 0:
      f.write(f"## Step {self.step_formula}\n")
      f.write(f"$$\n{pre_string}\n$$\n")
      f.write(f"$$\n{pos_string}\n$$\n")
      f.write("```\n")
      f.write("[\n  ")
      n_strings = 0
      for el in arr:
        n_strings += len(el)
        f.write(el)
        if n_strings > 30:
          f.write("\n  ")
          n_strings = 0
      f.write("\n]\n")
      f.write("```\n")
    elif len(arr) == 0 and len(pre_arr) + len(pos_arr) > 0:
      # f.write("~~~ ~~~ ~~~ ~~~\n")
      f.write(f"## Step {self.step_formula}\n")
      if len(pre_arr) > 0:
        f.write(f"$$\n{pre_string}\n$$\n")
        f.write("```\n")
        f.write(f"*[\n  Animation(mob[__i],)\n  for __i in {pre_arr}\n]\n")
        f.write("```\n")
      if len(pos_arr) > 0:
        f.write("```\n")
        f.write(f"*[\n  Animation(mob[__i],)\n  for __i in {pos_arr}\n]\n")
        f.write("```\n")
        f.write(f"$$\n{pos_string}\n$$\n")
    else:
      print("You have not selected anything")
      return
    f.write("\n--------------\n")
    f.write("\n")

    f.close()
    print(f"The file {index_file} has been created successfully")
    print("To print the file press C key")

  def print_indexes_file(self):
    import os.path
    index_file = f"{self.indexes_file_name}.md"
    if os.path.isfile(f"./{index_file}"):
      print(f"=============== {index_file} ================")
      f = open(index_file, "r")
      print(f.read())
      f.close()
    else:
      print(f"File {index_file} does't exist")

from moderngl import Texture
from manim_imports_custom import *
from char_creature.char_creature import CharCreature, ShowBubble, RoundBubble

class ACreature(CharCreature):
  def __init__(self, eyes_scale=2.7,
                     eyes_prop=[0.5,0.1],
                     eyes_buff=0.09,
                     body_scale=7,
                     color=TEAL,
                     **kwargs):
    body = Tex("A").scale(body_scale).set_color(color)
    super().__init__(body,
                     eyes_scale=eyes_scale,
                     eyes_prop=eyes_prop,
                     eyes_buff=eyes_buff,
                     **kwargs)

class OmegaCreature(CharCreature):
  def __init__(self, eyes_scale=2.7,
                     eyes_prop=[0.5,0.05],
                     eyes_buff=0.09,
                     body_scale=7,
                     color=RED,
                     **kwargs):
    body = Tex("\\Omega").scale(body_scale).set_color(color)
    super().__init__(body,
                     eyes_scale=eyes_scale,
                     eyes_prop=eyes_prop,
                     eyes_buff=eyes_buff,
                     **kwargs)


class TCreature(CharCreature):
  def __init__(self, eyes_scale=2.7,
                     eyes_prop=[0.5,0.25],
                     eyes_buff=0,
                     body_scale=7,
                     color=RED,
                     **kwargs):
    body = Tex("t").scale(body_scale).set_color(color)
    super().__init__(body,
                     eyes_scale=eyes_scale,
                     eyes_prop=eyes_prop,
                     eyes_buff=eyes_buff,
                     **kwargs)



class Example1(Scene):
  def construct(self):
    # start
    a_creature = ACreature().to_corner(DL)
    omega_creature = OmegaCreature()
    omega_creature.next_to(a_creature, UP).to_edge(RIGHT)
    t_creature = TCreature().to_corner(UL)

    a_bubble = RoundBubble(R"""\flushleft
    This is an example of how to use \\
    {\tt CharCreature}, you can define the \\
    Char and eyes position.
    """, a_creature.get_right(), RIGHT)

    o_bubble = RoundBubble(R"""\flushleft
    You can also animate the blinking of\\
    the eyes and move them to positions\\
    on the screen.
    """, omega_creature.get_left(), LEFT, flip=UP)
    t_bubble = RoundBubble("WOW, that's amazing!", t_creature.get_right())
    self.play(FadeIn(a_creature, omega_creature))
    self.play(a_creature.look_at(UP * 0.3 + RIGHT))
    self.play(a_creature.blink())
    self.play(omega_creature.look_at(DOWN * 0.3 + LEFT))
    self.play(omega_creature.blink())
    self.play(ShowBubble(a_bubble))
    self.play(omega_creature.blink())
    self.play(ShowBubble(o_bubble))
    self.wait()
    self.play(FadeIn(t_creature))
    self.play(ShowBubble(t_bubble))
    self.play(
      a_creature.look_at(UP),
      omega_creature.look_at(UP * 0.3 + LEFT),
    )
    self.play(t_creature.blink())
    self.play(a_creature.blink())
    self.play(omega_creature.blink())
    self.wait(3)

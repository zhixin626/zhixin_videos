from numpy.random import normal
from manimlib import *

LEFT_EYE_INDEX = 0
RIGHT_EYE_INDEX = 1
LEFT_PUPIL_INDEX = 2
RIGHT_PUPIL_INDEX = 3
BODY_INDEX = 4
MOUTH_INDEX = 5

EYES_SVG = "char/omega_creature_y.svg"
EYES_SVG2 = "char/eye.svg"
BUBBLE_SVG = "char/Bubbles_speech.svg"

get_norm = np.linalg.norm
class test2(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        kun=SVGMobject("char/kun2")
        kun.scale(3)
        kun.remove(kun[5])
        kun[10:13].set_stroke(WHITE,1)  #body,strips
        kun[6:8].set_stroke(WHITE,1)     # arm
        kun[14:17].set_stroke(BLACK,1)   # 篮球线
        kun[2:4].match_color(kun[9])  #腮红
        kun[13].match_color(kun[4])    # 篮球
        mouth=kun[4]
        index=index_labels(kun) 
        # self.add(kun)
        # self.add(kun[10:13])

        # testclass
        kun2=Kun()
        kun2.scale(3)
        self.add(kun2)
        dot=Dot(np.array([-4,2,0]))
        self.add(dot)
        line=Line(dot.get_center(),kun2.right_eye[0].get_center())
        self.add(line)
        self.play(kun2.animate.look(dot))

        # define new eye
        ax=Axes()
        self.add(ax)
        eye=Circle(radius=1)
        iris=Circle(radius=0.5)
        pupil=Circle(radius=0.1)
        eye.set_style(stroke_color=WHITE,stroke_opacity=0,stroke_width=1
          ,fill_color=WHITE,fill_opacity=1)
        iris.set_style(stroke_color=BLACK,stroke_opacity=0,stroke_width=1
          ,fill_color=BLACK,fill_opacity=1)
        pupil.set_style(stroke_color=WHITE,stroke_opacity=0,stroke_width=1
          ,fill_color=WHITE,fill_opacity=1)
        eye_grp=VGroup(eye,iris,pupil)
        eye_grp.shift(LEFT)
        dot=Dot(np.array([-3,2,2]))
        def get_projection_point(n,p1,p2):
          factor=((np.dot(n,p1)-np.dot(n,p2)))/np.linalg.norm(n)**2
          return factor*n+p2
        self.add(dot)
        half_width=kun[1].get_width()/2
        factor_width=0.4
        left_eye=eye_grp.copy()
        right_eye=eye_grp.copy()
        left_eye.set_width(half_width*factor_width)
        left_eye.move_to(kun[1]).shift(LEFT*half_width*factor_width)
        right_eye.set_width(half_width*factor_width)
        right_eye.move_to(kun[1]).shift(RIGHT*half_width*factor_width)
        self.add(left_eye,right_eye)
        def get_direction(eye,mob):
          ratio_iris=0.8
          ratio_pupil=0.9
          unit_norm=eye[0].get_unit_normal()
          p_dot_coord=get_projection_point(unit_norm,eye[0].get_center(),mob.get_center())
          direction1=(ratio_iris*(eye[0].get_radius()-eye[1].get_radius()))*normalize(p_dot_coord-eye[0].get_center())
          direction2=(ratio_pupil*(eye[1].get_radius()-eye[2].get_radius()))*normalize(p_dot_coord-eye[0].get_center())+direction1
          return direction1,direction2
        d1,d2=get_direction(left_eye,dot)
        d3,d4=get_direction(right_eye,dot)
        self.play(left_eye[1].animate.shift(d1),left_eye[2].animate.shift(d2),
          right_eye[1].animate.shift(d3),right_eye[2].animate.shift(d4))
        
        # mouth
        new_kun=VGroup(kun,left_eye,right_eye)
        new_kun.center()
        shift_up=(mouth.get_top()-mouth.get_bottom())*0.25
        shift_down=(mouth.get_bottom()-mouth.get_top())*0.25
        shift_right=(mouth.get_right()-mouth.get_left())*0.1
        shift_left=(mouth.get_left()-mouth.get_right())*0.1
        p1=mouth.get_left()+shift_right
        p2=mouth.get_right()+shift_left
        peace=Line(p1,p2)
        smile=VMobject().set_points_smoothly([p1,mouth.get_bottom()+shift_up,p2])
        sad=VMobject().set_points_smoothly([p1,mouth.get_top()+shift_down,p2])
        peace.set_stroke(BLACK,5)
        smile.set_stroke(BLACK,5)
        sad.set_stroke(BLACK,5)
        
        self.add(peace)
        self.play(ReplacementTransform(peace,smile))
        self.play(ReplacementTransform(smile,sad))
        
class Kun(SVGMobject):
    def __init__(self,**kwargs) -> None:
       super().__init__(
        file_name="char/kun2",**kwargs)
       self.init_structrue()
    def init_structrue(self):
      # self.scale(3)
      self.remove(self[5]) #remove lip  
      self.neck=self[0]
      self.face=self[1]
      self.cheek=self[2:4] # 腮红 cheek color
      self.mouth=self[4]
      self.hair=self[5]
      self.arms=self[6:8]
      self.feet=self[8:10]
      self.body=self[10]
      self.strips=self[11:13]
      self.basketball=self[13]
      self.basketball_lines=self[14:17]
      self.init_eyes()
      self.init_lip()
      self.set_submobjects([self.feet,self.arms,self.basketball,self.basketball_lines,
        self.neck,self.face,self.cheek,self.mouth,self.left_eye,
        self.right_eye,self.lip,self.hair,self.body,self.strips])
    def init_style(self):
      self.neck.set_color("#F7D289")
      self.arms.set_stroke(WHITE,1) # arm
      self.strips.set_stroke(WHITE,1)
      self.body.set_stroke(WHITE,1).set_fill(BLACK,1)
      self.basketball_lines.set_stroke(BLACK,1)   # 篮球线 
      self.basketball.set_color("#FF8800")    # 篮球
      self.cheek.set_color("#FF0000")
    def init_eyes(self):
      eye=Circle(radius=1)
      iris=Circle(radius=0.5)
      pupil=Circle(radius=0.1)
      eye.set_style(stroke_color=BLACK,stroke_opacity=1,stroke_width=1
        ,fill_color=WHITE,fill_opacity=1)
      iris.set_style(stroke_color=BLACK,stroke_opacity=0,stroke_width=1
        ,fill_color=BLACK,fill_opacity=1)
      pupil.set_style(stroke_color=WHITE,stroke_opacity=0,stroke_width=1
        ,fill_color=WHITE,fill_opacity=1)
      eye_grp=VGroup(eye,iris,pupil)
      half_width=self.face.get_width()/2
      factor_width=0.4
      left_eye=eye_grp.copy()
      right_eye=eye_grp.copy()
      left_eye.set_width(half_width*factor_width)
      left_eye.move_to(self.face).shift(LEFT*half_width*factor_width)
      right_eye.set_width(half_width*factor_width)
      right_eye.move_to(self.face).shift(RIGHT*half_width*factor_width)
      self.left_eye=left_eye
      self.right_eye=right_eye
    def init_lip(self):
      shift_right=(self.mouth.get_right()-self.mouth.get_left())*0.1
      shift_left=(self.mouth.get_left()-self.mouth.get_right())*0.1
      p1=self.mouth.get_left()+shift_right
      p2=self.mouth.get_right()+shift_left
      peace=Line(p1,p2)
      peace.set_stroke(BLACK,5)
      self.lip=peace
    def get_projection_point(self,n,p1,p2):
      factor=((np.dot(n,p1)-np.dot(n,p2)))/np.linalg.norm(n)**2
      return factor*n+p2
    def get_direction(self,eye,mob):
      ratio_iris=0.8
      ratio_pupil=0.9
      unit_norm=eye[0].get_unit_normal()
      p_dot_coord=self.get_projection_point(unit_norm,eye[0].get_center(),mob.get_center())
      direction1=(ratio_iris*(eye[0].get_radius()-eye[1].get_radius()))*normalize(p_dot_coord-eye[0].get_center())
      direction2=(ratio_pupil*(eye[1].get_radius()-eye[2].get_radius()))*normalize(p_dot_coord-eye[0].get_center())+direction1
      return direction1,direction2
    def look(self,mob):
      d1,d2=self.get_direction(self.left_eye,mob)
      d3,d4=self.get_direction(self.right_eye,mob)
      self.left_eye[1].move_to(self.left_eye[0].get_center()+d1)
      self.left_eye[2].move_to(self.left_eye[0].get_center()+d2)
      self.right_eye[1].move_to(self.right_eye[0].get_center()+d3)
      self.right_eye[2].move_to(self.right_eye[0].get_center()+d4)
      return self
    def smile(self):
      shift_up=(self.mouth.get_top()-self.mouth.get_bottom())*0.25
      shift_down=(self.mouth.get_bottom()-self.mouth.get_top())*0.25
      shift_right=(self.mouth.get_right()-self.mouth.get_left())*0.1
      shift_left=(self.mouth.get_left()-self.mouth.get_right())*0.1
      p1=self.mouth.get_left()+shift_right
      p2=self.mouth.get_right()+shift_left
      smile=VMobject().set_points_smoothly([p1,self.mouth.get_bottom()+shift_up,p2])
      smile.set_stroke(BLACK,5)
      self.lip.become(smile)
      return self
    def sad(self):
      shift_up=(self.mouth.get_top()-self.mouth.get_bottom())*0.25
      shift_down=(self.mouth.get_bottom()-self.mouth.get_top())*0.25
      shift_right=(self.mouth.get_right()-self.mouth.get_left())*0.1
      shift_left=(self.mouth.get_left()-self.mouth.get_right())*0.1
      p1=self.mouth.get_left()+shift_right
      p2=self.mouth.get_right()+shift_left
      sad=VMobject().set_points_smoothly([p1,self.mouth.get_top()+shift_down,p2])
      sad.set_stroke(BLACK,5)
      self.lip.become(sad)
      return self


class Eyes(SVGMobject):
  def __init__(self, eyes_buff=0.1, **kwargs):
    super().__init__(EYES_SVG2, **kwargs)
    self.name_parts(eyes_buff)
    self.init_pupils()

  def name_parts(self, eyes_buff):
    self.pupils = VGroup(
      self.submobjects[LEFT_PUPIL_INDEX],
      self.submobjects[RIGHT_PUPIL_INDEX]
    )
    self.eyes = VGroup(
      self.submobjects[LEFT_EYE_INDEX],
      self.submobjects[RIGHT_EYE_INDEX]
    )
    self.submobjects.remove(self.submobjects[MOUTH_INDEX])
    self.submobjects.remove(self.submobjects[BODY_INDEX])
    self.eyes.set_color(WHITE)
    self.eyes.set_stroke(width=4, color=BLACK)
    self.eye_parts = VGroup(self.eyes, self.pupils)
    self.eyes_parts = VGroup(
      VGroup(self.pupils[0], self.eyes[0]),
      VGroup(self.pupils[1], self.eyes[1]),
    )
    self.eyes_parts.arrange(RIGHT, buff=eyes_buff)
    self.parts_named = True

  def init_pupils(self):
    for eye, pupil in zip(self.eyes, self.pupils):
      pupil_r = eye.get_width() / 2
      pupil_r *= self.pupil_to_eye_width_ratio
      dot_r = pupil_r
      dot_r *= self.pupil_dot_to_pupil_width_ratio

      new_pupil = Circle(
        radius=pupil_r,
        color=BLACK,
        fill_opacity=1,
        stroke_width=0,
      )
      dot = Circle(
        radius=dot_r,
        color=WHITE,
        fill_opacity=1,
        stroke_width=0,
      )
      new_pupil.move_to(pupil)
      pupil.become(new_pupil)
      dot.shift(
        new_pupil.get_boundary_point(UL) -
        dot.get_boundary_point(UL)
      )
      pupil.add(dot)

  def look(self, direction):
    direction = direction.copy()
    norm = get_norm(direction)
    if norm == 0:
      return
    direction /= norm
    # VMobject.purposeful_looking_direction
    # self.purposeful_looking_direction = direction
    for pupil, eye in zip(self.pupils.split(), self.eyes.split()):
      c        = eye.get_center()
      right    = eye.get_right() - c
      up       = eye.get_top() - c
      vect     = direction[0] * right + direction[1] * up
      v_norm   = get_norm(vect)
      p_radius = pupil.get_width() / 2
      vect    *= (v_norm - 0.75 * p_radius) / v_norm
      pupil.move_to(c + vect)
    self.pupils[1].align_to(self.pupils[0], DOWN)
    return self

  def look_at(self, point_or_mobject):
    if isinstance(point_or_mobject, Mobject):
      point = point_or_mobject.get_center()
    else:
      point = point_or_mobject
    self.look(point - self.eye_parts.get_center())
    return self

  def blink(self):
    eye_parts    = self.eye_parts
    eye_bottom_y = eye_parts.get_center()[1]
    eye_parts.apply_function(
      lambda p: [p[0], eye_bottom_y, p[2]]
    )
    return self

  def anim_blink(self, **kwargs):
    if "rate_func" not in kwargs.keys():
      kwargs["rate_func"] = there_and_back
    return self.animate(**kwargs).blink()

  def anim_look_at(self, pom, **kwargs):
    return self.animate(**kwargs).look_at(pom)

  def anim_look(self, pom, **kwargs):
    return self.animate(**kwargs).look(pom)


class Bubble(SVGMobject):
    def __init__(self, 
                 direction=LEFT,
                 center_point=ORIGIN,
                 content_scale_factor=0.75,
                 height=5, width=8,
                 bubble_center_adjustment_factor = 1. / 8,
                 fill_opacity=0,
                 **kwargs):
        super().__init__(BUBBLE_SVG, fill_opacity=fill_opacity, **kwargs)
        self.direction = direction
        self.center_point = center_point
        self.content_scale_factor = content_scale_factor
        self._width = width
        self._height = height
        self.bubble_center_adjustment_factor = bubble_center_adjustment_factor
        self.center()
        self.stretch_to_fit_height(self._height)
        self.stretch_to_fit_width(self._width)
        if self.direction[0] > 0:
            Mobject.flip(self)
        self.direction_was_specified = ("direction" in kwargs)
        self.content = Mobject()
        self.set_style(stroke_width=3, stroke_opacity=1)

    def get_tip(self):
        # return self.get_corner(DOWN + self.direction) - 0.6 * self.direction
        return self.submobjects[0].get_all_points()[4]

    def get_bubble_center(self):
        factor = self.bubble_center_adjustment_factor
        return self.get_center() + factor * self.get_height() * UP

    def move_tip_to(self, point):
        mover = VGroup(self)
        if self.content is not None:
            mover.add(self.content)
        mover.shift(point - self.get_tip())
        return self

    def _flip(self, **kwargs):
        Mobject.flip(self, **kwargs)
        self.direction = -np.array(self.direction)
        return self

    def pin_to(self, mobject):
        mob_center = mobject.get_center()
        want_to_flip = np.sign(mob_center[0]) != np.sign(self.direction[0])
        can_flip = not self.direction_was_specified
        if want_to_flip and can_flip:
            self.flip()
        boundary_point = mobject.get_critical_point(UP - self.direction)
        vector_from_center = 1.0 * (boundary_point - mob_center)
        self.move_tip_to(mob_center + vector_from_center)
        return self

    def position_mobject_inside(self, mobject):
        scaled_width = self.content_scale_factor * self.get_width()
        if mobject.width > scaled_width:
            mobject.set(width=scaled_width)
        mobject.shift(
            self.get_bubble_center() - mobject.get_center()
        )
        return mobject

    def add_content(self, mobject):
        self.position_mobject_inside(mobject)
        self.content = mobject
        return self.content

    def write(self, *text):
        self.add_content(Tex(*text))
        return self

    def resize_to_content(self):
        target_width = self.content.get_width()
        target_width += max(MED_LARGE_BUFF, 2)
        target_height = self.content.get_height()
        target_height += 2.5 * LARGE_BUFF
        tip_point = self.get_tip()
        self.stretch_to_fit_width(target_width)
        self.stretch_to_fit_height(target_height)
        self.move_tip_to(tip_point)
        self.position_mobject_inside(self.content)

    def clear(self):
        self.add_content(VMobject())
        return self


class CharCreature(VGroup):
  def __init__(self, body=Tex("A"), eyes_scale=1, eyes_prop=[0,0], **kwargs):
    super().__init__()
    eyes  = Eyes(**kwargs).scale(eyes_scale)
    vline = Line(body.get_corner(UL), body.get_corner(UR))
    hline = Line(body.get_corner(UL), body.get_corner(DL))
    eyes_center = [
      vline.point_from_proportion(eyes_prop[0])[0],
      hline.point_from_proportion(eyes_prop[1])[1],
      0
    ]
    eyes.move_to(np.array(eyes_center))
    self.eyes = eyes
    self.body = body
    self.add(body, eyes)

  def blink(self, **kwargs):
    return self.eyes.anim_blink(**kwargs)

  def set_color_body(self, color):
    self.body.set_color(color)

  def add_text(self, tex: Tex, position=ORIGIN, flip=False, resize_content=True):
    bubble = Bubble()
    if flip:
      bubble.flip()
    t = bubble.add_content(tex)
    if resize_content:
      bubble.resize_to_content()
    bubble.move_tip_to(position)
    bubble.match_color(tex)
    self.bubble = VGroup(bubble.submobjects[0], t)
    self.subbubble = bubble

  def position_to_bubble(self, mob):
    self.subbubble.position_mobject_inside(mob)

  def change_bubble(self):
    b = self.bubble[0]
    n = VMobject().set_points(b.get_all_points()[8:])
    n.match_style(b)
    self.bubble[0].become(n)

  def add_tip(self, point):
    b = self.bubble[0]
    tip = VMobject().set_points_as_corners([
      b.get_start(),
      point,
      b.get_end()
    ])
    n = VMobject().set_points([
      *b.get_all_points(), *tip.get_all_points()
    ])
    n.match_style(b)
    b.become(n)

  def look_at(self, *args, **kwargs):
    return self.eyes.anim_look(*args, **kwargs)

  def add_custom_bubble(self, tex: Tex, scale=1.2, direction=ORIGIN, buff=0.1, tip=LEFT, **kwargs):
    self.add_text(tex, **kwargs)
    self.bubble.scale(scale)
    self.change_bubble()
    self.bubble.next_to(self, direction, buff=buff)
    self.add_tip(tip)

  def add_custom_bubble_move(self, tex: Tex, scale=1.2, funcs=lambda x: x, tip=LEFT, **kwargs):
    self.add_text(tex, **kwargs)
    self.bubble.scale(scale)
    self.change_bubble()
    funcs(self.bubble)
    self.add_tip(tip)


class Acreature(CharCreature):
  def __init__(self, eyes_scale=1, eyes_prop=[0.5,0.1], eyes_buff=0.09, body_scale=2, **kwargs):
    body = Tex("A").scale(body_scale).set_color("#2F346C")
    super().__init__(body, eyes_scale=eyes_scale, eyes_prop=eyes_prop, eyes_buff=eyes_buff, **kwargs)


class Pcreature(CharCreature):
  def __init__(self, eyes_scale=0.8, eyes_prop=[0.5,0.15], eyes_buff=0.03, body_scale=2, **kwargs):
    body = Tex("P").scale(body_scale)
    super().__init__(body, eyes_scale=eyes_scale, eyes_prop=eyes_prop, eyes_buff=eyes_buff, **kwargs)



class Test1(Scene):
  def construct(self):
    self.camera.background_color = WHITE
    bubble = Bubble().set_color(BLACK)

    dot = Dot(bubble.submobjects[0].get_start()).set_color(RED)
    self.add(dot, bubble)


class RoundBubble(VGroup):
  def __init__(self, 
               text,
               bubble_start,
               direction=RIGHT,
               start_alpha=0.03,
               end_alpha=0.97,
               border_buff=0.2,
               round_radius=0.1,
               buff=0.4,
               rotate=True,
               flip=None,
               tex_class=TexText,
               font_size=40,
               shift=ORIGIN,
               **kwargs):
    super().__init__(**kwargs)
    tex = tex_class(text, font_size=font_size)
    r = Rectangle(width=(tex.get_width()+border_buff), height=(tex.get_height()+border_buff), **kwargs)
    r.round_corners(round_radius)
    r.move_to(tex)
    bubble = r.get_subcurve(start_alpha, end_alpha)
    if rotate:
      bubble.rotate(PI)
    if flip is not None:
      bubble.flip(flip)
    VGroup(tex, bubble)\
        .next_to(bubble_start, direction, buff=buff)\
        .shift(shift)
    tip = VMobject().set_points_as_corners([
      bubble.get_start(),
      bubble_start,
      bubble.get_end(),
    ]).match_style(r)
    complete_bubble = VMobject(**kwargs).set_points([
      *bubble.get_points(), *tip.get_points()
    ])
    self.tex = tex
    self.bubble = complete_bubble
    self.add(tex, complete_bubble)

class ShowBubble(AnimationGroup):
  def __init__(self, bubble, lag_ratio=0.1, **kwargs):
    self.bubble = bubble
    super().__init__(
      ShowCreation(bubble.bubble),
      Write(bubble.tex),
      lag_ratio=lag_ratio,
      **kwargs
    )

  def clean_up_from_scene(self, scene: Scene) -> None:
    scene.add(self.bubble)
    return super().clean_up_from_scene(scene)

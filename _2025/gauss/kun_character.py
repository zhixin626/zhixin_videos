from manim_imports_custom import *


class test_character(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        frame.reorient(0, 0, 0, (0.6, 0.2, 0.0), 4.19)
        kun=Kun()
        self.add(kun)
        self.play(kun.animate.sad())
        self.play(kun.animate.smile())

class Kun(SVGMobject):
    def __init__(self,_file_name="SVG/kun",stroke_color=BLACK,stroke_width=3,**kwargs):
        self._stroke_color=stroke_color
        self._stroke_width=stroke_width
        super().__init__(
        file_name=_file_name,stroke_color=self._stroke_color,stroke_width=self._stroke_width,**kwargs)
        self.init_structrue()
        self.init_eye_position()
        self.scale(1.5)
    def reset_color(self):
        self.body.set_style(fill_color="#fed573",fill_opacity=1,stroke_color=BLACK,
            stroke_width=3,stroke_opacity=1)
        for mob in self.basketball:
            mob.set_style(fill_color="#ec8931",fill_opacity=1,stroke_color=BLACK,stroke_width=3,stroke_opacity=1)
        self.pant.set_style(fill_color="#808080",fill_opacity=1,stroke_color=BLACK,stroke_width=3,stroke_opacity=1)
        self.hair.set_style(fill_color="#808080",fill_opacity=1,stroke_color=BLACK,stroke_width=3,stroke_opacity=1)
        self.strips.set_style(fill_color=WHITE,fill_opacity=1,stroke_color=BLACK,stroke_width=3,stroke_opacity=1)
        self.cheek1.set_style(fill_color="#ff0000",fill_opacity=1,stroke_color=BLACK,stroke_width=3,stroke_opacity=1)
        self.cheek2.set_style(fill_color="#ff0000",fill_opacity=1,stroke_color=BLACK,stroke_width=3,stroke_opacity=1)
        self.eye1_outline.set_style(fill_color=WHITE,fill_opacity=1,stroke_color=BLACK,stroke_width=3,stroke_opacity=1)
        self.eye2_outline.set_style(fill_color=WHITE,fill_opacity=1,stroke_color=BLACK,stroke_width=3,stroke_opacity=1)
        self.eye1_iris.set_style(fill_color=BLACK,fill_opacity=1,stroke_color=BLACK,stroke_width=0,stroke_opacity=1)
        self.eye2_iris.set_style(fill_color=BLACK,fill_opacity=1,stroke_color=BLACK,stroke_width=0,stroke_opacity=1)
        self.eye1_pupil.set_style(fill_color=WHITE,fill_opacity=1,stroke_color=BLACK,stroke_width=0,stroke_opacity=1)
        self.eye2_pupil.set_style(fill_color=WHITE,fill_opacity=1,stroke_color=BLACK,stroke_width=0,stroke_opacity=1)
        self.mouth_out.set_style(fill_color="#ec8931",fill_opacity=1,stroke_color=BLACK,stroke_width=3,stroke_opacity=1)
        self.mouth_in.set_style(fill_color="#ff0000",fill_opacity=1,stroke_color=BLACK,stroke_width=3,stroke_opacity=1)   # 也许有问题当sad
        return self
    def init_structrue(self):
        parts=self.submobjects
        self.body=parts[0]
        self.basketball=parts[1:5]
        self.pant=parts[5]
        self.strips=parts[6]
        self.cheek1=parts[9]
        self.cheek2=parts[10]
        self.eye1_outline=parts[7]
        self.eye1_iris=parts[8]
        self.eye1_pupil=parts[11]
        self.eye2_outline=parts[12]
        self.eye2_iris=parts[13]
        self.eye2_pupil=parts[14]
        self.mouth_out=parts[15]
        self.mouth_in=parts[16]
        self.hair=parts[17]
        self.left_eye=Group(parts[7],parts[8],parts[11])
        self.right_eye=Group(parts[12],parts[13],parts[14])
        self.init_mouth()
        for submob in self.submobjects:
            submob.insert_n_curves(100)
    def init_mouth(self):
        default=SVGMobject("SVG/little_smile",stroke_color=BLACK,stroke_width=3)
        mouth_position=(self.cheek1.get_center()+self.cheek2.get_center())/2
        self.mouth_out.move_to(mouth_position)
        default.replace(self.mouth_out)
        default[0].insert_n_curves(100)
        default[1].insert_n_curves(100)
        self.mouth_out.become(default[0])
        self.mouth_in.become(default[1])
    def smile(self):
        smile=SVGMobject("SVG/smile",stroke_color=BLACK,stroke_width=3)
        smile.replace(self.mouth_out)
        smile[0].insert_n_curves(100)
        smile[1].insert_n_curves(100)
        self.mouth_out.become(smile[0])
        self.mouth_in.become(smile[1])
        return self
    def sad(self):
        sad=SVGMobject("SVG/sad",stroke_color=BLACK,stroke_width=3)
        sad.replace(self.mouth_out)
        sad.insert_n_curves(100)
        self.mouth_out.become(sad[0])
        self.mouth_in.become(sad[0])
        return self
    def shock(self):
        shock=SVGMobject("SVG/shock",stroke_color=BLACK,stroke_width=3)
        shock.replace(self.mouth_out)
        shock[0].insert_n_curves(100)
        shock[1].insert_n_curves(100)
        self.mouth_out.become(shock[0])
        self.mouth_in.become(shock[1])
        return self
    def default(self):
        default=SVGMobject("SVG/little_smile",stroke_color=self._stroke_color,stroke_width=self._stroke_width)
        default.replace(self.mouth_out)
        default[0].insert_n_curves(100)
        default[1].insert_n_curves(100)
        self.mouth_out.become(default[0])
        self.mouth_in.become(default[1])
        return self
    def peace(self):
        peace=SVGMobject("SVG/peace",stroke_color=self._stroke_color,stroke_width=self._stroke_width)
        peace.replace(self.mouth_out)
        peace[0].insert_n_curves(100)
        peace[1].insert_n_curves(100)
        self.mouth_out.become(peace[0])
        self.mouth_in.become(peace[1])
        return self
    def init_eye_position(self):
        self.eye1_iris.move_to(self.eye1_outline)
        self.eye1_pupil.move_to(self.eye1_outline)
        self.eye2_iris.move_to(self.eye2_outline)
        self.eye2_pupil.move_to(self.eye2_outline)
    def get_projection_point(self,n,p1,p2):
        factor=((np.dot(n,p1)-np.dot(n,p2)))/np.linalg.norm(n)**2
        return factor*n+p2
    def look(self,directon):
        point1=self.eye1_outline.get_center()+directon
        point2=self.eye2_outline.get_center()+directon
        d1,d2=self.get_direction(self.left_eye,point1)
        d3,d4=self.get_direction(self.right_eye,point2)
        self.eye1_iris.move_to(self.eye1_outline.get_center()+d1)
        self.eye1_pupil.move_to(self.eye1_outline.get_center()+d2)
        self.eye2_iris.move_to(self.eye2_outline.get_center()+d3)
        self.eye2_pupil.move_to(self.eye2_outline.get_center()+d4)
        return self
    def get_direction(self,eye,point_or_mob):
        ratio_iris=0.8
        ratio_pupil=0.9
        unit_norm=eye[0].get_unit_normal()
        if isinstance(point_or_mob,Mobject):
          p2=point_or_mob.get_center()
        else:p2=point_or_mob
        p_dot_coord=self.get_projection_point(unit_norm,eye[0].get_center(),p2)
        direction1=(ratio_iris*(eye[0].get_radius()-eye[1].get_radius()))*normalize(p_dot_coord-eye[0].get_center())
        direction2=(ratio_pupil*(eye[1].get_radius()-eye[2].get_radius()))*normalize(p_dot_coord-eye[0].get_center())+direction1
        return direction1,direction2
    def look_at(self,point_or_mob):
        d1,d2=self.get_direction(self.left_eye,point_or_mob)
        d3,d4=self.get_direction(self.right_eye,point_or_mob)
        self.eye1_iris.move_to(self.eye1_outline.get_center()+d1)
        self.eye1_pupil.move_to(self.eye1_outline.get_center()+d2)
        self.eye2_iris.move_to(self.eye2_outline.get_center()+d3)
        self.eye2_pupil.move_to(self.eye2_outline.get_center()+d4)
        return self
    def close_eyes(self):
        eye_bottom_y1 = self.eye1_outline.get_center()[1]
        eye_bottom_y2 = self.eye2_outline.get_center()[1]
        self.eye1_outline.apply_function(lambda p: [p[0], eye_bottom_y1, p[2]])
        self.eye1_iris.apply_function(lambda p: [p[0], eye_bottom_y1, p[2]])
        self.eye1_pupil.apply_function(lambda p: [p[0], eye_bottom_y1, p[2]])
        self.eye2_outline.apply_function(lambda p: [p[0], eye_bottom_y2, p[2]])
        self.eye2_iris.apply_function(lambda p: [p[0], eye_bottom_y2, p[2]])
        self.eye2_pupil.apply_function(lambda p: [p[0], eye_bottom_y2, p[2]])
        return self
    def say(self,content,**kwargs):
        bubble=Bubble(content,pin_point=self.right_eye,**kwargs)
        return Write(bubble)
    def to_frame_corner(self,frame,direction,buff:float=0):
        self.move_to(frame.get_corner(direction))
        shift_vec=self.get_center()-self.get_corner(direction)
        self.shift(shift_vec)
        self.shift(-direction*buff)
        return self
        
        
class YellowChicken(Kun):
    def __init__(self, _file_name="SVG/kun2", stroke_color=BLACK, stroke_width=3, **kwargs):
        super().__init__(_file_name, stroke_color, stroke_width, **kwargs)
    def init_structrue(self):
        parts=self.submobjects
        self.body=parts[0]
        self.cheek1=parts[4]
        self.cheek2=parts[3]
        self.eye1_outline=parts[6]
        self.eye1_iris=parts[7]
        self.eye1_pupil=parts[8]
        self.eye2_outline=parts[1]
        self.eye2_iris=parts[2]
        self.eye2_pupil=parts[5]
        self.mouth_out=parts[9]
        self.mouth_in=parts[10]
        self.left_eye=Group(parts[6],parts[7],parts[8])
        self.right_eye=Group(parts[1],parts[2],parts[5])
        self.init_mouth()
    def say(self,content,**kwargs):
        bubble=Bubble(content,**kwargs).flip()
        bubble.pin_to(self.left_eye)
        return Write(bubble)
    def raise_hand(self):
        new_body=SVGMobject("SVG/body_right",stroke_color=BLACK, stroke_width=3)
        new_body[0].replace(self.body)
        self.body.become(new_body[0])
        self.body.shift(LEFT*0.05)
        if self.is_fixed_in_frame:self.fix_in_frame()
        return self
        


        
        
        

        
        
from manimlib import *
from typing import Optional
# index_labels()

# functions
def fonts():
    return manimpango.list_fonts()


# animations
class FadeInFromPoint2(FadeIn):
    def __init__(self, mobject: Mobject, point,start_opacity=0.6, **kwargs):
        self.start_opacity=start_opacity
        super().__init__(
            mobject,
            shift=mobject.get_center() - point,
            scale=np.inf,
            **kwargs,
        )
    def create_starting_mobject(self) -> Mobject:
        start = super().create_starting_mobject()
        start.set_opacity(self.start_opacity)
        start.scale(0)
        # start.shift(-self.shift_vect)
        return start

class FadeOutToPoint2(FadeOut):
    def __init__(self, mobject: Mobject, point,final_opacity=0.3 ,**kwargs):
        self.final_opacity=final_opacity
        super().__init__(
            mobject,
            shift=point - mobject.get_center(),
            scale=0,
            **kwargs,
        )
    def create_target(self) -> Mobject:
        result = self.mobject.copy()
        result.set_opacity(self.final_opacity)
        result.shift(self.shift_vect)
        result.scale(self.scale_factor)
        return result

class TransformFromCopy2(Transform):
    def __init__(self, mobject, target_mobject, **kwargs):
        super().__init__(mobject.copy(), target_mobject.copy(), **kwargs)
    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.remove(self.mobject)
        scene.remove(self.target_mobject)

# class
class ArrowCustom(Arrow):
    def __init__(self,
        start= LEFT,
        angle: float=0,
        length: float=1.5,
        end=None,
        **kwargs):
        direction=np.array([np.cos(angle), np.sin(angle), 0])
        if end is None:
            end = start + length*direction
        else:
            end=end
        super().__init__(start,end,**kwargs)
    def point_to(self,mob,angle:float=0, buff:float=0.2,length:float=1.5):
        if isinstance(mob,Mobject):
            end=mob.get_center()
        else:
            end = np.array(mob)
        direction=np.array([np.cos(angle), np.sin(angle), 0])
        end=end-buff*direction
        start = end - length *direction 
        self.put_start_and_end_on(start, end)
        return self
    def point_from(self,mob,angle:float=0, buff:float=0.2,length:float=1.5):
        if isinstance(mob,Mobject):
            start=mob.get_center()
        else:
            start=np.array(mob)
        direction=np.array([np.cos(angle), np.sin(angle), 0])
        start=start+buff*direction
        end = start + length*direction
        self.put_start_and_end_on(start, end)
        return self
    def put_to_start(self,mob,buff=0.3):
        mob.move_to(self.get_start())
        mob.shift(-self.get_unit_vector()*buff)
    def put_to_end(self,mob,buff=0.3):
        mob.move_to(self.get_end())
        mob.shift(self.get_unit_vector()*buff)
class Textch(Text):
    def __init__(self, text:str, font="SJsuqian",**kwargs):
        super().__init__(text, font=font, **kwargs)
        self.set_fill(WHITE,1,0)
class Texten(Text):
    def __init__(self, text:str, font="Mongolian Baiti",**kwargs):
        super().__init__(text, font=font, **kwargs)
class TextCustom(VGroup):
    def __init__(self, 
        en: Optional[str]=None                   ,ch: Optional[str]=None,
        direction=DOWN,
        buff=0.2,
        font_en="Mongolian Baiti" ,font_ch="SJsuqian",
        font_size_en=48           ,font_size_ch=40,
        en_config=dict()          ,ch_config=dict(),
        **kwargs):
        super().__init__()
        self.en: Optional[Text] = None
        self.ch: Optional[Text] = None
        if en is not None:
            self.en = Text(en, font=font_en, font_size=font_size_en,**en_config)
            self.add(self.en)
        if ch is not None:
            self.ch = Text(ch, font=font_ch, font_size=font_size_ch,**ch_config)
            self.add(self.ch)
        if self.en and self.ch:
            self.ch.next_to(self.en, direction, buff=buff,**kwargs)

class ThreeDAxesCustom(ThreeDAxes):
    def __init__(
        self,
        x_range = (-6.0, 6.0, 1.0),
        y_range = (-3.0, 3.0, 1.0),
        z_range = (-4.0, 4.0, 1.0),
        **kwargs
        ):
        super().__init__(x_range, y_range, z_range,**kwargs)
        # axes color
        self.x_axis.set_color(PURPLE_B)
        self.y_axis.set_color(PURPLE_B)
        self.z_axis.set_color(PURPLE_B)
        # ticks color
        self.x_axis.ticks.set_color(YELLOW)
        self.y_axis.ticks.set_color(YELLOW)
        self.z_axis.ticks.set_color(YELLOW)
        # remove the tick in origin
        self.remove(self.x_axis.ticks[int(self.x_axis.x_max)])
        self.remove(self.y_axis.ticks[int(self.y_axis.x_max)])
        self.remove(self.z_axis.ticks[int(self.z_axis.x_max)])

    def add_coordinate_labels(self,
        x_values=None,
        y_values=None,
        excluding=[0],
        z_values=None,font_size=18,**kwargs) :
        super().add_coordinate_labels(
            x_values=x_values,
            y_values=y_values,
            excluding=excluding,font_size=font_size,**kwargs) 
        z_labels = self.z_axis.add_numbers(z_values, 
            excluding=excluding,direction=LEFT,font_size=font_size,**kwargs)
        for label in z_labels:
            label.rotate(PI / 2, RIGHT)
        self.coordinate_labels.add(z_labels)
        # (3,2,-1,0,1,2,3) labels color
        self.coordinate_labels.set_color(YELLOW)
        # self.set_zero_opacity()
        return self.coordinate_labels
    def add_axis_labels(self,*args,**kwargs):
        super().add_axis_labels(*args,**kwargs,font_size=70,buff=0.3)
        # axes labels (x,y,z) color
        self.axis_labels.set_color(YELLOW)
    def get_x_unit_size(self) -> float:
        return self.get_x_axis().get_unit_size()
        



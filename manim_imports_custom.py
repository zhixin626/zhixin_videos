from manimlib import *
from typing import Optional
from itertools import cycle
# index_labels()

# functions
def fonts():
    return manimpango.list_fonts()

class Safe(VGroup):
    def __init__(
        self,
        *,
        aspect_ratio=4/3,
        y=-2.7,
        show_line=True,
        **kwargs
    ):
        super().__init__(**kwargs)

        # 基础尺寸
        frame_h = FRAME_HEIGHT
        frame_w = FRAME_WIDTH
        rect_w = frame_h * aspect_ratio

        # 安全线
        self.line = Line()
        self.line.set_length(frame_w)
        self.line.set_y(y)

        # 4:3 矩形
        self.rec = Rectangle(width=rect_w, height=frame_h)

        # 计算安全高度（注意不用 //）
        safe_height = frame_h / 2 - y
        self.rec.set_height(
            safe_height,
            stretch=True,
            about_edge=UP
        )

        # 组合
        self.add(self.rec)
        if show_line:
            self.add(self.line)
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

        



from manimlib import *
import itertools
from typing import Optional
# search font:manimpango.list_fonts()
# index_labels()
# custom functions
def get_current_frame_rectangle(frame,**kwargs):
    rec=Rectangle(
        width=frame.get_shape()[0],height=frame.get_shape()[1],
        stroke_opacity=0,fill_color=WHITE,fill_opacity=0.3,**kwargs)
    rec.apply_matrix(frame.get_orientation().as_matrix())
    rec.move_to(frame.get_center())
    return rec
def get_current_frame_surface(frame,**kwargs):
    frame_width_half=np.round(frame.get_width()/2,2)
    frame_height_half=np.round(frame.get_height()/2,2)
    sf=Surface(u_range=(-frame_width_half,frame_width_half),
        v_range=(-frame_height_half,frame_height_half),opacity=0.5,**kwargs)
    sf.apply_matrix(frame.get_inv_view_matrix()[:3,:3])
    sf.move_to(frame.get_center())
    return sf

# custom scene
import ctypes
from ctypes import wintypes
class InteractiveScene(InteractiveScene):
    def place_window_ontop(self):
        hwnd = self.window._window._hwnd
        user32 = ctypes.windll.user32
        SetWindowPos = user32.SetWindowPos
        SetWindowPos.argtypes = (
            wintypes.HWND,  # Handle to the window whose position is to be changed.
            wintypes.HWND,  # Handle to the window to precede the positioned window in the Z order.
            ctypes.c_int,   # X coordinate (ignored if SWP_NOMOVE flag is set).
            ctypes.c_int,   # Y coordinate (ignored if SWP_NOMOVE flag is set).
            ctypes.c_int,   # New width of the window (ignored if SWP_NOSIZE flag is set).
            ctypes.c_int,   # New height of the window (ignored if SWP_NOSIZE flag is set).
            ctypes.c_uint   # Flags that control window sizing, positioning, and visibility.
        )
        # Constants for setting window position:
        HWND_TOPMOST   = -1  # Places the window above all non-topmost windows.
        HWND_NOTOPMOST = -2  # Places the window above all non-topmost windows but below any topmost ones.
        SWP_NOSIZE     = 0x0001  # Retains the current size (ignores width and height parameters).
        SWP_NOMOVE     = 0x0002  # Retains the current position (ignores x and y parameters).
        SWP_SHOWWINDOW = 0x0040  # Displays the window.
        if not self.window._visible:
            self.window._window.maximize()
            self.window.to_default_position()
        # Bring the window to the foreground by temporarily setting it as topmost.
        SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
        # Remove the topmost attribute to allow normal window behavior while keeping it in front.
        SetWindowPos(hwnd, HWND_NOTOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
        

# custom class
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
    def __init__(self, text:str, **kwargs):
        super().__init__(text, font="SJsuqian", **kwargs)
        self.set_fill(WHITE,1,0)
class Texten(Text):
    def __init__(self, text:str, **kwargs):
        super().__init__(text, font="Mongolian Baiti", **kwargs)
class TransformFromCopy2(Transform):
    def __init__(self, mobject, target_mobject, **kwargs):
        super().__init__(mobject.copy(), target_mobject.copy(), **kwargs)
    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.remove(self.mobject)
        scene.remove(self.target_mobject)
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
        
class NumberPlaneCustom(NumberPlane):
    default_axis_config: dict = dict(
        stroke_color=PURPLE_A,
        stroke_width=2,
        include_ticks=False,
        include_tip=False,
        line_to_number_buff=SMALL_BUFF,
        line_to_number_direction=DL,
        )
    default_y_axis_config: dict = dict(
        line_to_number_direction=DL,
        )
    def __init__(self, 
        x_range=(-6,6,1), 
        y_range=(-3,3,1),
        background_line_style: dict = dict(
            stroke_color=YELLOW_A,
            stroke_width=2,
            stroke_opacity=0.3,
            ), 
        faded_line_style: dict = dict(
            stroke_color=PURPLE_B,
            stroke_width=1,
            stroke_opacity=0.3,),
         **kwargs
    ):
        super().__init__(
            x_range=x_range, y_range=y_range,
            background_line_style=background_line_style,
            faded_line_style=faded_line_style,
            **kwargs)
    def get_lines(self) -> tuple[VGroup, VGroup]:
        x_axis = self.get_x_axis()
        y_axis = self.get_y_axis()

        x_lines1, x_lines2 = self.get_lines_parallel_to_axis(x_axis, y_axis)
        y_lines1, y_lines2 = self.get_lines_parallel_to_axis(y_axis, x_axis)
        lines1 = VGroup(x_lines1, y_lines1)
        lines2 = VGroup(x_lines2, y_lines2)
        return lines1, lines2
    def index_lines(self,x,y):
        xlines=self.background_lines[0]
        ylines=self.background_lines[1]
        if x==0:
            yline=self.y_axis
        elif x>0:
            yline=ylines[int(x-self.x_axis.x_min)-1]
        else:
            yline=ylines[int(x-self.x_axis.x_min)]
        if y==0:
            xline=self.x_axis
        elif y>0:
            xline=xlines[int(y-self.y_axis.x_min)-1]
        else:
            xline=xlines[int(y-self.y_axis.x_min)]
        return VGroup(xline,yline)


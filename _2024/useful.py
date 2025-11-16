from manimlib import *
from typing import Optional
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
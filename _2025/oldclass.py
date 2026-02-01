from manim_imports_custom import *
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
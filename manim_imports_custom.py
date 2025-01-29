from manimlib import *
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
# custom class
class TransformFromCopy2(Transform):
    def __init__(self, mobject, target_mobject, **kwargs):
        super().__init__(mobject.copy(), target_mobject.copy(), **kwargs)
    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.remove(self.mobject)
        scene.remove(self.target_mobject)
class TextCustom(VGroup):
    def __init__(self, 
        en=None                   ,ch=None,
        direction=DOWN,
        buff=0.2,
        font_en="Mongolian Baiti" ,font_ch="SJsuqian",
        font_size_en=48           ,font_size_ch=40,
        en_config=dict()          ,ch_config=dict(),
        **kwargs):
        super().__init__()
        self.en = None
        self.ch = None
        if en is not None:
            self.en = Text(en, font=font_en, font_size=font_size_en,**en_config)
            self.add(self.en)
        if ch is not None:
            self.ch = Text(ch, font=font_ch, font_size=font_size_ch,**ch_config)
            self.add(self.ch)
        if self.en and self.ch:
            self.ch.next_to(self.en, direction, buff=buff,**kwargs)

class MatrixCustom(Matrix):
    def __init__(self,matrix_arr,color_palette=[TEAL_B,YELLOW,BLUE,RED_A],**kwargs):
        super().__init__(matrix_arr,**kwargs)
        # attributes
        self.nparr=matrix_arr # just easy to get matrix array
        self.number_of_columns=len(self.nparr[0,:])
        self.color_palette=color_palette
        # position
        self.to_corner(UL)
        # colors
        self.set_col_colors()
        self.bracket_color=WHITE
        self.brackets.set_color(self.bracket_color)
    def set_col_colors(self):
        for i in range(self.number_of_columns):
            self.columns[i].set_color(self.color_palette[i])
    def get_linear_combination(self,**kwargs):
        # 
        coefficients=['a','b','c','d','e']
        a=Tex('a').set_color(self.color_palette[0])
        first_vector=self.get_matrix_nth_column_vector(0)
        vector_matrices=self.get_all_column_vectors()
        grp=VGroup(a,vector_matrices[0])
        self.parts=VGroup(a)
        for i in range(self.number_of_columns-1):
            plus=Tex('+')
            tex=Tex(coefficients[i+1]).set_color(self.color_palette[i+1])
            vec=vector_matrices[i+1]
            grp.add(plus,tex,vec)
            self.parts.add(VGroup(plus,tex))
        grp.arrange(RIGHT,**kwargs).to_corner(UR)
        self.vector_matrices=vector_matrices
        self.linear_combination=grp
        return self.linear_combination
    def get_changeable_parts(self,places=1,font_size=30,first_buff=0.2,inner_buff=0.1):
        number_of_parts=len(self.parts)
        changeable_parts=VGroup()
        for i in range(number_of_parts):
            if i == 0 :
                number=DecimalNumber(1,num_decimal_places=places,include_sign=True,font_size=font_size)
                VGroup(number[0],number[1:]).arrange(RIGHT,buff=inner_buff)
                number[0].set_color(WHITE)
                number[1:].set_color(self.color_palette[i])
                number.move_to(self.parts[i]).shift(LEFT*first_buff)
            else :
                number=DecimalNumber(1,num_decimal_places=places,include_sign=True,font_size=font_size)
                VGroup(number[0],number[1:]).arrange(RIGHT,buff=inner_buff)
                number[0].set_color(WHITE)
                number[1:].set_color(self.color_palette[i])
                number.move_to(self.parts[i])
            changeable_parts.add(number)
        self.changeable_parts=changeable_parts
        return self.changeable_parts
    def get_all_column_vectors(self):
        grp=VGroup()
        for i in range(self.number_of_columns):
            grp.add(self.get_matrix_nth_column_vector(i))
        grp.arrange(RIGHT)
        return grp
    def get_matrix_nth_column_vector(self,nth):
        new_arr=self.nparr[:,nth:nth+1]
        new_mat=MatrixCustom(new_arr)
        new_mat.nparr=new_arr
        new_mat.set_color(self.color_palette[nth])
        new_mat.brackets.set_color(self.bracket_color)
        return new_mat
    def get_column_arrows(self,ax,**kwargs):
        grp=VGroup()
        for i in range(self.number_of_columns):
            if i ==3:
                arrow=Arrow(ax.c2p_4d(0,0,0,0),ax.c2p_4d(*self.nparr[:,i]),buff=0,**kwargs)
            else:
                arrow=Arrow(ax.c2p(0,0,0),ax.c2p(*self.nparr[:3,i]),buff=0,**kwargs)
            arrow.nparr=self.nparr[:,i]
            arrow.set_color(self.color_palette[i])
            grp.add(arrow)
        return grp






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


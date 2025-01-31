from manim_imports_ext import *
import numpy as np
from scipy.spatial.transform import Rotation

def get_xyz(camera_position,z1=OUT):
    # x_vector=camera_position
    # y_vector=in the plane (z_axis and x_vector)
    # z_vector=cross product of x_vector and y_vector
    x=camera_position
    y=np.cross(np.cross(x,z1),x)
    z=np.cross(x,y)
    return normalize(x),normalize(y),normalize(z)
def get_rotation_matrix(camera_postion): # combine new basis
    x,y,z=get_xyz(camera_postion)
    B=np.array([x,y,z]).T
    return B
def get_projection_point(point,frame_center,camera_postion): # perspective 
    #convert list to numpy comlumn vector 
    frame_center=np.array([frame_center]).T
    point=np.array([point]).T
    camera_postion=np.array([camera_postion]).T
    # codes:
    point=point-frame_center
    n=camera_postion-frame_center 
    proj_mat=np.dot(n,n.T)/np.dot(n.T,n)
    proj_point=np.dot(proj_mat,point)
    dirc_vector=point-proj_point
    scale_factor=get_norm(n)/(get_norm(n-proj_point))
    target_point=scale_factor*dirc_vector
    final_point=target_point+frame_center
    return final_point.T[0]   # column --> row --> first row (a list)

    
class matrix(InteractiveScene):
    def construct(self):
        # start
        frame=self.frame
        ax=ThreeDAxes((-6,6),(-3,3))
        ax.add_coordinate_labels()
        ax.add_axis_labels(font_size=60)
        rec=Rectangle(FRAME_WIDTH,FRAME_HEIGHT,fill_opacity=0.5)
        self.add(rec,ax)
        self.play(frame.animate.reorient(50, 30, 0))
        camera_position=frame.get_implied_camera_location()
        mat=get_rotation_matrix(camera_position)
        angles=Rotation.from_matrix(mat).as_euler('xyz')
        self.play(rec.animate.apply_matrix(mat))
        ax2=ax.copy()
        self.play(frame.animate.set_orientation(Rotation.from_matrix(mat)),run_time=2)

        # way1
        # self.play(ax2.animate.rotate(angles[0],axis=RIGHT,about_point=ORIGIN))
        # self.play(ax2.animate.rotate(angles[1],axis=UP,about_point=ORIGIN))
        # self.play(ax2.animate.rotate(angles[2],axis=OUT,about_point=ORIGIN))

        # way2
        self.play(ax2.animate.apply_matrix(mat).make_smooth()) 

        # delet y,z,rec
        self.remove(ax2[1],ax2[2],rec)
        self.play(frame.animate.reorient(50, 30, 0))

        # perspective proj
        fc=frame.get_center()
        cp=frame.get_implied_camera_location()
        def projection_wrapper(point):
            point=point
            fc=frame.get_center()
            cp=frame.get_implied_camera_location()
            return get_projection_point(point,fc,cp)
        self.play(ax.animate.apply_function(
            projection_wrapper))

class axes4d(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        ax=FourDAxesCustom(show_w_axis=True)
        self.add(ax)
        ax.add_coordinate_labels()
        ax.add_axis_labels()
        # proj
        self.play(frame.animate.set_orientation(ax.frame.get_orientation()))
        ax.save_state()
        self.play(ax.animate.make_xyz_flat())
        # restore
        self.play(frame.animate.reorient(-34, 50, 0, (0,0,0), 9.43))
        self.play(ax.animate.restore())
        # rec
        rec=get_current_frame_rectangle(frame)
        self.play(ShowCreation(rec))
        arrow=Arrow(start=ax.c2p_4d(0,0,0,0),end=ax.c2p_4d(0,0,1,0),buff=0)
        arrow.set_perpendicular_to_camera(ax.frame)
        self.add(arrow)

        

class FourDAxesCustom(ThreeDAxesCustom):
    def __init__(
        self,
        x_range=(-6.0, 6.0, 1.0),
        y_range=(-3.0, 3.0, 1.0),
        z_range=(-4.0, 4.0, 1.0),
        w_range=(-6.0, 6.0, 1.0),
        frame=None,
        show_w_axis=False,
        **kwargs):
        super().__init__(x_range, y_range, z_range,**kwargs)
        self.w_range=w_range
        self.ghost=ThreeDAxesCustom(x_range, y_range, z_range,**kwargs) 
        self.init_w_axis(frame)
        self.show_w_axis=show_w_axis
        if show_w_axis:
            self.add_w_axis()
    def get_projection_plane(self):
        rec=Rectangle(width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            fill_color=WHITE,fill_opacity=0.3,stroke_opacity=0)
        mat=self.frame.get_inv_view_matrix()[:3,:3]
        rec.apply_matrix(mat)
        rec.move_to(self.frame.get_center())
        rec.set_height(self.frame.get_height())
        return rec
    def make_xyz_flat(self,frame=None):
        if frame is None:
            frame=self.frame
        else : frame=frame
        def projection_wrapper(point):
            return FourDAxesCustom.get_projection_point(point,frame)
        self[0:3].apply_function(projection_wrapper)
        self.projection_function=projection_wrapper
        return self
    def c2p_4d(self,*coords):
        # ax.c2p_4d(1,1,1,1) --> array([1,12,0.89,1.39])
        ax2=self.ghost
        func=FourDAxesCustom.get_projection_point
        point=self.w_axis.n2p(coords[-1])+func(ax2.c2p(*coords[:3]),self.frame)
        return point
    # overrides
    def add_coordinate_labels(self, 
        x_values=None, 
        y_values=None, 
        excluding=[0], 
        z_values=None, font_size=18, **kwargs):
        super().add_coordinate_labels(
            x_values=x_values, y_values=y_values, 
            excluding=excluding, z_values=z_values,font_size=font_size, **kwargs)
        if self.show_w_axis:
            self.add_w_axis_numbers()
        return self.coordinate_labels
    def add_axis_labels(self, *args, **kwargs):
        super().add_axis_labels(*args, **kwargs)
        if self.show_w_axis:
            self.add_w_axis_label()
    # sub functions
    def add_w_axis(self):
        if not self.show_w_axis:
            self.show_w_axis=True
        self.add(self.w_axis)
        self.axes.add(self.w_axis)
    def add_w_axis_label(self):
        self.axis_labels.add(self.w_label)
        self.w_axis.add(self.w_label)
    def add_w_axis_numbers(self):
        self.w_axis.add(self.w_numbers)
        self.w_axis.numbers=self.w_numbers

    def init_w_axis(self,frame):
        # w-axis
        if frame is None:
            rot=Rotation.from_quat(
                np.array([0.24558994, 0.04225083, 0.16419859, 0.95443139]))
            self.frame=CameraFrame().set_orientation(rot)
        else:
            self.frame=frame
        w_axis =  NumberLine(self.w_range)
        w_axis.shift(w_axis.n2p(0))
        w_axis.ticks.remove(w_axis.ticks[int(w_axis.x_max)])
        w_axis_ghost=w_axis.copy()
        # w-label
        w_label=Tex('w',font_size=70)
        w_label.next_to(w_axis,RIGHT,0.3)
        w_axis_ghost.add(w_label)
        # w-numbers
        w_numbers=w_axis_ghost.add_numbers(excluding=[0])
        # w-colors
        w_axis.set_color(PURPLE_B)
        w_axis.ticks.set_color(YELLOW)
        w_label.set_color(YELLOW)
        w_numbers.set_color(YELLOW)
        # get matrix
        camera_position=self.frame.get_implied_camera_location()
        mat=FourDAxesCustom.get_rotation_matrix(camera_position)
        w_axis.apply_matrix(mat)
        w_axis_ghost.apply_matrix(mat)
        # make smooth
        w_axis.make_smooth()
        w_label.make_smooth()
        w_numbers.make_smooth()
        self.w_axis=w_axis
        self.w_label=w_label
        self.w_numbers=w_numbers

    @staticmethod
    def get_projection_point(point,frame): # perspective 
        #convert list to numpy column vector
        camera_postion=frame.get_implied_camera_location()
        frame_center=frame.get_center()
        frame_center=np.array([frame_center]).T
        point=np.array([point]).T
        camera_postion=np.array([camera_postion]).T
        # codes:
        point=point-frame_center
        n=camera_postion-frame_center 
        proj_mat=np.dot(n,n.T)/np.dot(n.T,n)
        proj_point=np.dot(proj_mat,point)
        dirc_vector=point-proj_point
        scale_factor=get_norm(n)/(get_norm(n-proj_point))
        target_point=scale_factor*dirc_vector
        final_point=target_point+frame_center
        return final_point.T[0]   # column --> row --> first row (a list)
    @staticmethod
    def get_xyz(camera_position,z1=OUT):
        # x_vector=camera_position
        # y_vector=in the plane (z_axis and x_vector)
        # z_vector=cross product of x_vector and y_vector
        x=camera_position
        y=np.cross(np.cross(x,z1),x)
        z=np.cross(x,y)
        return normalize(x),normalize(y),normalize(z)
    @staticmethod
    def get_rotation_matrix(camera_postion): # combine new basis
        x,y,z=FourDAxesCustom.get_xyz(camera_postion)
        B=np.array([x,y,z]).T
        return B    
        
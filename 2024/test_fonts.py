from manimlib import *
class testupdater(InteractiveScene):
    def construct(self):
        # start
        dot=Dot()
        square = Square().next_to(dot,UP)
        self.add(dot)
        self.play(ShowCreation(square))
        # square=always_redraw(lambda:Square().next_to(dot,UP))
        square.always.next_to(dot,UP)
        self.play(dot.animate.shift(RIGHT*2),run_time=2)
        self.play(FadeOut(square),FadeOut(dot))
        # end
        nbp=NumberPlane()
        light=self.camera.light_source
        light.move_to(np.array([-5,3,3]))
        ax=ThreeDAxes()
        ax.add_axis_labels(font_size=48)
        frame=self.frame
        sphere=Sphere(radius=2)
        textured_sphere=TexturedSurface(
            sphere,"D:\\a_ManimGL1.7.0\\my_videos\\assets\\day.jpg",
            "D:\\a_ManimGL1.7.0\\my_videos\\assets\\night.jpg"
            )
        # self.add(ax,textured_sphere)
        self.add(ax,nbp)
        self.play(frame.animate.reorient(30, 45, 0, (0.54, 0.48, 0.18), 8.57))
        self.play(GrowFromCenter(textured_sphere))
        self.play(light.animate.move_to([5,0,0]),run_time=5)
        mat=np.array([[1,0,0],[0,1,0],[0,0,0.01]])
        self.play(textured_sphere.animate.apply_matrix(mat),run_time=2)

        self.remove(*self.mobjects)
        # play with tex
        frame.reorient(0, 0, 0)
        title=Title('title')
        self.play(Write(title))

        # play with matrix 
        self.remove(*self.mobjects)
        mat=Matrix(np.array([[1,0,0],[0,1,0],[0,0,1]]))
        mat2=Tex(r"""\begin{bmatrix}
            1&0&0\\
            0&1&0\\
            0&0&1
            \end{bmatrix}""",font_size=48)
        grp=VGroup(mat,mat2).arrange(RIGHT)
        self.add(grp)
class testmobjects(InteractiveScene):
    def construct(self):
        for mob in [*self.mobjects]:
            print(mob.__class__.__name__ )
        # print : CmeraFrame ; Group
class surface(InteractiveScene):
    def construct(self):
        # start
        # self.clear()
        ax=ThreeDAxes()
        sf=Surface(u_range=(-6,6),v_range=(-6,6))
        sf.set_z(-3)
        for mob in [*self.mobjects]:
            print(mob.__class__.__name__ )
        frame=self.frame
        frame.reorient(35, 53, 0, (1.19, 0.22, -0.76), 11.84)
        self.add(sf,ax)
class surface2(InteractiveScene):
    def construct(self):
        # start
        # self.clear()
        ax=ThreeDAxes()
        sf=Surface(u_range=(-6,6),v_range=(-6,6))
        sf.set_z(-3)
        ax.apply_depth_test()
        frame=self.frame
        frame.reorient(35, 53, 0, (1.19, 0.22, -0.76), 11.84)
        self.add(sf,ax)
class surface3(InteractiveScene):
    def construct(self):
        # start1
        self.clear()
        window=self.window
        camera=self.camera
        frame=self.frame
        ax=ThreeDAxes()
        ax.add_axis_labels(font_size=100)
        nbp=NumberPlane()
        nbp.set_z(-3)
        sf=Surface(RED,u_range=(-6,6),v_range=(-6,6))
        ax.apply_depth_test()
        sf.set_opacity(0.5)
        sf.set_z(10)
        frame=self.frame
        # frame.reorient(35, 53, 0, (1.19, 0.22, -0.76), 11.84)
        self.add(ax,nbp)
        dots=VGroup()
        for location in frame.get_points():
            print(location)
            dots.add(Dot(location,fill_color=RED))
        self.add(dots)

class applymatrix(InteractiveScene):
    def construct(self):
        # start
        window=self.window
        camera=self.camera
        frame=self.frame
        ax=ThreeDAxes()
        ax.add_axis_labels(font_size=100)
        ax.apply_depth_test()
        sf=Surface(
            BLUE_A,u_range=(-FRAME_WIDTH/2,FRAME_WIDTH/2),
            v_range=(-FRAME_HEIGHT/2,FRAME_HEIGHT/2),opacity=0.5
            )
        cube=Cube()
        self.add(cube,ax,sf)
class MyAxes(Axes):
    def __init__(
        self,**kwargs
        ):
        super().__init__(**kwargs)
        self.z_axis=self.create_axis(
            (-5,5,1),
            {"include_ticks":False,"include_tip":True},
            None
            )
        self.z_axis.rotate(-PI/2,axis=UP,about_point=ORIGIN)
        self.add(self.z_axis)


class axes(InteractiveScene):
    def construct(self):
        # start        
        self.clear()
        frame=self.frame
        camera=self.camera
        frame_center=frame.get_center()
        camera_position=frame.get_implied_camera_location()
        dot1=always_redraw(lambda:GlowDot(frame_center,radius=0.5))
        dot2=always_redraw(lambda:GlowDot(camera_position,color=RED))
        ax=ThreeDAxes()
        ax.add_axis_labels(font_size=100)
        vec=always_redraw(
            lambda:Arrow(
                ax.c2p(0,0,0),
                ax.c2p(*frame.get_orientation().as_rotvec()),
                buff=0)
            )
        self.add(ax,dot1,dot2,vec)
        # frame
        self.clear()
        frame.to_default_state() 

        def updater(mob):
            center=frame.get_center()
            width=frame.get_width()
            height=frame.get_height()
            mob.become(
                Rectangle(
                width=width,height=height,fill_color=WHITE,fill_opacity=0.2
                ).move_to(center)
            )
        sq=Rectangle(
                width=frame.get_width(),height=frame.get_height()
                ,fill_color=WHITE,fill_opacity=0.2
                ).move_to(frame.get_center())
        sq2=sq.copy()
        self.add(sq2)
        sq.add_updater(updater)
        dots = VGroup(*[
        always_redraw(lambda i=i: Dot(frame.get_points()[i], fill_color=RED))
        for i in range(1, 5)
                        ])
        # def updater2(mob):
        #     vertices=sq.get_vertices()
        #     mob[0].become(DashedLine(dot2.get_center(),vertices[0]))
        #     mob[1].become(DashedLine(dot2.get_center(),vertices[1]))
        #     mob[2].become(DashedLine(dot2.get_center(),vertices[2]))
        #     mob[3].become(DashedLine(dot2.get_center(),vertices[3]))
        # lines=VGroup(DashedLine(),DashedLine(),DashedLine(),DashedLine())
        # lines.add_updater(updater2)
        cube=Cube(opacity=0.5).scale(2)
        self.add(ax,sq,dot1,dot2,dots,cube)
        cube.stretch_to_fit_width(frame.get_width()).stretch_to_fit_height(frame.get_height())
        # state4
        self.play(frame.animate.increment_theta(30*DEGREES),run_time=2) # 1 RADIUS=57.29 DEGREES
        self.play(frame.animate.increment_phi(60*DEGREES),run_time=2)
        # self.play(frame.animate.increment_gamma(1),run_time=2)
        # camera.get_image().show()
        # self.show()
        mat=frame.get_view_matrix()[:3,:3] 
        mat_inv=np.linalg.inv(mat)
        dots.clear_updaters()
        self.play(sq2.animate.apply_matrix(mat_inv),
            dots.animate.apply_matrix(mat_inv),
            ax.animate.apply_matrix(mat_inv))
        self.wait()
        self.play(sq2.animate.apply_matrix(mat),
            dots.animate.apply_matrix(mat),
            ax.animate.apply_matrix(mat))
        a=Mobject()

class data(InteractiveScene):
    def construct(self):
        # square
        self.clear()
        sq=Square().scale(2)
        self.add(sq)
        for point in sq.data["point"]:
            print(point)
            self.add(Dot(point))
        # circle
        self.clear()
        cir=Circle().scale(2)
        self.add(cir)
        for point in cir.data["point"]:
            print(point)
            self.add(Dot(point))
        # cube
        self.clear()
        cube=Cube(opacity=0.4).scale(2)
        self.add(cube)
        print(cube.has_points())
        # axis
        self.clear()
        axis=Axes()
        self.add(axis)
        print(axis.has_points())
        self.clear()
        # sphere and circle2
        self.frame.reorient(-57, 55, 0, (-0.01, 0.0, 0.0), 9.92)
        light=self.camera.light_source
        light.move_to([-5,0,0])
        glowdot=always_redraw(lambda:GlowDot(radius=0.5).move_to(light))
        ax=ThreeDAxes()
        ax.add_axis_labels(font_size=50)
        sphere=Sphere(radius=2)
        sphere.has_points()
        self.add(sphere,ax,glowdot)
        print(len(sphere.data["point"]))
        cir=Circle().scale(2)
        self.add(cir)
        for point in cir.data["point"]:
            print(point)
            self.add(Dot(point))
        self.frame.add_ambient_rotation(5*DEGREES)
        self.play(light.animate.move_to([0,0,4]),run_time=3)
        self.play(light.animate.move_to([5,0,0]),run_time=3)
        # self.play(FadeTransform(cir,sphere))
def get_line_from_point_to_plane(axis,point,plane):
    axis=axis
    point=point
    plane=plane
    if "z" not in plane:
        line=DashedLine(axis.p2c(np.array(point)),
                    axis.p2c(np.array([point[0],point[1],0]))
                    )
        return line
    if "y" not in plane:
        line=DashedLine(axis.p2c(np.array(point)),
                axis.p2c(np.array([point[0],0,point[2]]))
                )
        return line
    if "x" not in plane:
        line=DashedLine(axis.p2c(np.array(point)),
                axis.p2c(np.array([0,point[1],point[2]]))
                )
        return line
    

class fourthdimension(InteractiveScene):
    def construct(self):
        # start3
        # Mobject()
        frame=self.frame
        ax=ThreeDAxes(
            z_axis_config={"include_ticks":True,"include_tip":True,
            "include_numbers":True,"numbers_to_exclude":[0],
            "tip_config":{"width":0.1,"length":0.1,"tip_style":2}}
            )
        for number in ax.get_axes()[2].numbers:
            number.rotate(PI/2,DOWN,number.get_center())
            number.rotate(PI,OUT,number.get_center())
        ax.add_coordinate_labels()
        ax.add_axis_labels(font_size=60)
        dot=Sphere(radius=0.05).move_to(ax.p2c(np.array([1,4,3])))
        line=get_line_from_point_to_plane(ax,[1,4,3],"zy")
        self.add(ax)
        # frame2
        self.play(frame.animate.reorient(36, 42, 0,(0,0,0), 9.95))
        cube=Cube()
        dframe=Rectangle(
                width=FRAME_WIDTH,height=FRAME_HEIGHT
                ,fill_color=WHITE,fill_opacity=0.2
                ).move_to(frame.get_center())
        self.play(ShowCreation(dframe))

        nl=NumberLine((-5,5,1),include_ticks=False)
        nl.rotate(-PI/2,UP).rotate(PI/2,OUT)

        
        mat=frame.get_inv_view_matrix()[:3,:3]
        self.play(dframe.copy().animate.apply_matrix(mat))
        self.add(nl.apply_matrix(mat))
        mat2=get_proj_onto_plane_matrix(nl.get_vector())
        axcopy=ax.copy().set_color(RED)
        ax.apply_matrix(mat2)
        self.add(axcopy)
        dframe.set_color(RED_A)
        self.wait()
        # self.play(frame.animate.reorient(-40, 75, 0, (0,0,0), 9.95))
        # self.play(ax.animate.apply_matrix(mat2))
        # self.play(frame.animate.reorient(36, 42, 0, (0, 0,0), 9.95))
        # self.play(frame.animate.reorient(-59, 83, 0, (0,0,0), 9.95))
        self.play(frame.animate.reorient(36, 42, 0, (0, 0,0), 9.95))

        # ar=Arrow(start=ORIGIN,end=np.matmul(
        #     frame.get_inv_view_matrix()[:3,:3],
        #     np.transpose(np.array([[0,0,1]]))).flatten() )
        # self.add(ar)

        camera_location=normalize(frame.get_implied_camera_location())
        frame_norm_vec=normalize(get_frame_perp_vector(frame))
        # check if they are parallel
        print(camera_location)
        print(frame_norm_vec)
        # cube
        line2=DashedLine(start=ORIGIN,
                end=np.array(frame.get_implied_camera_location()),color=YELLOW)
        cube=Cube()
        self.add(cube,line2)
        self.play(cube.animate.apply_matrix(mat2))

def get_frame_perp_vector(frame):
    frame=frame
    vec=np.matmul(
            frame.get_inv_view_matrix()[:3,:3],
            np.transpose(np.array([[0,0,1]]))).flatten()
    return np.array([vec])
def get_proj_onto_plane_matrix(vector):
    # cross origin
    a=vector[0]
    b=vector[1]
    c=vector[2]
    mat=np.array([[1,0],[0,1],[-a/c,-b/c]])
    return get_proj_onto_plane_matrix_bymat(mat)
    return mat
def get_proj_onto_plane_matrix_bymat(mat):
    mat=mat
    mat2=np.dot(np.dot(mat,np.linalg.inv(np.dot(mat.T,mat))),mat.T)
    return mat2
def vector_angle(a, b): # unit:radius # same as "angle_between_vectors"
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    cos_theta = np.clip(dot_product / (norm_a * norm_b), -1.0, 1.0)
    return np.arccos(cos_theta)
class perspective(InteractiveScene):
    def construct(self):
        # start
        m=Mobject()
        CameraFrame()
        index_labels
        frame=self.frame
        ax=ThreeDAxes(
            z_axis_config={"include_ticks":True,"include_tip":True,
            "include_numbers":True,"numbers_to_exclude":[0],
            "tip_config":{"width":0.1,"length":0.1,"tip_style":2}}
            )
        for number in ax.get_axes()[2].numbers:
            number.rotate(PI/2,DOWN,number.get_center())
            number.rotate(PI,OUT,number.get_center())
        ax.add_coordinate_labels()
        ax.add_axis_labels(font_size=60)
        self.add(ax)
        # frame
        dframe=Rectangle(
        width=FRAME_WIDTH,height=FRAME_HEIGHT
        ,fill_color=WHITE,fill_opacity=0.2
        ).move_to(frame.get_center())
        self.add(dframe)
        dframe2=dframe.copy()
        # a test_orientation
        self.play(frame.animate.reorient(36, 42, 0,(0,0,0), 9.95))
        self.play(dframe2.animate.apply_matrix(frame.get_inv_view_matrix()[:3,:3]))
        # state2
        cp=frame.get_implied_camera_location() #used for function:get_pers_point_from_cp_view

        # def get_pers_point(point):
        #     frame=self.frame
        #     camera_position=frame.get_implied_camera_location()
        #     c_norm=np.linalg.norm(camera_position)
        #     frame_vec=get_frame_perp_vector(frame).T
        #     proj_mat=np.dot(frame_vec,frame_vec.T)/(np.dot(frame_vec.T,frame_vec))
        #     Px0_vec=np.dot(proj_mat.T,point)
        #     Px0_norm=np.linalg.norm(Px0_vec)
        #     dirc_vec=point-Px0_vec
        #     factor=(c_norm)/np.linalg.norm(camera_position-Px0_vec) # same as "get_norm"
        #     projection_vec=dirc_vec*factor
        #     return projection_vec
        # def get_pers_point_from_cp_view(point): 
        #     camera_position=cp
        #     c_norm=np.linalg.norm(camera_position)
        #     frame_vec=np.array([camera_position]).T
        #     proj_mat=np.dot(frame_vec,frame_vec.T)/(np.dot(frame_vec.T,frame_vec))
        #     Px0_vec=np.dot(proj_mat.T,point)
        #     Px0_norm=np.linalg.norm(Px0_vec)
        #     dirc_vec=point-Px0_vec
        #     factor=(c_norm)/np.linalg.norm(camera_position-Px0_vec)
        #     projection_vec=dirc_vec*factor
        #     return projection_vec
        # get_pers_point(np.array([0,0,1]))
        # dot=Dot(np.array([0,-3,3]),fill_color=RED).apply_depth_test()
        # dot2=Dot(get_pers_point(dot.get_center()),fill_color=YELLOW).apply_depth_test()
        # self.add(dot,dot2)
        # self.play(frame.animate.reorient(-55, 76, 0, (0,0,0), 14.31))
        # self.play(ax.animate.apply_function(get_pers_point_from_cp_view))
        # self.play(frame.animate.reorient(36, 42, 0,(0,0,0), 9.95))

        # state for tip test
        # from scipy.spatial.transform import Rotation
        nl=NumberLine((-8,8,1),include_ticks=True,include_numbers=True)
        n_default=OUT
        n_target=np.cross(cp,OUT)
        angle=angle_between_vectors(n_default,n_target)
        rotvec=normalize(np.cross(n_default,n_target))
        mat=Rotation.from_rotvec(angle*rotvec).as_matrix()
        nl.apply_matrix(mat)
        self.add(nl)


        # nl.rotate(
        #     angle_between_vectors(
        #     nl.get_vector(),cp),
        #     axis=np.cross(nl.get_vector(),cp)
        #     ) 

        # self.add(nl)
        # nl.add_ticks()
        # nl.add_numbers(direction=IN,excluding=[0])
        # for tick in nl.ticks:
        #     tick.rotate(vector_angle(tick.get_vector(),OUT),axis=nl.get_vector())
        # # nl.add_numbers(direction=DOWN)
        # n_after_rot=normalize(np.cross(cp,OUT))
        # for number in nl.numbers:
        #     number.rotate(
        #         vector_angle(n_after_rot,OUT),
        #         axis=np.cross(OUT,n_after_rot))
        # tip=ArrowTip()
        # align_tip_for_line(nl,tip)
class tiparrow(InteractiveScene):
    def construct(self):
        # start
        Mobject()
        arc=Arc().scale(3)
        nl=NumberLine((-3,3))
        at=ArrowTip()
        dots=VGroup()
        colors=[PURPLE,RED_B,RED_C,RED_D,BLUE_A,BLUE_B,GREEN]
        for point,color in zip(at.get_points(),colors):
            dots.add(Dot(point,fill_color=color))
        index1=index_labels(dots)
        dots2=VGroup()
        for i,point in enumerate(arc.get_points()):
            dots2.add(Dot(point,radius=0.02,fill_color=colors[i%len(colors)]))
        index2=index_labels(dots2)
        # self.add(arc,dots,dots2)
        # self.add(nl,at,index1)
        print(len(arc.get_points()))
        index2[-1].shift(UP*0.1)

        
        # setup axes line 
        ax=ThreeDAxes()
        line=Line([-3,0,0],[3,0,0]).rotate(PI/4)
        line.rotate(PI/4,axis=UP)

        # position_tip
        self.clear()
        at=ArrowTip(width=0.2)
        self.add(line,at,ax)
        

        
        
def align_norm_vector(plane,n1,n2):
    angle=angle_between_vectors(n1,n2) # the angle between n1 and n2
    plane.rotate(angle,-np.cross(n1,n2))  # put tip in target plane
def align_tip_for_line(line,tip,axis=OUT,tip_norm=OUT):
    n1=np.cross(line.get_vector(),axis) # the norm vector for target plane
    n2=tip_norm                         # the norm vector for object plane
    align_norm_vector(tip,n1,n2)
    tip.rotate(                         # put the direction of tip along with line
            angle=angle_between_vectors(
            (tip.get_tip_point()-tip.get_base()),line.get_vector()),
            axis=n1,about_point=tip.get_base()
            )
    tip.shift(line.get_end()-tip.get_base())  # put tip base at the end of the line
    self.add(tip)

class tex(InteractiveScene):
    def construct(self):
        # play with text
        # useful command:manimpango.list_fonts()
        # with register_font("C:/Windows/Fonts/FZYTK.TTF"):
        self.clear()
        text5=Text("Smile落霞",font="Sans")
        text0=Text("Smile仿宋",font="FangSong") #not work
        text1=Text("Smile仿宋",font="Forte") 
        text2=Text("Smile落霞",font="Segoe Print")
        text3=Text("Smile落霞",font="MaoKenWangXingYuan")
        text4=Text("Smile落霞",font="STsong")
        text6=Text("Smile落霞",font="zcoolqingkehuangyouti")
        text7=Text("Smile落霞",font="Poppins")
        text8=Text("Smile落霞",font="xiaowei")
        text_grp=VGroup(text0,text1,text2,text3,text4,text5,text6,text7,text8).arrange_in_grid(3,3)
        self.add(text_grp)
        # play with tex
        self.clear()
        
        tex=Text("Equation")
        tex2=TexText("Equation0.00")
        self.add(tex2)

        # play with decimal number
        self.clear()
        rec=Rectangle()
        number=DecimalNumber(text_config={"font":"SmileySans-Oblique"}).shift(UP)
        number2=DecimalNumber(text_config={"font":"FZYTK"}).shift(UP)
        self.add(rec,number2)
        number.add_updater(lambda mob: mob.set_value(rec.get_width() ))
        self.play(rec.animate.set_width(5),run_time=2)
        self.play(rec.animate.set_width(1),run_time=2)

        # english and chinese font
        text_A=Text('Augmented Matrix',font="Times New Roman")
        text_B=Text('增广矩阵',font='SimSun')
        grp_A=VGroup(text_A,text_B).arrange(DOWN)
        self.add(grp_A)
        

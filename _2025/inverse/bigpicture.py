from manim_imports_custom import *
class bigpicture(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        axis_config={"include_ticks":False,"stroke_width":5,"stroke_color":GREY}
        row=Square(3,fill_color="#f4911e",fill_opacity=1,stroke_opacity=0)
        null=Rectangle(2,3,fill_color="#6c6b18",fill_opacity=1,stroke_opacity=0)
        null.shift(row.get_corner(DR)-null.get_corner(UL))
        grpleft=VGroup(row,null).rotate(-PI/4)
        ax1=Axes((-3,2,1),(-3,3,1),
            axis_config=axis_config)
        ax1.move_to(row.pfp(0.75)-ax1.c2p(0,0,0))
        ax1.rotate(-PI/4,about_point=row.pfp(0.75))
        picture1=VGroup(grpleft,ax1)

        col=Square(3,fill_color="#b90c4c",fill_opacity=1,stroke_opacity=0)
        leftnull=Rectangle(3,2,fill_color="#005a7c",fill_opacity=1,stroke_opacity=0)
        leftnull.shift(col.get_corner(DR)-leftnull.get_corner(UL))
        grpright=VGroup(col,leftnull).rotate(-PI/4)
        ax2=Axes((-3,3,1),(-2,3,1),
            axis_config=axis_config)
        ax2.move_to(col.pfp(0.75)-ax2.c2p(0,0,0))
        ax2.rotate(-PI/4,about_point=col.pfp(0.75))
        picture2=VGroup(grpright,ax2)

        big_picture=VGroup(picture1,picture2).arrange(RIGHT,buff=6)
        big_picture.scale(0.75).to_edge(DOWN,buff=0.6)
        title=Text("The Big Picture of Linear Algebra",font_size=36).to_edge(UP)
        self.add(big_picture)
        self.add(title)

        # arrows
        y=Arrow(ax1.c2p(0,0,0),ax1.c2p(0,3,0),buff=0,fill_color=WHITE)
        z=Arrow(ax1.c2p(0,0,0),ax1.c2p(2,0,0),buff=0,fill_color=WHITE)
        b=Arrow(ax2.c2p(0,0,0),ax2.c2p(-3,0,0),buff=0,fill_color=WHITE)
        x=DashedLine(ax1.c2p(0,0,0),ax1.c2p(2,3,0)).add_tip(length=0.2,width=0.2)
        dash1=DashedLine(x.get_end(),y.get_end())
        dash2=DashedLine(x.get_end(),z.get_end())
        self.add(z,y,b,x,dash1,dash2)

        # labels
        o1_label=Tex("O",font_size=36).next_to(ax1.c2p(0,0,0),LEFT)
        o2_label=Tex("O",font_size=36).next_to(ax2.c2p(0,0,0),RIGHT)
        z_label=Tex("z").next_to(z.get_end(),
            normalize(z.get_vector()),buff=0.15)
        y_label=Tex("y").next_to(y.get_end(),
            normalize(y.get_vector()),buff=0.15)
        b_label=Tex("b").next_to(b.get_end(),
            normalize(b.get_vector()),buff=0.15)
        x_label=Tex("x=y+z",font_size=36)
        x_label.next_to(x.get_end(),normalize(x.get_vector()),buff=0.15)
        labels=VGroup(o1_label,o2_label,z_label,y_label,x_label,b_label)
        self.add(labels)

        # dimension
        rn=Tex(r"\mathbb{R}^n")
        rn.next_to(picture1,UP)
        rm=Tex(r"\mathbb{R}^m")
        rm.next_to(picture2,UP)
        r_row=Tex("r",font_size=60).move_to(row)
        r_col=Tex("r",font_size=60).move_to(col)
        n_r=Tex("n-r").move_to(null)
        m_r=Tex("m-r").move_to(leftnull)
        self.add(rn,rm,r_row,r_col,n_r,m_r)

class test(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        ax=ThreeDAxes()
        v1=np.array([1,1,1])
        v2=np.array([-1,2,1])
        self.add(Vector(v1),Vector(v2),ax)
        A=np.column_stack((v1,v2))
        q, r = np.linalg.qr(A)
        p=A@np.linalg.inv(A.T@A)@A.T
        plane=Surface((-1,1),(-1,1))
        # self.add(plane)
        plane.rotate(angle_between_vectors(OUT,np.cross(v1,v2)),
            axis=np.cross(OUT,np.cross(v1,v2)))
        self.frame.reorient(50, 62, 0)
        cube=Cube()
        self.add(cube)
        q2=np.column_stack((q,np.array([0,0,0])))
        self.play(cube.animate.apply_matrix(q2),run_time=4)

class test2(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        ax=ThreeDAxes()
        v1=np.array([2,0,0])
        v2=np.array([1,3,0])
        A=np.column_stack((v1,v2))
        p=A@np.linalg.inv(A.T@A)@A.T
        q, r = np.linalg.qr(A)
        print(p)
        cube=Cube()
        self.frame.reorient(29, 63, 0, (-0.12, -0.01, 0.1))
        self.add(cube,ax)
        self.play(cube.animate.apply_matrix(p))



class test3(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        A=np.array([[1,0,0],[0,1,0],[1,0,0]])
        cube=Cube()
        ax=ThreeDAxes()
        self.add(cube,ax)
        frame.reorient(25, 43, 0)
        self.play(cube.animate.apply_matrix(A))

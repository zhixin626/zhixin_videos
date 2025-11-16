from manim_imports_custom import *
from typing import Tuple
from _2025.sphere.useful import *
class end_ch(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # setup

        def line_func(x):
            return x**2+1
        def surface_func(u, v):
            return (v, np.cos(u) * line_func(v), np.sin(u) * line_func(v))
        def get_cap(x0,direction="right"):
            R=line_func(x0)
            cap=ParametricSurface(
                lambda u,r:(x0,r*np.sin(u),r*np.cos(u)),
                u_range=(0,TAU),v_range=(0,R),resolution=(32,8))
            normals = np.tile(np.array([0.02, 0.0, 0.0]), (cap.data["point"].shape[0], 1))
            cap.data["d_normal_point"] = cap.data["point"] + normals
            cap.note_changed_data()
            if direction=="right":
                return cap
            elif direction=="left":
                return cap.invert_normals()
            else:
                raise ValueError(f"Invalid direction: {direction}. Must be 'right' or 'left'.")

        # start
        RAIDUS=2
        frame.reorient(28, 69, 0, (0.19, 0.62, 0.51))
        ax=ThreeDAxesCustom()
        ax.add_axis_labels()
        ax.set_opacity(0.5)
        ball=Sphere(radius=RAIDUS,clockwise=True,prefered_creation_axis=0)
        sf=ParametricSurface(
            surface_func,
            u_range=(0,TAU),v_range=(-1,1),resolution=(101,51))
        sf.set_opacity(1)

        sf_top=ParametricSurface(
            surface_func,
            u_range=(0,PI),v_range=(-1,1),resolution=(101,51))
        sf_bottom=ParametricSurface(
            surface_func,
            u_range=(PI,TAU),v_range=(-1,1),resolution=(101,51))

        def r_func(x):
            x = np.clip(x, -RAIDUS, RAIDUS)
            return np.sqrt(RAIDUS**2 - x**2)
        def ball_func(u, v):
            return (v, np.cos(u) * r_func(v), np.sin(u) * r_func(v))
        NUDGE=1e-3
        ball_top=ParametricSurface(
            ball_func,
            u_range=(0,PI),v_range = (-RAIDUS+NUDGE, RAIDUS-NUDGE),resolution=(101,51))
        ball_bottom=ParametricSurface(
            ball_func,
            u_range=(PI,TAU),v_range = (-RAIDUS+NUDGE, RAIDUS-NUDGE),resolution=(101,51))
        sf.always_sort_to_camera(self.camera)
        cap1=get_cap(-1,direction="left")
        cap2=get_cap(1,direction="right")
        mesh_ball=SurfaceMesh(ball)
        mesh_ball.set_anti_alias_width(1)
        frame.clear_updaters()
        frame.add_ambient_rotation(angular_speed=-2*DEG)
        ball.set_opacity(1)
        ball_top.set_opacity(1)
        ball_bottom.set_opacity(1)
        ball.always_sort_to_camera(self.camera)
        ball_top.always_sort_to_camera(self.camera)
        ball_bottom.always_sort_to_camera(self.camera)
        self.play(ShowCreation(ball),
            # Write(mesh_ball),
            Write(ax))
        self.wait(5)
        self.remove(ball)
        self.add(ball_top,ball_bottom,
            # mesh_ball,
            ax)

        # test
        self.play(
            ReplacementTransform(ball_top,sf_top),
            ReplacementTransform(ball_bottom,sf_bottom),
            GrowFromCenter(cap1),
            GrowFromCenter(cap2),
            # FadeOut(mesh_ball),
            run_time=2)
        self.remove(sf_top,sf_bottom)
        self.add(sf,ax)
        self.wait(3)

        # title
        # t=Text("Calculus").scale(1.5).to_corner(UL).fix_in_frame()
        t=Textch("微积分").scale(1.3).to_corner(UL).fix_in_frame()
        underline=Underline(t,stroke_color=YELLOW).fix_in_frame()
        self.play(LaggedStartMap(FadeIn,VGroup(t,underline),shift=RIGHT,lag_ratio=0.2))
        self.wait(2)

        # sf
        def get_segments(n=10):
            v_min, v_max = -1, 1
            segments = SGroup()
            for i in range(n):
                a = v_min + i * (v_max - v_min) / n
                b = v_min + (i+1) * (v_max - v_min) / n
                seg = ParametricSurface(
                    surface_func,
                    u_range=(0, TAU),
                    v_range=(a, b),
                    resolution=(101, 11)  # 注意 v 的分辨率要小一点
                ).invert_normals()
                seg.add(get_cap(a,direction="left"))
                seg.add(get_cap(b,direction="right"))
                segments.add(seg)
            return segments
        segments=get_segments(15)
        self.remove(sf,cap2,cap1)
        self.add(segments,ax)
        self.play(segments.animate.arrange(RIGHT,buff=0.5))
        self.wait()

        # tex
        text=VGroup(
            # Text("Volume"),
            Textch("体积"),
            Tex(R"=\int dv"))\
            .arrange(RIGHT).fix_in_frame().to_edge(UP)
        self.play(
            LaggedStart(
            *[FadeOutToPoint2(segments[i].copy(),
            frame.from_fixed_frame_point(text[1]["dv"].get_center()))
            for i in range(0,len(segments))]
            ),
            Write(text[1][R"=\int"]),
            FadeIn(text[0],shift=RIGHT),
            FadeIn(text[1][R"dv"],time_span=[1,2]),
            segments.animate.arrange(RIGHT,buff=0).set_anim_args(time_span=[1,2]),
            run_time=2)
        self.wait(6)






class begin_ch(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        # title=Text("Geometric Results Known to Archimedes")
        title=Textch("阿基米德时代已经知道的知识",font='Microsoft YaHei')
        title.to_edge(UP)
        under_line=Underline(title,stroke_color=YELLOW)
        ax=ThreeDAxesCustom()
        ax.add_axis_labels()
        title.fix_in_frame()
        under_line.fix_in_frame()
        self.add(under_line)
        self.add(title)

        # setup
        # knowns=VGroup(
        #     Text("Area of a circle:").fix_in_frame(),
        #     Text("Volume of a cylinder:").fix_in_frame(),
        #     Text("Volume of a cone:").fix_in_frame(),
        #     ).scale(0.7).arrange(DOWN,aligned_edge=LEFT,buff=1).to_edge(LEFT)
        knowns=VGroup(
            Textch("圆的面积公式：",font='Microsoft YaHei').fix_in_frame(),
            Textch("圆柱的体积公式：",font='Microsoft YaHei').fix_in_frame(),
            Textch("圆锥的体积公式：",font='Microsoft YaHei').fix_in_frame(),
            ).scale(0.7).arrange(DOWN,aligned_edge=LEFT,buff=1).to_edge(LEFT)
        eqns=VGroup(
            Tex(r"\pi r^2"),
            Tex(r"\pi r^2 h"),
            Tex(R"\frac{1}{3} \pi r^2 h"),
            ).scale(0.7).set_color(YELLOW)
        for eqn,known in zip(eqns,knowns):
            eqn.next_to(known,RIGHT).fix_in_frame()
        self.add(knowns)

        # dsk
        circle=Disk3DPatched(opacity=0.5)
        line=Line(start=ORIGIN,stroke_color=WHITE).set_z(0.001)
        line.apply_depth_test()
        label_r=Tex("r")
        def updater(mob):
            center=line.get_center()
            direction=rotate_vector(line.get_unit_vector(),90*DEG)
            mob.move_to(center+direction*0.2)
        eq=Tex(r"\pi r^2 h").next_to(circle,buff=1)
        label_r.add_updater(updater)
        self.play(ShowCreation(line),Write(label_r))
        self.play(
            FadeIn(eq[r"\pi r^2"],shift=RIGHT),
            Rotating(line,angle=TAU,about_point=ORIGIN),
            ShowCreation(circle),run_time=2,rate_func=linear)
        self.play(ReplacementTransform(eq[r"\pi r^2"][0].copy(),eqns[0]))
        self.wait()

        # cylinder
        cylinder=CylinderCustom()
        cylinder.get_bottom_cap()
        cylinder.get_top_cap()
        temp=Line(np.array([1,0,0]),np.array([1,0,2]))
        br=Brace(cylinder,RIGHT,buff=0.1).rotate(PI/2,axis=RIGHT)
        h=Tex("h").rotate(PI/2,axis=RIGHT)
        br.put_at_tip(h)
        self.play(frame.animate.reorient(8, 41, 0, (-0.41, 0.64, 0.84), 8.00))
        self.play(
            GrowFromCenter(br),
            Write(h),
            ShowCreation(cylinder),
            circle.animate.move_to(cylinder.top_cap),
            line.animate.shift(OUT*2),
            label_r.animate.shift(OUT*2),
            eq.animate.shift(OUT*2),
            )
        self.wait()
        self.play(ReplacementTransform(eq.copy(),eqns[1]))
        self.wait()


        # cone
        cone=ConePatched(prefered_creation_axis=0)
        cone.get_bottom_cap()
        eq_cone=Tex(R"\frac{1}{3} \pi r^2 h").move_to(eq).shift(RIGHT*0.3)
        cy=CylinderCustom().move_to((4,0,1))
        cy.get_top_cap().set_x(4)
        cy.get_bottom_cap().set_x(4)
        dsk=Disk3DPatched().move_to((-4,0,1)).rotate(PI/2,axis=RIGHT)
        cone_grp=SGroup(cone,cone.bottom_cap)
        cylinder_grp=SGroup(cy,cy.top_cap,cy.bottom_cap)
        self.play(
            ShrinkToCenter(circle),
            frame.animate.reorient(8, 46, 0, (0.03, 0.63, 0.76)),
            ReplacementTransform(cylinder,cone),
            ReplacementTransform(eq,eq_cone[R"\pi r^2 h"][0]),
            FadeIn(eq_cone[R"\frac{1}{3}"],shift=RIGHT),
            run_time=2
            )
        self.play(ReplacementTransform(eq_cone,eqns[2]))
        self.wait()
        self.play(
            LaggedStartMap(FadeOut,knowns,shift=LEFT),
            LaggedStartMap(FadeOut,eqns,shift=LEFT),
            LaggedStartMap(FadeOut,VGroup(h,label_r,br,line),shift=RIGHT),
            FadeIn(cone.bottom_cap),
            FadeIn(cylinder_grp,shift=LEFT),
            FadeIn(dsk,shift=RIGHT),
            )
        self.play(frame.animate.reorient(-7, 91, 0, (-0.07, -0.03, 1.05), 8.00))

        # center of mass
        l1=DashedLine(np.array([-4,0,2.5]),np.array([-4,0,-0.5]))
        l2=DashedLine(np.array([0,0,2.5]),np.array([0,0,-0.5]))
        l3=DashedLine(np.array([4,0,2.5]),np.array([4,0,-0.5]))
        c1=Dot(dsk.get_center()).rotate(PI/2,axis=RIGHT)
        c2=Dot(np.array([0,0,0.5])).rotate(PI/2,axis=RIGHT)
        c3=Dot(cy.get_center()).rotate(PI/2,axis=RIGHT)
        self.play(LaggedStartMap(ShowCreation,VGroup(l1,l2,l3)),run_time=1)
        self.play(
            ReplacementTransform(c1.copy().scale(10),c1),
            ReplacementTransform(c2.copy().scale(10),c2),
            ReplacementTransform(c3.copy().scale(10),c3),
            )


class scene2(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        light_default_position=light.get_center()
        # start
        DEFAULT_FOCAL_DISTANCE=frame.get_focal_distance()
        circle=Circle(radius=2,stroke_color=TEAL)
        eq=Tex("x^2+y^2=a^2")
        eq.to_corner(UL)
        eq.fix_in_frame()
        line=Line(circle.get_center(),circle.get_start())
        brace=Brace(line,direction=UP,buff=0.15)
        radius=Tex("a")
        radius.move_to(brace.get_tip()).shift(line.copy().rotate(PI/2).get_unit_vector()/2)
        ax=Axes(x_range=(-7,7,1),y_range=(-4.0, 4.0, 1.0),
            axis_config={"include_ticks":False,"include_tip":True})
        ax.shift(-ax.c2p(0,0,0))
        ax.set_opacity(0.5)
        frame.scale(1.05)
        self.play(ShowCreation(circle),Write(eq))
        self.play(ShowCreation(line))
        self.play(LaggedStart(
            GrowFromCenter(brace),FadeTransform(eq["a"].copy(),radius),lag_ratio=0.2
            ))
        self.play(FadeIn(ax))
        self.wait()

        # the Pythagorean
        tracker=ValueTracker(0)
        dot=GlowDot(circle.get_start(),radius=0.5,color=TEAL)
        v_line=always_redraw(lambda:
        ax.get_v_line(dot.get_center(),line_func=Line))
        h_line=always_redraw(lambda:Line(ORIGIN,v_line.get_start()))
        tilt_line=always_redraw(lambda:Line(ORIGIN,v_line.get_end()))
        self.add(v_line,h_line,tilt_line)
        self.remove(line)
        def brace_updater(mob):
            if tracker.get_value()<0.25 or 0.5<tracker.get_value()<0.75 :
                direction=tilt_line.copy().rotate(PI/2).get_unit_vector()
            else:
                direction=tilt_line.copy().rotate(-PI/2).get_unit_vector()
            new=Brace(tilt_line,direction)
            mob.become(new)
        brace.add_updater(brace_updater)
        def radius_updater(mob):
            mob.move_to(brace.get_tip())
            if tracker.get_value()<0.25 or 0.5<tracker.get_value()<0.75 :
                mob.shift(tilt_line.copy().rotate(PI/2).get_unit_vector()/2)
            else:
                mob.shift(tilt_line.copy().rotate(-PI/2).get_unit_vector()/2)
        radius.add_updater(radius_updater)
        x=Tex("x")
        def x_updater(mob):
            mob.next_to(h_line,DOWN if tracker.get_value()<0.5 else UP)
        x.add_updater(x_updater)
        y=Tex("y")
        def y_updater(mob):
            if tracker.get_value()<0.25 or tracker.get_value()>0.75:
                mob.next_to(v_line,RIGHT )
            else:
                mob.next_to(v_line,LEFT )
        y.add_updater(y_updater)
        def dot_updater(mob):
            mob.move_to(circle.point_from_proportion(tracker.get_value()))
        dot.add_updater(dot_updater)
        self.add(dot)
        self.play(tracker.animate.set_value(0.05),run_time=1,rate_func=smooth)
        self.play(LaggedStart(
            TransformFromCopy(eq["x"][0],x),TransformFromCopy(eq["y"][0],y),lag_ratio=0.2,run_time=2))
        self.play(tracker.animate.set_value(1),run_time=8,rate_func=linear)
        grp=Group(tilt_line,brace,dot,x,y,radius,v_line,h_line)
        for mob in grp:mob.clear_updaters()
        self.play(LaggedStartMap(FadeOut,grp,lag_ratio=0))
        self.wait()

        # tangent to the y-axis
        tracker1=ValueTracker(-4)
        tracker2=ValueTracker(0)
        sp1=Sphere(u_range=(0,TAU),v_range=(PI/2,PI),color=TEAL,radius=2)
        sp2=Sphere(u_range=(0,TAU),v_range=(0,PI/2),color=TEAL,radius=2)
        sp1.shift(RIGHT*2).set_opacity(0.7)
        sp2.shift(RIGHT*2).set_opacity(0.7)
        def sp1_updater(mob):
            mob.set_clip_plane(RIGHT,tracker1.get_value())
        def sp2_updater(mob):
            mob.set_clip_plane(LEFT,tracker2.get_value())
        sp1.add_updater(sp1_updater)
        sp2.add_updater(sp2_updater)
        eq2=Tex("(x-a)^2+y^2=a^2")
        eq2.to_corner(UL)
        eq2.fix_in_frame()
        sp=Sphere(color=TEAL,radius=2).shift(RIGHT*2)
        mesh=SurfaceMesh(sp,stroke_opacity=0.5)
        self.play(circle.animate.move_to([2,0,0]))
        self.play(TransformMatchingStrings(eq,eq2))
        self.wait()
        self.add(sp1,sp2)
        self.play(
            frame.animate.reorient(14, 43, 0, (1.41, -1.46, 1.35), 6.16),
            LaggedStart(
            circle.animate.rotate(PI,axis=DOWN).set_anim_args(path_arc=PI),
            AnimationGroup(tracker1.animate.set_value(0),
            tracker2.animate.set_value(4)),lag_ratio=0.01,
            run_time=3),rate_func=linear)
        self.play(FadeIn(mesh),FadeOut(circle))
        self.play(frame.animate.reorient(0, 0, 0, (0.05, 0.06, 0.0), 8.22),
            FadeOut(mesh),FadeOut(sp1),FadeOut(sp2),FadeIn(circle))
        self.wait()

        # eqns
        eq3=Tex("x^2-2ax+a^2+y^2=a^2")
        eq3.next_to(eq2,DOWN,aligned_edge=LEFT)
        eq4=Tex("x^2+y^2=2ax")
        eq4.next_to(eq2,DOWN,aligned_edge=LEFT)
        eq5=Tex(r"\pi x^2+\pi y^2=\pi 2ax").to_corner(UL)
        eq5[r"\pi"].set_color(TEAL)
        self.play(TransformFromCopy(VGroup(eq2[1],eq2[5]),eq3[0:2]))
        self.play(
            TransformFromCopy(eq2[2],eq3[2]),
            TransformFromCopy(eq2[3].copy(),eq3[4]),
            TransformFromCopy(eq2[1].copy(),eq3[5]),
            FadeTransform(eq2[5].copy(),eq3[3]),
            )
        self.play(
            TransformFromCopy(VGroup(eq2[3],eq2[5].copy()),eq3[7:9]),
            TransformFromCopy(eq2[2].copy(),eq3[6]),
            )
        self.play(TransformFromCopy(eq2[6:],eq3[9:]))
        self.wait()
        self.play(
            FadeOut(eq3["+a^2"],shift=DOWN),
            FadeOut(eq3["a^2"],shift=DOWN),
            )
        eq3["+a^2"].set_opacity(0)
        eq3["a^2"].set_opacity(0)
        self.play(TransformMatchingStrings(
            eq3,eq4,path_arc=90 * DEG,matched_keys=["x^2"]))
        self.play(eq4.animate.to_corner(UL),
            FadeOut(eq2,shift=UP))
        self.wait() 
        self.play(
            LaggedStart(
            AnimationGroup(
            ReplacementTransform(eq4["x^2"],eq5["x^2"]),
            ReplacementTransform(eq4["+"],eq5["+"]),
            ReplacementTransform(eq4["="],eq5["="]),
            ReplacementTransform(eq4["y^2"],eq5["y^2"]),
            ReplacementTransform(eq4["2ax"],eq5["2ax"]),),
            FadeIn(eq5[r"\pi"],shift=UP*0.5),lag_ratio=0.5
            ))
        self.wait()
        self.play(LaggedStart(
            FlashAround(eq5[r"\pi x^2"]),
            FlashAround(eq5[r"\pi y^2"]),lag_ratio=0.5,run_time=2))

        # (x,y)dot
        tracker=ValueTracker(0.1)
        dot=get_special_dot()
        dot.f_always.move_to(lambda:circle.pfp(tracker.get_value()))
        coord=Tex("(x,y)")
        coord.always.next_to(dot,UP)
        h_line=Line(stroke_color=GREEN)
        v_line=Line(stroke_color=BLUE)
        h_line.f_always.put_start_and_end_on(lambda:ORIGIN,
            lambda: dot.get_center() * np.array([1, 0, 1]))
        v_line.f_always.put_start_and_end_on(
            lambda:dot.get_center(),
            lambda:dot.get_center() * np.array([1, 0, 1]))
        # h_line = always_redraw(lambda: Line(
        #     ORIGIN,
        #     dot.get_center() * np.array([1, 0, 1]),
        #     stroke_color=GREEN
        # ))

        # v_line = always_redraw(lambda: Line(
        #     dot.get_center(),
        #     dot.get_center() * np.array([1, 0, 1]),
        #     stroke_color=BLUE
        # ))
        x_coord=Tex("x")
        x_coord.always.next_to(h_line,DOWN)
        y_coord=Tex("y")
        y_coord.always.next_to(v_line,RIGHT)
        # self.add(dot,coord,v_line,h_line,x_coord,y_coord)
        self.play(FadeIn(dot),
            Write(coord[0]),Write(coord[2]),Write(coord[4]),
            TransformFromCopy(eq5[1],coord[1],path_arc=90*DEG),
            TransformFromCopy(eq5[5],coord[3],path_arc=90*DEG),
            run_time=1.5)
        self.add(coord)
        self.wait()
        self.play(tracker.animate.set_value(0.3),run_time=1.5,rate_func=linear)
        h_line.update()
        v_line.update()
        h_line.suspend_updating()
        v_line.suspend_updating()
        self.play(
            LaggedStart(
            ShowCreation(h_line),
            TransformFromCopy(coord["x"],x_coord),
            ShowCreation(v_line),
            TransformFromCopy(coord["y"],y_coord),lag_ratio=0.2
            ))
        h_line.resume_updating()
        v_line.resume_updating()
        eq5.fix_in_frame()
        eq5.shift(-frame.get_center())
        eq5.scale(1/frame.get_scale(),about_point=ORIGIN)
        z_axis=NumberLine((-3,3,1),include_ticks=False,include_tip=True)
        z_axis.move_to(ax.c2p(0,0,0)).rotate(PI/2,axis=DOWN).rotate(PI/2,axis=IN).set_opacity(0.5)
        self.play(tracker.animate.set_value(0.1),
            x_coord.animate.set_opacity(0.3),
            h_line.animate.set_opacity(0.3),
            *[coord[i].animate.set_opacity(0.3) for i in range(3)],
            frame.animate.reorient(41, 55, 0, (0.27, 0.27, 0.12), 4.30),
            TransformFromCopy(ax.x_axis,z_axis),
            run_time=1.5,rate_func=linear)
        self.wait()

        # disks
        NUM=10
        tracker_list = np.linspace(0.1, 0.5, num=NUM)
        def get_y_radius(value):
            theta=(PI/0.5)*value
            return np.sin(theta)*2
        def get_y_dsk(value):
            dsk=Disk3D2(radius=get_y_radius(value),
                color=BLUE,opacity=0.5)
            return dsk
        def frame_updater(start, end, duration, rate_func=linear):
            start_angles = np.array(start[:3])
            start_center = np.array(start[3])
            start_scale  = start[4]

            end_angles = np.array(end[:3])
            end_center = np.array(end[3])
            end_scale  = end[4]

            elapsed = [0.0]  # 可变对象，用于累计 dt

            def updater(mob, dt):
                elapsed[0] += dt
                alpha = min(elapsed[0] / duration, 1.0)
                t = rate_func(alpha)
                angles = (1 - t) * start_angles + t * end_angles
                center = (1 - t) * start_center + t * end_center
                scale  = (1 - t) * start_scale  + t * end_scale
                mob.reorient(*angles, center, scale)
            return updater
        
        start = (41, 55, 0, (0.27, 0.27, 0.12), 4.30)
        end   = (41, 55, 0, (1.42, 0.76, -0.43), 5.50)
        dsks_y= Group(*[get_y_dsk(i) for i in tracker_list])
        t0=self.time
        t=13
        for i, (value, dsk) in enumerate(zip(tracker_list, dsks_y)):
            if i==0:
                dsk.rotate(PI/2,axis=UP).rotate(PI/2,axis=RIGHT).match_x(v_line)
                self.play(ShowCreation(dsk))
                self.play(FadeOutToPoint2(dsk.copy(),
                    frame.from_fixed_frame_point(eq5[r"\pi y^2"].get_bottom())),
                    FlashAround(eq5[r"\pi y^2"].set_color(BLUE),color=BLUE),rate_func=linear)
                frame.add_updater(frame_updater(start, end, t))  # insert time here
            elif i==1:
                self.play(tracker.animate.set_value(value))
                dsk.rotate(PI/2,axis=UP).rotate(PI/2,axis=RIGHT).match_x(v_line)
                self.play(ShowCreation(dsk))
                self.play(FadeOutToPoint2(dsk.copy(),
                    frame.from_fixed_frame_point(eq5[r"\pi y^2"].get_bottom())),
                    FlashAround(eq5[r"\pi y^2"].set_color(BLUE),color=BLUE),rate_func=linear)
            else:
                self.play(tracker.animate.set_value(value),run_time=0.5)
                dsk.rotate(PI/2,axis=UP).rotate(PI/2,axis=RIGHT).match_x(v_line)
                self.play(ShowCreation(dsk),run_time=0.5)
        print(self.time-t0,math.isclose(self.time-t0,t))
        self.wait()
        frame.clear_updaters()

        # add sphere
        RUN_TIME=1.5
        sp=Sphere(color=BLUE,radius=2).shift(RIGHT*2)
        mesh=SurfaceMesh(sp,stroke_opacity=0.5)
        sp.set_opacity(0.6)
        self.play(FadeIn(sp))
        self.play(frame.animate.reorient(-23, 61, 0, (1.42, 0.76, -0.43), 5.50),
            tracker.animate.set_value(0.1),
            sp.animate.set_opacity(0.2),run_time=2,rate_func=linear)
        frame.add_updater(frame_updater(
            start=(-23, 61, 0, (1.42, 0.76, -0.43), 5.50),
            end=(41, 55, 0, (1.42, 0.76, -0.43), 5.50),duration=len(dsks_y)*RUN_TIME))
        for i, (value, dsk) in enumerate(zip(tracker_list, dsks_y)):
            testdsk=dsk.copy().set_color(RED)
            testdsk.deactivate_depth_test()
            self.play(
            FadeInFromPoint2(
            testdsk,frame.from_fixed_frame_point(eq5[r"\pi y^2"].get_bottom())
               ,remover=True ),
            FlashAround(eq5[r"\pi y^2"],color=RED),
            dsk.animate.set_color(RED).set_anim_args(rate_func=there_and_back),
            tracker.animate.set_value(value).set_anim_args(time_span=[0,0.5]),
            run_time=RUN_TIME)
            
        frame.clear_updaters()

        # \pi x^2
        self.play(
            frame.animate.reorient(0, 0, 0, (0,0,0), 8.22),
            tracker.animate.set_value(0.1),
            LaggedStartMap(FadeOut,dsks_y,shift=OUT),
            FadeOut(z_axis),FadeOut(sp),rate_func=linear,run_time=2
            ) 
        self.play(
            y_coord.animate.set_opacity(0.3),
            v_line.animate.set_opacity(0.3),
            x_coord.animate.set_opacity(1),
            h_line.animate.set_opacity(1),
            coord["(x"].animate.set_opacity(1),
            coord["y)"].animate.set_opacity(0.3),
            frame.animate.reorient(0, 0, 0, (0,0,0), 5.70)
            )
        self.add(coord)
        self.wait()
        def get_x_radius(value):
            theta=(PI/0.5)*value
            return 2-np.cos(theta)*2
        def get_x_dsk(value):
            dsk=Disk3D2(radius=get_x_radius(value),
                color=GREEN,opacity=0.5)
            return dsk
        dsks_x=Group(*[get_x_dsk(i) for i in tracker_list])
        for i,dsk in enumerate(dsks_x):
            # dsk.set_opacity(1-i*(0.9)/len(dsks_x))
            dsk.set_z(i*0.001)
            dsk.set_opacity(0.3+i*(0.2)/len(dsks_x))
        start=(0, 0, 0, (0,0,0), 5.70)
        end=(0, 0, 0, (0,0,0), 8.14)
        t=12
        for i, (value, dsk) in enumerate(zip(tracker_list, dsks_x)):
            if i ==0:
                self.play(ShowCreation(dsk))
                frame.add_updater(frame_updater(start,end,duration=t))
                t0=self.time
            elif i <=3:
                self.play(tracker.animate.set_value(value))
                self.play(ShowCreation(dsk))
            else:
                self.play(tracker.animate.set_value(value),run_time=0.5)
                self.play(ShowCreation(dsk),run_time=0.5)
        frame.clear_updaters()
        print(self.time-t0,math.isclose(self.time-t0,t))

        # rotating
        dsks_x.save_state()
        self.play(FadeIn(z_axis),
            frame.animate.reorient(-2, 87, 0, (-0.0, -0.0, 0.0), 7.10))
        self.play(dsks_x.animate.arrange(IN))
        start=(-2, 87, 0, (-0.0, -0.0, 0.0), 7.10)
        end=(-55, 66, 0, (-0.09, -0.19, -0.61), 7.10)
        frame.add_updater(frame_updater(start,end,3))
        self.wait(3)
        frame.clear_updaters()
        start=end
        end=(0, 0, 0, (0,0,0), 8.22)
        frame.add_updater(frame_updater(start,end,3))
        self.play(
            tracker.animate.set_value(0.1),
            LaggedStartMap(FadeOut,dsks_x,shift=OUT),
            FadeOut(z_axis)
            ,run_time=3)
        frame.clear_updaters()
        dsks_x.restore()


        # y=x
        graph=Line(ORIGIN,np.array([4,4,0]))
        graph_label=Tex("y=x")
        graph_label.next_to(graph.get_end(),RIGHT+DOWN)
        # graph_label.fix_in_frame()
        m_lines=VGroup(*[
            Line(stroke_color=GREEN,
            start=np.array([get_x_radius(value),0,0]),
            end=np.array([get_x_radius(value),get_x_radius(value),0]))
            for value in tracker_list])
        self.play(LaggedStart(
            ShowCreation(graph),Write(graph_label),lag_ratio=0.2))
        FRAME_SCALE=3.42
        graph_label.save_state()
        self.play(frame.animate.reorient(0, 0, 0, (0,0,0), FRAME_SCALE),
        graph_label.animate.scale(FRAME_SCALE/8,about_point=ORIGIN)
        )
        
        # show equal
        frame.set_focal_distance(50)
        dsks_x=Group(*[get_x_dsk(i) for i in tracker_list])
        for i,dsk in enumerate(dsks_x):
            # dsk.set_opacity(1-i*(0.9)/len(dsks_x))
            dsk.set_z(i*0.001)
            dsk.set_opacity(0.3+i*(0.2)/len(dsks_x))
        dsks_x_rotated=Group()
        for dsk,m_line in zip(dsks_x,m_lines):
            dsks_x_rotated.add(
                dsk.copy().rotate(PI/2,axis=UP).match_x(m_line)\
                .set_opacity(0.5).rotate(PI/2,axis=RIGHT)
                )
        for i,dsk in enumerate(dsks_x_rotated):
            maxopacity=0.5
            minopacity=0.2
            num=len(dsks_x_rotated)
            k=(maxopacity-minopacity)/num
            dsk.set_opacity(-k*i+maxopacity)
        cone=RevolvedCone(max_u=4)
        cone.set_opacity(0.5)
        cone.set_color(WHITE)
        cone.deactivate_depth_test()
        templine=h_line.copy().clear_updaters().reverse_points()
        self.play(ReplacementTransform(templine,m_lines[0],path_arc=-90*DEG))
        self.play(ShowCreation(dsks_x[0]))
        self.play(frame.animate.reorient(37, 46, 0, (0.42, -0.14, 0.08), 2.70),
            FadeIn(z_axis))
        self.play(ShowCreation(dsks_x_rotated[0]))
        self.play(dsks_x[0].animate.rotate(PI/2,axis=UP))
        dsks_x[0].rotate(PI/2,axis=RIGHT)
        self.play(ReplacementTransform(dsks_x[0],dsks_x_rotated[0]))
        testdsk=dsks_x[0].copy().set_color(GREEN_E)
        testdsk.deactivate_depth_test()
        self.play(FlashAround(eq5[r"\pi x^2"].set_color(GREEN),color=GREEN_E),
            FadeInFromPoint2(
            testdsk,frame.from_fixed_frame_point(eq5[r"\pi x^2"].get_bottom())
               ,remover=True ),run_time=1.5
            )

        # tracker_list[1]
        self.play(tracker.animate.set_value(tracker_list[1]))
        templine=h_line.copy().clear_updaters().reverse_points()
        self.play(ReplacementTransform(templine,m_lines[1],path_arc=-90*DEG))
        self.play(ShowCreation(dsks_x[1]))
        self.play(ShowCreation(dsks_x_rotated[1]))
        self.play(dsks_x[1].animate.rotate(PI/2,axis=UP))
        dsks_x[1].rotate(PI/2,axis=RIGHT)
        self.play(ReplacementTransform(dsks_x[1],dsks_x_rotated[1]))
        testdsk=dsks_x[1].copy().set_color(GREEN)
        testdsk.deactivate_depth_test()
        self.play(FlashAround(eq5[r"\pi x^2"],color=GREEN_E),
            FadeInFromPoint2(
            testdsk,frame.from_fixed_frame_point(eq5[r"\pi x^2"].get_bottom())
               ,remover=True ),run_time=1.5
            )
        
        # i>=2
        start=(37, 46, 0, (0.42, -0.14, 0.08), 2.70)
        end=(26, 53, 0, (1.67, 0.53, -0.23), 7.42)
        t=18
        frame.add_updater(frame_updater(start,end,t))
        t0=self.time
        for i, (value,dskr) in enumerate(zip(tracker_list,dsks_x_rotated)):
            if i<=1:
                continue
            if i<=3:
                self.play(
                    tracker.animate.set_value(value),
                    ShowCreation(m_lines[i]))
                templine=h_line.copy().clear_updaters().reverse_points()
                self.play(ReplacementTransform(templine,m_lines[i],path_arc=-90*DEG))
                self.play(ShowCreation(dskr))
                testdsk=dskr.copy().set_color(GREEN_E)
                self.play(
                FadeInFromPoint2(
                testdsk,frame.from_fixed_frame_point(eq5[r"\pi x^2"].get_bottom())
                   ,remover=True ),
                FlashAround(eq5[r"\pi x^2"],color=GREEN_E),
                run_time=RUN_TIME)
            else:
                self.play(tracker.animate.set_value(value),
                    ShowCreation(m_lines[i]),run_time=0.5)
                templine=h_line.copy().clear_updaters().reverse_points()
                self.play(ReplacementTransform(templine,m_lines[i],path_arc=-90*DEG),
                    run_time=0.5)
                self.play(ShowCreation(dskr),run_time=0.5)
        print(self.time-t0,math.isclose(self.time-t0,t))
        frame.clear_updaters()

        # show cone
        cone.set_opacity(0.5)
        self.play(frame.animate.reorient(88, 25, 0, (1.67, 0.53, -0.23), 7.42))
        cone_bottom=dsks_x_rotated[-1].match_style(cone)
        self.play(
            frame.animate.reorient(87, 31, 0, (1.67, 0.53, -0.23), 7.42),
            Rotate(graph,angle=2 * PI,axis=RIGHT,about_point=ORIGIN ),
            ShowCreation(cone),
            ShowCreation(cone_bottom),
            run_time=4,            
            rate_func=linear)

        # go back
        for dsk in dsks_x_rotated: dsk.save_state()
        self.play(
            frame.animate.reorient(0, 0, 0, (2.46, 0.15, 0.0), 6.39),
            FadeOut(z_axis),
            cone.animate.set_opacity(0.1),
            *[dsk.animate.set_opacity(0.1) for dsk in dsks_x_rotated],
            LaggedStartMap(FadeOut,m_lines,shift=OUT),
            graph_label.animate.restore(),
            run_time=2,rate_func=linear)
        coord_00=Tex("(0,0)").scale(0.7)
        coord_00.next_to(np.array([0,0,0]),LEFT+DOWN)
        self.play(tracker.animate.set_value(0).set_anim_args(time_span=[0,1.3]),
            Write(coord_00,time_span=[0.5,2]),run_time=2)
        self.wait()
        coord_2a=Tex("(0,2a)").scale(0.7)
        coord_2a.next_to(np.array([4,0,0]),RIGHT+DOWN)
        self.play(tracker.animate.set_value(0.5).set_anim_args(time_span=[0,1.3]),
            Write(coord_2a,time_span=[0.5,2]),run_time=2)
        self.play(*[dsk.animate.restore() for dsk in dsks_x_rotated],
            cone.animate.set_opacity(0.3),rate_func=there_and_back)
        self.play(LaggedStart(
            *[dsk.animate.set_opacity(1)\
            .set_color(MAROON_A)
            .set_anim_args(rate_func=there_and_back)
            for dsk in dsks_x_rotated],
            lag_ratio=0.1
            ),FlashAround(eq5[r"\pi x^2"],color=MAROON_A),
            cone.animate.set_opacity(0.2),run_time=2)
        self.play(LaggedStart(
            *[dsk.animate.set_opacity(1)\
            .set_color(MAROON_A)
            .set_anim_args(rate_func=there_and_back)
            for dsk in dsks_x_rotated[::-1]],
            lag_ratio=0.1
            ),FlashAround(eq5[r"\pi x^2"],color=MAROON_A),
            cone.animate.set_opacity(0.2),run_time=2)
        
        # fadeout
        self.play(frame.animate.reorient(0, 0, 0, (0.06, 0.06, 0.0), 8.22),
            LaggedStartMap(FadeOut,dsks_x_rotated,shift=RIGHT),
            FadeOut(graph_label,shift=RIGHT),
            FadeOut(cone),FadeOut(graph),
            coord.animate.set_opacity(1),
            v_line.animate.set_opacity(1),
            y_coord.animate.set_opacity(1),
            *[mob.animate.set_opacity(0.2) for mob in Group(x_coord,y_coord,v_line,h_line,coord,dot)],
            tracker.animate.set_value(0)
            )
        # tracker.set_value(0)
        self.wait()

        # we already know
        sp=Sphere(color=BLUE,radius=2).shift(RIGHT*2)
        mesh=SurfaceMesh(sp,stroke_opacity=0.5)
        sp.set_opacity(0.5)
        sp.deactivate_depth_test()
        cone.set_opacity(0.5)
        cone.set_color(GREEN)
        light.move_to(sp.get_top()+OUT*1)
        self.play(Indicate(eq5[r"\pi x^2"],2,GREEN))
        self.play(FadeIn(cone,rate_func=there_and_back))
        self.play(Indicate(eq5[r"\pi y^2"],2,GREEN))
        self.play(FadeIn(sp,rate_func=there_and_back))
        self.play(Indicate(eq5[r"\pi 2ax"],2,WHITE))
        self.remove(sp)
        
        # multiply by 2a
        eq6=Tex(r"2a(\pi x^2+\pi y^2)=\pi (2a)^2x",
            t2c={r"\pi x^2":GREEN,r"\pi y^2":BLUE,r"\pi (2a)^2":TEAL}).to_corner(UL)
        eq6.fix_in_frame()
        self.play(
            ReplacementTransform(eq5[0:7],eq6[3:10]),
            ReplacementTransform(eq5[7:9],eq6[11:13]),
            ReplacementTransform(eq5[9:11],eq6[14:16]),
            ReplacementTransform(eq5[11],eq6[18]),
            )
        self.play(
            FadeIn(eq6[2],shift=UP),FadeIn(eq6[13],shift=UP),
            FadeIn(eq6[10],shift=UP),FadeIn(eq6[16],shift=UP),
            )
        temp2a1=Tex("2a").next_to(eq6[r"2a"][0],DOWN)
        temp2a2=Tex("2a").next_to(eq6[r")^2"],DOWN)
        self.play(Write(temp2a1),Write(temp2a2))
        self.play(LaggedStart(
            ReplacementTransform(temp2a1,eq6[0:2]),
            FadeTransform(temp2a2,eq6[17]),lag_ratio=0.5))
        self.wait()
        self.play(Indicate(eq6[r"\pi (2a)^2"],2,TEAL))

        # meaning of pi 2a square
        self.frame.set_focal_distance(DEFAULT_FOCAL_DISTANCE)
        dashline1=DashedLine(np.array([0,4,0]),np.array([4,4,0]))
        dashline2=DashedLine(np.array([4,4,0]),np.array([4,0,0]))
        dsks_cylinder=Group(*[Disk3D2(radius=4) for _ in tracker_list])
        for dsk,m_line in zip(dsks_cylinder,m_lines):
            dsk.rotate(PI/2,axis=UP).match_x(m_line)\
            .set_opacity(0.3).rotate(PI/2,axis=RIGHT)\
            .set_color(TEAL)
        cylinder=RevolvedCylinder(color=WHITE)
        cylinder.set_opacity(0.3).set_color(TEAL)
        cylinder_top=Disk3D2(radius=4).rotate(PI/2,axis=UP).rotate(PI/2,axis=RIGHT).set_x(0)
        cylinder_top.match_style(dsks_cylinder[0])
        diameter1=Line(ORIGIN,np.array([4,0,0]))
        diameter2=Line(ORIGIN,np.array([0,4,0]))
        brace1=Brace(diameter1,UP)
        brace2=Brace(diameter2,LEFT)
        diameter_label1=Tex("2a")
        diameter_label2=Tex("2a")
        brace1.put_at_tip(diameter_label1)
        brace2.put_at_tip(diameter_label2)
        self.play(GrowFromCenter(brace1),GrowFromCenter(diameter1))
        self.play(Write(diameter_label1))
        self.play(
            ReplacementTransform(brace1,brace2,path_arc=90*DEG),
            ReplacementTransform(diameter_label1,diameter_label2,path_arc=90*DEG),
            ReplacementTransform(diameter1,diameter2,path_arc=90*DEG),
            )
        self.play(FadeIn(z_axis),
            frame.animate.reorient(28, 51, 0, (0.97, 0.53, 0.02), 8.22))
        self.play(
            ShowCreation(cylinder_top),
            Rotate(diameter2,angle=TAU,about_point=ORIGIN,axis=RIGHT),
            rate_func=linear
            )
        self.play(frame.animate.reorient(0, 0, 0, (0.03, 0.06, 0.0), 8.45))
        self.play(*[mob.animate.set_opacity(1) for mob in Group(x_coord,y_coord,v_line,h_line,coord,dot)])
        self.play(Write(dashline1),run_time=0.5)
        self.play(Write(dashline2),run_time=0.5)
        self.play(tracker.animate.set_value(tracker_list[0]))
        self.play(diameter2.animate.match_x(dot))
        self.play(frame.animate.reorient(18, 54, 0, (0.97, 0.53, 0.02), 8.22))
        self.play(ShowCreation(dsks_cylinder[0]),
            Rotate(diameter2,angle=TAU,about_point=ORIGIN,axis=RIGHT))

        # show cylinder
        start=(18, 54, 0, (0.97, 0.53, 0.02), 8.22)
        end=(62, 61, 0, (1.6, 0.82, -0.13), 10.52)
        t=21
        frame.add_updater(frame_updater(start,end,t))
        cylinder_bottom=dsks_cylinder[-1].match_style(cylinder)
        t0=self.time
        for i,(dsk,value) in enumerate(zip(dsks_cylinder,tracker_list)):
            if i==0:
                continue
            elif i<=2:
                RUN_TIME=1
            else:
                RUN_TIME=0.5
            self.play(tracker.animate.set_value(value),run_time=RUN_TIME)
            self.play(diameter2.animate.match_x(dot),run_time=RUN_TIME)
            if i !=len(tracker_list)-1:
                self.play(
                    ShowCreation(dsk),
                    Rotate(diameter2,angle=TAU,about_point=ORIGIN,axis=RIGHT),
                    run_time=RUN_TIME)
        self.play(
            Rotate(dashline1,angle=2 * PI,axis=RIGHT,about_point=ORIGIN ),
            ShowCreation(cylinder),
            ShowCreation(cylinder_bottom),
            run_time=4)
        self.wait()
        frame.clear_updaters()
        print(self.time-t0,math.isclose(self.time-t0,t))

        # slice is pi 2a square
        start=(62, 61, 0, (1.6, 0.82, -0.13), 10.52)
        frame.reorient(*start)
        end=(-37, 62, 0, (0.56, 1.49, -0.24), 10.52)
        frame.add_updater(frame_updater(start,end,6))
        self.wait()
        cylinder.deactivate_depth_test()
        self.play(
            LaggedStart(
            *[mob.animate\
            .set_opacity(1)\
            .set_color(RED)\
            .set_anim_args(rate_func=there_and_back) 
            for mob in Group(cylinder_top,*dsks_cylinder)[::-1]],
            lag_ratio=0.2
            ),
            # LaggedStart(
            # *[FadeInFromPoint2(
            # dsk.copy().deactivate_depth_test().set_color(RED),
            # frame.from_fixed_frame_point(eq6[r"\pi (2a)^2"].get_center()),
            # remover=True)
            # for dsk in Group(cylinder_top,*dsks_cylinder)[::-1]
            # ],
            # lag_ratio=0.2
            # ),
            FlashAround(eq6[r"\pi (2a)^2"],color=RED),
            run_time=5)
        frame.clear_updaters()
        self.play(
            frame.animate.reorient(0, 0, 0, (0,0,0), 10.24).set_focal_distance(50),
            FadeOut(Group(z_axis)),
            diameter2.animate.set_x(0),
            cylinder.animate.set_opacity(0.3).set_color(TEAL),
            tracker.animate.set_value(0.25),
            *[mob.animate.set_opacity(0.1).set_color(TEAL) 
            for mob in Group(cylinder_top,*dsks_cylinder)],rate_func=linear)
        self.play(FadeOut(cylinder),FadeOut(dsks_cylinder),FadeOut(cylinder_top))
        self.wait()

        
        # what about 2a and x?
        light.move_to(np.array([6,6,0]))
        self.remove(cone)
        ar1=ArrowCustom().point_to(eq6[0:2],angle=PI/2,length=1,buff=0.3)
        ar2=ArrowCustom().point_to(eq6[-1],angle=PI/2,length=1,buff=0.3)
        ar1.fix_in_frame().set_color(YELLOW)
        ar2.fix_in_frame().set_color(YELLOW)
        self.play(
            GrowArrow(ar1,time_span=[0,1]),
            GrowArrow(ar2,time_span=[0,1]),
            FlashAround(eq6[0:2]),
            FlashAround(eq6[-1]),
            run_time=2
            )
        self.wait(2)
        self.play(
            FlashAround(eq6[0:2]),
            FlashAround(eq6[-1]),
            run_time=2
            )
        self.wait()
        self.play(
            ar1.animate.point_to(eq6[r"\pi x^2+\pi y^2"],angle=PI/2,length=1,buff=0.3).set_anim_args(time_span=[0,1]),
            ar2.animate.point_to(eq6[r"\pi (2a)^2"],angle=PI/2,length=1,buff=0.3).set_anim_args(time_span=[0,1]),
            FlashAround(eq6[r"\pi x^2+\pi y^2"]),
            FlashAround(eq6[r"\pi (2a)^2"]),
            run_time=2
            )
        self.wait()
        # i=2
        # self.add(graph,graph_label)
        # self.play(tracker.animate.set_value(tracker_list[i]))
        # self.add(m_lines[2])
        # self.play(ShowCreation(dsks_x[i]))
        # self.play(ShowCreation(dsks_y[i]))
        # self.play(ShowCreation(dsks_z[i]))
        # self.play(Indicate(x_coord,2,RED))

        # create a scale
        self.set_floor_plane("xz")
        beam=Line(np.array([-10,0,0]),np.array([10,0,0])).set_color(YELLOW)
        beam.add_tip()
        beam.add(beam.tip.copy().flip().move_to(beam.get_left()))
        stand=Line(ORIGIN,np.array([0,-12,0])).set_color(YELLOW)
        scale_base_top=Circle().rotate(PI/2,axis=RIGHT).move_to(stand.get_bottom())
        scale_base_top.match_style(beam.tip).set_opacity(0.9)
        HEIGHT=0.2
        scale_base_body=Cylinder(height=HEIGHT).rotate(PI/2,axis=RIGHT).move_to(stand.get_bottom())\
        .deactivate_depth_test()
        scale_base_body.shift(DOWN*HEIGHT/2).set_color(YELLOW)
        scale_base_bottom=scale_base_top.copy().shift(DOWN*HEIGHT)
        base_decorator=VGroup(
            Line(stand.get_bottom()+UP,scale_base_top.pfp(value))\
            .set_color(YELLOW).set_opacity(0.5)
            for value in np.linspace(0,1,15)
            )
        scale=Group(beam,stand,scale_base_top,scale_base_body,scale_base_bottom,base_decorator)
        tracker_grp=Group(dot,coord,x_coord,y_coord,v_line,h_line,)
        things=Group(tracker_grp,circle,coord_00,coord_2a,dashline1,dashline2,
            brace2,diameter2,diameter_label2,ax)
        # self.add(dsks_x2,dsks_y2,sp2,cone2)
        # self.add(hang_circ,hang_line)
        # self.add(cylinder,dsks_z)
        self.play(frame.animate.reorient(0, 0, 0, (-0.41, -3.59, 0.0), 18.70),
            FadeOut(ar1),FadeOut(ar2))
        self.play(FadeIn(scale,shift=DOWN*2))
        self.wait()
        for mob in tracker_grp[1:]:
            mob.suspend_updating()
        self.play(
            Rotate(beam,angle=PI/4),
            Rotate(things,angle=PI/4),
            rate_func=smooth_decay,run_time=2)
        for mob in tracker_grp[1:]:
            mob.resume_updating()

        # recreate 
        dsks_x=Group()
        for i,m_line in zip(tracker_list,m_lines):
            dsks_x.add(
                get_x_dsk(i).rotate(PI/2,axis=UP).match_x(m_line)\
                .rotate(PI/2,axis=RIGHT)
                )
        dsks_y= Group()
        for i,m_line in zip(tracker_list,m_lines):
            dsks_y.add(
                get_y_dsk(i).rotate(PI/2,axis=UP).match_x(m_line).rotate(PI/2,axis=RIGHT)
                )
        dsks_z=Group()
        for _,m_line in zip(tracker_list,m_lines):
            dsks_z.add(
                Disk3D2(radius=4).rotate(PI/2,axis=UP).match_x(m_line).rotate(PI/2,axis=RIGHT)
                )
        for mob1,mob2,mob3 in zip(dsks_x,dsks_y,dsks_z):
            mob1.set_opacity(0.5).set_color(GREEN) 
            mob2.set_opacity(0.5).set_color(BLUE)
            mob3.set_opacity(0.5).set_color(TEAL)
            mob1.deactivate_depth_test() 
            mob2.deactivate_depth_test() 
            mob3.deactivate_depth_test()
        cone.set_opacity(0.5).deactivate_depth_test()
        sp.set_opacity(0.5).deactivate_depth_test()
        cylinder.set_opacity(0.5).deactivate_depth_test()
        # hanging disks
        i=0
        dsks_x2=dsks_x.copy().rotate(-PI/2,axis=OUT,about_point=ORIGIN)\
                .set_x(-4).set_y(-8)
        dsks_y2=dsks_y.copy().rotate(-PI/2,axis=OUT,about_point=ORIGIN)\
                .set_x(-4).set_y(-3)
        hang_base=Circle(radius=0.1,stroke_color=YELLOW).rotate(PI/2,axis=UP)\
                .move_to(np.array([-4.,  0.,  0.]))
        hang_circ=DashedVMobject(hang_base)
        # hang_line=DashedLine(np.array([-4.,  0.,  0.]),
        #     cone2.get_top(),color=YELLOW)
        hang_line_top=Line(np.array([-4.,  0.,  0.]),
            dsks_y2[i].get_top(),color=YELLOW)
        diameter3=Line(ORIGIN,np.array([-4,0,0]))
        brace3=Brace(diameter3,UP)
        diameter_label3=Tex("2a")
        diameter_label3.next_to(brace3.get_tip(),UP)
        tracker.set_value(0.25)
        LEN=abs(dsks_x2[i].get_y())-abs(dsks_y2[i].get_y())
        self.play(
            frame.animate.reorient(46, -9, 0, (0.47, 0.84, 0.0), 7.59),
            tracker.animate.set_value(tracker_list[i]),
            rate_func=smooth)
        v_line.suspend_updating()
        self.play(ShowCreation(dsks_y[i]),
            Rotate(v_line,angle=TAU,about_point=ORIGIN,axis=RIGHT),)
        v_line.resume_updating()
        self.play(
            LaggedStart(
            ReplacementTransform(diameter2,diameter3,path_arc=90*DEG),
            brace2.animate.flip().rotate(90*DEG,about_point=ORIGIN)\
            .move_to(brace3),
            ReplacementTransform(diameter_label2,diameter_label3,path_arc=90*DEG),
            lag_ratio=0.2
            ))
        self.remove(brace2)
        self.add(brace3)
        self.play(ShowCreation(hang_circ),
            ShowCreation(hang_line_top)
                )
        self.play(ReplacementTransform(dsks_y[i],dsks_y2[i]))

        # stimulate gravity
        grp=Group(beam,diameter3,brace3,diameter_label3)
        hang_circ.f_always.move_to(lambda:diameter3.get_end())
        hang_line_top.f_always.put_start_and_end_on(
            lambda:diameter3.get_end(),
            lambda:diameter3.get_end()+DOWN*hang_line_top.get_length())
        dsks_y2[i].f_always.move_to(lambda:hang_line_top.get_bottom())
        self.play(Rotate(grp,3*DEG,about_point=ORIGIN))
        self.play(ShowCreation(graph),Write(graph_label))
        templine=h_line.copy().clear_updaters().reverse_points()
        self.play(frame.animate.reorient(46, -8, 0, (0.44, 0.62, 0.09), 5.57))
        self.play(ReplacementTransform(templine,m_lines[i],path_arc=-90*DEG))
        # pix=Tex(r"\pi x^2").rotate(PI/2,axis=UP).set_color(GREEN)
        self.play(ShowCreation(dsks_x[i]),
            Rotate(m_lines[i],angle=TAU,about_point=ORIGIN,axis=RIGHT))
        self.remove(m_lines[i])
        self.play(frame.animate.reorient(36, -14, 0, (-0.45, -1.62, 0.47), 8.78))
        hang_line_bottom=Line(color=YELLOW)
        hang_line_bottom.put_start_and_end_on(
            hang_line_top.get_end(),
            hang_line_top.get_end()+DOWN*LEN)
        self.play(ShowCreation(hang_line_bottom))
        hang_line_bottom.f_always.put_start_and_end_on(
            lambda:hang_line_top.get_end(),
            lambda:hang_line_top.get_end()+DOWN*LEN)
        dsks_x2[i].f_always.move_to(lambda:hang_line_bottom.get_bottom())
        self.play(ReplacementTransform(dsks_x[i],dsks_x2[i]))
        self.play(Rotate(grp,3*DEG,about_point=ORIGIN))
        self.wait()

        # z disk
        temp=Line(ORIGIN,np.array([0,4,0]))
        temp.match_x(dot).set_color(TEAL)
        self.play(frame.animate.reorient(36, -14, 0, (-0.6, -2.33, 0.8), 12.88))
        self.play(FadeIn(temp,shift=RIGHT))
        self.play(ShowCreation(dsks_z[i]),
            Rotate(temp,angle=TAU,about_point=ORIGIN,axis=RIGHT))
        self.remove(temp)
        self.play(frame.animate.reorient(0, -4, 0, (-0.53, -1.98, 0.65), 11.98))
        ar1=ArrowCustom().point_to(x_coord).set_color(RED)
        ar2=ArrowCustom().point_to(x_coord,angle=PI).set_color(RED)
        ar1.rotate(6*DEG,about_point=x_coord.get_center())
        ar2.rotate(6*DEG,about_point=x_coord.get_center())
        ar1.shift(DOWN*0.5)
        ar2.shift(DOWN*0.5)
        x_brace=Brace(Line(ORIGIN,dsks_z[i].get_center()),DOWN)
        x_coord.suspend_updating()
        x_coord.save_state()
        self.play(GrowArrow(ar1),GrowArrow(ar2),
            GrowFromCenter(x_brace),
            x_coord.animate.next_to(x_brace.get_tip(),DOWN).set_opacity(1)\
            .rotate(6*DEG))
        self.play(Indicate(x_coord,4,RED),FadeOut(ar1),FadeOut(ar2))

        # opacity to 0.3
        opacity_grp=Group(diameter3,brace3,diameter_label3,
           coord_00,coord_2a,x_coord,y_coord,coord,
           graph,graph_label,
           dashline1,dashline2,x_brace )
        OPACITY1=0.3
        OPACITY2=0.8
        OPACITY3=OPACITY2-0.3
        temp1=dsks_z[i].copy().rotate(3*DEG,about_point=ORIGIN).move_to(beam.get_end())
        temp2=dsks_z[i].copy().rotate(3*DEG,about_point=ORIGIN)
        self.play(Transform(dsks_z[i],temp1,path_arc=150*DEG))
        self.play(Transform(dsks_z[i],temp2),rate_func=slow_into)
        self.play(
            # FadeIn(dsks_z[i],shift=LEFT*2),
            *[mob.animate.set_opacity(OPACITY1)
            for mob in opacity_grp],
            circle.animate.set_fill(opacity=0).set_stroke(opacity=OPACITY1),
            dsks_x2[i].animate.set_opacity(OPACITY2),
            dsks_y2[i].animate.set_opacity(OPACITY2),
            dsks_z[i].animate.set_opacity(OPACITY2),
            )
        self.wait()
        self.play(
            diameter_label3.animate.set_opacity(1),
            brace3.animate.set_opacity(1),
            x_coord.animate.set_opacity(1),
            x_brace.animate.set_opacity(1),
            )
        self.wait(3)

        # describe eqn
        self.play(Rotate(grp,-6*DEG,about_point=ORIGIN),
            Rotate(dsks_z[i],-3*DEG,about_point=ORIGIN),
            x_coord.animate.rotate(-6*DEG))
        self.wait()
        self.play(
            FadeOut(x_brace),
            diameter_label3.animate.set_opacity(OPACITY1),
            brace3.animate.set_opacity(OPACITY1),
            x_coord.animate.set_opacity(OPACITY1).resume_updating(),
            frame.animate.reorient(1, -6, 0, (-0.81, -3.81, 0.86), 17.11),
            )
        self.wait()


        
        # all
        start=(19, -9, 0, (-0.53, -1.98, 0.65), 11.98)
        end=(21, -22, 0, (-0.44, -3.59, 0.0), 18.70)
        OPACITY3=0.1
        self.play(frame.animate.reorient(*start),
            dsks_z[i].animate.set_opacity(0.1))
        t0=self.time
        t=104
        frame.add_updater(frame_updater(start,end,t))
        def newp(theta,L):
            return np.array([-4*np.cos(theta),-4*np.sin(theta)-L,0])
        def dskupdater(mob):
            angle=beam.get_angle()
            posi=newp(angle,mob.L)
            mob.move_to(posi)
        for dsk in [*dsks_y2[1:-1], *dsks_x2[1:-1]]:
            dsk.L=abs(dsk.get_y())
            dsk.add_updater(dskupdater)
        THETA=3*DEG
        grp.add(dsks_z[i])
        for i,value in enumerate(tracker_list[1:-1]):
            i=i+1
            dsks_x[i].set_opacity(OPACITY2)
            dsks_x2[i].set_opacity(OPACITY2)
            dsks_y[i].set_opacity(OPACITY2)
            dsks_y2[i].set_opacity(OPACITY2)
            dsks_z[i].set_opacity(OPACITY3)
            self.play(tracker.animate.set_value(value))
            # pi y^2
            v_line.suspend_updating()
            self.play(ShowCreation(dsks_y[i]),
                Rotate(v_line,angle=TAU,about_point=ORIGIN,axis=RIGHT),)
            v_line.resume_updating()
            self.play(ReplacementTransform(dsks_y[i],dsks_y2[i]))
            self.play(Rotate(grp,THETA,about_point=ORIGIN))
            # pi x^2
            temp=h_line.copy().clear_updaters().reverse_points()
            self.play(ReplacementTransform(temp,m_lines[i],path_arc=-90*DEG))
            self.play(ShowCreation(dsks_x[i]),
                Rotate(m_lines[i],angle=TAU,about_point=ORIGIN,axis=RIGHT))
            self.remove(m_lines[i])
            self.play(ReplacementTransform(dsks_x[i],dsks_x2[i]))
            self.play(Rotate(grp,THETA,about_point=ORIGIN))
            # pi (2a)^2
            temp=Line(ORIGIN,np.array([0,4,0]))
            temp.match_x(dot).set_color(TEAL)
            self.play(FadeIn(temp,shift=RIGHT))
            self.play(ShowCreation(dsks_z[i]),
                Rotate(temp,angle=TAU,about_point=ORIGIN,axis=RIGHT))
            self.remove(temp)
            # dsks_z[i].rotate(THETA*2,about_point=ORIGIN)
            grp.add(dsks_z[i])
            temp1=dsks_z[i].copy().rotate(THETA*2,about_point=ORIGIN).move_to(beam.get_end())
            temp2=dsks_z[i].copy().rotate(THETA*2,about_point=ORIGIN)
            self.play(Transform(dsks_z[i],temp1,path_arc=150*DEG))
            self.play(Transform(dsks_z[i],temp2),rate_func=slow_into)
            # self.play(FadeIn(dsks_z[i],shift=LEFT*2))
            self.play(Rotate(grp,-THETA*2,about_point=ORIGIN) )
        print(self.time-t0,math.isclose(self.time-t0,t))
        frame.clear_updaters()
        self.wait()

        # fadein cone sphere cylinder
        cone2=cone.copy()
        cone2.add(dsks_z[-1].copy().set_color(GREEN).set_opacity(0.3))\
                .rotate(-PI/2,axis=OUT,about_point=ORIGIN)\
                .set_x(-4).set_y(-8)
        sp2=sp.copy().rotate(-PI/2,axis=OUT,about_point=ORIGIN)\
                .set_x(-4).set_y(-3)
        cytop=Disk3D2(radius=4).rotate(PI/2,axis=UP).rotate(PI/2,axis=RIGHT)\
            .set_x(0).set_opacity(0.6).set_color(TEAL).deactivate_depth_test()
        cybot=Disk3D2(radius=4).rotate(PI/2,axis=UP).rotate(PI/2,axis=RIGHT)\
            .set_x(4).set_opacity(0.5).set_color(TEAL).deactivate_depth_test()
        cylinder.add(cybot,cytop)
        cylinder.deactivate_depth_test()
        self.play(
            frame.animate.reorient(-17, -9, 0, (-0.44, -3.59, 0.0), 18.70),
            LaggedStartMap(FadeIn,Group(sp2,cone2,cylinder)),
            LaggedStartMap(FadeOut,dsks_x2),
            LaggedStartMap(FadeOut,dsks_y2),
            LaggedStartMap(FadeOut,dsks_z)
            )
        self.wait()
        self.play(frame.animate.reorient(0, -6, 0, (-0.44, -3.59, 0.0), 18.70))
        self.wait()

        # graphlize equation
        sp_eq=sp2.copy().scale(0.2)
        cone_eq=cone2.copy().scale(0.2)
        cylinder_eq=cylinder.copy().scale(0.2)
        left_br=Tex("(")
        plus=Tex("+")
        right_br=Tex(")")
        product1=Tex(R"\cdot")
        distance1=Tex("2a")
        equal=Tex("=")
        product2=Tex(R"\cdot")
        distance2=Tex("a")
        graph_eq=Group(left_br,sp_eq,plus,cone_eq,right_br,product1,distance1,equal,
            cylinder_eq,product2,distance2).arrange(RIGHT).scale(3).next_to(scale,DOWN,buff=3)
        self.play(frame.animate.reorient(0, -5, 0, (-0.73, -7.65, 0.43), 25.98),
            FadeOut(eq6,shift=UP),
            FadeOut(graph),FadeOut(graph_label),
            FadeOut(Group(v_line,h_line,dot,x_coord,y_coord,coord)),
            diameter3.animate.set_opacity(1),
            brace3.animate.set_opacity(1),
            diameter_label3.animate.set_opacity(1),
            circle.animate.set_stroke(WHITE,1),
            )
        self.play(TransformFromCopy(sp2,sp_eq))
        self.play(TransformFromCopy(cone2,cone_eq))
        self.play(Write(left_br),Write(plus),Write(right_br))
        self.play(
            diameter_label3.animate.set_color(RED).set_opacity(1).scale(3)\
            .set_anim_args(rate_func=there_and_back),
            brace3.animate.set_color(RED).set_opacity(1)\
            .set_anim_args(rate_func=there_and_back),
            diameter3.animate.set_color(RED).set_opacity(1)\
            .set_anim_args(rate_func=there_and_back),
            )
        self.play(TransformFromCopy(diameter_label3,distance1),
            FadeIn(product1,shift=UP))
        self.play(Write(equal))
        self.play(TransformFromCopy(cylinder,cylinder_eq))
        self.play(FadeIn(product2,shift=UP))
        
        # center of mass
        origin=Dot(np.array([0,0,0]))
        centr=Dot(np.array([2,0,0]))
        right=Dot(np.array([4,0,0]))
        radi=Tex("a")
        br=Brace(Line(ORIGIN,RIGHT*2),DOWN)
        br.put_at_tip(radi)
        frame.save_state()
        self.play(frame.animate.reorient(0, -4, 0, (1.05, -0.39, -0.21), 10.55))
        frame.add_ambient_rotation(-1*DEG)
        self.wait()
        self.play(
            ReplacementTransform(origin.copy().scale(10),origin),
            ReplacementTransform(centr.copy().scale(10),centr),
            ReplacementTransform(right.copy().scale(10),right),
            coord_00.animate.set_opacity(1),
            coord_2a.animate.set_opacity(1),
            )
        self.wait()
        self.play(GrowFromCenter(br),Write(radi),)
        frame.clear_updaters()
        self.play(frame.animate.restore(),)
        self.play(TransformFromCopy(radi,distance2))

        # change equation
        eq_ofcone=Tex(R"\frac{1}{3} \pi (2a)^3").scale(3).set_color(GREEN)
        eq_ofcylinder=Tex(R"\pi(2a)^22a").scale(3).set_color(TEAL)
        changed_eq=Group(
            left_br.copy(),sp_eq.copy(),plus.copy(),
            eq_ofcone,
            right_br.copy(),product1.copy(),distance1.copy(),equal.copy(),
            eq_ofcylinder,
            product2.copy(),distance2.copy())\
            .arrange(RIGHT,buff=0.5).next_to(graph_eq,DOWN,buff=3)
        self.play(frame.animate.shift(DOWN*8))
        self.play(
            TransformFromCopy(graph_eq[0:3],changed_eq[0:3]),
            TransformFromCopy(graph_eq[4:8],changed_eq[4:8]),
            TransformFromCopy(graph_eq[9:],changed_eq[9:]),
            )
        self.play(FadeTransform(graph_eq[3].copy(),changed_eq[3]))
        self.play(FadeTransform(graph_eq[8].copy(),changed_eq[8]))
        self.wait()
            

        # final equation
        sp_eq_final=Tex(R"\frac{4}{3}\pi a^3").scale(3)
        final_eq=Group(sp_eq.copy(),equal.copy(),sp_eq_final)\
            .arrange(RIGHT,buff=0.5).next_to(changed_eq,DOWN,buff=3)
        self.play(frame.animate.shift(DOWN*7))
        self.play(TransformFromCopy(changed_eq[1],final_eq[0]),
            Write(final_eq[1]))
        dotsgrp=VGroup(*[Dot(mob.get_center()) for mob in changed_eq])
        dotsgrp.set_submobject_colors_by_gradient(BLUE,GREEN,TEAL)
        self.play(TransformFromCopy(dotsgrp,sp_eq_final))
        self.wait()
        







class testdashline(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        d1=DashedLine()
        d2=DashedLine(LEFT*2,RIGHT*5).shift(DOWN)
        self.add(d1,d2)
        

class testratefunc(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        Func=[running_start,overshoot,wiggle,not_quite_there,
        lingering,exponential_decay,rush_into,rush_from,slow_into,double_smooth]

        # test
        ax=Axes(num_sampled_graph_points_per_tick=30)
        line=Line(LEFT*5,RIGHT*5).set_color(YELLOW)
        def decaying_sin(t):
            return np.exp(-2 * t) * np.sin(5 * PI * t)    
        def smooth_decay(t):
            return np.sin(6 * PI * t) * np.exp(-5 * t**1.5)

        self.add(ax,line)
        g=ax.get_graph(smooth_decay,(0,1))
        self.add(g)
        ANGLE=PI/10
        dashline=DashedLine(np.array([0,ANGLE,0]),np.array([3,ANGLE,0]))
        self.add(dashline)
        self.play(Rotate(line,angle=ANGLE),rate_func=smooth_decay)
        
        
               
                      

            
                
class testwag(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        pole = Line(ORIGIN, UP * 2, color=WHITE)
        # 旗帜：3×1 的长方形，贴在杆子顶部
        flag = Rectangle(width=3, height=1).set_fill(BLUE, 0.8).next_to(pole.get_end(), RIGHT, buff=0)
        self.add(pole,flag)
        self.play(flag.animate.wag(direction=IN),rate_func=there_and_back)

        
class yxsquare(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        ax=ThreeDAxesCustom()
        def func(u, v):
            return v,v*np.tan(u),v**2+v**2*np.tan(u)**2
        a=ParametricSurface(func,u_range=(0,TAU),v_range=(-1,1))
        self.add(a)
        self.add(ax)



        

class RevolvedCylinder(Surface):
    """
    RevolvedCylinder: 将直线 y = radius（u ∈ x_range）绕 x 轴旋转一周生成圆柱面。
    """
    def __init__(
        self,
        x_range: tuple[float, float] = (0, 4),
        radius: float = 4.0,
        resolution: tuple[int, int] = (51, 101),
        **kwargs
    ):
        self.radius = radius
        super().__init__(
            u_range=x_range,
            v_range=(0, TAU),
            resolution=resolution,
            **kwargs
        )

    def uv_func(self, u: float, v: float) -> np.ndarray:
        # Parametric mapping:
        #   x = u
        #   y = radius * cos(v)
        #   z = radius * sin(v)
        return np.array([
            u,
            self.radius * math.cos(v),
            self.radius * math.sin(v),
        ])

class testcylinder(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        ax=ThreeDAxesCustom()
        ax.add_coordinate_labels()
        c=RevolvedCylinder()
        self.add(c,ax)
        self.play(ShowCreation(c))
        
class testdsk3d(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        sf=Surface()
        self.add(sf)
        sf.get_points()
        sf.data['d_normal_point']
        
class Disk3D2(Surface):
    def __init__(
        self,
        radius: float = 1,
        u_range: Tuple[float, float] = (0, 1),
        v_range: Tuple[float, float] = (0, TAU),
        resolution: Tuple[int, int] = (2, 100),
        true_normals: bool = True,
        **kwargs
    ):
        super().__init__(
            u_range=u_range,
            v_range=v_range,
            resolution=resolution,
            **kwargs,
        )
        # 按给定半径缩放
        self.scale(radius)

        if true_normals:
            pts = self.data["point"]               # (N,3)
            # 所有点的法线都设成向上 [0,0,1]
            normals = np.tile(np.array([0.0, 0.0, 1.0]), (pts.shape[0], 1))
            # 微调 shading 用的点
            self.data["d_normal_point"] = pts + self.normal_nudge * normals

    def uv_func(self, u: float, v: float) -> np.ndarray:
        # u∈[0,1] 半径比例，v∈[0,2π] 角度
        return np.array([
            u * math.cos(v),
            u * math.sin(v),
            0
        ])


class RevolvedCone(Surface):
    """
    RevolvedCone: 将曲线 y = x（u ∈ [0, max_u]）绕 x 轴旋转，
    生成一个圆锥面 (cone)。
    
    参数说明：
    - max_u: float
        控制 y=x 这条直线在 x 轴上的最大范围；即 cone 的轴向长度 (height)。
    - resolution: Tuple[int, int]
        (u_steps, v_steps) UV 网格分辨率。
    - true_normals: bool
        是否对 apex（u=0 处）做特殊法线处理，避免 degenerate triangles 导致的黑洞。
    - normal_nudge: float (来自父类 kwargs)
        沿法线方向微移的距离，用于 shading。
    """
    def __init__(
        self,
        max_u: float = 2.0,
        resolution: tuple[int, int] = (101, 51),
        true_normals: bool = True,
        **kwargs
    ):
        self.max_u = max_u
        super().__init__(
            # 只传 uv_range、resolution 给父类，自己负责尺寸
            u_range=(0, max_u),
            v_range=(0, TAU),
            resolution=resolution,
            **kwargs
        )

        if true_normals:
            # apex = (0,0,0)
            apex = np.array([0.0, 0.0, 0.0])
            pts = self.data["point"]            # (N,3)
            dirs = pts - apex                   # directions from apex to each point
            norms = np.linalg.norm(dirs, axis=1, keepdims=True)  # (N,1)

            mask = norms[:, 0] > 1e-6           # 非退化点布尔掩码 (N,)
            # 对非退化点做单位化 (unit normalization)
            dirs[mask] = dirs[mask] / norms[mask]  # (M,3)/(M,1) -> broadcast 正常
            # 对退化点（即 apex 本身），指定一个法线方向，这里选沿负 x 轴
            dirs[~mask] = np.array([-1.0, 0.0, 0.0])

            # 把微调后法线点写回 data，结合 normal_nudge 做 shading
            self.data["d_normal_point"] = pts + self.normal_nudge * dirs

    def uv_func(self, u: float, v: float) -> np.ndarray:
        """
        参数化映射 Parametric mapping：
        - u ∈ [0, max_u]：y = x 这条直线在 x 轴的投影
        - v ∈ [0, 2π]：绕 x 轴旋转的角度
        生成点 (x, y, z)：
          x = u
          y = u * cos(v)
          z = u * sin(v)
        """
        return np.array([
            u,                   # x = u
            u * np.cos(v),       # y = u * cos(v)
            u * np.sin(v)        # z = u * sin(v)
        ])
class Cone2(Cone):
    def __init__(
        self,
        u_range=(0,TAU),
        v_range=(0,1),
        true_normals: bool = True,
        **kwargs,
    ):
        super().__init__(u_range,v_range, **kwargs)
        if true_normals:
            apex = np.array([0,0,self.height])
            pts = self.data["point"]
            dirs = pts - apex
            norms = np.linalg.norm(dirs, axis=1, keepdims=True)
            mask = norms[:,0] > 1e-6
            dirs[mask] /= norms[mask]
            dirs[~mask] = np.array([0,0,1])
            self.data["d_normal_point"] = pts + self.normal_nudge * dirs

class testcone(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        c=Cone2(radius=2,height=2)
        ax=ThreeDAxesCustom()
        ax.add_coordinate_labels()
        self.add(ax,c)
        c.shift(OUT*0.5)

        r=RevolvedCone()
        gf=Line(ORIGIN,np.array([2,2,0]))
        self.add(ax,gf)
        self.play(ShowCreation(r))

        sp=Sphere()
        frame.reorient(-2, 64, 0)

        # self.add(sp)
        cone=ConeAboutX(prefered_creation_axis=0,resolution=(101,51))
        frame.reorient(-71, 79, 0, (0.15, -0.2, 0.21), 2.07)
        self.add(cone)
        cone.set_shading(0.2,0.1,0.3)
        cone.reverse_points()
        cone.set_opacity(0.5)
        self.play(ShowCreation(cone),run_time=2,rate_func=linear)
        




class GrowCircleFill(Animation):
    def __init__(self, circle: Circle, **kwargs):
        assert isinstance(circle, Circle)
        self.radius = circle.get_radius()
        self.start_angle = circle.get_start_angle()
        super().__init__(circle, **kwargs)
    def interpolate_mobject(self, alpha: float):
        alpha=self.rate_func(alpha)
        current_angle = alpha * TAU
        new_sector = Sector(
            angle=current_angle,
            radius=self.radius,
            start_angle=self.start_angle,
        ).match_style(self.starting_mobject)
        self.mobject.become(new_sector)

class testgrowsector(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        ax=ThreeDAxes()
        self.add(ax)
        circle = Circle(
                    radius=2,
                    stroke_opacity=0,
                    fill_color=BLUE,
                    fill_opacity=0.5
                )
        self.add(circle)
        circle.get_start_angle()
        circle.rotate(PI/2,axis=UP)
        self.play(GrowCircleFill(circle, run_time=2, rate_func=smooth))

        # surface
        sf=Disk3D(resolution=(100,100),color=BLUE)
        sf.set_opacity(0.5)
        sf.set_shading(0,0,0)
        self.add(sf)
        self.play(ShowCreation(sf))

class test_always_sort_to_camera(InteractiveScene):
    def construct(self):
        # --- 1) 定义一个球面（参数曲面） ---
        # spherical coordinates: theta∈(0,π), phi∈(0,2π)
        def sphere_uv(theta, phi, R=2.0):
            x = R*np.sin(theta)*np.cos(phi)
            y = R*np.sin(theta)*np.sin(phi)
            z = R*np.cos(theta)
            return (x, y, z)

        u_range = (1e-3, PI-1e-3)  # 避免极点奇异 / avoid singularities at the poles
        v_range = (0, TAU)

        # --- 2) 左（不排序）& 右（实时排序）两个球 ---
        left = ParametricSurface(
            uv_func=sphere_uv,
            u_range=u_range,
            v_range=v_range,
            resolution=(60, 120),
            color=BLUE,
            shading=(0.5, 0.2, 0.4),   # 反射/高光/阴影 reflectiveness/gloss/shadow
            depth_test=True,
        ).set_opacity(0.4)

        right = left.copy()

        group = SGroup(left, right).arrange(RIGHT, buff=2)
        self.add(group)
        self.wait()

        # --- 3) 给右边开启“始终对相机排序” ---
        # Always sort triangles back-to-front relative to the camera
        # （画家算法 Painter's algorithm）
        right.always_sort_to_camera(self.camera)
        

class testbug(InteractiveScene):
# 修复了shader_wrapper.py 151行的clip plane 问题
# 启用 GL_CLIP_DISTANCE0 可能导致 fill (Tex/Surface) 渲染错误，
# 原因是 gl_ClipDistance[0] 在理论为0时因浮点误差小于0，
# 导致 OpenGL discard 三角形，出现局部镂空或闪烁。
#
# Enabling GL_CLIP_DISTANCE0 may cause rendering artifacts (e.g. gaps or flickering)
# in filled objects like Tex or Surface. Although gl_ClipDistance[0] is expected to be 0,
# floating-point precision errors can make it slightly negative, triggering OpenGL discard.
    def construct(self):
        # init
        frame=self.frame
        # start
        eq=Tex("a+b=c").to_corner(UL)
        sf=Surface(u_range=(-2,2),v_range=(-3,3))
        self.add(eq,sf)
        sf.set_clip_plane(LEFT,0)

        eq.fix_in_frame()
        eq.shader_wrapper.program_code["fill_geom"]


        eq.shader_wrapper.fill_program

        eq.uniforms
        eq.shader_wrapper.program.fragment_shader_code


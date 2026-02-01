from manim_imports_custom import *
from numpy.linalg import det as np_det
from fractions import Fraction
def FadeInOut(_in:Mobject,_out:Mobject):
    return AnimationGroup(FadeOut(_out,shift=UP),FadeIn(_in,shift=UP))
class PhaseAlignedTransform(ReplacementTransform):
    def __init__(self, src, dst, offset=0, **kwargs):
        self.refresh_points_like(dst, src, offset=offset)
        super().__init__(src, dst, **kwargs)

    def refresh_points_like(self,dst, src, offset=0):
        pts_src, pts_dst = src.get_points(), dst.get_points()
        if len(pts_src) != len(pts_dst):
            raise ValueError("Point count mismatch")
        n = len(pts_dst) - 1
        step = int((src.phase + offset) % max(n, 1))
        self.refresh_points(dst, step)

    def refresh_points(self,vmob, step):
        if not hasattr(vmob, "phase"):
            vmob.phase = 0
        pts = vmob.get_points()
        n = len(pts) - 1
        vmob.phase = (vmob.phase + step) % max(n, 1)
        vmob.set_points(self.rotate_closed_polyline(pts, step))

    def rotate_closed_polyline(self,arr, step):
        pts = arr[:-1]
        pts2 = np.roll(pts, -step, axis=0)
        return np.vstack([pts2, pts2[0:1]])

class CoverScene(InteractiveScene):
    kwargs={"font":"WenYue XinQingNianTi (Authorization Required)"}
    def get_safe_rec43(self):
        height=FRAME_HEIGHT
        width=height*4/3
        safe_line=Line()
        safe_line.set_length(FRAME_WIDTH)
        y=-2.7
        safe_line.set_y(y)
        rec43=Rectangle(width,height)
        safe_height=FRAME_HEIGHT//2-y
        safe_rec=rec43.set_height(safe_height,stretch=True,about_edge=UP)
        return safe_rec
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source

        # start
        def get_safe_rec34():
            width=FRAME_WIDTH
            height=width*4/3
            rec34=Rectangle(width,height)
            rec34.match_height(frame)
            return rec34
        safe_rec=get_safe_rec34()
        # self.add(safe_rec)
        # safe_rec=self.get_safe_rec43()
        t=Text("如何计算",**self.kwargs)
        t2=Text("行列式",**self.kwargs)
        t2.next_to(t,DOWN)
        title=VGroup(t,t2)
        title.scale(2.8)
        title.to_frame_edge(safe_rec,UP).set_color(YELLOW)

        m=detMatrix(np.array([[1,2,3],[4,5,6],[7,8,9]]))
        m.scale(1)
        m.bars.set_color(BLUE)
        m.to_frame_edge(safe_rec,DOWN)
        ar=Arrow(
            start=title.get_bottom(),
            end=m.get_top(),
            # path_arc=-60*DEGREES
            )
        self.add(t,t2,m,ar)

class detMatrix(Matrix):
    def __init__(self,matrix,replace_brackets_with_bars=True,*args,**kwargs):
        super().__init__(matrix,*args,**kwargs)
        if replace_brackets_with_bars:
            self.replace_brackets_with_bars()
    def replace_brackets_with_bars(self,color=TEAL):
        bars=self.get_bars(color)
        self.remove(*self.brackets)
        self.add(bars)
        self.bars=bars
        return self
    def get_bars(self,color=TEAL):
        bars=VGroup(
        Line(self.brackets[0].get_top(),self.brackets[0].get_bottom()).set_color(color),
        Line(self.brackets[1].get_top(),self.brackets[1].get_bottom()).set_color(color)
        )
        return bars

class detMatrixScene(InteractiveScene):
    def det(self,m:np.ndarray):
        x=np_det(m)
        frac = Fraction(x).limit_denominator()
        if frac.denominator == 1:
            return frac.numerator
        return x
    def get_c_r(self,m:Matrix,color_col=GREEN,color_row=YELLOW,
        fill_opacity=0.5,stroke_opacity=0,**kwargs):
        c=VGroup()
        r=VGroup()
        for row in m.rows:
            rec=SurroundingRectangle(row,fill_color=color_row,fill_opacity=fill_opacity,stroke_opacity=stroke_opacity,**kwargs)
            r.add(rec)
        for col in m.columns:
            rec=SurroundingRectangle(col,fill_color=color_col,fill_opacity=fill_opacity,stroke_opacity=stroke_opacity,**kwargs)
            c.add(rec)
        return c,r

    def get_bars(self,m:Matrix,color=TEAL):
        bars=VGroup(
        Line(m.brackets[0].get_top(),m.brackets[0].get_bottom()).set_color(color),
        Line(m.brackets[1].get_top(),m.brackets[1].get_bottom()).set_color(color)
        )
        return bars
    def matrix_cr_anims(self,m:Matrix):
        _c,_r=self.get_c_r(m)
        self.play(
                AnimationGroup(
                    *[FadeIn(r,shift=RIGHT) for r in _r],
                    *[FadeIn(c,shift=DOWN) for c in _c],lag_ratio=0.3)
                )
        s=SurroundingRectangle(m,fill_color=TEAL,fill_opacity=0.5,stroke_color=TEAL,buff=0)
        self.play(FadeTransform(VGroup(_c,_r),s))
        self.play(FadeOut(s))

    def get_flowing_updater(self,velocity):
        step = 2 * velocity
        def updater(mob):
            self.refresh_points(mob, step)
        return updater

    def refresh_points(self,vmob, step):
        if not hasattr(vmob, "phase"):
            vmob.phase = 0
        pts = vmob.get_points()
        n = len(pts) - 1
        vmob.phase = (vmob.phase + step) % max(n, 1)
        vmob.set_points(self.rotate_closed_polyline(pts, step))

    def rotate_closed_polyline(self,arr, step):
        pts = arr[:-1]
        pts2 = np.roll(pts, -step, axis=0)
        return np.vstack([pts2, pts2[0:1]])


    def create_rrec(self,surround, buff=0.1,
                    color=[RED, BLUE],
                    width=[1,3],
                    opacity=[0.2,1],
                    velocity=1,
                    num_insert_curves=150):
        rrec = RoundedRectangle(corner_radius=0.2)
        rrec.set_stroke(color, width, opacity)
        rrec.surround(surround, buff=buff)
        rrec.insert_n_curves(num_insert_curves)
        rrec.add_updater(self.get_flowing_updater(velocity))
        return rrec
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        t1=Text('第1个例子',font='WenCang',t2f={'1':'Cambria Math'},t2c={'1':WHITE},fill_color=TEAL)\
        .scale(2).to_edge(UP)
        n1=np.array([[6]])
        m1=Matrix(n1).scale(2)
        self.add(m1,t1)
        bars=self.get_bars(m1,WHITE)
        def FadeInOut(_in:Mobject,_out:Mobject):
            return AnimationGroup(FadeOut(_out,shift=UP),FadeIn(_in,shift=UP))
        # self.play(FadeInOut(t1['1'],t2))
        # self.play(FadeInOut(t2,t3))
        self.wait()
        self.matrix_cr_anims(m1)
        self.play(FadeInOut(bars,m1.brackets))
        self.wait()

        # eq
        det6=VGroup(m1.elements[0],bars)
        eq=Tex('=').next_to(m1,RIGHT).scale(1.5).set_opacity(0)
        result=Tex('6').next_to(eq,RIGHT).scale(2).set_opacity(0)
        grp=VGroup(det6,eq,result)
        tracker = ValueTracker(0)
        eq.add_updater(lambda mob:mob.set_opacity(tracker.get_value()))
        self.play(grp.animate.arrange(RIGHT).center(),tracker.animate.set_value(1))
        eq.clear_updaters()
        self.wait()
        trans_reuslt=result.copy().set_opacity(1)
        self.play(TransformFromCopy(m1.get_entry(0,0),trans_reuslt,path_arc=-3))
        grp.remove(result).add(trans_reuslt)
        self.wait(2)

        # example2
        n2=np.array([[1,2],[3,4]])
        m2=Matrix(n2).scale(1.5)
        bars_m2=self.get_bars(m2)
        p=np.copy(t1.get_center())
        self.play(FadeOut(grp),t1.animate.scale(1.5).to_frame_center(frame))
        t2=Text('2',font='Cambria Math').scale(3).to_edge(UP).move_to(t1['1'])
        self.play(FadeInOut(t2,t1['1']),run_time=1.5)
        new_title=VGroup(t2,t1[0],t1[2:])
        self.play(new_title.animate.scale(1/1.5).move_to(p),
            FadeIn(m2,shift=UP))
        self.wait()
        self.matrix_cr_anims(m2)
        self.wait()

        # +-
        def get_m_sign():
            m_sign=Matrix(
                [['+','-','+','-'],['-','+','-','+'],
                ['+','-','+','-'],['-','+','-','+']],
                element_alignment_corner=ORIGIN)
            m_sign.scale(1.5)
            m_sign.remove(*m_sign.brackets)
            for sign in m_sign.elements:
                sign.set_color(RED if sign.tex_string == '+' else BLUE)
            return m_sign
        m_sign=get_m_sign()
        m_sign.next_to(new_title,RIGHT,buff=2.5,aligned_edge=UP)
        eq=Tex('=').scale(2.5)
        eq.next_to(m2,DOWN*1.5,buff=1.3,aligned_edge=LEFT)
        self.play(frame.animate.move_to(VGroup(m_sign,m2)).shift(DOWN*1))
        self.play(Write(m_sign.elements[0]),run_time=1)
        self.play(Write(m_sign.elements[1]),run_time=0.8)
        self.play(Write(m_sign.elements[2]),run_time=0.5)
        self.play(Write(m_sign.elements[3]),run_time=0.5)
        self.wait(2)
        self.play(Write(m_sign.elements[4]),run_time=1)
        self.play(Write(m_sign.elements[5]),run_time=0.8)
        self.play(LaggedStart(
            *[Write(m_sign.elements[i]) for i in range(6,len(m_sign.elements))],
            lag_ratio=0.3
            ))

        # insert
        self.play(frame.animate.scale(1.3,about_edge=UP))
        self.play(FadeInOut(bars_m2,m2.brackets),FadeIn(eq,shift=RIGHT))
        self.wait()
        # step2
        m_grp1=Matrix([[4]])
        m_grp2=Matrix([[2]])
        grp=VGroup(
            Tex('+').set_color(RED),Tex('1'),Tex(R'\times'),m_grp1,
            Tex('-').set_color(BLUE),Tex('3'),Tex(R'\times'),m_grp2
            )
        grp.scale(2).arrange(RIGHT).next_to(eq,RIGHT)
        bars_grp1=self.get_bars(m_grp1)
        bars_grp2=self.get_bars(m_grp2)
        grp.add(bars_grp1,bars_grp2)
        rrec=self.create_rrec(m2.get_columns()[0])
        rrec.suspend_updating()
        self.play(ShowCreation(rrec))
        rrec.resume_updating()
        self.wait()
        self.play(
            TransformFromCopy(m2.elements[0],grp[1]),
            TransformFromCopy(m2.elements[2],grp[5]),
            run_time=1.5,rate_func=rush_into)
        self.wait(2)
        self.play(
            FadeIn(grp[2],shift=UP),
            FadeIn(grp[6],shift=UP),
            )
        self.play(
            LaggedStartMap(FadeIn,VGroup(*bars_grp1,*bars_grp2),shift=UP,lag_ratio=0
            ))
        self.wait(4)

        # + - sign
        m2_grp=Group(*m2.elements,rrec)
        p=m2_grp.copy().get_center()
        eq2=Tex('=').scale(2.5)
        eq2.next_to(eq,DOWN*1.5,buff=1.3,aligned_edge=LEFT)
        def get_shake_updater(t0,p,A=0.25,w=1):
            def shake_updater(mob):
                t=self.time-t0
                x =A * np.sin(w * t)
                mob.move_to(p+np.array([x,0,0]))
            return shake_updater
        ar1=ArrowCustom().point_to(grp[0],angle=90*DEGREES,length=1).set_color(YELLOW)
        ar2=ArrowCustom().point_to(grp[4],angle=90*DEGREES,length=1).set_color(YELLOW)
        self.play(GrowArrow(ar1),GrowArrow(ar2),run_time=1)
        self.play(
            FlashAround( Square(0.5).move_to(grp[0]) ),
            FlashAround( Square(0.5).move_to(grp[4]) ),run_time=2
            )
        self.wait(2)
        self.play(m2_grp.animate.align_to(m_sign,UL))
        shake_updater=get_shake_updater(self.time,np.copy(m2_grp.get_center()))
        m2_grp.add_updater(shake_updater)
        self.wait(4)
        self.play(
            TransformFromCopy(m_sign.elements[0],grp[0],path_arc=1),
            TransformFromCopy(m_sign.mob_matrix[1][0],grp[4],path_arc=1),
            rate_func=rush_into,run_time=1.5,
            )
        self.play(FadeOut(ar1),FadeOut(ar2),run_time=0.5)
        self.wait(4)
        m2_grp.remove_updater(shake_updater)
        self.play(m2_grp.animate.move_to(p))
        self.wait()


        # rrec2
        rrec_top   =self.create_rrec(m2.elements[0],buff=0.2)
        rrec_bottom=self.create_rrec(m2.elements[2],buff=0.2)
        ar1=ArrowCustom().point_to(grp[3],angle=90*DEGREES,length=1,buff=0.5).set_color(YELLOW)
        ar2=ArrowCustom().point_to(grp[7],angle=90*DEGREES,length=1,buff=0.5).set_color(YELLOW)
        self.play(GrowArrow(ar1),GrowArrow(ar2),run_time=2)
        self.play(
            FlashAround( grp[3] ),
            FlashAround( grp[7] ),run_time=2
            )
        self.wait(2)
        # rrec.suspend_updating()
        self.play(PhaseAlignedTransform(rrec,rrec_top))
        self.wait(2)
        def get_cover_strip(m:Matrix,row_index:int,col_index:int):
            grp=VGroup()
            row_rec=Rectangle(stroke_opacity=0,fill_color=GREY,fill_opacity=0.8)
            col_rec=Rectangle(stroke_opacity=0,fill_color=GREY,fill_opacity=0.8)
            row_rec.surround(m.get_row(row_index))
            col_rec.surround(m.get_column(col_index))
            grp.add(row_rec,col_rec)
            return grp
        strips=get_cover_strip(m2,0,0)
        self.play(LaggedStart(
            FadeIn(strips[0],shift=RIGHT),
            FadeIn(strips[1],shift=DOWN),
            lag_ratio=0.3
            ))
        self.wait(2)
        self.play(TransformFromCopy(m2.elements[-1],grp[3].elements[0]),run_time=1.5)
        self.play(FadeOut(ar1),run_time=0.5)
        self.play(LaggedStart(
            FadeOut(strips[1],shift=UP),
            FadeOut(strips[0],shift=LEFT),
            lag_ratio=0.3
            ))
        self.wait(2)
        self.play(PhaseAlignedTransform(rrec_top,rrec_bottom))
        strips=get_cover_strip(m2,1,0)
        self.play(LaggedStart(
            FadeIn(strips[0],shift=RIGHT),
            FadeIn(strips[1],shift=DOWN),
            lag_ratio=0.3
            ))
        self.wait()
        self.play(TransformFromCopy(m2.elements[1],grp[7].elements[0]),run_time=1.5)
        self.play(FadeOut(ar2),run_time=1)
        self.wait(2)
        self.play(LaggedStart(
            FadeOut(strips[1],shift=UP),
            FadeOut(strips[0],shift=LEFT),
            lag_ratio=0.3
            ))
        self.play(
            FadeOut(rrec_bottom),
            FadeIn(eq2,shift=RIGHT),
            frame.animate.scale(1.1,about_edge=UP))
        self.wait()

        # flowing result
        result_before=Tex('4-6').scale(2)
        result_before.next_to(eq2,RIGHT)
        result=Tex('-2').scale(2)
        result.next_to(eq2,RIGHT)
        def arcs(source:Group,target:Mobject,angle=30*DEGREES) -> VGroup:
            pts=[mob.get_center() for mob in source]
            arcs=VGroup()
            for p in pts:
                arc=VMobject().set_points(p)
                arc.add_arc_to(target.get_center(),angle)
                arc.set_stroke([WHITE,BLUE],[0,0,4],[0,0,1])
                arcs.add(arc)
            return arcs

        ars=arcs(Group(*grp[:4],*bars_grp1),result_before[0])
        rec=Rectangle().surround(grp).set_color(YELLOW)
        rec1=Rectangle().surround(grp[3]).set_color(YELLOW)
        rec2=Rectangle().surround(grp[7]).set_color(YELLOW)
        self.play(ShowCreation(rec))
        self.play(
            ReplacementTransform(rec,rec1),
            TransformFromCopy(rec,rec2),
            )
        self.play(FadeOut(rec1),FadeOut(rec2))

        self.play(
            LaggedStartMap(Write,ars,stroke_color=BLUE),
            Write(result_before[0],time_span=[0.5,1]),
            run_time=1)
        self.play(FadeOut(ars),run_time=0.5)
        self.play(FadeTransform(grp[4].copy(),result_before[1]),run_time=0.5)

        ars=arcs(Group(*bars_grp2,*grp[6:-2]),result_before[2])
        self.play(
            LaggedStartMap(Write,ars,stroke_color=BLUE),
            Write(result_before[2],time_span=[0.5,1]),run_time=1)
        self.play(FadeOut(ars),run_time=0.5)
        self.play(ReplacementTransform(result_before,result),run_time=0.8)
        self.wait()

        # fadeout
        self.play(
            FadeOut(VGroup(*m2.elements,bars_m2),shift=LEFT),
            FadeOut(VGroup(eq,eq2,grp[0:3],grp[4:7],*grp[3].elements,
                *grp[7].elements,bars_grp1,bars_grp2,result),shift=DOWN),
            FadeOut(m_sign,shift=RIGHT),
            VGroup(t2,t1[0],t1[2:]).animate.move_to(frame).scale(2)
            )
        t3=Text('3',font='Cambria Math').match_width(t2).move_to(t2)
        self.play(FadeInOut(t3,t2))
        title=VGroup(t3,t1[0],t1[2:])
        n3=np.array([[1,2,3],[4,5,6],[7,8,9]])
        self.play(title.animate.scale(0.5).to_frame_edge(frame,UP),
            frame.animate.scale(0.6,about_edge=UP))
        m3=Matrix(n3).replace(m2).to_frame_center(frame)
        self.play(FadeIn(m3,shift=UP))
        self.play(m3.animate.next_to(title,DOWN,buff=1).shift(LEFT*3))

        # example 3
        m_sign=get_m_sign()
        m_sign.scale(0.7)
        m_sign.next_to(m3,RIGHT,buff=3)
        eq=Tex("=").scale(2)
        eq.next_to(m3,DOWN,buff=1.5,aligned_edge=LEFT)
        grp_eq=VGroup(
            VGroup(Tex('+').set_color(RED) ,Tex('1'),Tex(R'\times'),detMatrix([[5,6],[8,9]])).arrange(RIGHT),
            VGroup(Tex('-').set_color(BLUE),Tex('4'),Tex(R'\times'),detMatrix([[2,3],[8,9]])).arrange(RIGHT),
            VGroup(Tex('+').set_color(RED) ,Tex('7'),Tex(R'\times'),detMatrix([[2,3],[5,6]])).arrange(RIGHT),
             )
        grp_eq.arrange(RIGHT).next_to(eq,RIGHT)
        self.play(LaggedStartMap(FadeIn,m_sign,shift=LEFT,lag_ratio=0.2),
            run_time=3)
        self.wait()
        bars_m3=self.get_bars(m3)
        self.add(bars_m3)
        self.play(FadeInOut(bars_m3,m3.brackets),FadeIn(eq,shift=RIGHT),
            frame.animate.scale(1.2,about_edge=UP))
        self.wait()

        # ad
        rrec=self.create_rrec(m3.get_column(0),buff=0.2)
        rrec.suspend_updating()
        self.play(ShowCreation(rrec),run_time=2)
        rrec.resume_updating()
        self.wait()
        self.play(
            TransformFromCopy(m3.mob_matrix[0][0],grp_eq[0][1]),
            TransformFromCopy(m3.mob_matrix[1][0],grp_eq[1][1]),
            TransformFromCopy(m3.mob_matrix[2][0],grp_eq[2][1]),
            rate_func=rush_into,run_time=2
            )
        self.wait(2)
        self.play(
            FadeIn(grp_eq[0][2],shift=UP),
            FadeIn(grp_eq[1][2],shift=UP),
            FadeIn(grp_eq[2][2],shift=UP),
            )
        self.wait()
        self.play(
            FadeIn(grp_eq[0][3].bars,shift=UP),
            FadeIn(grp_eq[1][3].bars,shift=UP),
            FadeIn(grp_eq[2][3].bars,shift=UP),
            )
        self.wait(2)

        # 7seconds
        ar1=ArrowCustom().point_to(grp_eq[0][0],angle=90*DEGREES,length=1).set_color(YELLOW)
        ar2=ArrowCustom().point_to(grp_eq[1][0],angle=90*DEGREES,length=1).set_color(YELLOW)
        ar3=ArrowCustom().point_to(grp_eq[2][0],angle=90*DEGREES,length=1).set_color(YELLOW)
        self.play(
            GrowArrow(ar1),
            GrowArrow(ar2),
            GrowArrow(ar3),
            run_time=2)
        self.play(
            FlashAround( Square(0.5).move_to(grp_eq[0][0]) ),
            FlashAround( Square(0.5).move_to(grp_eq[1][0]) ),
            FlashAround( Square(0.5).move_to(grp_eq[2][0]) ),
            run_time=2
            )
        self.wait(3)

        # 4 sec
        shake_grp=VGroup(*m3.elements,rrec)
        p=np.copy(shake_grp.get_center())
        self.play(shake_grp.animate.scale(0.9).align_to(m_sign,UL))
        shake_updater=get_shake_updater(self.time,np.copy(shake_grp.get_center()))
        shake_grp.add_updater(shake_updater)
        self.wait(3)
        self.play(
            TransformFromCopy(m_sign.mob_matrix[0][0],grp_eq[0][0]),
            TransformFromCopy(m_sign.mob_matrix[1][0],grp_eq[1][0]),
            TransformFromCopy(m_sign.mob_matrix[2][0],grp_eq[2][0]),
            FadeOut(ar1),
            FadeOut(ar2),
            FadeOut(ar3),
            rate_func=rush_into,run_time=2
            )
        self.wait(2)
        shake_grp.remove_updater(shake_updater)
        self.play(shake_grp.animate.scale(1/0.9).move_to(p))
        self.wait()

        # inside det
        rrec1=self.create_rrec(m3.mob_matrix[0][0],buff=0.2)
        rrec2=self.create_rrec(m3.mob_matrix[1][0],buff=0.2)
        rrec3=self.create_rrec(m3.mob_matrix[2][0],buff=0.2)
        cover_strip1=get_cover_strip(m3,0,0)
        cover_strip2=get_cover_strip(m3,1,0)
        cover_strip3=get_cover_strip(m3,2,0)
        self.play(
            FlashAround(grp_eq[0][3]),
            FlashAround(grp_eq[1][3]),
            FlashAround(grp_eq[2][3]),run_time=1.5
            )
        self.play(PhaseAlignedTransform(rrec,rrec1))
        self.play(LaggedStart(
            FadeIn(cover_strip1[0],shift=RIGHT),
            FadeIn(cover_strip1[1],shift=DOWN),
            lag_ratio=0.3
            ))
        self.wait(2)
        self.play(TransformFromCopy(m3.get_minor(0,0),grp_eq[0][3].get_entries()),
            rate_func=rush_into,run_time=2)
        self.play(FadeOut(cover_strip1[0],shift=LEFT),FadeOut(cover_strip1[1],shift=UP),)

        self.play(PhaseAlignedTransform(rrec1,rrec2))
        self.play(LaggedStart(
            FadeIn(cover_strip2[0],shift=RIGHT),
            FadeIn(cover_strip2[1],shift=DOWN),
            lag_ratio=0.3
            ))
        self.wait(2)
        self.play(TransformFromCopy(m3.get_minor(1,0),grp_eq[1][3].get_entries()),
            rate_func=rush_into,run_time=2)
        self.play(FadeOut(cover_strip2[0],shift=LEFT),FadeOut(cover_strip2[1],shift=UP),)

        self.play(PhaseAlignedTransform(rrec2,rrec3))
        self.play(LaggedStart(
            FadeIn(cover_strip3[0],shift=RIGHT),
            FadeIn(cover_strip3[1],shift=DOWN),
            lag_ratio=0.3
            ))
        self.wait(2)
        self.play(TransformFromCopy(m3.get_minor(2,0),grp_eq[2][3].get_entries()),
            rate_func=rush_into,run_time=2)
        self.play(FadeOut(cover_strip3[0],shift=LEFT),FadeOut(cover_strip3[1],shift=UP),)
        eq2=Tex("=").replace(eq).next_to(eq,DOWN,buff=2)
        self.play(FadeIn(eq2,shift=RIGHT),FadeOut(rrec3),
            frame.animate.scale(1.3,about_edge=UP))
        self.wait()

        # eq2
        rrec1=self.create_rrec(grp_eq[0][3].get_column(0),color=[PINK,YELLOW_A])
        rrec2=self.create_rrec(grp_eq[1][3].get_column(0),color=[PINK,YELLOW_A])
        rrec3=self.create_rrec(grp_eq[2][3].get_column(0),color=[PINK,YELLOW_A])
        rrec1.suspend_updating()
        rrec2.suspend_updating()
        rrec3.suspend_updating()
        grp_eq2=VGroup(
            VGroup(Tex('+').set_color(RED), Tex('1'),Tex(R'\times'),Tex('('),Tex('+').set_color(RED),Tex('5'),Tex(R'\times'),detMatrix([[9]]),Tex('-').set_color(BLUE),Tex('8'),Tex(R"\times"),detMatrix([[6]]),Tex(')')).arrange(RIGHT),
            VGroup(Tex('-').set_color(BLUE),Tex('4'),Tex(R'\times'),Tex('('),Tex('+').set_color(RED),Tex('2'),Tex(R'\times'),detMatrix([[9]]),Tex('-').set_color(BLUE),Tex('8'),Tex(R"\times"),detMatrix([[3]]),Tex(')')).arrange(RIGHT),
            VGroup(Tex('+').set_color(RED), Tex('7'),Tex(R'\times'),Tex('('),Tex('+').set_color(RED),Tex('2'),Tex(R'\times'),detMatrix([[6]]),Tex('-').set_color(BLUE),Tex('5'),Tex(R"\times"),detMatrix([[3]]),Tex(')')).arrange(RIGHT),
            ).arrange(DOWN).next_to(eq2,RIGHT)
        rec=Rectangle().surround(grp_eq).set_color(YELLOW)
        rec1=Rectangle().surround(grp_eq[0][3]).set_color(YELLOW)
        rec2=Rectangle().surround(grp_eq[1][3]).set_color(YELLOW)
        rec3=Rectangle().surround(grp_eq[2][3]).set_color(YELLOW)
        self.play(ShowCreation(rec))
        self.play(
            ReplacementTransform(rec,rec1),
            TransformFromCopy(rec,rec2),
            TransformFromCopy(rec,rec3),
            )
        self.wait(2)
        self.play(
            FadeOut(rec1),
            FadeOut(rec2),
            FadeOut(rec3),
            )

        self.play(
            AnimationGroup(
            TransformFromCopy(grp_eq[0][0:3],grp_eq2[0][0:3],path_arc=-1),
            FadeIn(grp_eq2[0][3]),
            FadeIn(grp_eq2[0][-1]),lag_ratio=0.3)
            )
        self.play(
            AnimationGroup(
            TransformFromCopy(grp_eq[1][0:3],grp_eq2[1][0:3],path_arc=-1),
            FadeIn(grp_eq2[1][3]),
            FadeIn(grp_eq2[1][-1]),lag_ratio=0.3),
            run_time=1.3)
        self.play(
            AnimationGroup(
            TransformFromCopy(grp_eq[2][0:3],grp_eq2[2][0:3],path_arc=-1),
            FadeIn(grp_eq2[2][3]),
            FadeIn(grp_eq2[2][-1]),lag_ratio=0.3),
            run_time=2)

        self.play(
            ShowCreation(rrec1),
            ShowCreation(rrec2),
            ShowCreation(rrec3),
            )
        rrec1.resume_updating()
        rrec2.resume_updating()
        rrec3.resume_updating()
        self.wait()

        # rrec
        self.play(
            TransformFromCopy(grp_eq[0][3].mob_matrix[0][0],grp_eq2[0][5]),
            TransformFromCopy(grp_eq[0][3].mob_matrix[1][0],grp_eq2[0][9]),
            )
        self.wait(0.5)
        self.play(
            TransformFromCopy(grp_eq[1][3].mob_matrix[0][0],grp_eq2[1][5]),
            TransformFromCopy(grp_eq[1][3].mob_matrix[1][0],grp_eq2[1][9]),)
        self.wait(0.5)
        self.play(
            TransformFromCopy(grp_eq[2][3].mob_matrix[0][0],grp_eq2[2][5]),
            TransformFromCopy(grp_eq[2][3].mob_matrix[1][0],grp_eq2[2][9]),)
        self.wait(0.5)
        self.play(
            FadeIn(grp_eq2[0][6],shift=UP),
            FadeIn(grp_eq2[0][10],shift=UP),
            FadeIn(grp_eq2[1][6],shift=UP),
            FadeIn(grp_eq2[1][10],shift=UP),
            FadeIn(grp_eq2[2][6],shift=UP),
            FadeIn(grp_eq2[2][10],shift=UP),
            )
        self.wait(0.5)
        self.play(
            FadeIn(grp_eq2[0][7].bars,shift=UP),
            FadeIn(grp_eq2[0][11].bars,shift=UP),
            FadeIn(grp_eq2[1][7].bars,shift=UP),
            FadeIn(grp_eq2[1][11].bars,shift=UP),
            FadeIn(grp_eq2[2][7].bars,shift=UP),
            FadeIn(grp_eq2[2][11].bars,shift=UP),
            )
        self.wait(0.5)

        # +-+-+-
        def shake_transform_anims(shake_grp,m_sign,target_signs):
            SCALE=1
            p=np.array(shake_grp.get_center())
            self.play(shake_grp.animate.scale(SCALE).align_to(m_sign,UL))
            shake_updater=get_shake_updater(self.time,np.copy(shake_grp.get_center()))
            shake_grp.add_updater(shake_updater)
            self.wait()
            self.play(
                TransformFromCopy(m_sign.mob_matrix[0][0],target_signs[0]),
                TransformFromCopy(m_sign.mob_matrix[1][0],target_signs[1]),
                rate_func=rush_into
                )
            shake_grp.remove_updater(shake_updater)
            self.play(shake_grp.animate.scale(1/SCALE).move_to(p))

        shake_grp=VGroup(grp_eq[0][3].get_entries(),rrec1)
        targets=VGroup(grp_eq2[0][4],grp_eq2[0][8])
        shake_transform_anims(shake_grp,m_sign,targets)

        shake_grp=VGroup(grp_eq[1][3].get_entries(),rrec2)
        targets=VGroup(grp_eq2[1][4],grp_eq2[1][8])
        shake_transform_anims(shake_grp,m_sign,targets)

        shake_grp=VGroup(grp_eq[2][3].get_entries(),rrec3)
        targets=VGroup(grp_eq2[2][4],grp_eq2[2][8])
        shake_transform_anims(shake_grp,m_sign,targets)

        # 3 cover strips
        det_matrix1=grp_eq[0][3]
        det_matrix2=grp_eq[1][3]
        det_matrix3=grp_eq[2][3]
        target1=grp_eq2[0][7].mob_matrix[0][0]
        target2=grp_eq2[1][7].mob_matrix[0][0]
        target3=grp_eq2[2][7].mob_matrix[0][0]
        cover_strips1=get_cover_strip(det_matrix1,0,0)
        cover_strips2=get_cover_strip(det_matrix2,0,0)
        cover_strips3=get_cover_strip(det_matrix3,0,0)
        target_rrec1=self.create_rrec(det_matrix1.mob_matrix[0][0],color=[PINK,YELLOW_A])
        target_rrec2=self.create_rrec(det_matrix2.mob_matrix[0][0],color=[PINK,YELLOW_A])
        target_rrec3=self.create_rrec(det_matrix3.mob_matrix[0][0],color=[PINK,YELLOW_A])
        self.play(
            PhaseAlignedTransform(rrec1,target_rrec1),
            PhaseAlignedTransform(rrec2,target_rrec2),
            PhaseAlignedTransform(rrec3,target_rrec3),
            )
        self.play(
            FadeIn(cover_strips1[0],shift=RIGHT),FadeIn(cover_strips1[1],shift=DOWN),
            FadeIn(cover_strips2[0],shift=RIGHT),FadeIn(cover_strips2[1],shift=DOWN),
            FadeIn(cover_strips3[0],shift=RIGHT),FadeIn(cover_strips3[1],shift=DOWN),
            )
        self.play(
            TransformFromCopy(det_matrix1.get_minor(0,0)[0],target1,path_arc=-1),
            TransformFromCopy(det_matrix2.get_minor(0,0)[0],target2,path_arc=-1),
            TransformFromCopy(det_matrix3.get_minor(0,0)[0],target3,path_arc=-1),
            )
        self.play(
            FadeOut(cover_strips1[0],shift=RIGHT),FadeOut(cover_strips1[1],shift=DOWN),
            FadeOut(cover_strips2[0],shift=RIGHT),FadeOut(cover_strips2[1],shift=DOWN),
            FadeOut(cover_strips3[0],shift=RIGHT),FadeOut(cover_strips3[1],shift=DOWN),
            )
        target1=grp_eq2[0][11].mob_matrix[0][0]
        target2=grp_eq2[1][11].mob_matrix[0][0]
        target3=grp_eq2[2][11].mob_matrix[0][0]
        cover_strips1=get_cover_strip(det_matrix1,1,0)
        cover_strips2=get_cover_strip(det_matrix2,1,0)
        cover_strips3=get_cover_strip(det_matrix3,1,0)
        new_target_rrec1=self.create_rrec(det_matrix1.mob_matrix[1][0],color=[PINK,YELLOW_A])
        new_target_rrec2=self.create_rrec(det_matrix2.mob_matrix[1][0],color=[PINK,YELLOW_A])
        new_target_rrec3=self.create_rrec(det_matrix3.mob_matrix[1][0],color=[PINK,YELLOW_A])
        self.play(
            PhaseAlignedTransform(target_rrec1,new_target_rrec1),
            PhaseAlignedTransform(target_rrec2,new_target_rrec2),
            PhaseAlignedTransform(target_rrec3,new_target_rrec3),
            )
        self.play(
            FadeIn(cover_strips1[0],shift=RIGHT),FadeIn(cover_strips1[1],shift=DOWN),
            FadeIn(cover_strips2[0],shift=RIGHT),FadeIn(cover_strips2[1],shift=DOWN),
            FadeIn(cover_strips3[0],shift=RIGHT),FadeIn(cover_strips3[1],shift=DOWN),
            )
        self.play(
            TransformFromCopy(det_matrix1.get_minor(1,0)[0],target1,path_arc=-1),
            TransformFromCopy(det_matrix2.get_minor(1,0)[0],target2,path_arc=-1),
            TransformFromCopy(det_matrix3.get_minor(1,0)[0],target3,path_arc=-1),
            )
        self.play(
            FadeOut(cover_strips1[0],shift=RIGHT),FadeOut(cover_strips1[1],shift=DOWN),
            FadeOut(cover_strips2[0],shift=RIGHT),FadeOut(cover_strips2[1],shift=DOWN),
            FadeOut(cover_strips3[0],shift=RIGHT),FadeOut(cover_strips3[1],shift=DOWN),
            )
        self.play(*map(FadeOut,[new_target_rrec1,new_target_rrec2,new_target_rrec3]))

        # compute result
        result_before=VGroup(
            VGroup(Tex('+').set_color(RED),  Tex('1'),Tex(R'\times'),Tex('('),Tex('-3'),Tex(')')).arrange(RIGHT),
            VGroup(Tex('-').set_color(BLUE), Tex('4'),Tex(R'\times'),Tex('('),Tex('-6'),Tex(')')).arrange(RIGHT),
            VGroup(Tex('+').set_color(RED),  Tex('7'),Tex(R'\times'),Tex('('),Tex('-3'),Tex(')')).arrange(RIGHT),
            ).arrange(DOWN).next_to(eq2,RIGHT)
        result_after=VGroup(Tex('-3'),Tex('+24'),Tex('-21')).arrange(RIGHT,buff=0.5).next_to(eq2,RIGHT)
        result=Tex('0').scale(1.5).next_to(eq2,RIGHT)
        self.play(LaggedStart(
            AnimationGroup(
            ReplacementTransform(grp_eq2[0][:4],result_before[0][:4]),
            ReplacementTransform(grp_eq2[0][4:-1],result_before[0][4:-1]),
            ReplacementTransform(grp_eq2[0][-1],result_before[0][-1]),),
            AnimationGroup(
            ReplacementTransform(grp_eq2[1][:4],result_before[1][:4]),
            ReplacementTransform(grp_eq2[1][4:-1],result_before[1][4:-1]),
            ReplacementTransform(grp_eq2[1][-1],result_before[1][-1]),),
            AnimationGroup(
            ReplacementTransform(grp_eq2[2][:4],result_before[2][:4]),
            ReplacementTransform(grp_eq2[2][4:-1],result_before[2][4:-1]),
            ReplacementTransform(grp_eq2[2][-1],result_before[2][-1]),),
            lag_ratio=0.5
            ))
        self.play(LaggedStart(
            ReplacementTransform(result_before[0],result_after[0],path_arc=60*DEGREES),
            ReplacementTransform(result_before[1],result_after[1],path_arc=60*DEGREES),
            ReplacementTransform(result_before[2],result_after[2],path_arc=60*DEGREES),
            lag_ratio=0.5
            ))
        self.wait(0.5)
        self.play(ReplacementTransform(result_after,result,path_arc=60*DEGREES))
        self.wait(0.5)

        # fadeout2
        m3.remove(*m3.brackets).add(bars_m3)
        self.play(
            FadeOut(title,shift=UP),
            FadeOut(m_sign,shift=RIGHT),
            FadeOut(eq,shift=DOWN),FadeOut(grp_eq,shift=DOWN),
            VGroup(m3,eq2,result).animate.arrange(RIGHT).to_frame_center(frame),
            frame.animate.scale(0.7),
            run_time=1.5
            )
        self.wait(3)
        self.play(FlashAround(result,color=[YELLOW,TEAL],stroke_width=5),run_time=1.5)

        # rank
        new_m3 = m3.copy()
        bars_m3_copy = new_m3.submobjects[m3.submobjects.index(bars_m3)]
        new_m3.remove(bars_m3_copy)
        new_m3.add(new_m3.create_brackets(new_m3.rows,0.2,0.25))
        grp=VGroup(
            VGroup(Text('秩',font='WenCang'),Tex('('))\
            .arrange(RIGHT).scale(3).set_color(TEAL),
            new_m3,
            VGroup( Tex(')'),Tex('<'),Tex('3') )\
            .arrange(RIGHT).scale(3).set_color(TEAL)
            ).arrange(RIGHT).to_frame_center(frame)
        grp[0][1].stretch_to_fit_height(new_m3.get_height())
        grp[2][0].stretch_to_fit_height(new_m3.get_height())
        self.play(
            FadeOut(eq2,shift=RIGHT),
            FadeOut(result,shift=RIGHT),
            ReplacementTransform(m3[:-1],new_m3[:-1]),
            FadeTransform(m3[-1],new_m3[-1]))
        self.play(
            FadeIn(grp[0][1],shift=UP*2),
            FadeIn(grp[2][0],shift=DOWN*2),
            Write(grp[0][0],stroke_color=WHITE)
            )
        self.play(FadeIn(grp[2][1],shift=LEFT))

        # decimal number
        colrec,rowrec=self.get_c_r(new_m3,color_col=TEAL)
        num1=DecimalNumber(1,num_decimal_places=0).replace(grp[2][2]).match_style(grp[2][2])
        self.play(LaggedStart(*[FadeIn(c,shift=DOWN) for c in colrec],lag_ratio=0.2))
        self.play(ReplacementTransform(colrec[0],num1[0][0],path_arc=-150*DEGREES))
        target=Tex('+1').scale(2).set_color(YELLOW).next_to(num1,RIGHT+UP).rotate(10*DEGREES)
        self.play(
            Transform(colrec[1],target,path_arc=-150*DEGREES,remover=True),
            ChangeDecimalToValue(num1,2))
        self.play(
            Transform(colrec[2],target,path_arc=-150*DEGREES,remover=True),
            ChangeDecimalToValue(num1,3))
        self.wait(6)

        # next_video
        rainbow=[RED,ORANGE,YELLOW,GREEN,TEAL,BLUE,PURPLE]
        next_video=Text('下个视频介绍',font='WenCang')
        next_video.scale(1.5)
        next_video.to_frame_edge(frame,UP)
        rrec=self.create_rrec(VGroup(grp[0],grp[1],grp[2][0]).copy().to_frame_center(frame).shift(DOWN),
            buff=0.5,color=rainbow,width=[1,5],
            num_insert_curves=300)
        arrow=Arrow(next_video.get_bottom(),rrec.get_top())
        how_to=Text('如何求?',font='WenCang').scale(1.5)
        how_to.next_to(arrow,RIGHT)
        rrec.suspend_updating()
        self.play(
            FadeOut(grp[2][1],shift=RIGHT),
            FadeOut(num1,shift=RIGHT),
            VGroup(grp[0],grp[1],grp[2][0]).animate.to_frame_center(frame).shift(DOWN),
            ShowCreation(rrec),
            FadeIn(next_video,lag_ratio=0.3))
        rrec.resume_updating()
        self.play(GrowArrow(arrow),FadeIn(how_to,lag_ratio=0.2))
        self.wait(20)

class higher_matrix(detMatrixScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        self.set_floor_plane('xz')
        # frame.set_focal_distance(50)
        np1=np.array([[1]])
        np2=np.array([[1,2],[3,4]])
        np3=np.array([[1,2,3],[4,5,6],[7,8,9]])
        np4=np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
        np5=np.array([[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]])
        t=Tex('.').get_grid(1,10)
        t.arrange(IN,buff=1)
        m1=detMatrix(np1,replace_brackets_with_bars=False)
        m2=detMatrix(np2,replace_brackets_with_bars=False)
        m3=detMatrix(np3,replace_brackets_with_bars=False)
        m4=detMatrix(np4,replace_brackets_with_bars=False)
        m5=detMatrix(np5,replace_brackets_with_bars=False)
        grp=VGroup(m1,m2,m3,m4,m5,t).arrange(IN,buff=5)
        grp.set_opacity(0)
        m3.set_opacity(1)
        self.add(m3)
        frame.move_to(m3).scale(0.4)
        m1.shift(IN*5)
        m2.shift(IN*2)
        m5.shift(IN*4)
        self.wait()
        self.play(
            frame.animate.reorient(43, -17, 0, (-3.18, -1.45, 3.07), 12.71),
            grp.animate.set_opacity(1),rate_func=linear,run_time=2
            )
        anims=[]
        rrecs=[]
        for m in grp[0:5]:
            rrec=self.create_rrec(m.get_column(0))
            rrec.suspend_updating()
            rrecs.append(rrec)
            bars=m.get_bars()
            anims.append( FadeInOut(bars,m.brackets) )
        frame.add_ambient_rotation()
        self.play(*anims,run_time=1.5)
        self.play(*[ShowCreation(rrec) for rrec in rrecs])
        for rrec in rrecs:
            rrec.resume_updating()
        self.wait(10)
        frame.clear_updaters()
        # self.add(grp)


class intro(detMatrixScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        det = np.linalg.det
        a1=np.array([[1,2],[3,4]])
        a2=np.array([[1,2,3],[4,5,6]])
        a3=np.array([[1,2],[3,4],[5,6]])
        a4=np.array([[1,2,3],[4,5,6],[7,8,9]])
        title=Textch('如何求矩阵的行列式',font='WenCang')
        title.scale(3)
        self.add(title)
        self.play(FadeIn(title,lag_ratio=0.5))
        self.wait()

        # play a game
        t1=Text('找正方形',font='WenCang')\
        .scale(2).to_edge(UP).set_color(TEAL)
        m1=Matrix(a1)
        m2=Matrix(a2)
        m3=Matrix(a3)
        m4=Matrix(a4)
        grp=VGroup(m1,m2,m3,m4).arrange_in_grid(2,2).next_to(t1,DOWN,buff=0.5)
        # self.add(t1)
        # self.add(grp)
        self.remove(title)
        self.play(LaggedStartMap(FadeIn,VGroup(t1,m1,m2,m3,m4),shift=LEFT,
            lag_ratio=0.3))
        c1,r1=self.get_c_r(m1)
        c2,r2=self.get_c_r(m2)
        c3,r3=self.get_c_r(m3)
        c4,r4=self.get_c_r(m4)
        bars1=self.get_bars(m1)
        bars4=self.get_bars(m4)
        self.wait()
        self.play(
            AnimationGroup(
                *[FadeIn(r,shift=RIGHT) for r in r1],
                *[FadeIn(c,shift=DOWN) for c in c1],lag_ratio=0.3)
            )
        s1=SurroundingRectangle(m1,fill_color=TEAL,fill_opacity=0.5,stroke_color=TEAL,buff=0)
        self.play(FadeTransform(VGroup(c1,r1),s1))
        self.play(FadeOut(s1))
        self.play(FadeInOut(VGroup(bars1[0],bars1[1]),VGroup(m1.brackets[0],m1.brackets[1])),)
        self.wait(0.5)

        # m2
        self.play(
            AnimationGroup(
                *[FadeIn(r,shift=RIGHT) for r in r2],
                *[FadeIn(c,shift=DOWN) for c in c2],lag_ratio=0.3)
            )
        cross2=Cross(m2)
        self.play(ShowCreation(cross2),FadeOut(c2),FadeOut(r2))
        self.wait(0.5)
        self.play(
            AnimationGroup(
                *[FadeIn(r,shift=RIGHT) for r in r3],
                *[FadeIn(c,shift=DOWN) for c in c3],lag_ratio=0.3)
            )
        cross3=Cross(m3)
        self.play(ShowCreation(cross3),FadeOut(c3),FadeOut(r3))
        self.wait(0.5)
        self.play(
            AnimationGroup(
                *[FadeIn(r,shift=RIGHT) for r in r4],
                *[FadeIn(c,shift=DOWN) for c in c4],lag_ratio=0.3)
            )
        s4=SurroundingRectangle(m4,fill_color=TEAL,fill_opacity=0.5,stroke_color=TEAL,buff=0)
        self.play(FadeTransform(VGroup(c4,r4),s4))
        self.play(FadeOut(s4))
        self.play(FadeInOut(VGroup(bars4[0],bars4[1]),VGroup(m4.brackets[0],m4.brackets[1])),)
        self.wait(0.5)



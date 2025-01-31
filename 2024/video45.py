from manim_imports_custom import *

class video4(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame

        # write title
        title0=TextCustom(en='Linear Transformation Wizard',ch='线性变换魔法师')
        title0.en["Linear Transformation"].set_color(RED_A)
        title0.ch["线性变换"].set_color(RED_A)
        title0.scale(1.3)
        self.play(FadeIn(title0.en,shift=RIGHT),FadeIn(title0.ch,shift=LEFT))
        self.wait(2)
        # self.play(FadeOut(title0.en,shift=RIGHT),FadeOut(title0.ch,shift=LEFT))
         
        # title--rotation
        title=TextCustom(en='Rotation Transformation',ch='旋转变换')
        title.scale(1.5)
        title.en["Rotation"].set_color(TEAL_A)
        title.ch["旋转"].set_color(TEAL_A)
        # self.play(FadeIn(title.en,shift=RIGHT),FadeIn(title.ch,shift=LEFT))
        title2=TextCustom(en='Rotation Marix',ch='旋转矩阵')
        title2.en["Rotation"].set_color(TEAL)
        title2.ch["旋转"].set_color(TEAL)
        title2.scale(1.5)
        title2.add_updater(lambda m,dt:m.rotate(dt*PI/20,axis=UP))
        self.play(ReplacementTransform(title0.en,title.en),
            ReplacementTransform(title0.ch,title.ch),run_time=2)
        self.wait()
        self.play(ReplacementTransform(title.en['Rotation'],title2.en["Rotation"]),
            ReplacementTransform(title.ch['旋转'],title2.ch["旋转"]),
            LaggedStartMap(FadeOut,VGroup(title.en["Transformation"],title.ch["变换"]),shift=DOWN*2),
            LaggedStartMap(FadeIn,VGroup(title2.en["Marix"],title2.ch["矩阵"]),shift=DOWN*2))
        self.play(title2.animate.arrange(DOWN,aligned_edge=LEFT).scale(0.7).to_edge(LEFT,buff=1))
        
        # arrange down
        text_orthogonal=TextCustom(en='Orthogonal Matrix',ch='正交矩阵',aligned_edge=LEFT)
        text_det=TextCustom(en='Determinant is 1',ch='行列式为1',aligned_edge=LEFT)
        text_grp=VGroup(text_orthogonal,text_det)
        text_grp.arrange(DOWN,buff=2,aligned_edge=LEFT)
        text_grp.to_edge(RIGHT,buff=1)
        tex_orthogonal=Tex(R"A A^\intercal=I",t2c={R"\intercal":TEAL})
        tex_det=Tex(R"\det (A)=1",t2c={R"\det":TEAL})
        tex_orthogonal.scale(1.5)
        tex_det.scale(1.5)
        tex_orthogonal.move_to(text_orthogonal,aligned_edge=LEFT)
        tex_det.move_to(text_det,aligned_edge=LEFT)
        tex_grp=VGroup(tex_orthogonal,tex_det)
        brace=Brace(text_grp,direction=LEFT,buff=1)
        text_orthogonal.en['Orthogonal'].set_color(TEAL)
        text_orthogonal.ch['正交'].set_color(TEAL)
        text_det.en['Determinant'].set_color(TEAL)
        text_det.ch['行列式'].set_color(TEAL)
        self.play(Write(brace),run_time=1)
        self.play(LaggedStartMap(Write,VGroup(text_orthogonal.en,text_orthogonal.ch)),run_time=1)
        self.wait(2)
        self.play(LaggedStartMap(Write,VGroup(text_det.en,text_det.ch)),run_time=1)
        self.wait(2)
        self.play(LaggedStartMap(FadeOut,text_grp,shift=RIGHT*2),
                LaggedStartMap(FadeIn,tex_grp,shift=RIGHT*2),run_time=1)
        self.wait(3)
        self.play(LaggedStartMap(FadeOut,VGroup(title2,brace),shift=LEFT,run_time=0.5),
                 tex_grp.animate.set_anim_args(run_time=1.5)
                 .scale(0.7).arrange(DOWN,aligned_edge=LEFT,buff=0.5).to_corner(UL))
        
        # check matrix 
        mat=Matrix([[Tex(R"\cos \theta"),Tex(R"-\sin \theta"),Tex(R'0')],
                    [Tex(R"\sin \theta"),Tex(R"\cos \theta") ,Tex(R'0')],
                    [Tex(R'0')          ,Tex(R'0')           ,Tex(R'1')]])

        color_palette=[RED,BLUE,YELLOW]
        for row, color in zip(mat.rows, color_palette):
            row.set_color(color)
        mat_t=Matrix(list(map(list, zip(*mat.deepcopy().get_mob_matrix()))))
        mat_t.to_edge(RIGHT)
        mats=VGroup(mat,mat_t).arrange(RIGHT)
        mat.save_state()
        mat.center()
        text_A=Tex('A',font_size=60)
        text_A.always.next_to(mat,UP)
        text_A.suspend_updating()
        self.play(LaggedStartMap(Write,VGroup(mat,text_A),lag_ratio=0.5),run_time=1)
        text_A.resume_updating()

        # transpose animation
        run_time=1
        row=col=0
        text_A_T=Tex(R'A^\intercal',t2c={R"\intercal":TEAL},font_size=60)
        text_A_T.next_to(mat_t,UP)
        self.play(mat.animate.restore())
        self.play(Write(mat_t.brackets[0]),Write(text_A_T))
        self.play(LaggedStart(
            TransformMatchingStrings(mat.get_row(row)[0].copy(),mat_t.get_column(col)[0]),
            TransformMatchingStrings(mat.get_row(row)[1].copy(),mat_t.get_column(col)[1]),
            TransformMatchingStrings(mat.get_row(row)[2].copy(),mat_t.get_column(col)[2]),
            lag_ratio=0.02),run_time=run_time)
        row=col=1
        self.play(LaggedStart(
            TransformMatchingStrings(mat.get_row(row)[0].copy(),mat_t.get_column(col)[0]),
            TransformMatchingStrings(mat.get_row(row)[1].copy(),mat_t.get_column(col)[1]),
            TransformMatchingStrings(mat.get_row(row)[2].copy(),mat_t.get_column(col)[2]),
            lag_ratio=0.02),run_time=run_time)
        row=col=2
        self.play(LaggedStart(
            TransformMatchingStrings(mat.get_row(row)[0].copy(),mat_t.get_column(col)[0]),
            TransformMatchingStrings(mat.get_row(row)[1].copy(),mat_t.get_column(col)[1]),
            TransformMatchingStrings(mat.get_row(row)[2].copy(),mat_t.get_column(col)[2]),
            lag_ratio=0.02),run_time=run_time)
        self.play(Write(mat_t.brackets[1]),run_time=0.5)


        # multiply animation
        tex_grp.fix_in_frame()
        self.play(frame.animate.reorient(0, 0, 0, (1.88, 0.36, 0.0), 9.61))

        # multi_layout
        equal_sign=Tex(R'=')
        equal_sign.next_to(mat_t,RIGHT)
        mat_result=Matrix([[1,0,0],[0,1,0],[0,0,1]])
        mat_result.elements[0].set_color(color_palette[0])
        mat_result.elements[4].set_color(color_palette[1])
        mat_result.elements[8].set_color(color_palette[2])
        mat_result.next_to(equal_sign,RIGHT)
        self.play(Write(equal_sign),run_time=0.5)

        # ani
        def create_temp_multiply(part1,part2,part3,result,color=RED):
            part1=Tex(part1).set_color(color)
            part2=Tex(part2).set_color(color)
            part3=Tex(part3).set_color(color)
            result=Tex(result).set_color(color)
            plus1=Tex('+')
            plus2=Tex('+')
            equal=Tex('=')
            temp_grp=VGroup(part1,plus1,part2,plus2,part3,equal,result)
            temp_grp.arrange(RIGHT,aligned_edge=DOWN)
            equal.match_y(plus1)
            temp_grp.next_to(VGroup(mat,mat_t),UP,buff=0.5)
            return temp_grp

        def mutiply_animation(temp_grp,row=0,col=0,run_time=1):
            temp_grp=temp_grp
            self.play(FlashAround(mat.get_row(row)),
                FlashAround(mat_t.get_column(col)),run_time=run_time)
            self.play(
                LaggedStart(
                TransformFromCopy(VGroup(mat.get_row(row)[0],mat_t.get_column(col)[0]),temp_grp[0]),
                TransformFromCopy(VGroup(mat.get_row(row)[1],mat_t.get_column(col)[1]),temp_grp[2]),
                TransformFromCopy(VGroup(mat.get_row(row)[2],mat_t.get_column(col)[2]),temp_grp[4]),
                lag_ratio=0.5),run_time=run_time,
                )
            self.play(LaggedStart(
                LaggedStartMap(Write,VGroup(temp_grp[1],temp_grp[3],temp_grp[5]),lag_ratio=0.2),
                TransformFromCopy(VGroup(temp_grp[0],temp_grp[2],temp_grp[4]),temp_grp[6],path_arc=-1),
                lag_ratio=0.3),run_time=run_time)
            self.play(TransformFromCopy(temp_grp[6],mat_result.elements[row*3+col]),
                LaggedStartMap(FadeOut,temp_grp,shift=RIGHT),run_time=run_time/2)

        temp_grp0=create_temp_multiply(R"\cos^2\theta",R"\sin^2\theta",R'0',R'1',RED)
        temp_grp1=create_temp_multiply(R"\cos\theta\sin\theta",R"(-\sin\theta\cos\theta)",R'0',R'0',WHITE)
        temp_grp2=create_temp_multiply(R"0",R"0",R'0',R'0',WHITE)
        temp_grp3=create_temp_multiply(R"\sin\theta\cos\theta",R"(-\cos\theta\sin\theta)",R'0',R'0',WHITE)
        temp_grp4=create_temp_multiply(R"\sin^2\theta",R"\cos^2\theta",R'0',R'1',BLUE)
        temp_grp5=create_temp_multiply(R"0",R"0",R'0',R'0',WHITE)
        temp_grp6=create_temp_multiply(R"0",R"0",R'0',R'0',WHITE)
        temp_grp7=create_temp_multiply(R"0",R"0",R'0',R'0',WHITE)
        temp_grp8=create_temp_multiply(R"0",R"0",R'1',R'1',YELLOW)

        text_A.clear_updaters()
        text_A_T.clear_updaters()
        self.play(Write(mat_result.brackets[0]),
                text_A.animate.next_to(mat,DOWN),
                text_A_T.animate.next_to(mat_t,DOWN),run_time=1)
        mutiply_animation(temp_grp0,0,0,run_time=1.5)
        mutiply_animation(temp_grp1,0,1,run_time=1.5)
        mutiply_animation(temp_grp2,0,2,run_time=1)
        mutiply_animation(temp_grp3,1,0,run_time=1)
        mutiply_animation(temp_grp4,1,1,run_time=1)
        mutiply_animation(temp_grp5,1,2,run_time=1)
        mutiply_animation(temp_grp6,2,0,run_time=1)
        mutiply_animation(temp_grp7,2,1,run_time=1)
        mutiply_animation(temp_grp8,2,2,run_time=1)

        # identity
        text_I=Tex(R"I",font_size=60)
        text_I.next_to(mat_result,DOWN)
        text_A_copy=text_A.copy()
        check_grp=VGroup(text_A_copy,text_A_T,equal_sign,text_I)
        check_mark1=Tex(R"\checkmark")
        check_mark1.set_color(RED)
        check_mark1.fix_in_frame()
        check_mark1.next_to(tex_orthogonal,RIGHT)
        text_A.always.next_to(mat,DOWN)
        self.play(Write(mat_result.brackets[1]),Write(text_I),run_time=0.5)
        self.play(LaggedStartMap(FadeOut,VGroup(mat_t,mat_result),shift=RIGHT),
            mat.animate.center(),frame.animate.to_default_state(),
            check_grp.animate.arrange(RIGHT).fix_in_frame().next_to(check_mark1,RIGHT,buff=1))
        self.play(ReplacementTransform(check_grp,check_mark1))
        # self.play(Write(check_mark1,run_time=1.5),FadeOut(check_grp,shift=UP))

        # determinant-arrange
        left_vert=Line(start=mat.get_corner(DL),end=mat.get_corner(UL),color=TEAL)
        left_vert.scale(1.1)
        right_vert=Line(start=mat.get_corner(DR),end=mat.get_corner(UR),color=TEAL)
        right_vert.scale(1.1)
        verts=VGroup(left_vert,right_vert)
        tex_det2=Tex(R"\det")
        tex_brackets=Tex(R"(\hspace{9pt})")
        tex_det2.next_to(text_A,LEFT).set_color(TEAL)
        tex_brackets.next_to(tex_det2,RIGHT,buff=0.12).set_color(TEAL)
        text_A.clear_updaters()
        grp_det_A=VGroup(tex_det2,tex_brackets,text_A)
        grp_det_A.suspend_updating()
        mat_elements_grp=VGroup(*mat.elements)
        grp_det_A.always.next_to(mat_elements_grp,DOWN,buff=0.2)
        left_vert.always.match_height(mat_elements_grp).next_to(mat_elements_grp,LEFT)
        right_vert.always.match_height(mat_elements_grp).next_to(mat_elements_grp,RIGHT)
        self.play(FadeTransform(mat.brackets,verts),Write(tex_det2),Write(tex_brackets))
        self.play(mat_elements_grp.animate.arrange_in_grid(3,3,buff=0.2).set_color(WHITE),
            grp_det_A.animate.resume_updating())
        grp_det_A.resume_updating()
        self.play(mat_elements_grp.animate.to_edge(UP))

        # determinant--calculate
        equal_sign=Tex(R'=')
        equal_sign.scale(1.5)
        path=VMobject()
        path.set_points(mat.get_row(0)[2].get_center())
        path.add_arc_to(mat.get_row(2)[1].get_center(),angle=-TAU*6/10)
        path.add_line_to(mat.get_row(1)[0].get_center())
        coefficient1=Tex('0')
        det1=MatrixDet([[Tex(R"-\sin\theta"),Tex(R'0')],
                        [Tex(R'\cos\theta'),Tex(R'0')]],v_buff=0.25,h_buff=0,bracket_v_buff=0.1)
        sign1=Tex('-')
        sign1.set_color(RED)
        coefficient2=Tex('0')
        det2=MatrixDet([[Tex(R'\cos\theta'),Tex(R"0")],
                        [Tex(R'\sin\theta'),Tex(R'0')]],v_buff=0.25,h_buff=0,bracket_v_buff=0.1)
        sign2=Tex('+')
        coefficient3=Tex('1')
        det3=MatrixDet([[Tex(R'\cos\theta'),Tex(R"-\sin\theta")],
                        [Tex(R'\sin\theta'),Tex(R'\cos\theta')]],v_buff=0.25,h_buff=0.2,bracket_v_buff=0.1)
        det_grp=VGroup(equal_sign,coefficient1,det1,sign1,coefficient2,det2,sign2,coefficient3,det3).arrange(RIGHT)
        line1=Line(mat.get_row(2)[0].get_top()+UP*0.05,mat.get_row(2)[0].get_top()+UP*1.5)
        line2=Line(mat.get_row(2)[0].get_right()+RIGHT*0.05,mat.get_row(2)[0].get_right()+RIGHT*3.8)
        line3=Line(mat.get_row(2)[1].get_top()+UP*0.05,mat.get_row(2)[1].get_top()+UP*1.5)
        line4=Line(mat.get_row(2)[1].get_right()+RIGHT*0.05,mat.get_row(2)[1].get_right()+RIGHT*2.3)
        line5=Line(mat.get_row(2)[1].get_left()+LEFT*0.05,mat.get_row(2)[1].get_left()+LEFT*2.9)
        line6=Line(mat.get_row(2)[2].get_top()+UP*0.05,mat.get_row(2)[2].get_top()+UP*1.5)
        line7=Line(mat.get_row(2)[2].get_left(),mat.get_row(2)[2].get_left()+LEFT*4.3)
        line_grp1=VGroup(line1,line2)
        line_grp2=VGroup(line3,line4,line5)
        line_grp3=VGroup(line6,line7)
        self.play(Write(equal_sign))
        self.play(*map(Write,line_grp1),
            VGroup( mat.get_row(0)[0],mat.get_row(1)[0],mat.get_row(2)[1],mat.get_row(2)[2])\
            .animate.set_opacity(0.5) )
        self.play(TransformFromCopy(mat.get_row(2)[0],coefficient1),
            TransformMatchingParts( VGroup(mat.get_row(0)[1:],mat.get_row(1)[1:]).copy(),
                VGroup(*det1.elements) ),Write(det1.brackets) )
        self.play(Write(sign1),*map(Uncreate,line_grp1),VGroup(*mat.elements).animate.set_opacity(1))
        self.play(*map(Write,line_grp2),
            VGroup( mat.get_row(0)[1],mat.get_row(1)[1],mat.get_row(2)[0],mat.get_row(2)[2])\
            .animate.set_opacity(0.5) )
        self.play(TransformFromCopy(mat.get_row(2)[1],coefficient2),
            TransformMatchingParts( VGroup(mat.get_row(0)[0],mat.get_row(0)[2],
                mat.get_row(1)[0],mat.get_row(1)[2]).copy(),
                VGroup(*det2.elements) ),Write(det2.brackets) )
        self.play(Write(sign2),*map(Uncreate,line_grp2),VGroup(*mat.elements).animate.set_opacity(1))
        self.play(*map(Write,line_grp3),
            VGroup( mat.get_row(0)[2],mat.get_row(1)[2],mat.get_row(2)[0],mat.get_row(2)[1])\
            .animate.set_opacity(0.5) )
        self.play(TransformFromCopy(mat.get_row(2)[2],coefficient3),
            TransformMatchingParts( VGroup(mat.get_row(0)[0],mat.get_row(0)[1],
                mat.get_row(1)[0],mat.get_row(1)[1]).copy(),
                VGroup(*det3.elements) ),Write(det3.brackets) )
        self.play(*map(Uncreate,line_grp3),VGroup(*mat.elements).animate.set_opacity(1))

        # cancel equation
        line1=Line(end=RIGHT*2.5).rotate(-30*DEGREES).set_color(RED)
        line1.move_to(det1)
        line2=line1.copy().move_to(det2)
        self.play( LaggedStart(Write(line1),Write(line2),lag_ratio=0.5),
        LaggedStart(VGroup(coefficient1,det1).animate.set_opacity(0.5),
        VGroup(sign1,coefficient2,det2).animate.set_opacity(0.5),lag_ratio=0.5) )
        self.play( LaggedStart(LaggedStartMap(FadeOut,VGroup(
                coefficient1,line1,det1,sign1,coefficient2,line2,det2,sign2,coefficient3
            ),shift=LEFT*3),det3.animate.next_to(equal_sign,RIGHT) ,lag_ratio=0.5))
        
        # cos^2+sin^2
        path=VMobject(stroke_color=TEAL,stroke_width=5)\
            .set_points_smoothly([det3.elements[0].get_center(),
            det3.elements[3].get_center(),det3.elements[1].get_center(),
            det3.elements[2].get_center(),])
        path.close_path()
        dot=GlowDot(path.get_start(),radius=0.3)
        tt=TracingTail(dot,time_traced=0.7)
        eqn=Tex(R"\cos^2\theta-(-\sin^2\theta)")
        eqn[5].set_color(RED)
        equal_sign2=equal_sign.copy()
        equal_sign2.next_to(equal_sign,DOWN,buff=1.5)
        eqn.next_to(equal_sign2,RIGHT)
        self.add(tt)
        self.play(MoveAlongPath(dot,path),Write(equal_sign2),Write(eqn[5]))
        self.play(LaggedStart(
            AnimationGroup(FadeTransform(det3.elements[0][R"\cos"].copy(),eqn[0:3]),
                           FadeTransform(det3.elements[0][R"\theta"].copy(),eqn[4]),
                           det3.elements[0].animate.set_opacity(0.5),
                           det3.elements[3].animate.set_opacity(0.5)),
            TransformFromCopy(det3.elements[3],eqn[3]),lag_ratio=0.5),run_time=2 )
        self.play(LaggedStart(
            MoveAlongPath(dot,path),
            AnimationGroup(FadeTransform(det3.elements[1][R"-\sin"].copy(),eqn[7:11]),
                           FadeTransform(det3.elements[1][R"\theta"].copy(),eqn[12]),
                           det3.elements[1].animate.set_opacity(0.5),
                           det3.elements[2].animate.set_opacity(0.5)),
            TransformFromCopy(det3.elements[2],eqn[11]),
            AnimationGroup(Write(eqn[6]),Write(eqn[-1])),lag_ratio=0.5),run_time=2 )
        plus=Tex(R'+').move_to(eqn[5])
        self.play(FadeOut(dot),ReplacementTransform(VGroup(eqn[5:8],eqn[-1]),plus),
                eqn[8:13].animate.next_to(plus,RIGHT).match_y(eqn[:5]))
        one=Tex("1").next_to(equal_sign2)
        self.play(ReplacementTransform(VGroup(eqn,plus),one))
        self.play(LaggedStartMap(FadeOut,VGroup(equal_sign,det3),shift=LEFT),
            VGroup(equal_sign2,one).animate.next_to(grp_det_A,RIGHT))
        check_mark2=check_mark1.copy().next_to(tex_det)
        grp_det_A.clear_updaters()
        self.play(ReplacementTransform(VGroup(grp_det_A,equal_sign2,one),check_mark2))
        self.play(LaggedStartMap(FadeOut,VGroup(tex_grp,check_mark1,check_mark2),shift=LEFT))
        
        # move matrix to corner
        mat.brackets.set_height(VGroup(*mat.elements).get_height()+0.3)
        mat.brackets.set_width(VGroup(*mat.elements).get_width()+0.5)
        mat.brackets.move_to(VGroup(*mat.elements)).set_color(TEAL)
        self.play(FadeTransform(verts,mat.brackets),run_time=0.5,rate_func=linear)
        self.play(mat.animate.to_corner(UL,buff=0.2),run_time=1)
        mat.fix_in_frame()


        # ax
        ax=ThreeDAxesCustom(
            x_range = (-4.0, 4.0, 1.0),
            y_range = (-4.0, 4.0, 1.0),
            z_range = (-4.0, 4.0, 1.0),)
        ax.add_axis_labels()
        ax.apply_depth_test()
        nbp=NumberPlaneCustom( 
            x_range = (-4.0, 4.0, 1.0),
            y_range = (-4.0, 4.0, 1.0),)
        self.play(Write(ax),frame.animate.reorient(28, 44, 0, (-0.03, 0.43, 0.23), 9.17),
            Write(nbp))

        # pick a point
        arrow=Arrow(ax.c2p(0,0,0),ax.c2p(2,0,2),buff=0)
        arrow.set_opacity(0.5)
        glow=GlowDot(ax.c2p(2,0,2),radius=0.4)
        tt=TracingTail(glow)
        path=Arc(angle=TAU,radius=2)
        path.set_z(2)
        self.play(GrowArrow(arrow),ShowCreation(glow))
        arrow.add_updater(lambda m: m.put_start_and_end_on(ax.c2p(0,0,0),glow.get_center()))
        arrow.always.set_perpendicular_to_camera(frame)
        self.add(tt)
        def glow_updater(m,dt):
            # Clamp pfp to prevent it from exceeding the bounds
            m.pfp = min(m.pfp + dt * 1/2, 1)   # 1 cycle every 2 seconds
            # Reset pfp if close to 1
            if abs(1 - m.pfp) < 1e-15:
                m.pfp = 0
            # Update position along the path
            position = path.pfp(m.pfp)
            m.move_to(position)
        glow.pfp=0
        glow.add_updater(glow_updater)
        self.wait(2)
        self.play(frame.animate.reorient(0, 0, 0, (0,0,0), 9.69),run_time=3)
        self.play(frame.animate.reorient(29, 39, 0, (0.1, 0.13, 0.0), 9.69),run_time=3)

        # matrix change
        tex00=Tex('0')
        tex01=Tex(R'-1')
        tex10=Tex('1')
        tex11=Tex('0')
        tex00.move_to(mat.get_row(0)[0])
        tex01.move_to(mat.get_row(0)[1])
        tex10.move_to(mat.get_row(1)[0])
        tex11.move_to(mat.get_row(1)[1])
        tex_change=VGroup(tex00,tex01,tex10,tex11)
        tex_change.set_color(YELLOW)
        tex_change.fix_in_frame()
        tex_90degree1=Tex(R"90^\circ")
        tex_90degree1.fix_in_frame()
        tex_90degree1.set_color(YELLOW)
        tex_90degree1.scale(0.9)
        tex_90degree1.move_to(mat.get_row(0)[0][R"\theta"].get_center()+RIGHT*0.1)
        tex_90degree2=tex_90degree1.copy().move_to(mat.get_row(0)[1][R"\theta"].get_center()+RIGHT*0.1)
        tex_90degree3=tex_90degree1.copy().move_to(mat.get_row(1)[0][R"\theta"].get_center()+RIGHT*0.1)
        tex_90degree4=tex_90degree1.copy().move_to(mat.get_row(1)[1][R"\theta"].get_center()+RIGHT*0.1)
        tex_90degrees=VGroup(tex_90degree1,tex_90degree2,tex_90degree3,tex_90degree4)
        self.play(LaggedStartMap(FlashAround,
            VGroup(mat.get_row(0)[0][R"\theta"],mat.get_row(0)[1][R"\theta"],
                mat.get_row(1)[0][R"\theta"],mat.get_row(1)[1][R"\theta"]),
            lag_ratio=0))
        self.play(
            ReplacementTransform(mat.get_row(0)[0][R"\theta"],tex_90degree1),
            ReplacementTransform(mat.get_row(0)[1][R"\theta"],tex_90degree2),
            ReplacementTransform(mat.get_row(1)[0][R"\theta"],tex_90degree3),
            ReplacementTransform(mat.get_row(1)[1][R"\theta"],tex_90degree4),)
        self.play(LaggedStart(
            Transform(VGroup(mat.get_row(0)[0],tex_90degree1),tex00),
            Transform(VGroup(mat.get_row(0)[1],tex_90degree2),tex01),
            Transform(VGroup(mat.get_row(1)[0],tex_90degree3),tex10),
            Transform(VGroup(mat.get_row(1)[1],tex_90degree4),tex11),lag_ratio=0.3),)

        # matrix change2
        mat2=Matrix([[0,-1,0],[1,0,0],[0,0,1]],v_buff=0.3,h_buff=0.3)
        mat2.brackets.set_color(TEAL)
        mat2.get_row(0)[:2].set_color(YELLOW)
        mat2.get_row(1)[:2].set_color(YELLOW)
        mat2.to_corner(UL)
        mat2.fix_in_frame()
        self.play(FadeTransform(mat,mat2),FadeOut(tex_90degree2),FadeOut(tt),
            frame.animate.to_default_state(),run_time=0.8)
        mat=mat2
        

        # mat.get_row(0)[1].become(tex01)
        # mat_elements=VGroup(*mat.elements)
        # self.play(mat_elements.animate.arrange_in_grid(3,3,buff=0.3).to_corner(UL),)
        # self.play(mat.brackets[0].animate.next_to(mat_elements,LEFT),
        #             mat.brackets[1].animate.next_to(mat_elements,RIGHT),

        #             FadeOut(tt),
        #             frame.animate.to_default_state(),run_time=0.8)

        # 90 degrees
        glow.suspend_updating()
        glow_coord=np.round(glow.get_center(),2).reshape(3,1)
        glow_mat=Matrix(glow_coord)
        mat_arr=np.array([[0,-1,0],[1,0,0],[0,0,1]])
        result_mat_arr=np.dot(mat_arr,glow_coord)
        result_mat=Matrix(result_mat_arr)
        equal_sign=Tex(R'=')
        right_grp=VGroup(glow_mat,equal_sign,result_mat).arrange(RIGHT)
        right_grp.set_height(mat.get_height())
        right_grp.next_to(mat,RIGHT)
        right_grp.fix_in_frame()
        result_glow=GlowDot(ax.c2p(*result_mat_arr.reshape(1,3)[0]),radius=0.4)
        # result_glow.set_opacity(0.5)
        # elbow.set_points_as_corners(arrow.pfp(0.3),arrow_result_glow.pfp(0.3))
        self.wait()
        self.play(FadeTransform(glow.copy(),glow_mat))
        self.wait()
        self.play(LaggedStartMap(Write,VGroup(equal_sign,result_mat),lag_ratio=0.3 ))
        self.wait()
        self.play(FadeOutToPoint(result_mat.unfix_from_frame(),ax.c2p(*result_mat_arr.reshape(1,3)[0])),
                FadeOut(glow_mat,shift=UP),FadeIn(result_glow),
                FadeOut(equal_sign,shift=UP))

        # say 90 degrees
        arrow_result_glow=Arrow(ax.c2p(0,0,0),ax.c2p(*result_mat_arr.reshape(1,3)[0]),buff=0).set_opacity(0.5)
        arrow_result_glow.always.set_perpendicular_to_camera(frame)
        arrow_result_glow.clear_updaters()
        dashedline1=DashedLine(ax.c2p(0,0,2),ax.c2p(*arrow.get_end()))
        dashedline2=DashedLine(ax.c2p(0,0,2),ax.c2p(*arrow_result_glow.get_end()))
        albow=VMobject()
        line1=Line(ax.c2p(0,0,2),ax.c2p(*arrow.get_end()))
        line2=Line(ax.c2p(0,0,2),ax.c2p(*arrow_result_glow.get_end()))
        point_start=line1.pfp(0.2)
        point_start[2]=0
        point_end=line2.pfp(0.2)
        point_end[2]=0
        point_middle=point_start+point_end
        albow.set_points_as_corners([point_start,point_middle,point_end] )
        albow.set_z(2)
        tex90=Tex(R"90^\circ")
        tex90.rotate(PI/4,axis=RIGHT)
        tex90.next_to(albow,RIGHT)
        # self.add(dashedline1,dashedline2)
        # self.add(albow)
        self.play(GrowArrow(arrow_result_glow))
        self.play(Write(albow))
        self.wait()
        self.play(Write(dashedline1),Write(dashedline2),
            frame.animate.reorient(-13, 28, 0),Write(tex90))
        self.play(LaggedStartMap(FadeOut,Group(dashedline1,dashedline2,albow,tex90,
            result_glow,arrow,arrow_result_glow)))
        self.wait()

        # add cloud
        sp=Sphere(radius=2,resolution=(20,20))
        points=sp.get_points()
        cloud=DotCloud(points)
        mesh=SurfaceMesh(sp,resolution=(20,20))
        im=ImageMobject('kun.jpg')
        surface_base=Sphere(radius=2,resolution=(101,101))
        basketball=TexturedSurface(surface_base,'basketball.jpg')
        mesh[10:20].reverse_points()

        # group
        n_groups = 20
        group_size = len(cloud.data) // n_groups
        groups = [cloud.data[i * group_size:(i + 1) * group_size] for i in range(n_groups)]
        cloud_grp1=Group()
        cloud_grp2=Group()
        for i in range(10):
            cloud1 = cloud.copy()
            cloud2 = cloud.copy()
            cloud1.data=np.concatenate([groups[i]],axis=0)
            cloud2.data=np.concatenate([groups[10+i][::-1]],axis=0)
            cloud1.note_changed_data()
            cloud2.note_changed_data()
            cloud_grp1.add(cloud1)
            cloud_grp2.add(cloud2)
    
        whole_time=3
        run_time=whole_time/20
        frame.add_ambient_rotation(angular_speed=-1 * DEG)
        for i in range(10):
            self.play(MoveAlongPath(glow,mesh[i]),
                ShowCreation(cloud_grp1[i]),rate_func=linear,run_time=run_time)
            self.play(MoveAlongPath(glow,mesh[10+i]),
                ShowCreation(cloud_grp2[i]),rate_func=linear,run_time=run_time)

        # mesh
        self.play(ShowCreation(mesh),run_time=3)
        self.play(ShowCreation(basketball),Uncreate(mesh),
            *map(FadeOut,cloud_grp1),FadeOut(glow),Uncreate(nbp),*map(FadeOut,cloud_grp2),
            frame.animate.reorient(-42, 41, 0, (0.45, 0.24, 0.42), 8.00),run_time=3)
        frame.clear_updaters()

        # apply matrix to basketball
        def attach_to_ball(point):
            r=2
            x=point[0]
            y=point[1]
            z=point[2]
            a=np.sqrt((x**2+y**2+z**2)/(r**2))
            return np.array([x/a,y/a,z/a])
        def get_ball_coord(x,y):
            r=2
            z=r**2-x**2-y**2
            return np.sqrt(z)
        def get_perpendicular_vector_to_frame(frame):
            rotmat=frame.get_inv_view_matrix()[:3,:3]
            return np.dot(rotmat,OUT)
        mat_attached_grp=VGroup()
        hint_arrow=CurvedArrow(ax.c2p(0,-2,2),ax.c2p(2,0,2),angle=PI/2)
        hint_arrow.set_color(YELLOW)
        hint_arrow.apply_depth_test()
        line1=ax.get_line_from_axis_to_point(2,hint_arrow.get_end())
        line2=ax.get_line_from_axis_to_point(2,hint_arrow.get_start())
        elbow=Elbow(width=0.5)
        elbow.rotate(-PI/2,about_point=ORIGIN).shift(OUT*2)
        for i in range(4):
            mat_attached=mat.deepcopy()
            mat_attached.scale(0.8)
            mat_attached.unfix_from_frame()
            vector=np.array([-2,0,2])
            mat_attached.move_to(2*normalize(vector))
            mat_attached.rotate(-PI/2)
            mat_attached.rotate(angle_between_vectors(OUT,vector),axis=DOWN)
            mat_attached.apply_function(attach_to_ball)
            self.play(TransformFromCopy(mat,mat_attached),run_time=1)
            if i==0:
                self.play(ShowCreation(hint_arrow),ShowCreation(line1),
                    ShowCreation(line2),ShowCreation(elbow),run_time=1)
            mat_attached_grp.add(mat_attached)
            self.play(basketball.animate.set_anim_args(path_arc=PI/2)\
                .apply_matrix(mat_arr),
                mat_attached_grp.animate.set_anim_args(path_arc=PI/2)\
                .apply_matrix(mat_arr),)
            self.play(mat_attached_grp[i].animate.set_opacity(0.5),run_time=0.5)
            
        
        # fadeout
        self.play(FadeOut(mat,shift=LEFT),
            LaggedStartMap(FadeOut,
            Group(hint_arrow,line1,line2,ax,elbow,mat_attached_grp,basketball),shift=RIGHT,
            lag_ratio=0.02),)

class video5(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        mat=np.array([[1,0],[0,1],[0,0]])
        proj_mat=mat@np.linalg.inv(mat.T@mat)@mat.T

        # title--projection
        frame.reorient(0, 55, 0, (-0.14, -0.2, 0.08), 8.00)
        title=TextCustom(en='Projection',ch='投影')
        nbp=NumberPlaneCustom(x_range=(-3,3,1),y_range=(-4,4,1))
        nbp.axes.set_opacity(0.5)
        title.scale(1.5)
        title.set_color(TEAL_A)
        title.set_z(3)
        tt1_en=TracingTail(title.en[0],stroke_color=TEAL)
        tt2_en=TracingTail(title.en[-1],stroke_color=TEAL)
        tt1_ch=TracingTail(title.ch[0],stroke_color=TEAL)
        tt2_ch=TracingTail(title.ch[-1],stroke_color=TEAL)
        title.fix_in_frame()
        self.play(FadeIn(title.en,shift=RIGHT),FadeIn(title.ch,shift=LEFT))
        self.play(Write(nbp),title.animate.unfix_from_frame())
        self.add(tt1_en,tt2_en,tt1_ch,tt2_ch)
        self.play(title.animate.center())
        self.wait()
        self.remove(tt1_en,tt2_en,tt1_ch,tt2_ch)
        self.play(FadeOut(nbp),frame.animate.to_default_state())

        # projection matrix
        title2=TextCustom(en="Projection Matrix",ch="投影矩阵")
        title2.en["Projection"].set_color(TEAL_A)
        title2.ch["投影"].set_color(TEAL_A)
        title2.scale(1.5)
        self.play(FadeTransform(title.en,title2.en["Projection"]),
            FadeTransform(title.ch,title2.ch["投影"]),
            Write(title2.en["Matrix"]),Write(title2.ch["矩阵"]))
        self.wait()

        # P^2=P
        tex=Tex(R"P^2=P",t2c={"^2":TEAL_A})
        tex.scale(3)
        self.play(FadeOut(title2,shift=LEFT*2),FadeIn(tex,shift=LEFT*2))
        self.wait()
        self.play(tex.animate.scale(0.6).to_corner(UL))
        self.wait()

        # for example
        title=TextCustom(en='For Example',ch='举个栗子')
        title.scale(1.5)
        self.play(FadeIn(title.en,shift=LEFT*2),FadeIn(title.ch,shift=LEFT*2))
        self.wait()
        self.play(FadeOut(title.en,shift=LEFT*2),FadeOut(title.ch,shift=LEFT*2))
        self.wait()

        # functions  
        def get_steps(mat1:Matrix,mat2:Matrix):
            mat1_arr=mat1.arr
            mat2_arr=mat2.arr
            result_arr=mat1_arr@mat2_arr
            plus_sign=Tex(R"+")
            equal_sign=Tex(R"=")
            num_of_cols=mat1_arr.shape[1]
            num_of_rows=mat1_arr.shape[0]
            num_of_steps=mat2_arr.shape[1]
            steps=VGroup()
            for i in range(num_of_steps):
                eqn_grp=VGroup()
                for j in range(num_of_cols):
                    eqn_grp.add(mat2.get_column(i)[j].deepcopy())
                    m=Matrix( mat1_arr[:,j].reshape(num_of_rows,1) )
                    eqn_grp.add(m)
                    if j != num_of_cols-1: 
                        eqn_grp.add(plus_sign.deepcopy())
                    else:
                        eqn_grp.add(equal_sign.deepcopy())
                        m=Matrix(result_arr[:,i].reshape(num_of_cols,1))
                        eqn_grp.add(m)
                eqn_grp.arrange(RIGHT)
                eqn_grp.scale(0.5)
                eqn_grp.next_to(VGroup(mat1,mat2),UP)
                steps.add(eqn_grp)
            return steps

        def set_steps_color(steps,colors,opacity=0.5):
            for step in steps:
                step[0].set_color(colors[0])
                rec=Rectangle(width=step[1].get_width(),height=step[1].get_height(),
                    fill_color=colors[0],fill_opacity=opacity,stroke_width=0)
                rec.move_to(step[1])
                step[1].add_to_back(rec)
                step[3].set_color(colors[1])
                rec=Rectangle(width=step[4].get_width(),height=step[4].get_height(),
                    fill_color=colors[1],fill_opacity=opacity,stroke_width=0)
                rec.move_to(step[4])
                step[4].add_to_back(rec)
                step[6].set_color(colors[2])
                rec=Rectangle(width=step[7].get_width(),height=step[7].get_height(),
                    fill_color=colors[2],fill_opacity=opacity,stroke_width=0)
                rec.move_to(step[7])
                step[7].add_to_back(rec)


        # matrix col multiply
        colors=[YELLOW_B,PURPLE_B,BLUE_B]
        mat1=Matrix(np.array([[1,0,0],[0,1,0],[0,0,0]]))
        mat1.arr=np.array([[1,0,0],[0,1,0],[0,0,0]])
        mat2=mat1.deepcopy()
        mat_result=mat1.deepcopy()
        equal_sign=Tex(R"=")
        mat_grp=VGroup(mat1,mat2,equal_sign,mat_result)
        mat_grp.arrange(RIGHT)
        opacity=0.5
        rec1=Rectangle(width=mat1.get_width()/3,
                       height=mat1.get_height(),fill_color=colors[0],fill_opacity=opacity,
                       stroke_width=0)
        rec2=Rectangle(width=mat1.get_width()/3,
                       height=mat1.get_height(),fill_color=colors[1],fill_opacity=opacity,
                       stroke_width=0)
        rec3=Rectangle(width=mat1.get_width()/3,
                       height=mat1.get_height(),fill_color=colors[2],fill_opacity=opacity,
                       stroke_width=0)
        mat1_recs=VGroup(rec1,rec2,rec3).arrange(RIGHT,buff=0)

        mat1_recs.move_to(mat1)
        tex_p1=Tex(R'P')
        tex_p2=Tex(R'P')
        tex_p1.scale(1.5)
        tex_p2.scale(1.5)
        tex_p1.next_to(mat1,UP)
        tex_p2.next_to(mat2,UP)
        mat1.save_state()
        tex_p1.save_state()
        mat1.center()
        self.play(Write(mat1))
        tex_p1.next_to(mat1,UP)
        self.play(Write(tex_p1),run_time=0.5)
        self.play(mat1.animate.restore(),tex_p1.animate.restore())
        self.play(TransformFromCopy(VGroup(tex_p1,mat1),VGroup(tex_p2,mat2)))
        self.play(Write(equal_sign),run_time=0.5)
        tex_pd=Tex(R"P^2",t2c={"^2":TEAL_A})
        tex_pd.scale(1.5)
        tex_pd.next_to(VGroup(mat1,mat2),DOWN,buff=0.5)
        self.play( LaggedStart(ReplacementTransform(tex_p1,tex_pd[0]),
                   ReplacementTransform(tex_p2,tex_pd[1]),lag_ratio=0.2 ) )
        self.play( LaggedStartMap(FadeIn,mat1_recs,shift=DOWN,lag_ratio=0.2),run_time=1)

        # anims
        steps=get_steps(mat1,mat2)
        set_steps_color(steps,colors,opacity=opacity)
        step=0
        self.play(LaggedStart(
            TransformMatchingParts(
                VGroup(mat1.get_column(0),mat1.brackets).copy(),steps[step][1]),
            TransformMatchingParts(
                VGroup(mat1.get_column(1),mat1.brackets).copy(),steps[step][4]),
            TransformMatchingParts(
                VGroup(mat1.get_column(2),mat1.brackets).copy(),steps[step][7]),
            lag_ratio=0.5),
            VGroup(mat1,mat1_recs).animate.fade(0.2), run_time=1.5)
        self.play( LaggedStart(
            TransformFromCopy(mat2.get_column(step)[0],steps[step][0]),
            TransformFromCopy(mat2.get_column(step)[1],steps[step][3]),
            TransformFromCopy(mat2.get_column(step)[2],steps[step][6]),
            lag_ratio=0.2),
            mat2.get_column(step)[0].animate.fade(0.5),
            mat2.get_column(step)[1].animate.fade(0.5),
            mat2.get_column(step)[2].animate.fade(0.5),
            run_time=1.5 )
        self.play(LaggedStart(
            AnimationGroup(*map(Write,VGroup(steps[step][2],steps[step][5],steps[step][8]))),
            Write(steps[step][9])),run_time=1)
        self.play(ReplacementTransform(steps[step][9].get_column(0),mat_result.get_column(step)),
            Write(mat_result.brackets[0]),FadeOut(steps[step][-1].brackets),
            LaggedStartMap(FadeOut,steps[step][:-1],shift=RIGHT),run_time=1.5)
        step=1
        self.play(LaggedStart(
            TransformMatchingParts(
                VGroup(mat1.get_column(0),mat1.brackets).copy(),steps[step][1]),
            TransformMatchingParts(
                VGroup(mat1.get_column(1),mat1.brackets).copy(),steps[step][4]),
            TransformMatchingParts(
                VGroup(mat1.get_column(2),mat1.brackets).copy(),steps[step][7]),
            lag_ratio=0.5),
            VGroup(mat1,mat1_recs).animate.fade(0.2), run_time=1.5)
        self.play( LaggedStart(
            TransformFromCopy(mat2.get_column(step)[0],steps[step][0]),
            TransformFromCopy(mat2.get_column(step)[1],steps[step][3]),
            TransformFromCopy(mat2.get_column(step)[2],steps[step][6]),
            lag_ratio=0.2),
            mat2.get_column(step)[0].animate.fade(0.5),
            mat2.get_column(step)[1].animate.fade(0.5),
            mat2.get_column(step)[2].animate.fade(0.5),
            run_time=1.5 )
        self.play(LaggedStart(
            AnimationGroup(*map(Write,VGroup(steps[step][2],steps[step][5],steps[step][8]))),
            Write(steps[step][9])),run_time=1)
        self.play(ReplacementTransform(steps[step][9].get_column(0),mat_result.get_column(step)),
            FadeOut(steps[step][-1].brackets),
            LaggedStartMap(FadeOut,steps[step][:-1],shift=RIGHT),run_time=1.5)
        step=2
        self.play(LaggedStart(
            TransformMatchingParts(
                VGroup(mat1.get_column(0),mat1.brackets).copy(),steps[step][1]),
            TransformMatchingParts(
                VGroup(mat1.get_column(1),mat1.brackets).copy(),steps[step][4]),
            TransformMatchingParts(
                VGroup(mat1.get_column(2),mat1.brackets).copy(),steps[step][7]),
            lag_ratio=0.5),
            VGroup(mat1,mat1_recs).animate.fade(0.2), run_time=1.5)
        self.play( LaggedStart(
            TransformFromCopy(mat2.get_column(step)[0],steps[step][0]),
            TransformFromCopy(mat2.get_column(step)[1],steps[step][3]),
            TransformFromCopy(mat2.get_column(step)[2],steps[step][6]),
            lag_ratio=0.2),
            mat2.get_column(step)[0].animate.fade(0.5),
            mat2.get_column(step)[1].animate.fade(0.5),
            mat2.get_column(step)[2].animate.fade(0.5),
            run_time=1.5 )
        self.play(LaggedStart(
            AnimationGroup(*map(Write,VGroup(steps[step][2],steps[step][5],steps[step][8]))),
            Write(steps[step][9])),run_time=1)
        self.play(ReplacementTransform(steps[step][9].get_column(0),mat_result.get_column(step)),
            Write(mat_result.brackets[1]),FadeOut(steps[step][-1].brackets),
            LaggedStartMap(FadeOut,steps[step][:-1],shift=RIGHT),run_time=1.5)

        # fadeout matrix
        tex_p3=Tex(R"P")
        tex_p3.scale(1.5)
        tex_p3.next_to(mat_result,DOWN,buff=0.5)
        tex_p3.align_to(tex_pd,DOWN)
        equal_check=Tex(R"=")
        equal_check.next_to(tex_pd,RIGHT)
        check_mark=Tex(R"\checkmark").set_color(RED)
        check_mark.scale(1.5)
        check_mark.next_to(tex,RIGHT)
        self.play(Write(tex_p3),run_time=0.5)
        self.play(LaggedStartMap(FadeOut,VGroup(mat1_recs,mat2,mat_result,equal_sign),shift=RIGHT),
                mat1.animate.set_opacity(1),
                Write(equal_check),tex_p3.animate.next_to(equal_check,RIGHT).align_to(tex_pd,DOWN))
        self.play(ReplacementTransform(VGroup(tex_pd,equal_check,tex_p3),check_mark))
        self.play(LaggedStartMap(FadeOut,VGroup(tex,check_mark),shift=UP),
                mat1.animate.center())

        # muti [x,y,z]
        mat_xyz=Matrix([[Tex(R"x")],[Tex(R"y")],[Tex(R"z")]])
        mat_xyz.next_to(mat1,RIGHT)
        mat_result=Matrix([[Tex(R"x")],[Tex(R"y")],[Tex(R"0")]])
        equal=Tex(R"=")
        equal.next_to(mat_xyz,RIGHT)
        mat_result.next_to(equal,RIGHT)
        self.play(LaggedStartMap(Write,VGroup(mat_xyz,equal),lag_ratio=0.2),run_time=1)
        self.play(VGroup(mat1,mat_xyz,equal).animate.arrange(RIGHT).center(),run_time=1)
        mat_result.next_to(equal,RIGHT)
        steps=VGroup(Tex(R"x"),Matrix([[1],[0],[0]]),Tex(R"+"),Tex(R"y"),
            Matrix([[0],[1],[0]]),Tex(R"+"),Tex(R"z"),Matrix([[0],[0],[0]]),Tex(R"="),
            Matrix([[Tex(R"x")],[Tex(R"y")],[Tex(R"0")]]) )
        steps.arrange(RIGHT)
        steps.scale(0.5)
        steps.next_to(VGroup(mat1,mat_xyz),UP)
        steps=VGroup(steps)

        step=0
        self.play(LaggedStart(
            TransformMatchingParts(
                VGroup(mat1.get_column(0),mat1.brackets).copy(),steps[step][1]),
            TransformMatchingParts(
                VGroup(mat1.get_column(1),mat1.brackets).copy(),steps[step][4]),
            TransformMatchingParts(
                VGroup(mat1.get_column(2),mat1.brackets).copy(),steps[step][7]),
            lag_ratio=0.5),run_time=1)
        self.play( LaggedStart(
            TransformFromCopy(mat_xyz.get_column(step)[0],steps[step][0]),
            TransformFromCopy(mat_xyz.get_column(step)[1],steps[step][3]),
            TransformFromCopy(mat_xyz.get_column(step)[2],steps[step][6]),
            lag_ratio=0.2), run_time=1 )
        self.play(LaggedStart(
            AnimationGroup(*map(Write,VGroup(steps[step][2],steps[step][5],steps[step][8]))),
            Write(steps[step][9])),run_time=1)
        self.play(ReplacementTransform(steps[step][9].get_column(0),mat_result.get_column(step)),
            Write(mat_result.brackets),FadeOut(steps[step][-1].brackets),
            LaggedStartMap(FadeOut,steps[step][:-1],shift=RIGHT),run_time=1)
        self.play(VGroup(mat1,mat_xyz,equal,mat_result).animate.center(),run_time=0.5)

        # indicate x,y
        self.play(TransformFromCopy2(VGroup(mat_xyz.elements[:2]),VGroup(mat_result.elements[:2])))
        self.play(TransformFromCopy2(VGroup(mat_result.elements[:2]),VGroup(mat_xyz.elements[:2])))
        self.play(LaggedStartMap(FlashAround,VGroup(mat_xyz.elements[2],mat_result.elements[2])))
        self.play(LaggedStartMap(FadeOut,VGroup(mat_xyz,equal,mat_result),shift=RIGHT),
                mat1.animate.to_corner(UL))
        
        # solar system init
        self.remove(mat1)
        ax=ThreeDAxes((-200,200),(-200,200),(-200,200))
        sun=Sphere(radius=109)
        mercury=Sphere(radius=0.38,resolution=(51,101))
        venus=Sphere(radius=0.94,resolution=(70,25))
        earth=Sphere(radius=1,resolution=(101,101))
        moon=Sphere(radius=0.27,resolution=(101,51))           # radius of earth = 1
        mars=Sphere(radius=0.53,resolution=(51,101))
        jupiter=Sphere(radius=11,resolution=(51,101))
        saturn=Sphere(radius=9,resolution=(51,101))
        uranus=Sphere(radius=4,resolution=(51,101))
        neptune=Sphere(radius=3.8,resolution=(51,101))

        factor=23454     # 1 AU = 23454 * radius of earth
        correction_vector=np.array([factor,0,0])
        sun.move_to(np.array([0,0,0])-correction_vector)
        mercury.move_to(np.array([factor*0.38,0,0])-correction_vector)
        venus.move_to(np.array([factor*0.72,0,0])-correction_vector)
        earth.move_to(np.array([factor*1,0,0])-correction_vector)
        moon.move_to(np.array([factor*1.00257,0,0])-correction_vector)
        mars.move_to(np.array([factor*1.52,0,0])-correction_vector)
        jupiter.move_to(np.array([factor*5.20,0,0])-correction_vector)
        saturn.move_to(np.array([factor*9.58,0,0])-correction_vector)
        uranus.move_to(np.array([factor*19.14,0,0])-correction_vector)
        neptune.move_to(np.array([factor*30.2,0,0])-correction_vector)

        # universe background
        universe=Sphere(radius=factor*100)
        t_universe=TexturedSurface(universe,"milkyway.jpg").set_shading(0.3,0.1,0.6)

        # textured planet
        t_sun=TexturedSurface(sun,"sun.jpg")
        t_mercury=TexturedSurface(mercury,"mercury.jpg")
        t_venus=TexturedSurface(venus,"venus.jpg")
        t_earth=TexturedSurface(earth,"day.jpg","night.jpg")
        t_moon=TexturedSurface(moon,"moon.jpg")
        t_mars=TexturedSurface(mars,"mars.jpg")
        t_jupiter=TexturedSurface(jupiter,"jupiter.jpg")
        t_saturn=TexturedSurface(saturn,"saturn.jpg")
        t_uranus=TexturedSurface(uranus,"uranus.jpg")
        t_neptune=TexturedSurface(neptune,"neptune.jpg")

        # light
        light=self.camera.light_source
        light.move_to(sun.get_center())

        # set shading
        t_sun.set_shading(0.3,0.2,0.1)
        t_earth.set_shading(0.2,0.3,0)
        t_venus.set_shading(0.1,0.1,0.2)
        t_mercury.set_shading(0.05,0.2,0.2)
        t_mars.set_shading(0.05,0.1,0.2)
        t_jupiter.set_shading(0.05,0.1,0.1)
        t_saturn.set_shading(0,0.4,0.2)
        t_uranus.set_shading(0,0.1,0.1)
        t_neptune.set_shading(0,0.1,0.1)

        # mesh
        earth_mesh=SurfaceMesh(earth)

        # self.add(t_universe,sun,mercury,venus,earth,mars,jupiter,saturn,uranus,neptune)

        # self.add(t_universe,t_sun,t_mercury,t_venus,t_earth,t_moon,
        #     t_mars,t_jupiter,t_saturn,t_uranus,t_neptune)
        # frame.reorient(-4, 66, 0, sun.get_center(), 503.37)
        # frame.reorient(-4, 66, 0, mercury.get_center(), 3)
        # frame.reorient(-4, 66, 0, venus.get_center(), 3)
        # frame.reorient(-4, 66, 0, earth.get_center(), 3)
        # frame.reorient(83, 78, 0, moon.get_center()+np.array([0,moon.radius,0]), 0.1)  # moon
        # frame.reorient(-4, 66, 0, mars.get_center(), 3)
        # frame.reorient(-4, 66, 0, jupiter.get_center(), 33)
        # frame.reorient(-4, 66, 0, saturn.get_center(), 25)
        # frame.reorient(-4, 66, 0 ,uranus.get_center(), 10)
        # frame.reorient(-4, 66, 0, neptune.get_center(), 10)

        # from Earth back to Sun
        # frame.reorient(4, 73, 0, earth.get_center(),3.00)
        # self.play(frame.animate.reorient(68, 82, 0, (-0.59, -1.29, 0.47), 0.16),run_time=3)
        # self.play(frame.animate.reorient(68, 82, 0, venus.get_center(), 3),run_time=3,rate_func=smooth)
        # self.play(frame.animate.reorient(68, 82, 0, mercury.get_center(), 3), run_time=5,rate_func=smooth)
        # self.play(frame.animate.reorient(68, 82, 0, sun.get_center(), 3),run_time=5,rate_func=smooth)
        # self.play(frame.animate.reorient(68, 82, 0, saturn.get_center(), 30))
        # self.play(frame.animate.reorient(68, 82, 0, jupiter.get_center(), 30))
        # self.play(frame.animate.reorient(68, 82, 0, earth.get_center(), 3))
        # self.play(frame.animate.reorient(68, 82, 0, moon.get_center(), 3))

        # init_for_last_video
        mat1=Matrix([[1,0,0],[0,1,0],[0,0,0]])
        mat1.to_corner(UL)
        mat1.fix_in_frame()
        self.add(t_universe,t_sun)
        self.add(mat1)

        # init
        t_moon.clear_updaters()
        t_earth.clear_updaters()
        text_moon=TextCustom(en="Moon",ch="月球")
        text_moon.scale(0.5)
        text_moon.rotate(PI/2,axis=RIGHT)
        text_moon.always.next_to(t_moon,OUT)
        text_moon.rotate(PI/2,axis=OUT)

        # updater
        T=30 # seconds
        w_earth=TAU/T
        w_moon=w_earth*1/27
        t_earth.clear_updaters()
        t_earth.add_updater(lambda m,dt:m.rotate(w_earth*dt,axis=OUT))
        t_moon.add_updater(lambda m,dt:m.rotate(w_moon*dt,axis=OUT))
        t_moon.add_updater(lambda m,dt:m.rotate(w_moon*dt,axis=OUT,about_point=ORIGIN))
        t_moon.suspend_updating()
        self.play(frame.animate.reorient(68, 82, 0, (60.29, 0.1, 0.17), 3.74),
            *map(FadeIn,Group(t_moon,t_earth,t_earth)))
        text_moon.suspend_updating()
        self.play(Write(text_moon))
        text_moon.resume_updating()
        t_moon.resume_updating()
        self.wait(2)

        # orthogonal projection matrix
        ax=ThreeDAxesCustom(x_range=(-3,3,1),y_range=(-3,3,1),z_range=(-2,2,1))
        ax.move_to(t_earth)
        ax.apply_depth_test()
        ax.add_axis_labels()
        ax.remove(ax.axis_labels[-1])
        ax.axis_labels.set_opacity(1)
        ax.set_opacity(0.5)
        nbp=NumberPlaneCustom(x_range=(-10,10,1),y_range=(-5,5,1))
        nbp.faded_lines.set_opacity(0.2)
        nbp.background_lines.set_opacity(0.2)
        nbp.axes.set_opacity(0)
        nbp.remove(nbp.get_axes())
        nbp.apply_depth_test()
        text_earth=TextCustom(en="Earth",ch="地球")
        text_earth.rotate(PI/2,axis=RIGHT)
        text_earth.rotate(PI/2,axis=OUT)
        text_earth.next_to(t_earth,OUT,buff=1)
        self.play(frame.animate.reorient(59, 89, 0, (0.02, 0.01, 0.75), 5.34),run_time=4)
        self.play(Write(text_earth),Write(nbp),Write(ax))
        self.wait()

        # proj
        sf1=Surface(u_range=(0,mat1.get_width()),v_range=(0,mat1.get_height()))
        sf1.set_opacity(0.5)
        sf1.fix_in_frame()
        sf1.to_corner(UL)
        sf2=Surface(u_range=(-0.5,0.5),v_range=(-0.5,0.5))
        sf2.set_opacity(0.5)
        sf2.set_z(1)
        proj_mat=np.array([[1,0,0],[0,1,0],[0,0,0.0001]])
        mat2=mat1.copy()
        mat2.unfix_from_frame()
        mat2.set_width(1)
        mat2.move_to(sf2)
        self.play(ShowCreation(sf1))
        self.play(TransformFromCopy(mat1,mat2),TransformFromCopy(sf1,sf2),
            frame.animate.reorient(41, 73, 0, (0.05, 0.28, 0.39), 4.06),run_time=2)
        self.wait()
        self.play(t_earth.animate.apply_matrix(proj_mat),
            sf2.animate.shift(IN*0.99),mat2.animate.shift(IN*0.99),run_time=2)
        self.wait()
        self.play(frame.animate.reorient(60, 89, 0, (0.29, 0.49, 0.89), 5.34),
            ReplacementTransform(mat2,mat1),ReplacementTransform(sf2,sf1))
        self.wait(2)
        self.play(LaggedStartMap(FadeOut,Group(ax,nbp,t_earth,t_universe,t_sun)),
            LaggedStartMap(FadeOut,Group(sf1,mat1,text_earth),shift=LEFT))
        self.wait()
class end(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame

        # start
        thanks_title_en=Text("Credits:")
        thanks_title_ch=Text("致谢:",font='WenCang')
        thanks_en=Text("""
         This animation was created using Manim,
         a mathematical animation software 
         originally developed by Grant Sanderson,
         also known as 3Blue1Brown.
            """,t2c={'3Blue':BLUE,'1Brown':LIGHT_BROWN,'Grant Sanderson':TEAL_A})
        thanks_ch=Text("""
          本动画使用 Manim 制作
          这是一个由 Grant Sanderson\n（即 3Blue1Brown)
          最初开发的数学动画软件""",font='WenCang',t2c={'3Blue':BLUE,'1Brown':LIGHT_BROWN,'Grant Sanderson':TEAL_A})
        thanks_en.next_to(thanks_title_en,DOWN,aligned_edge=LEFT)
        thanks_ch.next_to(thanks_title_ch,DOWN,aligned_edge=LEFT)
        grp_en=VGroup(thanks_title_en,thanks_en)
        grp_ch=VGroup(thanks_title_ch,thanks_ch)
        grp_thanks=VGroup(grp_en,grp_ch).arrange(LEFT,buff=1,aligned_edge=UP)
        grp_thanks.set_width(FRAME_WIDTH-1)
        grp_thanks.to_edge(UP,buff=0.5)
        thanks_title_battery=Text(R"感谢充电：",font='WenCang')
        name3=Text(R"哈嘿哟哟",font='WenCang').set_color(BLUE_A)
        name2=Text(R"xiankoe").set_color(TEAL_A)
        name1=Text(R"_blue_dolphin").set_color(YELLOW_A)
        names=VGroup(name1,name2,name3).arrange(RIGHT,buff=1.5)
        grp_battery=VGroup(thanks_title_battery,names).arrange(DOWN,aligned_edge=LEFT)
        grp_battery.scale(0.6)
        grp_battery.next_to(grp_ch,DOWN,aligned_edge=LEFT,buff=1)
        self.play(LaggedStartMap(Write,grp_ch),LaggedStartMap(Write,grp_en),
            LaggedStartMap(Write,grp_battery),run_time=5)
        self.play(LaggedStartMap(Flash,VGroup(thanks_en['Grant Sanderson'],
            thanks_ch['Grant Sanderson'],name1,name2,name3)))
        
        # svgs
        svg1=SVGMobject('subscribe.svg')
        svg2=SVGMobject('thumbs.svg')
        svg3=SVGMobject('coin.svg')
        svg4=SVGMobject('star.svg')
        text_subscribe=Text('关注',font='WenCang')
        svg1.add(text_subscribe)
        text_subscribe.shift(RIGHT*0.5)
        grp_svg=VGroup(svg1,svg2,svg3,svg4)
        grp_svg.arrange(RIGHT,buff=1)
        grp_svg.set_style(stroke_width=3,stroke_color=YELLOW,
            stroke_opacity=1,fill_opacity=0.8,fill_color=BLUE)
        svg2.set_stroke(width=0)
        svg4.set_stroke(width=0)
        svg1.set_stroke(width=3)
        svg3.set_stroke(width=3)
        grp_svg.scale(0.5)
        grp_svg.next_to(grp_battery,DOWN,buff=1,aligned_edge=LEFT)
        grp_svg.save_state()
        self.play(LaggedStartMap(DrawBorderThenFill,grp_svg))
        self.wait()
        self.play(LaggedStartMap(FadeOut,self.mobjects))

        pass
class MatrixDet(Matrix):
    def create_brackets(self, rows, v_buff: float, h_buff: float) -> VGroup:
        brackets = Tex("".join((
            R"\left|\begin{array}{c}",
            *len(rows) * [R"\quad \\"],
            R"\end{array}\right|",
        )))
        brackets.set_height(rows.get_height() + v_buff)
        l_bracket = brackets[:len(brackets) // 2]
        r_bracket = brackets[len(brackets) // 2:]
        l_bracket.next_to(rows, LEFT, h_buff)
        r_bracket.next_to(rows, RIGHT, h_buff)
        return VGroup(l_bracket, r_bracket)
        
from manim_imports_custom import *
from fractions import Fraction
from _2025.gauss.kun_character import Kun,YellowChicken 
from _2025.gauss.elimination import * 
class test_sound(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        rec=Rectangle()
        self.play(ShowCreation(rec))
        self.wait()
        self.add_sound("whoosh",gain=1)
        rec.shift(DOWN)
        self.wait()
        self.add_sound("whoosh")
        rec.shift(DOWN)
        self.wait()

class opening(Elimination):
    def construct(self):
        # init
        frame=self.frame
        # start
        text=Textch("高斯消元")
        texts=VGroup(
            Textch("Part1:什么是高斯消元",t2f={"Part1:":"Mongolian Baiti"}),
            Textch("Part2:高斯消元的步骤",t2f={"Part2:":"Mongolian Baiti"}),
            Textch("Part3:高斯消元的矩阵形式",t2f={"Part3:":"Mongolian Baiti"}),
            ).arrange(DOWN,aligned_edge=LEFT,buff=1).scale(1.1)
        for t in texts:
            t.set_stroke(WHITE,0,0)
        rec=FullScreenRectangle(fill_opacity=0)
        rec.set_stroke(WHITE,3,1)
        rec2=ScreenRectangle().scale(0.9)
        arrow=ArrowCustom(length=1.8).point_from(rec2.get_top(),PI/2)
        arrow.put_to_end(text,buff=0.4)
        line=Line(frame.get_top(),frame.get_bottom())
        texts.next_to(line,RIGHT,buff=0.5)
        VGroup(rec2,arrow,text).next_to(line,LEFT,buff=0.2)
        frame.reorient(0, 0, 0, (-0.13, -0.07, 0.0), 7.78)
        self.wait(2)
        self.play(ShowCreation(rec2))
        self.play(GrowArrow(arrow),FadeIn(text,shift=UP))
        self.wait()
        # show gauss profile
        gauss=SVGMobject("ga7").scale(2.4)
        gauss.next_to(rec2,RIGHT,buff=2)
        name=Texten("Carl Friedrich Gauß").next_to(gauss,UP,aligned_edge=UP)
        arrow2=ArrowCustom(length=1).point_from(gauss.get_top(),PI/2,length=0.8)
        arrow2.put_to_end(name,buff=0.4)
        gauss_copy=gauss.copy()
        self.play(
            Write(gauss_copy.sort(lambda p:abs(p[0]-gauss_copy.get_center()[0]))),
            GrowArrow(arrow2,time_span=[0,1]),
            Write(name,time_span=[0,1]),
            FlashAround(text["高斯"],time_span=[2,5]),
            FlashAround(name,time_span=[2,5]),
            run_time=7)
        self.wait(2)
        self.play(
            LaggedStartMap(FadeOut,Group(name,arrow2,gauss_copy),
                shift=RIGHT,lag_ratio=0.2),
            LaggedStartMap(
            FadeIn,texts,shift=RIGHT,lag_ratio=0.2
            ),run_time=2)
        self.wait()
        # write titles
        copy1=texts[0].copy().set_stroke(WHITE,1,1).set_color_by_gradient(TEAL_A,WHITE)
        self.play(Write(copy1))
        self.wait()
        copy2=texts[1].copy().set_stroke(WHITE,1,1).set_color_by_gradient(YELLOW_A,WHITE)
        self.play(Write(copy2))
        self.wait()
        copy3=texts[2].copy().set_stroke(WHITE,1,1).set_color_by_gradient(RED_A,WHITE)
        self.play(Write(copy3))
        self.wait()
        self.remove(texts[0],texts[1],texts[2])
        # link_to part1
        simple_eqn=VGroup(
            Tex(r"x+y=2"),
            Tex(r"y=1"),
            ).scale(2).arrange(DOWN,aligned_edge=RIGHT).to_edge(LEFT,buff=1.5)
        rec=SurroundingRectangle(simple_eqn,buff=0.5).set_stroke(TEAL_A,1,1)
        self.play(
            FadeOut(rec2,shift=LEFT),
            FadeOut(arrow,shift=LEFT),
            FadeOut(text,shift=LEFT),
            )
        self.play(FadeIn(simple_eqn,shift=RIGHT),)
        self.play(ShowCreation(rec))
        # know how to
        know_this=Textch("知道怎么解这个").next_to(rec,UP,buff=1.5)
        ar=ArrowCustom().point_from(know_this.get_bottom(),angle=-PI/2,length=1)
        self.play(GrowArrow(ar),FadeIn(know_this,shift=DOWN))
        self.wait()
        self.play(            
            FadeOut(copy2,shift=RIGHT),
            FadeOut(copy3,shift=RIGHT),
            FadeOut(VGroup(ar,rec,know_this,simple_eqn),shift=LEFT),
            copy1.animate.scale(2).center())
        self.wait()



        
        
class EqnScene(Elimination):
    def move_to_frame_corner(self,mob,direction,buff:float=0.3):
        mob.move_to(self.frame.get_corner(direction))
        shift_vec=mob.get_center()-mob.get_corner(direction)
        mob.shift(shift_vec)
        mob.shift(-direction*buff)
    def construct(self):
        # init
        frame=self.frame
        # start
        eqn1=VGroup(
            Tex("x+y=3"),
            Tex("2x+y=5")).arrange(DOWN)
        eqn2=VGroup(
            Tex("x+y=3"),
            Tex("2x+y=5")).arrange(DOWN)
        eqn2.next_to(eqn1,DOWN,buff=0.5)
        sub1=Tex(R"y=3-x")
        sub1.move_to(eqn2[0])
        brace1=Brace(eqn1,LEFT)
        brace2=Brace(eqn2,LEFT)
        sub2=Tex(R"2x+3-x=5")
        sub2.move_to(eqn2[1])
        frame.scale(0.6).move_to(eqn1)
        self.add(eqn1)
        self.add(brace1)
        self.wait()
        self.play(
            TransformFromCopy(VGroup(brace1,eqn1),VGroup(brace2,eqn2)),
            frame.animate.move_to(VGroup(eqn1,eqn2)),
            eqn1.animate.set_opacity(0.5),
            brace1.animate.set_opacity(0.5),
             )
        self.wait()
        self.play(TransformMatchingTex(eqn2[0],sub1,key_map={"+":"-"},
            path_arc=-PI/2))
        self.play(sub1["y"].animate.set_color(RED),
            eqn2[1]["y"].animate.set_color(RED))
        self.play(
            brace2.animate.shift(LEFT*0.4),
            TransformFromCopy(sub1["3-x"],sub2["3-x"]),
            ReplacementTransform(eqn2[1]["2x+"],sub2["2x+"]),
            ReplacementTransform(eqn2[1]["=5"],sub2["=5"]),
            FadeOut(eqn2[1]["y"]),
            sub1["y"].animate.set_color(WHITE)
            )
        self.wait()
        
        # split
        sub22=Tex(R"x=5-3")
        sub22.move_to(sub2)
        sub11=Tex(R"y=3-2")
        sub111=Tex(R"y=1")
        sub222=Tex(R"x=2")
        sub11.move_to(sub1)
        sub222.move_to(sub22)
        sub111.move_to(sub11)
        mark=Tex(R"\checkmark").set_color(RED)
        brace1.put_at_tip(mark)
        self.play(
            FlashAround(sub2["x"][0],color=RED),
            FlashAround(sub2["x"][1],color=RED),
            )
        self.play(
            TransformMatchingTex(sub2,sub22,key_map={"2x":"x"}),
            brace2.animate.shift(RIGHT*0.4))
        self.play(TransformMatchingTex(sub22,sub222))
        self.play(
            FlashAround(sub222["x"][0],color=RED),
            FlashAround(sub1["x"][0],color=RED),
            )
        self.play(
            ReplacementTransform(sub222.copy(),
             VectorizedPoint(sub1["x"].get_center())),
            TransformMatchingTex(sub1,sub11))
        self.play(
            TransformMatchingTex(sub11,sub111),
            brace2.animate.shift(RIGHT*0.4))
        self.play(ReplacementTransform(VGroup(brace2,sub111,sub222),mark))
        self.play(FadeOut(mark),run_time=1)

        # three eqns
        eqn=VGroup(
            Tex("x+y+z=4"),
            Tex("2x+y+z=6"),
            Tex("x+y+2z=5")).arrange(DOWN)
        brace=Brace(eqn,LEFT)
        eqn_down=VGroup(
            Tex("x+y+z=4"),
            Tex("2x+y+z=6"),
            Tex("x+y+2z=5")).arrange(DOWN).next_to(eqn,DOWN,buff=0.5)
        brace_down=Brace(eqn_down,LEFT)
        self.play(TransformMatchingTex(eqn1[0],eqn[0],key_map={"3":"4"}),
            TransformMatchingTex(eqn1[1],eqn[1],key_map={"5":"6"}),
            ReplacementTransform(brace1,brace),
            FadeIn(eqn[2],shift=LEFT,time_span=[0.5,2]),run_time=2)
        self.wait()
        self.play(TransformFromCopy(VGroup(brace,eqn),VGroup(brace_down,eqn_down)),
            frame.animate.move_to(VGroup(eqn,eqn_down)),VGroup(brace,eqn).animate.set_opacity(0.5))
        

        # insert anims
        # self.wait()
        # self.play(FlashAround(eqn_down[0]["y+z"],color=RED),
        #     FlashAround(eqn_down[1]["y+z"],color=RED),run_time=2)
        # self.play(FlashAround(eqn_down[0]["x+y"],color=TEAL),
        #     FlashAround(eqn_down[2]["x+y"],color=TEAL),run_time=2)
        # self.wait()

        # solve
        arrow_right=Arrow(eqn_down[0].get_right(),eqn_down[0].get_right()+RIGHT)
        eqn_right=VGroup(Tex("y+z=4-x"),Tex("x+y=4-z"))
        eqn_right.next_to(arrow_right,RIGHT)
        # brace_right=Brace(eqn_right,LEFT)
        # VGroup(brace_right,eqn_right).next_to(arrow_right,RIGHT)
        eqn1=VGroup(Tex("2+y+1=4"),Tex("y=4-1-2"),Tex("y=1")).move_to(eqn_down[0])
        eqn2=VGroup(Tex("2x+4-x=6"),Tex("2x-x=6-4"),Tex("x=2")).move_to(eqn_down[1])
        eqn3=VGroup(Tex("4-z+2z=5"),Tex("-z+2z=5-4"),Tex("z=1")).move_to(eqn_down[2])
        mark2=Tex(R"\checkmark").set_color(RED)
        brace.put_at_tip(mark2)
        self.play(FlashAround(eqn_down[0]["y+z"],color=RED),
            FlashAround(eqn_down[1]["y+z"],color=RED),run_time=2)
        self.play(Write(arrow_right),frame.animate.shift(RIGHT*1.3))
        self.play(TransformMatchingTex(eqn_down[0].copy(),eqn_right[0],path_arc=-PI/4))
        self.play(FlashAround(eqn_right[0]["y+z"],color=RED),
            FlashAround(eqn_down[1]["y+z"],color=RED),run_time=2)
        self.play(ReplacementTransform(eqn_right[0]["4-x"],eqn2[0]["4-x"]),
                ReplacementTransform(eqn_down[1]["2x+"],eqn2[0]["2x+"]),
                ReplacementTransform(eqn_down[1]["=6"],eqn2[0]["=6"]),
                FadeOut(arrow_right),
                FadeOut(eqn_right[0]["y+z="]),
                FadeOut(eqn_down[1]["y+z"]),
                )
        self.play(TransformMatchingTex(eqn2[0],eqn2[1],path_arc=-PI/2,key_map={"+4":"-4"}), )
        self.play(TransformMatchingTex(eqn2[1],eqn2[2],key_map={"6-4":"2","2x-x":"x"}),)
        
        # to be continue
        self.play(FlashAround(eqn_down[0]["x+y"],color=RED),
            FlashAround(eqn_down[2]["x+y"],color=RED),run_time=2)
        self.play(Write(arrow_right),
            TransformMatchingTex(eqn_down[0].copy(),
            eqn_right[1],path_arc=-PI/4))
        self.play(FlashAround(eqn_right[1]["x+y"],color=RED),
            FlashAround(eqn_down[2]["x+y"],color=RED),run_time=2)
        self.play(
            ReplacementTransform(eqn_right[1]["4-z"],eqn3[0]["4-z"]),
            FadeOut(eqn_right[1]["x+y="]),
            FadeOut(arrow_right),
            FadeOut(eqn_down[2]["x+y"]),
            ReplacementTransform(eqn_down[2]["+2z=5"],eqn3[0]["+2z=5"]),
                )
        # self.play(FadeOut(arrow_right),FadeOut(brace_right),frame.animate.shift(LEFT))
        # self.play(LaggedStart(FlashUnder(eqn_down[1]),FlashUnder(eqn_down[2]),lag_ratio=0.2))
        # self.play(LaggedStart(FlashUnder(eqn_down[1]),FlashUnder(eqn_down[2]),lag_ratio=0.2))
        self.play(TransformMatchingTex(eqn3[0],eqn3[1],path_arc=-PI/4))
        self.play(TransformMatchingTex(eqn3[1],eqn3[2]))

        self.play(Indicate(VGroup(eqn_down[0]["x"],eqn2[2]["x"]))) 
        self.play(Indicate(VGroup(eqn_down[0]["z"],eqn3[2]["z"]))) 
        self.play(LaggedStart(
            TransformFromCopy(eqn2[2],VectorizedPoint(eqn_down[0]["x"].get_center())),
            TransformFromCopy(eqn3[2],VectorizedPoint(eqn_down[0]["z"].get_center())),lag_ratio=0.1),
            TransformMatchingTex(eqn_down[0],eqn1[0]),run_time=1.5)
        self.play(TransformMatchingTex(eqn1[0],eqn1[1],path_arc=PI/4))
        self.play(TransformMatchingTex(eqn1[1],eqn1[2],matched_keys={"4-1-2":"1"}),
            brace_down.animate.shift(RIGHT).set_anim_args(time_span=[0.5,1.5]),run_time=1.5)
        self.play(ReplacementTransform(VGroup(brace_down,eqn1[2],eqn2[2],eqn3[2]),mark2),
            frame.animate.move_to(eqn),
            eqn.animate.set_opacity(1),
            brace.animate.set_opacity(1))
        self.play(FadeOut(mark2),)
        self.wait()
        
        # 5 eqns 5 unknows
        def generate_random_equations(num_equations=5, num_variables=5, seed=42):
            np.random.seed(seed) 
            equations = []
            variables = ['x', 'y', 'z', 'w', 't'][:num_variables]  # 限制变量数量
            for _ in range(num_equations):
                coefficients = np.round(np.random.uniform(0.1, 9.9, num_variables), 1)  # 生成随机系数
                constant = np.round(np.random.uniform(10, 30), 1)  # 生成随机常数项
                equation = " + ".join(f"{coeff}{var}" for coeff, var in zip(coefficients, variables)) + f" = {constant}"
                equations.append(equation)
            return equations
        eqn_5=VGroup(
            Tex("x+y+z+w+t=15"),
            Tex("2x+y+z+w+t=16"),
            Tex("x+y+2z+w+t=18"),
            Tex("3x+y+z+w+t=22"),
            Tex("x+y+z+3w+t=23")
            ).arrange(DOWN)
        equations =generate_random_equations()
        eqn_5_decimal=VGroup(*[Tex(eq) for eq in equations]).arrange(DOWN)
        br=Brace(eqn_5,LEFT)
        br_decimal=Brace(eqn_5_decimal,LEFT)
        self.play(FadeOut(VGroup(brace,eqn),shift=LEFT),FadeIn(VGroup(br,eqn_5),shift=LEFT))
        self.wait()
        self.play(FadeOut(VGroup(br,eqn_5),shift=LEFT),
            FadeIn(VGroup(br_decimal,eqn_5_decimal),shift=LEFT),
            frame.animate.reorient(0, 0, 0, (0.04, 0.1, 0.0), 5.95))
        self.wait()

        # or even hundreds,thousands
        equations1 = generate_random_equations(seed=1)
        equations2 = generate_random_equations(seed=2)
        eqns=VGroup(
            *[Tex(eq) for eq in equations1],
            Tex(R'\vdots'),
            *[Tex(eq) for eq in equations2],
            ).arrange(DOWN)
        kun=Kun()
        br=Brace(eqns,LEFT)
        content=Textch("这么多！")
        self.play(FadeOut(VGroup(br_decimal,eqn_5_decimal),shift=LEFT),
            FadeIn(VGroup(eqns,br),shift=LEFT),
            frame.animate.reorient(0, 0, 0, (-1.78, 0.05, 0.0), 8.27))
        self.move_to_frame_corner(kun,DL)
        bubble=Bubble(content).pin_to(kun.right_eye)
        self.play(FadeIn(kun))
        self.play(kun.animate.shock().look_at(eqns))
        self.play(Write(bubble))
        self.play(kun.animate.close_eyes()\
            .set_anim_args(rate_func=there_and_back))
        self.play(kun.animate.sad())
        self.wait()
        eqns=VGroup(eqns,br).set_z(0)
        self.play(FadeOut(bubble),FadeOut(kun,shift=LEFT*2),
            eqns.animate.center(),frame.animate.center())

        # give to computer
        self.set_floor_plane("xz")
        laptop=Laptop(open_angle=PI/2)
        laptop.rotate(-PI/2,axis=RIGHT)
        laptop.remove(laptop.axis)
        laptop.screen_plate.rescale_to_fit(eqns.get_height()+2,1)
        laptop.screen_plate.stretch(1.3,0)
        laptop[0].rescale_to_fit(laptop.screen_plate.get_width(),0)
        direction=laptop[0].get_corner(UP+LEFT+IN)-laptop.screen_plate.get_corner(DL)
        laptop[0].shift(-direction)
        self.bring_to_back(laptop)
        texts=VGroup(
            Textch("第一步"),
            Textch("第二步"),
            Textch("第三步"),
            Textch("第四步"),
            Textch("第五步"),
            )
        rect=Rectangle(stroke_width=1)
        wen=Tex("?").scale(1.5)
        rect.add(wen)
        rects=rect.replicate(5).arrange(RIGHT)
        rects.set_width(FRAME_WIDTH-1)
        rects.to_edge(UP)
        colors=itertools.cycle([TEAL_A,TEAL_B,TEAL_C,TEAL_B,TEAL_A])
        for a,b in zip(texts,rects):
            color=next(colors)
            a.next_to(b,UP)
            a.set_color(color)
            b.set_color(color)
        texts.fix_in_frame()
        rects.fix_in_frame()
        VGroup(texts,rects).to_edge(UP)
        laptop_rec=Rectangle(7,4.5,stroke_width=1).fix_in_frame().to_edge(DOWN)
        self.play(frame.animate.reorient(-2, 0, 0, (1.33, 2.77, 0.0), 28.38),
            run_time=2)
        self.play(LaggedStart(
            *[ShowCreation(rec) for rec in rects],lag_ratio=0.1),
            LaggedStart(*
                [FadeIn(te) for te in texts],lag_ratio=0.1)
            )
        self.wait()
        self.play(rects.animate.arrange(DOWN).to_edge(RIGHT),
            texts.animate.arrange(DOWN,buff=1).to_edge(RIGHT,buff=3.3),
            # LaggedStartMap(FadeOut,texts,shift=UP),
            frame.animate.reorient(-58, 0, 0, (12.57, -0.19, 13.15), 35.34))
        
        # ar
        rec=Rectangle(6.3,4,stroke_width=1).fix_in_frame().to_edge(LEFT,buff=0.2)
        arrow=Arrow(texts.get_left(),rec.get_right()).fix_in_frame()
        self.play(LaggedStart(
            GrowArrow(arrow),
            ShowCreation(rec),lag_ratio=0.3))
        self.wait()
        # gauss
        self.play(
            LaggedStartMap(FadeOut,VGroup(laptop,arrow,eqns,rec,),shift=LEFT),
            VGroup(texts,rects).animate.to_edge(LEFT,buff=3),
            )
        br=Brace(rects,RIGHT).fix_in_frame().set_color(TEAL)
        text=Textch("高斯消元").fix_in_frame().scale(2)
        br.put_at_tip(text)
        self.play(Write(br),frame.animate.scale(0.5))
        self.play(FadeIn(text))
        self.wait()
        # link to part2
        title=Textch("Part2:高斯消元的步骤",t2f={"Part2:":"Mongolian Baiti"})\
            .fix_in_frame().scale(2).center()
        title.set_color(WHITE)
        self.play(
            LaggedStart(
            FadeOut(texts,shift=LEFT),
            FadeOut(rects,shift=LEFT),
            FadeOut(br,shift=LEFT),
            ReplacementTransform(text["高斯消元"],title["高斯消元"]),
            FadeIn(title["Part2:"],shift=RIGHT),
            FadeIn(title["的步骤"],shift=LEFT),lag_ratio=0.2),
            )
        self.wait()
        title2=title.copy().set_color_by_gradient(YELLOW_A,WHITE)
        self.play(Write(title2))
        self.wait()
        


class text_vcube(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        vcube=VCube(2)
        vcube.set_z(-4)
        t=Tex("2")
        self.bring_to_front(t)
        self.bring_to_back(vcube)
        t.apply_depth_test(anti_alias_width=0)
        t.deactivate_depth_test()
        t.set_fill(RED,1)
        t.set_stroke(WHITE,3,1)
        t.fix_in_frame()
        t.insert_n_curves(100)
        t.make_smooth()
        self.add(t)
class DashedRectangle(VGroup):
    def __init__(
        self,
        width: float = 4.0,
        height: float = 2.0,
        dash_length: float = 0.15,
        color: Color = WHITE,
        positive_space_ratio: float = 0.5,
        **kwargs
    ):
        super().__init__(**kwargs)
        UL = UP * (height / 2) + LEFT * (width / 2)   # 左上
        UR = UP * (height / 2) + RIGHT * (width / 2)  # 右上
        DR = DOWN * (height / 2) + RIGHT * (width / 2) # 右下
        DL = DOWN * (height / 2) + LEFT * (width / 2)  # 左下
        top_edge = DashedLine(UL, UR, dash_length=dash_length, color=color,positive_space_ratio=positive_space_ratio)
        right_edge = DashedLine(UR, DR, dash_length=dash_length, color=color,positive_space_ratio=positive_space_ratio)
        bottom_edge = DashedLine(DR, DL, dash_length=dash_length, color=color,positive_space_ratio=positive_space_ratio)
        left_edge = DashedLine(DL, UL, dash_length=dash_length, color=color,positive_space_ratio=positive_space_ratio)
        self.add(top_edge, right_edge, bottom_edge, left_edge)
class SurroundingDashedRectangle(DashedRectangle):
    def __init__(
        self,
        mobject: Mobject,
        buff: float = 0.1,
        dash_length: float = 0.15,
        color: Color = WHITE,
        **kwargs
    ):
        surrounding_rect = SurroundingRectangle(mobject, buff=buff, color=color)
        width = surrounding_rect.get_width()
        height = surrounding_rect.get_height()
        super().__init__(width=width, height=height, dash_length=dash_length, color=color, **kwargs)
        self.move_to(surrounding_rect.get_center())

                    



class TexEqn(Tex):
    def __init__(self,tex_strings, reference_eqn=None, **kwargs):
            super().__init__(tex_strings, **kwargs)
            self.reference_eqn = reference_eqn
    def align_eqn(self,rf=None):
        if rf is None and self.reference_eqn is not None:
            rf=self.reference_eqn.copy()
        elif rf is not None:
            rf = rf.copy()
        else:
            raise ValueError("align_eqn requires a reference equation, but none was provided.")
        variables = list(dict.fromkeys(re.findall(r"[a-zA-Z]",rf.string)))
        pattern_LHS = [re.compile(rf"[+-]?(\d*|\d*\.\d+|\\frac{{\d+}}{{\d+}}){var}") 
                    for var in variables]
        pattern_RHS =  re.compile(rf"=[+-]?(\d+|\d*\.\d+|\\frac{{\d+}}{{\d+}})")
        # left hand side
        y=self.get_y()
        for pattern in pattern_LHS:

            span=self.find_spans_by_selector(pattern)
            span_rf=rf.find_spans_by_selector(pattern)

            if not span:
                continue

            indices_eqn=self.get_submob_indices_list_by_span(span[0])
            indices_rf=rf.get_submob_indices_list_by_span(span_rf[0])
            start,end=span[0]
            start_rf,end_rf=span_rf[0]
            
            self[indices_eqn[-1]].align_to(rf[indices_rf[-1]],RIGHT) # x,y,z
            if self.string[start:end].startswith(("+","-")) : # to_align有符号
                if rf.string[start_rf:end_rf].startswith(("+","-")): # rf 也有符号  
                    self[indices_eqn[0]].align_to(rf[indices_rf[0]],RIGHT) # 匹配符号
                    if len(indices_eqn)>2 and len(indices_rf)>2:    # 二者都有内容
                        self[indices_eqn[1]:indices_eqn[-1]].align_to(rf[indices_rf[1]:indices_rf[-1]],RIGHT)
                    if len(indices_eqn)>2 and len(indices_rf)==2:  # to_align有内容,rf无内容
                        self[indices_eqn[1]:indices_eqn[-1]].next_to(self[indices_eqn[-1]],LEFT,buff=0.1).set_y(y)
                
                elif not rf.string[start_rf:end_rf].startswith(("+","-")):# to_align有符号 rf 无符号
                    self[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[0]:indices_rf[-1]],RIGHT)

            elif rf.string[start_rf:end_rf].startswith(("+","-")): # __x--->___+x  to_align无符号；参考有符号
                if len(indices_eqn)>1 and len(indices_rf)>2: # 2x --> +2x to_align有内容；参考有内容
                    self[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[1]:indices_rf[-1]],RIGHT)
                if len(indices_eqn)>1 and len(indices_rf)==2: # 2x --> +x  to_align有内容；参考无内容
                    # pass
                    self[indices_eqn[0]:indices_eqn[-1]].next_to(self[indices_eqn[-1]],LEFT,buff=0.1).set_y(y)
                if len(indices_eqn)==1 and len(indices_rf)>=2: # x --> +x  to_align无内容；参考有或无内容
                    pass
            elif not rf.string[start_rf:end_rf].startswith(("+","-")):
                if len(indices_eqn)>1 and len(indices_rf)>1:
                    self[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[0]:indices_rf[-1]],RIGHT)

        # right hand side
        span=self.find_spans_by_selector(pattern_RHS)
        span_rf=rf.find_spans_by_selector(pattern_RHS)

        if span==[]:
            return self
        start,end=span[0]
        start_rf,end_rf=span_rf[0]
        indices_eqn=self.get_submob_indices_list_by_span(span[0])
        indices_rf=rf.get_submob_indices_list_by_span(span_rf[0])

        self[indices_eqn[0]].align_to(rf[indices_rf[0]],RIGHT) # 匹配=
        if self.string[start:end].startswith(("+","-"),1) : # to_align 有符号
            if rf.string[start_rf:end_rf].startswith(("+","-"),1): # rf 也有符号
                self[indices_eqn[1]].align_to(rf[indices_rf[1]],RIGHT) # 匹配符号
                self[indices_eqn[2]:].match_x(rf[indices_rf[2]:]) # 匹配内容
        elif rf.string[start_rf:end_rf].startswith(("+","-"),1): # to_align 无符号 rf有符号
            self[indices_eqn[1]:].match_x(rf[indices_rf[2]:])
        elif not rf.string[start_rf:end_rf].startswith(("+","-"),1):# to_align 无符号 rf无符号
            self[indices_eqn[1]:].match_x(rf[indices_rf[1]:])
        return self

class VGroupCustom(VGroup):
    def __init__(self, *vmobjects, reference_eqn=None, **kwargs):
            super().__init__(*vmobjects, **kwargs)
            self.reference_eqn = reference_eqn
    def align_eqns(self):
        # re.compile(rf"[+-]?(\\frac{{\d+}}{{\d+}})k")
        rf=self.reference_eqn.copy()
        variables = list(dict.fromkeys(re.findall(r"[a-zA-Z]",rf.string)))
        pattern_LHS = [re.compile(rf"[+-]?(\d*|\d*\.\d+|\\frac{{\d+}}{{\d+}}){var}") 
                    for var in variables]
        pattern_RHS =  re.compile(rf"=[+-]?(\d+|\d*\.\d+|\\frac{{\d+}}{{\d+}})")
        for eqn in self:
            # left hand side
            y=eqn.get_y()
            for pattern in pattern_LHS:

                span=eqn.find_spans_by_selector(pattern)
                span_rf=rf.find_spans_by_selector(pattern)

                if span==[]:
                    continue

                indices_eqn=eqn.get_submob_indices_list_by_span(span[0])
                indices_rf=rf.get_submob_indices_list_by_span(span_rf[0])
                start,end=span[0]
                start_rf,end_rf=span_rf[0]
                
                eqn[indices_eqn[-1]].align_to(rf[indices_rf[-1]],RIGHT) # x,y,z
                if eqn.string[start:end].startswith(("+","-")) : # to_align有符号
                    if rf.string[start_rf:end_rf].startswith(("+","-")): # rf 也有符号  
                        eqn[indices_eqn[0]].align_to(rf[indices_rf[0]],RIGHT) # 匹配符号
                        if len(indices_eqn)>2 and len(indices_rf)>2:    # 二者都有内容
                            eqn[indices_eqn[1]:indices_eqn[-1]].align_to(rf[indices_rf[1]:indices_rf[-1]],RIGHT)
                        if len(indices_eqn)>2 and len(indices_rf)==2:  # to_align有内容,rf无内容
                            eqn[indices_eqn[1]:indices_eqn[-1]].next_to(eqn[indices_eqn[-1]],LEFT,buff=0.1).set_y(y)
                    
                    elif not rf.string[start_rf:end_rf].startswith(("+","-")):# to_align有符号 rf 无符号
                        eqn[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[0]:indices_rf[-1]],RIGHT)

                elif rf.string[start_rf:end_rf].startswith(("+","-")): # __x--->___+x  to_align无符号；参考有符号
                    if len(indices_eqn)>1 and len(indices_rf)>2: # 2x --> +2x to_align有内容；参考有内容
                        eqn[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[1]:indices_rf[-1]],RIGHT)
                    if len(indices_eqn)>1 and len(indices_rf)==2: # 2x --> +x  to_align有内容；参考无内容
                        # pass
                        eqn[indices_eqn[0]:indices_eqn[-1]].next_to(eqn[indices_eqn[-1]],LEFT,buff=0.1).set_y(y)
                    if len(indices_eqn)==1 and len(indices_rf)>=2: # x --> +x  to_align无内容；参考有或无内容
                        pass
                elif not rf.string[start_rf:end_rf].startswith(("+","-")):
                    if len(indices_eqn)>1 and len(indices_rf)>1:
                        eqn[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[0]:indices_rf[-1]],RIGHT)

            # right hand side
            span=eqn.find_spans_by_selector(pattern_RHS)
            span_rf=rf.find_spans_by_selector(pattern_RHS)

            if span==[]:
                continue
            start,end=span[0]
            start_rf,end_rf=span_rf[0]
            indices_eqn=eqn.get_submob_indices_list_by_span(span[0])
            indices_rf=rf.get_submob_indices_list_by_span(span_rf[0])

            eqn[indices_eqn[0]].align_to(rf[indices_rf[0]],RIGHT) # 匹配=
            if eqn.string[start:end].startswith(("+","-"),1) : # to_align 有符号
                if rf.string[start_rf:end_rf].startswith(("+","-"),1): # rf 也有符号
                    eqn[indices_eqn[1]].align_to(rf[indices_rf[1]],RIGHT) # 匹配符号
                    eqn[indices_eqn[2]:].match_x(rf[indices_rf[2]:]) # 匹配内容
            elif rf.string[start_rf:end_rf].startswith(("+","-"),1): # to_align 无符号 rf有符号
                eqn[indices_eqn[1]:].match_x(rf[indices_rf[2]:])
            elif not rf.string[start_rf:end_rf].startswith(("+","-"),1):# to_align 无符号 rf无符号
                eqn[indices_eqn[1]:].match_x(rf[indices_rf[1]:])
        return self
class Pentagram(VMobject):
    def __init__(self, outer_radius=2, **kwargs):
        super().__init__(**kwargs)
        # Calculate inner radius based on the ratio:
        # 内圈半径 = 外圈半径 * sin(18°) / sin(54°)
        inner_radius = outer_radius * np.sin(np.radians(18)) / np.sin(np.radians(54))
        points = []
        # 生成五角星的10个交替顶点 (交替使用 outer 和 inner 半径)
        # Start at 90° to make the top point vertical.
        for i in range(10):
            angle = np.radians(90 + i * 36)  # 每个点间隔36度 (360/10)
            radius = outer_radius if i % 2 == 0 else inner_radius
            point = radius * np.array([np.cos(angle), np.sin(angle), 0])
            points.append(point)
        # 使用 set_points_as_corners 方法将这些点连成闭合路径
        self.set_points_as_corners(points + [points[0]])

class Gaussian_elimination_steps(Elimination):
    def parse_equation(self,equation: str):
        left, right = equation.split("=")
        right_value = right.strip()
        matches = re.findall(r"([+-]?\s*(?:\\frac{\d+}{\d+}|\d*))\s*([xyz])", left)
        coefficients = {'x': "0", 'y': "0", 'z': "0"}
        for coef, var in matches:
            coef = coef.strip()  # 去掉前后空格
            if coef in ["", "+", "-"]:  # 处理 `-x` 或 `+y`
                coef += "1"
            if coef.startswith("+"):  # 移除 `+` 号
                coef = coef[1:]
            coefficients[var] = coef
        return coefficients['x'], coefficients['y'], coefficients['z'], right_value
    def extract_fraction_parts(self,vgroup, frac_pattern):
        numerator = VGroup()
        denominator = VGroup()
        fraction_symbol = None
        check = 0  
        for submob in vgroup[frac_pattern][0].submobjects:
            if isinstance(submob, VMobjectFromSVGPath) and check == 0:
                numerator.add(submob)
            elif isinstance(submob, Rectangle):  # 识别分数线
                fraction_symbol = submob
                check = 1
            elif isinstance(submob, VMobjectFromSVGPath) and check == 1:
                denominator.add(submob)
        return numerator, fraction_symbol, denominator
    def construct(self):
        # init
        frame=self.frame
        
        # add eqns_step0
        pattern=re.compile(r"\\frac\{\d+\}\{\d+\}|[a-zA-Z]|\+|\-|=|\d+")
        refer=Tex(R"+2x\,+2y\,+2z\,=+22",isolate=pattern).stretch(1.2,0)
        eqns_right=VGroupCustom(
            Tex("y+2x-z=8",isolate=pattern),
            Tex("2z-y-3x=-11",isolate=pattern),
            Tex("-2x+2z+y=-3",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN)
        eqns_step0=VGroupCustom(
            Tex("2x+y-z=8",isolate=pattern),
            Tex("-3x-y+2z=-11",isolate=pattern),
            Tex("-2x+y+2z=-3",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN)
        # define func "get_labels_to"
        def get_labels_to(grp,buff=0.5):
            labels=VGroup()
            for i,eqn in enumerate(grp):
                label=Tex(f"({i+1})",font_size=30)
                label.next_to(eqn,RIGHT,buff=buff)
                labels.add(label)
            for i,label in enumerate(labels):
                if i !=0:
                    label.align_to(labels[0],RIGHT)
            return labels
        frame.reorient(0, 0, 0, (-0.01, 0.08, 0.0), 4.55)
        self.add(eqns_right)
        self.play(TransformMatchingTex(eqns_right[0],eqns_step0[0],path_arc=PI/2))
        self.play(TransformMatchingTex(eqns_right[1],eqns_step0[1],path_arc=PI/2))
        self.play(TransformMatchingTex(eqns_right[2],eqns_step0[2],path_arc=PI/2,matched_keys={"+2z"}))
        self.play(eqns_step0.animate.align_eqns())
        labels_step0=get_labels_to(eqns_step0.align_eqns())
        self.play(LaggedStart(
            *[eqns_step0[i]["x"].animate.set_color(TEAL)\
            .set_anim_args(rate_func=there_and_back)
            for i in range(3)],
            FlashAround(
                VGroup(eqns_step0[i]["x"]
                    for i in range(3) )
                ,color=TEAL),
            *[eqns_step0[i]["y"].animate.set_color(RED)\
            .set_anim_args(rate_func=there_and_back)
            for i in range(3)],
            FlashAround(
                VGroup(eqns_step0[i]["y"]
                    for i in range(3) )
                ,color=RED),
            *[eqns_step0[i]["z"].animate.set_color(GREEN)\
            .set_anim_args(rate_func=there_and_back)
            for i in range(3)],
            FlashAround(
                VGroup(eqns_step0[i]["z"]
                    for i in range(3) )
                ,color=GREEN),
            lag_ratio=0.1,run_time=4
          ))
        self.play(LaggedStartMap(FadeIn,labels_step0,shift=LEFT))
        

        # eqns_step1
        ARROW_LENGTH=2.3
        REC_BUFF=0.05
        arrow_step1=Arrow(eqns_step0.get_bottom(),
            eqns_step0.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step1=VGroupCustom(
            Tex("2x+y-z=8",isolate=pattern),
            Tex(R"\frac{1}{2}y+\frac{1}{2}z=1",isolate=pattern),
            Tex("2y+z=5",isolate=pattern),
            reference_eqn=eqns_step0.reference_eqn
            ).arrange(DOWN).next_to(arrow_step1,DOWN).align_eqns()
        labels_step1=get_labels_to(eqns_step1)
        note_step1=VGroup(
            Textch("第一步"),
            Textch("用方程"),
            Textch("消去它下面的"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step1_insert=VGroup(
            labels_step0[0].copy().next_to(note_step1[1],RIGHT,buff=0.1),
            Tex("x").next_to(note_step1[2],RIGHT,buff=0.1)
            )
        note_step1.add(note_step1_insert)
        note_step1.next_to(arrow_step1,LEFT,buff=3,aligned_edge=UP)
        underline_step1=Underline(note_step1[0],stroke_color=YELLOW)
        operations=VGroup(
            Tex(R"(2)-\frac{-3}{2}(1)",font_size=30),
            Tex(R"(3)-\frac{-2}{2}(1)",font_size=30),
            ).arrange(DOWN).next_to(arrow_step1,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step1=VGroup(
            SurroundingRectangle(operations[0][frac_patn],stroke_width=2,buff=REC_BUFF),
            SurroundingRectangle(operations[1][frac_patn],stroke_width=2,buff=REC_BUFF)
            )
        back_rec0=SurroundingRectangle(VGroup(eqns_step0,labels_step0),
            stroke_color=WHITE,stroke_opacity=1,buff=0.2)
        back_rec1=SurroundingRectangle(VGroup(eqns_step1,labels_step1),
            stroke_color=WHITE,stroke_opacity=1,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        numerator1,frac_symbol1,denominator1=self.extract_fraction_parts(operations[0],frac_patn)
        numerator2,frac_symbol2,denominator2=self.extract_fraction_parts(operations[1],frac_patn)
        self.play(
            frame.animate.reorient(0, 0, 0, (0.0, -2.2, 0.0), 8.00),
            LaggedStart(
            FadeIn(note_step1[0],shift=RIGHT),
            ShowCreation(underline_step1),
            ShowCreation(back_rec0),
            GrowArrow(arrow_step1),
            ShowCreation(back_rec1)
            ))
        self.wait()
        self.play(LaggedStart(
            FadeIn(note_step1[1],shift=RIGHT),
            FadeIn(note_step1[3][0],shift=LEFT),
            FadeIn(note_step1[2],shift=RIGHT),
            FadeIn(note_step1[3][1],shift=LEFT),
            lag_ratio=0.05))
        
        # copy 1st eqn
        tilt_line1=Line(stroke_color=RED).match_width(eqns_step0[1]["-3x"]).rotate(-PI/4).move_to(eqns_step0[1]["-3x"])
        tilt_line2=Line(stroke_color=RED).match_width(eqns_step0[2]["-2x"]).rotate(-PI/4).move_to(eqns_step0[2]["-2x"])
        rec=SurroundingRectangle(eqns_step0[0],stroke_color=RED,stroke_opacity=1,fill_opacity=0.3,fill_color=RED)
        self.play(Write(rec))
        self.play(TransformFromCopy(rec,tilt_line1,path_arc=-PI/2),
            ReplacementTransform(rec,tilt_line2,path_arc=-PI/2))
        self.wait()
        self.play(FadeOut(tilt_line1),FadeOut(tilt_line2))
        self.play(TransformFromCopy(eqns_step0[0],eqns_step1[0]),
            TransformFromCopy(labels_step0[0],labels_step1[0]))
        # insert_change
        self.play(LaggedStart(
            TransformFromCopy(labels_step0[1],operations[0][0:3]),
            FadeIn(operations[0][3]),FadeIn(recs_step1[0]),
            TransformFromCopy(labels_step0[0],operations[0][-1:-4:-1].reverse_submobjects()),
            lag_ratio=0.6))
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(eqns_step0[1][0:2],numerator1,path_arc=PI/2),
            TransformFromCopy(eqns_step0[0][0],denominator1[0],path_arc=PI/2),
            Write(frac_symbol1),
            lag_ratio=0.2),run_time=2)
        # not write as 
        oper=Tex(R"\Leftrightarrow(2)+\frac{3}{2}(1)",font_size=30).next_to(operations[0],RIGHT)
        cross=Cross(oper)
        self.play(Write(oper))
        self.play(ShowCreation(cross[0]))
        self.wait()
        self.play(FadeOut(oper),FadeOut(cross[0]))
        self.play(LaggedStart(
            TransformFromCopy(eqns_step0[1][0:2],numerator1,path_arc=PI/2),
            TransformFromCopy(eqns_step0[0][0],denominator1[0],path_arc=PI/2),
            lag_ratio=0.2),run_time=3)
        self.wait()

        # messy calculation
        arrow_to_right=Arrow(operations[0].get_right(),operations[0].get_right()+RIGHT*2.3)
        m1=TexEqn("-3x-y+2z=-11",isolate=pattern)
        m2=TexEqn("2x+y-z=8",isolate=pattern)
        m2_change=TexEqn(R"3x+\frac{3}{2}y-\frac{3}{2}z=12",isolate=pattern)
        result=TexEqn(R"\frac{1}{2}y+\frac{1}{2}z=1",isolate=pattern)
        messy=VGroup(m1,VGroup(m2,m2_change),result).arrange(DOWN)
        m1.align_eqn(refer)
        m2.align_eqn(refer)
        m2_change.align_eqn(refer)
        result.align_eqn(refer)
        messy.next_to(arrow_to_right,RIGHT,buff=2)
        left_br=Tex("(").next_to(m2_change,LEFT)
        right_br=Tex(")").next_to(m2_change,RIGHT)
        l_factor=Tex(R"\frac{-3}{2}",isolate=pattern).next_to(left_br,LEFT)
        minus=Tex("-").next_to(l_factor,LEFT)
        d_line=Line(minus.get_left(),right_br.get_right()).next_to(m2,DOWN,buff=0.5)
        symbols=VGroup(minus,left_br,right_br,l_factor,d_line)
        rec_whole=SurroundingRectangle(VGroup(messy,minus,d_line),buff=0.2,stroke_color=WHITE,
            fill_color=GREY,fill_opacity=0.2)
        dont_worry=Textch("一些琐碎的计算，不必关心细节！").next_to(rec_whole,UP)
        dont_worry["计"].set_fill(WHITE,1,0)
        self.play(GrowArrow(arrow_to_right),
            frame.animate.reorient(0, 0, 0, (5.2, -2.2, 0.0), 8.00))
        self.play(FadeIn(rec_whole),FadeIn(dont_worry))
        self.play(LaggedStart(
            TransformFromCopy(operations[0][0:3],m1,path_arc=-PI/2),
            TransformFromCopy(operations[0][3],minus,path_arc=-PI/2),
            TransformFromCopy(operations[0][4:8],l_factor,path_arc=-PI/2),
            TransformFromCopy(operations[0][8:],m2,path_arc=-PI/2),
            Write(left_br),Write(right_br),ShowCreation(d_line)
            ,lag_ratio=0.5))
        self.play(LaggedStart(
            ReplacementTransform(VGroup(minus.copy(),l_factor.copy(),m2[0:2]),m2_change[0:2],path_arc=-PI/2),
            ReplacementTransform(VGroup(minus.copy(),l_factor.copy(),m2[2:4]),m2_change[2:7],path_arc=-PI/2),
            ReplacementTransform(VGroup(minus.copy(),l_factor.copy(),m2[4:6]),m2_change[7:12],path_arc=-PI/2),
            ReplacementTransform(VGroup(minus,l_factor,m2[6:]),m2_change[12:],path_arc=-PI/2),
            FadeOut(VGroup(left_br,right_br)),
            lag_ratio=0.5))
        self.play(LaggedStart(
            TransformFromCopy(VGroup(m1[0:3],m2_change[0:2]),VectorizedPoint(result.get_left()+LEFT)),
            TransformFromCopy(VGroup(m1[3:5],m2_change[2:7]),result[0:4]),
            TransformFromCopy(VGroup(m1[5:8],m2_change[7:12]),result[4:9]),
            TransformFromCopy(VGroup(m1[8],m2_change[12]),result[9]),
            TransformFromCopy(VGroup(m1[9:],m2_change[13:]),result[10]),
            lag_ratio=0.3))
        self.wait()
        # go_back
        self.play(LaggedStartMap(FadeOut,VGroup(arrow_to_right,m1,m2_change,d_line,dont_worry,rec_whole),shift=RIGHT),
            TransformMatchingStrings(result,eqns_step1[1],time_span=[0,1.3]),
            frame.animate.reorient(0, 0, 0, (0.0, -2.2, 0.0)),
            FadeIn(labels_step1[1],shift=LEFT,time_span=[1,1.5]),run_time=1.5)
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(labels_step0[2],operations[1][0:3]),
            FadeIn(operations[1][3]),FadeIn(recs_step1[1]),
            TransformFromCopy(labels_step0[0],operations[1][-1:-4:-1].reverse_submobjects()),
            lag_ratio=0.6))
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(eqns_step0[2][0:2],numerator2,path_arc=PI/2),
            TransformFromCopy(eqns_step0[0][0],denominator2[0],path_arc=PI/2),
            Write(frac_symbol2),
            lag_ratio=0.2),run_time=2)
        self.wait()
        # directly give eqn
        DartColrS=itertools.cycle(["#a5d75f","#00693e","#804c2b","#b9b7b6","#94c4e8"])
        def star_anims(operation,eqns,label):
            pantagram=Pentagram()
            pantagram.match_height(operation).set_fill(WHITE,1,1)\
                .set_stroke(RED,0,0).move_to(operation).scale(0.2)
            return LaggedStart(
            *[ReplacementTransform(pantagram.copy().set_color(next(DartColrS))
                ,submob)
            for submob in eqns.submobjects],
            FadeIn(label,shift=LEFT),lag_ratio=0.05)

        self.play(star_anims(operations[1],eqns_step1[2],labels_step1[2]))
        self.wait()
        self.play(
            FlashUnder(eqns_step0[0]),
            FlashUnder(eqns_step1[0]),
            eqns_step0[0].animate.set_opacity(0.5),
            labels_step0[0].animate.set_opacity(0.5),
            eqns_step1[0].animate.set_opacity(0.5),
            labels_step1[0].animate.set_opacity(0.5),
            run_time=2
            )
        
        
        # eqns_step2
        arrow_step2=Arrow(eqns_step1.get_bottom(),eqns_step1.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step2=VGroupCustom(
            Tex("2x+y-z=8",isolate=pattern),
            Tex(R"\frac{1}{2}y+\frac{1}{2}z=1",isolate=pattern),
            Tex("-z=1",isolate=pattern),
            reference_eqn=eqns_step0.reference_eqn
            ).arrange(DOWN).next_to(arrow_step2,DOWN).align_eqns()
        labels_step2=get_labels_to(eqns_step2)
        note_step2=VGroup(
            Textch("第二步"),
            Textch("用方程"),
            Textch("消去它下面的"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step2_insert=VGroup(
            labels_step1[1].copy().next_to(note_step2[1],RIGHT,buff=0.1),
            Tex("y").next_to(note_step2[2],RIGHT,buff=0.1)
            )
        note_step2.add(note_step2_insert)
        note_step2.next_to(arrow_step2,LEFT,buff=3,aligned_edge=UP)
        underline_step2=Underline(note_step2[0],stroke_color=YELLOW)
        operations2=Tex(R"(3)-\frac{2}{1/2}(2)",font_size=30).next_to(arrow_step2,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step2=SurroundingRectangle(operations2[frac_patn],stroke_width=2,buff=REC_BUFF)
        numerator2,frac_symbol2,denominator2=self.extract_fraction_parts(operations2,frac_patn)
        back_rec2=SurroundingRectangle(VGroup(eqns_step2,labels_step2),
            stroke_color=WHITE,stroke_opacity=1,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step2,eqns_step2,labels_step2,note_step2,underline_step2,operations2,recs_step2)
        self.play(frame.animate.reorient(0, 0, 0, (0.0, -6.97, 0.0), 8.00))
        self.play(FadeIn(note_step2[0],shift=RIGHT),
            ShowCreation(underline_step2),
            GrowArrow(arrow_step2),
            ShowCreation(back_rec2))
        self.play(FlashUnder(eqns_step1[1]))
        self.play(LaggedStart(
            FadeIn(note_step2[1],shift=RIGHT),
            FadeIn(note_step2[3][0],shift=LEFT),
            FadeIn(note_step2[2],shift=RIGHT),
            FadeIn(note_step2[3][1],shift=LEFT),
            lag_ratio=0.1))
        self.wait()
        # cross out
        eqns_step2[0].set_opacity(0.5)
        labels_step2[0].set_opacity(0.5)
        rec=SurroundingRectangle(eqns_step1[1],stroke_color=RED,stroke_opacity=0.5,fill_opacity=0.5,fill_color=RED)
        tilt_line3=Line(stroke_color=RED).match_width(eqns_step1[2]["2y"]).rotate(-PI/4).move_to(eqns_step1[2]["2y"])
        self.play(Write(rec))
        self.play(ReplacementTransform(rec,tilt_line3,path_arc=-PI/2),)
        self.play(FadeOut(tilt_line3))
        self.wait()
        self.play(
            TransformFromCopy(eqns_step1[0],eqns_step2[0]),
            TransformFromCopy(labels_step1[0],labels_step2[0]),
            TransformFromCopy(eqns_step1[1],eqns_step2[1]),
            TransformFromCopy(labels_step1[1],labels_step2[1])
            )
        self.play(LaggedStart(
            TransformFromCopy(labels_step1[2],operations2[0:3]),
            ShowCreation(recs_step2),
            Write(operations2[3]),
            TransformFromCopy(labels_step1[1],operations2[-1:-4:-1].reverse_submobjects()),
            lag_ratio=0.2))
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(eqns_step1[2][0],numerator2[0],path_arc=PI/2),
            TransformFromCopy(eqns_step1[1][0:3],denominator2,path_arc=PI/2),
            Write(frac_symbol2),
            lag_ratio=0.2),run_time=2)
        self.play(star_anims(operations2,eqns_step2[2],labels_step2[2]))
        self.play(
            eqns_step1[1].animate.set_opacity(0.5),
            labels_step1[1].animate.set_opacity(0.5),
            eqns_step2[1].animate.set_opacity(0.5),
            labels_step2[1].animate.set_opacity(0.5),
            )
        # we stop here
        vdots=Tex(r"\vdots").next_to(back_rec2,DOWN)
        new_refer=Tex(R"+2x\,+2y\,+2z\,+w\,=-1",isolate=pattern).stretch(1.2,0)
        eqns_add=VGroupCustom(
            TexEqn("2x+y-z=8",isolate=pattern),
            TexEqn(R"\frac{1}{2}y+\frac{1}{2}z=1",isolate=pattern),
            TexEqn("-z=1",isolate=pattern),
            TexEqn("2z=-2",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN).align_eqns().next_to(vdots,DOWN,buff=0.5)
        eqns_add[0].set_opacity(0.5)
        eqns_add[1].set_opacity(0.5)
        labels_eqns_add=get_labels_to(eqns_add)
        labels_eqns_add[0].set_opacity(0.5)
        labels_eqns_add[1].set_opacity(0.5)
        grp=VGroup(eqns_add,labels_eqns_add).match_x(vdots)
        dashrec=SurroundingDashedRectangle(grp,buff=0.2,positive_space_ratio=0.4)
        dashrec.set_color_by_gradient(TEAL_A,WHITE)
        self.play(
            frame.animate.shift(DOWN*5),
            TransformFromCopy(arrow_step2,vdots),
            FadeTransform(back_rec2.copy(),dashrec),
            TransformFromCopy(eqns_step2,eqns_add[0:3]),
            TransformFromCopy(labels_step2,labels_eqns_add[0:3]),
            run_time=2)
        self.wait()
        self.play(
            LaggedStart(
            FadeIn(VGroup(eqns_add[3],labels_eqns_add[3]),shift=LEFT),
            FadeIn(VGroup(eqns_add[4],labels_eqns_add[4]),shift=LEFT),
            lag_ratio=0.3
            ))
        sr_rec=SurroundingRectangle(VGroup(eqns_add[2],labels_eqns_add[2]))
        sr_rec.set_fill(RED,0.2).set_stroke(RED,2,1)
        tilt_line1=Line(stroke_color=RED).match_width(eqns_add[3]["2z"]).rotate(-PI/4).move_to(eqns_add[3]["2z"])
        tilt_line2=Line(stroke_color=RED).match_width(eqns_add[4]["z"]).rotate(-PI/4).move_to(eqns_add[4]["z"])
        self.play(ShowCreation(sr_rec))
        self.play(
            ReplacementTransform(sr_rec,tilt_line1),
            TransformFromCopy(sr_rec,tilt_line2),
            )
        self.wait()
        self.play(frame.animate.shift(UP*5),
            LaggedStartMap(FadeOut,VGroup(vdots,*grp,dashrec,tilt_line1,tilt_line2),shift=DOWN))
        self.wait()
        
        # we can now solve
        ar1=Arrow(labels_step2[2].get_right(),labels_step2[2].get_right()+RIGHT,buff=0.05)
        ar2=Arrow(labels_step2[1].get_right(),labels_step2[1].get_right()+RIGHT,buff=0.05)
        ar3=Arrow(labels_step2[0].get_right(),labels_step2[0].get_right()+RIGHT,buff=0.05)
        s1=Tex("z=-1").next_to(ar1,RIGHT)
        s2=Tex("y=3").next_to(ar2,RIGHT)
        s3=Tex("x=2").next_to(ar3,RIGHT)
        u1=Arrow(s1.get_top(),s1.get_top()+UP*0.5,buff=0.01)
        u2=Arrow(s2.get_top(),s2.get_top()+UP*0.5,buff=0.01).match_x(u1)
        u3=Arrow(s1.get_right(),s3.get_bottom(),path_arc=PI/2)
        self.play(LaggedStart(
            GrowArrow(ar1),
            FadeIn(s1,shift=RIGHT*1.5)
            ))
        self.play(FadeOut(ar1))
        self.play(LaggedStart(
            GrowArrow(ar2),
            GrowArrow(u1),
            FadeIn(s2,shift=RIGHT*1.5)
            ))
        self.play(FadeOut(u1),FadeOut(ar2))
        self.play(LaggedStart(
            GrowArrow(ar3),
            GrowArrow(u2),GrowArrow(u3),
            FadeIn(s3,shift=RIGHT*1.5)
            ))
        self.play(FadeOut(u2),FadeOut(ar3),FadeOut(u3))

        # called gaussian elimination
        frame.save_state()
        big_br=Brace(VGroup(eqns_step0,eqns_step2,note_step1),LEFT,buff=0.9)
        gaussian=TextCustom(en="Gaussian Elimination",ch="高斯消元",
            font_size_en=80,font_size_ch=80)
        big_br.put_at_tip(gaussian)
        self.play(frame.animate.reorient(0, 0, 0, (-3.07, -4.56, 0.0), 13.42),
            # eqns_step0.animate.set_opacity(1),
            # labels_step0.animate.set_opacity(1),
            # eqns_step1.animate.set_opacity(1),
            # labels_step1.animate.set_opacity(1),
            # eqns_step2.animate.set_opacity(1),
            # labels_step2.animate.set_opacity(1),
            )
        self.play(LaggedStartMap(FadeIn,
            VGroup(big_br,gaussian),shift=RIGHT,lag_ratio=0.02))
        self.wait(2)
        self.play(frame.animate.restore())

        # dont want solve this way
        line_out=VGroup(
            Line().insert_n_curves(20).set_stroke(RED,[3,6,0]).replace(s1,stretch=True),
            Line().insert_n_curves(20).set_stroke(RED,[3,6,0]).replace(s2,stretch=True),
            Line().insert_n_curves(20).set_stroke(RED,[3,6,0]).replace(s3,stretch=True),
            )
        self.play(FlashAround(VGroup(s3,s2,s1),color=RED),run_time=1.5)
        self.play(*map(ShowCreation,line_out))
        self.play(LaggedStartMap(FadeOut,VGroup(line_out,s3,s2,s1),shift=RIGHT))

        # jordan continue--step3
        arrow_step3=Arrow(eqns_step2.get_bottom(),eqns_step2.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step3=VGroupCustom(
            TexEqn("2x+y-z=8",isolate=pattern),
            TexEqn(R"\frac{1}{2}y+\frac{1}{2}z=1",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=eqns_step0.reference_eqn
            ).arrange(DOWN).next_to(arrow_step3,DOWN).align_eqns()
        labels_step3=get_labels_to(eqns_step3)
        note_step3=VGroup(
            Textch("第三步"),
            Textch("归一化"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step3_insert=VGroup(
            labels_step2[2].copy().next_to(note_step3[1],RIGHT,buff=0.1),
            )
        note_step3.add(note_step3_insert)
        note_step3.next_to(arrow_step3,LEFT,buff=3,aligned_edge=UP).align_to(note_step2,LEFT)
        underline_step3=Underline(note_step3[0],stroke_color=YELLOW)
        operations3=Tex(R"\frac{1}{-1}\cdot(3)",font_size=30).next_to(arrow_step3,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step3=SurroundingRectangle(operations3[frac_patn],stroke_width=2,buff=REC_BUFF)
        numerator3,frac_symbol3,denominator3=self.extract_fraction_parts(operations3,frac_patn)
        back_rec3=SurroundingRectangle(VGroup(eqns_step3,labels_step3),
            stroke_color=WHITE,stroke_opacity=1,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        eqns_step3[0].set_opacity(0.5)
        labels_step3[0].set_opacity(0.5)
        eqns_step3[1].set_opacity(0.5)
        labels_step3[1].set_opacity(0.5)
        self.play(frame.animate.reorient(0, 0, 0, (0.0, -11.7, 0.0), 8),
            GrowArrow(arrow_step3),ShowCreation(back_rec3))
        self.play(FadeIn(note_step3[0],shift=RIGHT),ShowCreation(underline_step3))
        self.play(FadeIn(note_step3[1:],shift=RIGHT))
        self.play(
            TransformFromCopy(eqns_step2[0],eqns_step3[0]),
            TransformFromCopy(eqns_step2[1],eqns_step3[1]),
            TransformFromCopy(labels_step2[0],labels_step3[0]),
            TransformFromCopy(labels_step2[1],labels_step3[1]),
            )
        self.play(FlashAround(eqns_step2[2]),run_time=2)
        self.play(FlashAround(eqns_step2[2][0]),run_time=1)
        self.play(eqns_step2[2][0].animate.next_to(eqns_step2[2][3],LEFT)\
            .set_anim_args(rate_func=there_and_back,path_arc=PI/2),run_time=2)
        self.wait()
        self.play(TransformFromCopy(labels_step2[2],operations3["(3)"][0]),
            FadeIn(operations3[R"\cdot"][0]),FadeIn(frac_symbol3),
                FadeIn(numerator3))
        self.play(ShowCreation(recs_step3))
        self.wait()
        self.play(TransformFromCopy(eqns_step2[2]["-"],denominator3))
        self.play(star_anims(operations3,eqns_step3[2],labels_step3[2]))
        self.wait()

        # step3_2
        arrow_step3_2=Arrow(eqns_step3.get_bottom(),eqns_step3.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step3_2=VGroupCustom(
            TexEqn("2x+y=7",isolate=pattern),
            TexEqn(R"\frac{1}{2}y=\frac{3}{2}",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN).next_to(arrow_step3_2,DOWN).align_eqns()
        labels_step3_2=get_labels_to(eqns_step3_2)
        note_step3_2=VGroup(
            Textch("用方程"),
            Textch("消去它上面的"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step3_2_insert=VGroup(
            labels_step3[2].copy().next_to(note_step3_2[0],RIGHT,buff=0.1),
            Tex("z").next_to(note_step3_2[1],RIGHT,buff=0.1),
            )
        note_step3_2.add(note_step3_2_insert)
        note_step3_2.next_to(arrow_step3_2,LEFT,buff=3,aligned_edge=UP).align_to(note_step3,LEFT)
        operations3_2=VGroup(
            Tex(R"(2)-\frac{1}{2}(3)",font_size=30).next_to(arrow_step3_2,RIGHT),
            Tex(R"(1)--1(3)",font_size=30).next_to(arrow_step3_2,RIGHT),
        ).arrange(DOWN,aligned_edge=LEFT).next_to(arrow_step3_2,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step3_2=VGroup(
            SurroundingRectangle(operations3_2[0][frac_patn],stroke_width=2,buff=REC_BUFF),
            SurroundingRectangle(operations3_2[1]["-1"],stroke_width=2,buff=REC_BUFF),
            )
        numerator3_2,frac_symbol3_2,denominator3_2=self.extract_fraction_parts(operations3_2[0],frac_patn)
        back_rec3_2=SurroundingRectangle(VGroup(eqns_step3_2,labels_step3_2),
            stroke_color=WHITE,stroke_opacity=1,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step3_2,eqns_step3_2,labels_step3_2,note_step3_2,operations3_2,
        #     recs_step3_2,back_rec3_2)
        self.play(
            frame.animate.reorient(0, 0, 0, (0, -15.88, 0.0), 8.00),
            GrowArrow(arrow_step3_2),ShowCreation(back_rec3_2))
        self.play(FadeIn(note_step3_2[0],shift=RIGHT),
            FadeIn(note_step3_2_insert[0],shift=RIGHT)
            )
        self.play(FadeIn(note_step3_2[1],shift=RIGHT),
            FadeIn(note_step3_2_insert[1],shift=RIGHT)
            )
        # add rec
        rec_to_top=SurroundingRectangle(eqns_step3[2],fill_opacity=0.2,fill_color=RED,stroke_color=RED)
        tilt_line_0=Line(stroke_color=RED).match_width(eqns_step3[0]["-z"]).rotate(-PI/4).move_to(eqns_step3[0]["-z"])
        tilt_line_1=Line(stroke_color=RED).match_width(eqns_step3[1][R"+\frac{1}{2}z"]).rotate(-PI/4).move_to(eqns_step3[1][R"+\frac{1}{2}z"])
        self.play(FadeIn(rec_to_top))
        self.play(ReplacementTransform(rec_to_top,tilt_line_0),
            TransformFromCopy(rec_to_top,tilt_line_1),
            eqns_step3[0].animate.set_opacity(1),
            labels_step3[0].animate.set_opacity(1),
            eqns_step3[1].animate.set_opacity(1),
            labels_step3[1].animate.set_opacity(1),
            )
        self.wait()
        self.play(FadeOut(tilt_line_0),FadeOut(tilt_line_1))
        self.play(
            TransformFromCopy(eqns_step3[2],eqns_step3_2[2]),
            TransformFromCopy(labels_step3[2],labels_step3_2[2]),
            )
        self.play(LaggedStart(
            TransformFromCopy(labels_step3[1],operations3_2[0]["(2)"][0]),
            FadeIn(operations3_2[0]["-"][0]),
            ShowCreation(recs_step3_2[0]),
            TransformFromCopy(labels_step3[2],operations3_2[0]["(3)"][0]),
            lag_ratio=0.5))
        self.wait()
        self.play(TransformFromCopy(eqns_step3[1][5:8],operations3_2[0][R"\frac{1}{2}"][0]),)
        self.play(star_anims(operations3_2[0],eqns_step3_2[1],labels_step3_2[1]))
        self.play(LaggedStart(
            TransformFromCopy(labels_step3[0],operations3_2[1]["(1)"][0]),
            FadeIn(operations3_2[1]["-"][0]),
            ShowCreation(recs_step3_2[1]),
            TransformFromCopy(labels_step3[2],operations3_2[1]["(3)"][0]),
            lag_ratio=0.5))
        self.play(TransformFromCopy(eqns_step3[0]["-"][0],operations3_2[1]["-1"][0]),)
        self.play(star_anims(operations3_2[1],eqns_step3_2[0],labels_step3_2[0]))
        self.wait()

        # step4
        arrow_step4=Arrow(eqns_step3_2.get_bottom(),eqns_step3_2.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step4=VGroupCustom(
            TexEqn("2x+y=7",isolate=pattern),
            TexEqn("y=3",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN).next_to(arrow_step4,DOWN).align_eqns()
        labels_step4=get_labels_to(eqns_step4)
        note_step4=VGroup(
            Textch("第四步"),
            Textch("归一化"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step4_insert=VGroup(
            labels_step3_2[1].copy().next_to(note_step4[1],RIGHT,buff=0.1),
            )
        note_step4.add(note_step4_insert)
        note_step4.next_to(arrow_step4,LEFT,buff=3,aligned_edge=UP).align_to(note_step2,LEFT)
        underline_step4=Underline(note_step4[0],stroke_color=YELLOW)
        operations4=Tex(R"\frac{1}{1/2}\cdot(2)",font_size=30).next_to(arrow_step4,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step4=SurroundingRectangle(operations4[frac_patn],stroke_width=2,buff=REC_BUFF)
        numerator4,frac_symbol4,denominator4=self.extract_fraction_parts(operations4,frac_patn)
        back_rec4=SurroundingRectangle(VGroup(eqns_step4,labels_step4),
            stroke_color=WHITE,stroke_opacity=1,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step4,eqns_step4,labels_step4)
        # self.add(note_step4,underline_step4,operations4,recs_step4,back_rec4)
        self.play(frame.animate.reorient(0, 0, 0, (0.0, -20.6, 0.0), 8),
            GrowArrow(arrow_step4),ShowCreation(back_rec4),
            FadeIn(note_step4[0],shift=RIGHT),ShowCreation(underline_step4)
            )
        self.play(FadeIn(note_step4[1:],shift=RIGHT))
        self.play(
            TransformFromCopy(eqns_step3_2[0],eqns_step4[0]),
            TransformFromCopy(eqns_step3_2[2],eqns_step4[2]),
            TransformFromCopy(labels_step3_2[0],labels_step4[0]),
            TransformFromCopy(labels_step3_2[2],labels_step4[2]),
            )
        self.play(TransformFromCopy(labels_step3_2[1],operations4["(2)"][0]),
            FadeIn(operations3[R"\cdot"][0]),FadeIn(frac_symbol4),
                FadeIn(numerator4))
        self.play(ShowCreation(recs_step4))
        self.wait()
        self.play(TransformFromCopy(eqns_step3_2[1][R"\frac{1}{2}"][0],denominator4))
        self.play(star_anims(operations4,eqns_step4[1],labels_step4[1]))
        self.wait()

        # step4_2
        arrow_step4_2=Arrow(eqns_step4.get_bottom(),eqns_step4.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step4_2=VGroupCustom(
            TexEqn("2x=4",isolate=pattern),
            TexEqn("y=3",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN).next_to(arrow_step4_2,DOWN).align_eqns()
        labels_step4_2=get_labels_to(eqns_step4_2)
        note_step4_2=VGroup(
            Textch("用方程"),
            Textch("消去它上面的"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step4_2_insert=VGroup(
            labels_step4[1].copy().next_to(note_step4_2[0],RIGHT,buff=0.1),
            Tex("y").next_to(note_step4_2[1],RIGHT,buff=0.1),
            )
        note_step4_2.add(note_step4_2_insert)
        note_step4_2.next_to(arrow_step4_2,LEFT,buff=3,aligned_edge=UP).align_to(note_step3,LEFT)
        operations4_2=Tex(R"(1)-\frac{1}{1}\,\,(2)",font_size=35).next_to(arrow_step3_2,RIGHT)\
            .next_to(arrow_step4_2,RIGHT)
        back_rec4_2=SurroundingRectangle(VGroup(eqns_step4_2,labels_step4_2),
            stroke_color=WHITE,stroke_opacity=1,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step4_2,eqns_step4_2,labels_step4_2,note_step4_2,operations4_2,
        #     recs_step4_2,back_rec4_2)
        self.play(frame.animate.reorient(0, 0, 0, (0, -24.5, 0.0), 8.00),
            GrowArrow(arrow_step4_2),ShowCreation(back_rec4_2),
            FadeIn(note_step4_2[0],shift=RIGHT),
            FadeIn(note_step4_2_insert[0],shift=RIGHT))
        self.play(FadeIn(note_step4_2[1],shift=RIGHT),
            FadeIn(note_step4_2_insert[1],shift=RIGHT)
            )
        self.wait()
        # add tilt line
        rec_to_top=SurroundingRectangle(eqns_step4[1],fill_opacity=0.2,fill_color=RED,stroke_color=RED)
        tilt_line=Line(stroke_color=RED).match_width(eqns_step4[0]["+y"]).rotate(-PI/4).move_to(eqns_step4[0]["+y"])
        rec_4_2=SurroundingRectangle(operations4_2[frac_patn])
        num4_2,frac_4_2,den4_2=self.extract_fraction_parts(operations4_2,frac_patn)
        ghost_eqns=VGroupCustom(
                TexEqn(r"2x+1y=7",isolate=pattern),
                TexEqn(r"1y=3",isolate=pattern),
                TexEqn(r"z=-1",isolate=pattern),
                reference_eqn=refer
            ).arrange(DOWN).next_to(arrow_step4,DOWN).align_eqns()
        self.play(FadeIn(rec_to_top))
        self.play(ReplacementTransform(rec_to_top,tilt_line))
        self.play(FadeOut(tilt_line))
        self.play(
            TransformFromCopy(eqns_step4[1],eqns_step4_2[1]),
            TransformFromCopy(labels_step4[1],labels_step4_2[1]),
            TransformFromCopy(eqns_step4[2],eqns_step4_2[2]),
            TransformFromCopy(labels_step4[2],labels_step4_2[2]),
            )
        self.play(
            LaggedStart(
            TransformFromCopy(labels_step4[0],operations4_2["(1)"][0]),
            Write(operations4_2[3]),
            ShowCreation(rec_4_2),
            Write(frac_4_2),
            TransformFromCopy(labels_step4[1],operations4_2["(2)"][0]),
            lag_ratio=0.3))
        self.play(
            ReplacementTransform(ghost_eqns[0]["1"],num4_2,path_arc=PI/2),
            ReplacementTransform(ghost_eqns[1]["1"],den4_2,path_arc=PI/2),
            )
        self.play(star_anims(operations4_2,eqns_step4_2[0],labels_step4_2[0]))

        # step5
        arrow_step5=Arrow(eqns_step4_2.get_bottom(),eqns_step4_2.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step5=VGroupCustom(
            TexEqn("x=2",isolate=pattern),
            TexEqn("y=3",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN).next_to(arrow_step5,DOWN).align_eqns()
        labels_step5=get_labels_to(eqns_step5)
        note_step5=VGroup(
            Textch("第五步"),
            Textch("归一化"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step5_insert=VGroup(
            labels_step5[0].copy().next_to(note_step5[1],RIGHT,buff=0.1),
            )
        note_step5.add(note_step5_insert)
        note_step5.next_to(arrow_step5,LEFT,buff=3,aligned_edge=UP).align_to(note_step2,LEFT)
        underline_step5=Underline(note_step5[0],stroke_color=YELLOW)
        operations5=Tex(R"\frac{1}{2}\cdot(1)",font_size=30).next_to(arrow_step5,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step5=SurroundingRectangle(operations5[frac_patn],stroke_width=2,buff=REC_BUFF)
        numerator5,frac_symbol5,denominator5=self.extract_fraction_parts(operations5,frac_patn)
        back_rec5=SurroundingRectangle(VGroup(eqns_step5,labels_step5),
            stroke_color=WHITE,stroke_opacity=1,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step4,eqns_step4,labels_step4)
        # self.add(note_step4,underline_step4,operations4,recs_step4,back_rec4)
        self.play(frame.animate.reorient(0, 0, 0, (0.0, -28.5, 0.0), 8),
            GrowArrow(arrow_step5),ShowCreation(back_rec5),
            FadeIn(note_step5[0],shift=RIGHT),ShowCreation(underline_step5)
            )
        self.play(FadeIn(note_step5[1:],shift=RIGHT))
        self.play(
            TransformFromCopy(eqns_step4_2[1],eqns_step5[1]),
            TransformFromCopy(eqns_step4_2[2],eqns_step5[2]),
            TransformFromCopy(labels_step4_2[1],labels_step5[1]),
            TransformFromCopy(labels_step4_2[2],labels_step5[2]),
            )
        self.play(TransformFromCopy(labels_step4_2[0],operations5["(1)"][0]),
            FadeIn(operations5[R"\cdot"][0]),FadeIn(frac_symbol5),
            FadeIn(numerator5),ShowCreation(recs_step5))
        self.play(TransformFromCopy(eqns_step4_2[0][0],denominator5[0]))
        self.play(star_anims(operations5,eqns_step5[0],labels_step5[0]))
        self.wait()
        # align variables
        eqns_step5.save_state()
        self.play(
            eqns_step5[0][0].animate.match_x(eqns_step5[2][0]),
            eqns_step5[1][0].animate.match_x(eqns_step5[2][0]),
            )
        self.wait()
        self.play(eqns_step5.animate.restore())

        # show gaussian jordan elimination
        big_br2=Brace(VGroup(eqns_step5,eqns_step0,gaussian),LEFT,buff=0.8)
        jordan=TextCustom(en="Gauss–Jordan Elimination",ch="高斯-若尔当消元",
            font_size_ch=200,font_size_en=200,buff=1)
        big_br2.put_at_tip(jordan)
        self.play(frame.animate.reorient(0, 0, 0, (-8.53, -14.74, 0.0), 35.05),
            eqns_step0.animate.set_opacity(1),
            labels_step0.animate.set_opacity(1),
            eqns_step1.animate.set_opacity(1),
            labels_step1.animate.set_opacity(1),
            eqns_step2.animate.set_opacity(1),
            labels_step2.animate.set_opacity(1),
            )
        self.play(LaggedStartMap(FadeIn,
            VGroup(big_br2,jordan),shift=RIGHT*2,lag_ratio=0.02))
        self.wait()
        # link to part3
        rec=get_current_frame_rectangle(frame)
        rec.set_fill(BLACK,0.8)
        title3=Textch("Part3:高斯消元的矩阵形式",t2f={"Part3:":"Mongolian Baiti"})
        title3.scale(10).move_to(frame.get_center())
        title3_use=title3.copy().set_color_by_gradient(RED,WHITE)
        self.play(FadeIn(rec),
            FadeIn(title3["Part3:"],time_span=[1,2],shift=RIGHT*2),
            FadeIn(title3["高斯消元的矩阵形式"],time_span=[1,2],shift=LEFT*2),
            run_time=2)
        self.play(Write(title3_use))
        self.wait()
        self.remove(title3)
        self.play(FadeOut(rec),
            FadeOut(title3_use["Part3:"],time_span=[0,1],shift=LEFT*2),
            FadeOut(title3_use["高斯消元的矩阵形式"],time_span=[0,1],shift=RIGHT*2),
            run_time=2)

        # let frame go to original position
        self.play(frame.animate.reorient(0, 0, 0, (0.15, -1.45, 0.0), 7.21)
            ,run_time=2)

        # go to right board
        SHIFT=10.5
        eqn_matrix=eqns_step0.copy().shift(RIGHT*SHIFT)
        labels_eqn_matrix=labels_step0.copy().shift(RIGHT*SHIFT)
        # self.add(eqn_matrix,labels_eqn_matrix)
        self.play(TransformFromCopy(eqns_step0,eqn_matrix),
            TransformFromCopy(labels_step0,labels_eqn_matrix),
            frame.animate.match_x(eqn_matrix),
            run_time=2)

        # write notes
        s1=SurroundingRectangle(VGroup(eqn_matrix,labels_eqn_matrix))
        ar_s1=ArrowCustom().point_to(s1.get_corner(DL),PI/4).set_color(YELLOW)
        text_original=Textch("原始方程组").move_to(ar_s1.get_start())\
        .shift(-ar_s1.get_vector()*0.5)
        text_redifine=Textch("用矩阵的形式\n重新定义这个方程组").move_to(ar_s1.get_start())\
        .shift(-ar_s1.get_vector()*0.8)
        # self.add(s1,ar_s1)
        # self.add(text_original)
        self.play(ShowCreation(s1),GrowArrow(ar_s1),FadeIn(text_original))
        self.wait()
        self.play(FadeOut(text_original,shift=RIGHT),
            FadeIn(text_redifine,shift=RIGHT))
        self.wait()

        # you may ask why??
        kun=Kun().next_to(text_redifine,RIGHT).shift(DOWN)
        bubble=Bubble(Textch("为什么非要写成矩阵形式？")).pin_to(kun.right_eye)
        self.play(FadeIn(kun,shift=LEFT))
        self.play(LaggedStart(
            kun.animate.look_at(bubble).shock(),
            ShowCreation(bubble),lag_ratio=0.3
            ))
        self.wait()
        self.play(FadeOut(bubble,shift=LEFT+DOWN),kun.animate.peace().look_at(eqns_step0))

        # go through steps
        eqns_steps = [eqns_step1, eqns_step2, eqns_step3, eqns_step3_2, 
                      eqns_step4, eqns_step4_2, eqns_step5]
        self.wait()
        self.play(frame.animate.scale(1.6).move_to(eqns_step0).shift(DOWN*3),
            kun.animate.next_to(eqns_step0,buff=1) )
        self.play(LaggedStart(*self.process_equations(eqns_step0, refer, pattern)),
            kun.animate.look([-1,-0.2,0]),run_time=1)
        TIME=20
        DISTANCE1=frame.get_top()[1]-eqns_step5.get_bottom()[1]
        DISTANCE2=DISTANCE1+10
        VELOCITY1=DISTANCE1/TIME
        VELOCITY2=DISTANCE2/TIME
        def updater1(mob,dt):
            if mob.get_y()>eqns_step4_2.get_y():
                mob.shift(DOWN*VELOCITY1*dt)
        def updater2(mob,dt):
            if mob.get_y()>eqns_step5.get_y():
                mob.shift(DOWN*VELOCITY2*dt)
        frame.add_updater(updater1)
        kun.add_updater(updater2)
        self.play_equation_steps(frame, kun, eqns_steps, refer, pattern,time=TIME)
        frame.clear_updaters()
        kun.clear_updaters()
        self.play(kun.animate.close_eyes().set_anim_args(rate_func=there_and_back))
        self.wait()
        self.remove(kun)

        # go back
        frame.reorient(0, 0, 0, (10.26, -1.73, 0.0), 7.15)
        s1_change=SurroundingRectangle(VGroup(eqn_matrix[0],labels_eqn_matrix[0]),buff=0.15)
        ar_s1_change=ArrowCustom().point_to(s1_change.get_left()).set_color(YELLOW)
        rec_x=SurroundingRectangle(VGroup(*[eqn_matrix[i]["x"] for i in range(3)]))
        rec_y=SurroundingRectangle(VGroup(*[eqn_matrix[i]["y"] for i in range(3)]))
        rec_z=SurroundingRectangle(VGroup(*[eqn_matrix[i]["z"] for i in range(3)]))
        # rec_x.set_stroke(TEAL_A,1)
        # rec_y.set_stroke(YELLOW_A,1)
        # rec_z.set_stroke(RED_A,1)
        text_parse=Textch("需要额外解析").next_to(rec_y,DOWN).match_y(text_redifine)
        text_parse.set_color(YELLOW_B)
        ar_x=Arrow(text_parse.get_corner(UL),rec_x).set_color(YELLOW_A)
        ar_y=ArrowCustom(start=text_parse.get_top(),end=rec_y).set_color(YELLOW_A)
        ar_z=Arrow(text_parse.get_corner(UR),rec_z).set_color(YELLOW_A)
        self.wait()
        self.play(
            ReplacementTransform(VGroup(s1.copy(),s1,s1.copy()),VGroup(rec_x,rec_y,rec_z)),
            ReplacementTransform(VGroup(ar_s1.copy(),ar_s1,ar_s1.copy()),VGroup(ar_x,ar_y,ar_z)),
            ReplacementTransform(text_redifine,text_parse),
            run_time=1.5)
        self.wait()
        self.play(LaggedStart(
            FadeOut(VGroup(rec_x,ar_x),shift=LEFT),
            FadeOut(VGroup(rec_z,ar_z),shift=RIGHT),
            FadeOut(text_parse,shift=DOWN)),
            Transform(rec_y,s1_change),Transform(ar_y,ar_s1_change),
            VGroup(eqn_matrix[1:],labels_eqn_matrix[1:]).animate.set_opacity(0.5))
        self.wait()

        # funcs
        def generate_dot_product(equation: str,vertical=False):
            x_coef, y_coef, z_coef, rhs_value = self.parse_equation(equation)
            dot_m1 = Matrix(np.array([[x_coef, y_coef, z_coef]]))  # 系数矩阵
            dot_sign = Tex(R"\cdot")  # 点积符号
            if vertical == False:
                dot_m2 = Matrix(np.array([["x", "y", "z"]]), element_alignment_corner=UP)  # 变量矩阵
            else:
                dot_m2 = Matrix(np.array([["x"], ["y"], ["z"]]), element_alignment_corner=UP)  # 变量矩阵
            equal_sign = Tex("=")  # 等号
            rhs = Tex(rhs_value)  # 右侧常数项
            dot_eqn = VGroup(dot_m1, dot_sign, dot_m2, equal_sign, rhs).arrange(RIGHT)
            return dot_eqn
        
        # to_dot_product
        faded_eqn=TexEqn("2x+1y-1z=8",isolate=pattern).align_eqn(eqn_matrix[0]).match_y(eqn_matrix[0])
        dot_eqns=VGroup(
            generate_dot_product(eqn_matrix[0].string,False), 
            generate_dot_product(eqn_matrix[1].string,False), 
            generate_dot_product(eqn_matrix[2].string,False), 
            ).arrange(DOWN,aligned_edge=LEFT,buff=0.3) 
        dot_eqns.next_to(eqn_matrix,DOWN)
        labels_dot_eqns=get_labels_to(dot_eqns,buff=1)
        rhs_ptn=re.compile(r"(?<==)[+-]?\d+")
        # self.add(dot_eqns)
        # self.add(labels_dot_eqns)
        self.play(FadeIn(faded_eqn[3]),FadeIn(faded_eqn[6]))
        self.play(LaggedStart(
            TransformFromCopy(eqn_matrix[0][0],dot_eqns[0][0][0][0]),
            ReplacementTransform(faded_eqn[3],dot_eqns[0][0][1][0]),
            TransformFromCopy(eqn_matrix[0][4],dot_eqns[0][0][2][0]),
            ReplacementTransform(faded_eqn[6],dot_eqns[0][0][2][1]),
            FadeIn(dot_eqns[0][0].brackets),
            lag_ratio=0.1,
            ))
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(eqn_matrix[0]["x"][0][0],dot_eqns[0][2][0][0]),
            TransformFromCopy(eqn_matrix[0]["y"][0][0],dot_eqns[0][2][1][0]),
            TransformFromCopy(eqn_matrix[0]["z"][0][0],dot_eqns[0][2][2][0]),
            FadeIn(dot_eqns[0][2].brackets),
            lag_ratio=0.1,
            ))
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(eqn_matrix[0]["="][0][0],dot_eqns[0][3][0]),
            TransformFromCopy(eqn_matrix[0][rhs_ptn][0][0],dot_eqns[0][4][0]),
            FadeIn(labels_dot_eqns[0],shift=LEFT),
            lag_ratio=0.1,
            ))
        self.wait()
        self.play(LaggedStart(
            ar_y.animate.point_to(dot_eqns[0][1],angle=PI/2),
            Write(dot_eqns[0][1],stroke_color=RED),
            lag_ratio=0.2,))

        # write dot product
        text_dot_pr=Textch("点积")
        ar_y.put_to_start(text_dot_pr)
        self.play(ReplacementTransform(VectorizedPoint(dot_eqns[0][1].get_center()),text_dot_pr))
        s1_dot=SurroundingRectangle(VGroup(dot_eqns[0],labels_dot_eqns[0]))
        ar_s1_dot=ar_y.copy().point_to(s1_dot.get_left(),angle=0)
        self.wait()
        self.play(FadeOut(text_dot_pr),
            ar_y.animate.point_to(rec_y.get_left(),angle=0),
            ShowCreation(s1_dot),FadeIn(ar_s1_dot))
        
        # show how we define
        def get_connected_line_pairs(eqn1,eqn2):
            grp=VGroup()
            variables_ptn=re.compile("x|y|z")
            variables=eqn1[variables_ptn]
            coeffi_ptn=re.compile(r"([+-]?\d+|[+-]|[+-]?\\frac{\d+}{\d+})(?=[xyz])")
            coeffi=eqn1[coeffi_ptn]
            for i in range(3):
                grp.add(VGroup(
                Line(coeffi[i].get_bottom(),eqn2[0][i].get_top()),
                Line(variables[i].get_bottom(),eqn2[2][i].get_top())
                ))
            grp.add(VGroup(
                Line(eqn1["="].get_bottom(),eqn2[3].get_top()),
                Line(eqn1[rhs_ptn].get_bottom(),eqn2[4].get_top())
                ))
            grp.set_color(TEAL)
            return grp
        def pairs_animation(pairs):
            self.add(pairs[0])
            self.wait()
            for i in range(3):
                self.remove(pairs[i])
                self.add(pairs[i+1])
                self.wait()
            self.remove(pairs[-1])
            
        # pair anims
        ar_s1=ar_y
        s1=rec_y
        pairs=get_connected_line_pairs(eqn_matrix[0],dot_eqns[0])
        pairs_animation(pairs)
        
        s2=SurroundingRectangle(VGroup(eqn_matrix[1],labels_eqn_matrix[1]))
        ar_s2=ArrowCustom().point_to(s2.get_left()).set_color(YELLOW)
        s2_dot=SurroundingRectangle(VGroup(dot_eqns[1],labels_dot_eqns[1]))
        ar_s2_dot=ArrowCustom().point_to(s2_dot.get_left()).set_color(YELLOW)
        pairs2=get_connected_line_pairs(eqn_matrix[1],dot_eqns[1])
        self.play(
            VGroup(eqn_matrix[0],labels_eqn_matrix[0]).animate.set_opacity(0.5),
            VGroup(dot_eqns[0],labels_dot_eqns[0]).animate.set_opacity(0.5),
            VGroup(eqn_matrix[1],labels_eqn_matrix[1]).animate.set_opacity(1),
            FadeIn(VGroup(dot_eqns[1],labels_dot_eqns[1])),
            Transform(s1,s2),
            Transform(s1_dot,s2_dot),
            Transform(ar_s1,ar_s2),
            Transform(ar_s1_dot,ar_s2_dot),
            )
        pairs_animation(pairs2)

        s3=SurroundingRectangle(VGroup(eqn_matrix[2],labels_eqn_matrix[2]))
        ar_s3=ArrowCustom().point_to(s3.get_left()).set_color(YELLOW)
        s3_dot=SurroundingRectangle(VGroup(dot_eqns[2],labels_dot_eqns[2]))
        ar_s3_dot=ArrowCustom().point_to(s3_dot.get_left()).set_color(YELLOW)
        pairs3=get_connected_line_pairs(eqn_matrix[2],dot_eqns[2])
        self.play(
            VGroup(eqn_matrix[1],labels_eqn_matrix[1]).animate.set_opacity(0.5),
            VGroup(dot_eqns[1],labels_dot_eqns[1]).animate.set_opacity(0.5),
            VGroup(eqn_matrix[2],labels_eqn_matrix[2]).animate.set_opacity(1),
            FadeIn(VGroup(dot_eqns[2],labels_dot_eqns[2])),
            Transform(s1,s3),
            Transform(s1_dot,s3_dot),
            Transform(ar_s1,ar_s3),
            Transform(ar_s1_dot,ar_s3_dot),
            )
        pairs_animation(pairs3)
        
        # big rec
        s4=SurroundingRectangle(VGroup(eqn_matrix,labels_eqn_matrix))
        ar_s4=ArrowCustom().point_to(s4.get_left()).set_color(YELLOW)
        s4_dot=SurroundingRectangle(VGroup(dot_eqns,labels_dot_eqns))
        ar_s4_dot=ArrowCustom().point_to(s4_dot.get_left()).set_color(YELLOW)
        self.play(
            eqn_matrix.animate.set_opacity(0.5),
            labels_eqn_matrix.animate.set_opacity(0.5),
            dot_eqns.animate.set_opacity(1),
            labels_dot_eqns.animate.set_opacity(1),
            Transform(s1,s4),
            Transform(s1_dot,s4_dot),
            Transform(ar_s1,ar_s4),
            Transform(ar_s1_dot,ar_s4_dot),
            )
        self.wait()
        self.play(*map(FadeOut,VGroup(s1,s1_dot,ar_s1,ar_s1_dot,labels_dot_eqns)))
        
        # show matrix mutiplication
        matrix_lhs1=Matrix(np.array([[2,1,-1],[-3,-1,2],[-2,1,2]]))
        dot_sign=Tex(R"\cdot")
        matrix_lhs2_middle1=Matrix(np.array([["x","y","z"],["x","y","z"],["x","y","z"]]),element_alignment_corner=ORIGIN)
        matrix_equal=Tex("=").scale(1.3)
        matrix_rhs=Matrix(np.array([[8],[-11],[-3]]))
        matrix_grp_middle1=VGroup(matrix_lhs1,dot_sign,matrix_lhs2_middle1,matrix_equal,matrix_rhs).arrange(RIGHT)
        matrix_grp_middle1.move_to(dot_eqns)
        left_br1=VGroup()
        left_br2=VGroup()
        right_br1=VGroup()
        right_br2=VGroup()
        elems1=VGroup()
        elems2=VGroup()
        cdots=VGroup()
        equals=VGroup()
        rhss=VGroup()
        for i in range(3):
            left_br1.add(dot_eqns[i][0].brackets[0])
            right_br1.add(dot_eqns[i][0].brackets[1])
            left_br2.add(dot_eqns[i][2].brackets[0])
            right_br2.add(dot_eqns[i][2].brackets[1])
            elems1.add(*dot_eqns[i][0].elements)
            elems2.add(*dot_eqns[i][2].elements)
            cdots.add(dot_eqns[i][1])
            equals.add(dot_eqns[i][3])
            rhss.add(dot_eqns[i][4])

        self.play(LaggedStart(
            FadeTransform(left_br1,matrix_lhs1.brackets[0]),
            ReplacementTransform(elems1,VGroup(*matrix_lhs1.elements)),
            FadeTransform(right_br1,matrix_lhs1.brackets[1]),lag_ratio=0.1
            ))
        self.play(FadeTransform(cdots,dot_sign))
        self.play(LaggedStart(
            FadeTransform(left_br2,matrix_lhs2_middle1.brackets[0]),
            ReplacementTransform(elems2,VGroup(*matrix_lhs2_middle1.elements)),
            FadeTransform(right_br2,matrix_lhs2_middle1.brackets[1]),lag_ratio=0.1
            ))
        self.play(FadeTransform(equals,matrix_equal))
        self.play(LaggedStart(
            FadeIn(matrix_rhs.brackets[0]),
            ReplacementTransform(rhss,VGroup(*matrix_rhs.elements)),
            FadeIn(matrix_rhs.brackets[1]),lag_ratio=0.1
            ))
        self.wait()
        # middle step2
        matrix_lhs2_middle2=Matrix(np.array([["x","y","z"]]),element_alignment_corner=ORIGIN)
        matrix_lhs2=Matrix(np.array([["x"],["y"],["z"]]))
        matrix_lhs2_middle2.move_to(matrix_lhs2_middle1)
        matrix_lhs2.move_to(matrix_lhs2_middle1)
        x_elems=matrix_lhs2_middle1.get_column(0)
        y_elems=matrix_lhs2_middle1.get_column(1)
        z_elems=matrix_lhs2_middle1.get_column(2)
        self.play(LaggedStart(
            AnimationGroup(
            ReplacementTransform(x_elems[0],matrix_lhs2_middle2[0]),
            ReplacementTransform(x_elems[1],matrix_lhs2_middle2[0]),
            ReplacementTransform(x_elems[2],matrix_lhs2_middle2[0]),),
            AnimationGroup(
            ReplacementTransform(y_elems[0],matrix_lhs2_middle2[1]),
            ReplacementTransform(y_elems[1],matrix_lhs2_middle2[1]),
            ReplacementTransform(y_elems[2],matrix_lhs2_middle2[1]),),
            AnimationGroup(
            ReplacementTransform(z_elems[0],matrix_lhs2_middle2[2]),
            ReplacementTransform(z_elems[1],matrix_lhs2_middle2[2]),
            ReplacementTransform(z_elems[2],matrix_lhs2_middle2[2]),),
            lag_ratio=0.4))
        self.wait()
        self.play(LaggedStart(
            AnimationGroup(
            ReplacementTransform(matrix_lhs2_middle2[0],matrix_lhs2[0]),
            ReplacementTransform(matrix_lhs2_middle2[1],matrix_lhs2[1]),
            ReplacementTransform(matrix_lhs2_middle2[2],matrix_lhs2[2]),),
            AnimationGroup(
            ReplacementTransform(matrix_lhs2_middle1.brackets[0],matrix_lhs2.brackets[0]),
            ReplacementTransform(matrix_lhs2_middle1.brackets[1],matrix_lhs2.brackets[1]),),
            lag_ratio=0.1))
        self.wait()
        matrix_Grp=VGroup(matrix_lhs1,matrix_lhs2,matrix_equal,matrix_rhs)
        self.play(FlashAround(dot_sign))
        self.play(FadeOut(dot_sign))
        self.play(matrix_Grp.animate.arrange(RIGHT).next_to(eqn_matrix,DOWN))
        self.wait()
        
        # this is matrix mutiplication
        arrow_to_up=Arrow(matrix_lhs1.get_left(),eqn_matrix.get_left(),path_arc=-PI*4/5)
        text_matrix_multi=Textch("矩阵乘法")
        text_matrix_multi.next_to(arrow_to_up,LEFT)
        def get_matrix_rectangle_pairs(matrix,vector,b,eqns):
            grp=VGroup()
            rows=len(matrix_lhs1.rows)
            columns=len(matrix_lhs1.columns)
            for j in range(columns):
                rs=get_eqn_rectangles(eqns[j])
                for i in range(rows):
                    r1=SurroundingRectangle(matrix.mob_matrix[j][i])
                    r2=SurroundingRectangle(vector.mob_matrix[i][0])
                    line1=Line(r1.get_corner(UL),rs[i].get_corner(DL)).set_color(YELLOW)
                    line2=Line(r2.get_corner(UR),rs[i].get_corner(DR)).set_color(YELLOW)
                    grp.add(VGroup(r1,r2,rs[i],line1,line2))
                r=SurroundingRectangle(b.mob_matrix[j][0])
                line1=Line(r.get_top(),rs[-1].get_bottom()).set_color(YELLOW)
                grp.add(VGroup(r,rs[-1],line1))
            return grp
        def matrix_rects_animation(rects,wait_time=0.5):
            self.add(rects[0])
            for old_rect, new_rect in zip(rects, rects[1:]):
                self.wait(wait_time)
                self.add(new_rect)
                self.remove(old_rect)
            self.wait(wait_time)
            self.remove(rects[-1])
        def get_eqn_rectangles(eqn):
            grp=VGroup()
            ptn=re.compile(r"[+-]?\d*[xyz]")
            ptn_rhs=re.compile(r"(?<==)([+-]?\d+)")
            for part in eqn[ptn]:
                grp.add(SurroundingRectangle(part))
            grp.add(SurroundingRectangle(eqn[ptn_rhs]))
            return grp


        rects=get_matrix_rectangle_pairs(matrix_lhs1,matrix_lhs2,matrix_rhs,eqn_matrix)
        self.play(GrowArrow(arrow_to_up),
            FadeIn(text_matrix_multi,shift=RIGHT),)
        matrix_rects_animation(rects)

        # step1 matrix elimination
        XCOORD=9
        def generate_mobmatrix(eqns, augmented=False,**kwargs):
            aug_matrix = []  
            for eqn in eqns:
                coef1, coef2, coef3, coef_rhs = self.parse_equation(eqn.string)
                aug_matrix.append([coef1, coef2, coef3, coef_rhs])
            
            aug_matrix = np.array(aug_matrix)
            if augmented:
                return MatrixAug(aug_matrix,**kwargs)  
            else :
                lhs1=Matrix(aug_matrix[:, :-1],**kwargs)
                lhs2=Matrix(np.array([["x"],["y"],["z"]]),**kwargs).match_height(lhs1)
                equal=Tex("=").scale(1.3)
                rhs=Matrix(aug_matrix[:,-1],**kwargs).match_height(lhs1)
                return VGroup(lhs1,lhs2,equal,rhs).arrange(RIGHT)  
        
        matrix_step1=generate_mobmatrix(eqns_step1,element_alignment_corner=ORIGIN)
        matrix_step2=generate_mobmatrix(eqns_step2,element_alignment_corner=ORIGIN)
        matrix_step3=generate_mobmatrix(eqns_step3,augmented=True,element_alignment_corner=ORIGIN)
        matrix_step3_2=generate_mobmatrix(eqns_step3_2,augmented=True,element_alignment_corner=ORIGIN)
        matrix_step4=generate_mobmatrix(eqns_step4,augmented=True,element_alignment_corner=ORIGIN)
        matrix_step4_2=generate_mobmatrix(eqns_step4_2,augmented=True,element_alignment_corner=ORIGIN)
        matrix_step5=generate_mobmatrix(eqns_step5,augmented=True,element_alignment_corner=ORIGIN)
        right_matrices=VGroup(matrix_Grp,matrix_step1,matrix_step2,matrix_step3,matrix_step3_2,
            matrix_step4,matrix_step4_2,matrix_step5)
        left_recs=VGroup(back_rec0,back_rec1,back_rec2,back_rec3,back_rec3_2,back_rec4,back_rec4_2,back_rec5)
        right_rects=left_recs.copy()
        for i in range(len(right_rects)):
            right_rects[i].set_stroke(WHITE,DEFAULT_STROKE_WIDTH,1)
        left_eqns=VGroup(eqns_step0,eqns_step1,eqns_step2,eqns_step3,eqns_step3_2,eqns_step4,eqns_step4_2,eqns_step5)
        right_rects.set_x(XCOORD)
        right_arrows=VGroup()
        for i in range(len(right_rects)-1):
            y1=right_rects[i].get_bottom()[1]
            y2=right_rects[i+1].get_top()[1]
            length=y1-y2
            ar=ArrowCustom(right_rects[i].get_bottom(),angle=-PI/2,length=length,buff=0.1)
            right_arrows.add(ar)

        for matrix,matrix_left in zip(right_matrices[1:],left_eqns[1:]):
            matrix.match_y(matrix_left)
            matrix.match_height(matrix_left)
            matrix.set_x(XCOORD)
        self.play(LaggedStart(
            LaggedStartMap(FadeOut,VGroup(arrow_to_up,text_matrix_multi,eqn_matrix,
            labels_eqn_matrix),shift=UP),
            matrix_Grp.animate.match_y(left_eqns[0]).match_height(left_eqns[0]).set_x(XCOORD),
            lag_ratio=0.2))
        # write step1 note
        NOTE_BUFF=4
        note_step1_right=VGroup(
            Textch("第一步"),
            Textch("寻找第一行的主元",t2c={"主元":YELLOW}),
            Textch("将主元之下的元素消为0",t2c={"主元":YELLOW,"0":YELLOW},t2f={"0":"Mongolian Baiti"}),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step1_right.next_to(right_arrows[0],RIGHT,buff=NOTE_BUFF)
        note_step1_right_line=Underline(note_step1_right[0],stroke_color=YELLOW).reverse_points()
        note_step1_right[1]["找"].set_fill(WHITE,1,0)
        note_step1_right[2]["为"].set_fill(WHITE,1,0)

        self.play(
            frame.animate.reorient(0, 0, 0, (12.18, -2.32, 0.0), 7.98),
            FadeIn(note_step1_right[0],shift=LEFT*2),
            ShowCreation(note_step1_right_line),
            ShowCreation(right_rects[0]),
            GrowArrow(right_arrows[0]),
            ShowCreation(right_rects[1])
            )
        self.play(FadeIn(note_step1_right[1],shift=LEFT*2),)
        self.wait()
        self.play(FadeIn(note_step1_right[2],shift=LEFT*2),)
        self.wait()
        
        # what is pivot
        content_whatispivot=Textch("什么是主元？",t2c={"主元":RED})
        kun.fix_in_frame()
        kun.to_corner(DL,buff=0.1)
        kun.look(ORIGIN).peace()
        bubble_whatispivot=Bubble(content_whatispivot).pin_to(kun.right_eye)
        bubble_whatispivot.fix_in_frame()
        self.play(FadeIn(kun,shift=RIGHT))
        self.play(Write(bubble_whatispivot),
            kun.animate.look_at(bubble_whatispivot))
        self.play(kun.animate.close_eyes().set_anim_args(rate_func=there_and_back))
        self.wait()
        self.play(FadeOut(bubble_whatispivot))
        
        # explain what is pivot
        arr=np.array([[1,2,3],[0,4,5],[0,0,6],[0,0,0]])
        ma=Matrix(arr).next_to(note_step1_right,RIGHT,buff=6)
        rec_0=SurroundingRectangle(ma.mob_matrix[0][0])
        rec_1=SurroundingRectangle(ma.mob_matrix[1][0])
        rec_2=SurroundingRectangle(ma.mob_matrix[2][0])
        rec_3=SurroundingRectangle(ma.mob_matrix[3][0])
        arrow_0=ArrowCustom().point_to(ma.get_row(0).get_left(),buff=0.6).set_color(YELLOW)
        arrow_1=ArrowCustom().point_to(ma.get_row(1).get_left(),buff=0.6).set_color(YELLOW)
        arrow_2=ArrowCustom().point_to(ma.get_row(2).get_left(),buff=0.6).set_color(YELLOW)
        arrow_3=ArrowCustom().point_to(ma.get_row(3).get_left(),buff=0.6).set_color(YELLOW)
        text_pivot_0=Textch("第一行的主元")
        text_pivot_1=Textch("第二行的主元")
        text_pivot_2=Textch("第三行的主元")
        text_pivot_3=Textch("第四行没有主元")
        arrow_t0=ArrowCustom().point_from(ma.get_row(0).get_right(),buff=0.6).set_color(YELLOW)
        arrow_t1=ArrowCustom().point_from(ma.get_row(1).get_right(),buff=0.6).set_color(YELLOW)
        arrow_t2=ArrowCustom().point_from(ma.get_row(2).get_right(),buff=0.6).set_color(YELLOW)
        arrow_t3=ArrowCustom().point_from(ma.get_row(3).get_right(),buff=0.6).set_color(YELLOW)
        text_pivot_0.next_to(arrow_t0,RIGHT)
        text_pivot_1.next_to(arrow_t1,RIGHT)
        text_pivot_2.next_to(arrow_t2,RIGHT)
        text_pivot_3.next_to(arrow_t3,RIGHT)
        self.add(ma)
        self.play(frame.animate.move_to(ma))
        self.play(GrowArrow(arrow_0),ShowCreation(rec_0))
        self.play(Transform(arrow_0,arrow_t0),FadeIn(text_pivot_0))

        self.play(Transform(arrow_0,arrow_1),ShowCreation(rec_1))
        self.play(arrow_0.animate.next_to(ma.mob_matrix[1][1],LEFT),rec_1.animate.move_to(ma.mob_matrix[1][1]))
        self.play(Transform(arrow_0,arrow_t1),FadeIn(text_pivot_1),
        kun.animate.close_eyes().set_anim_args(rate_func=there_and_back))

        self.play(Transform(arrow_0,arrow_2),ShowCreation(rec_2))
        self.play(arrow_0.animate.next_to(ma.mob_matrix[2][1],LEFT),rec_2.animate.move_to(ma.mob_matrix[2][1]))
        self.play(arrow_0.animate.next_to(ma.mob_matrix[2][2],LEFT),rec_2.animate.move_to(ma.mob_matrix[2][2]))
        self.play(Transform(arrow_0,arrow_t2),FadeIn(text_pivot_2))

        self.play(Transform(arrow_0,arrow_3),ShowCreation(rec_3))
        self.play(arrow_0.animate.next_to(ma.mob_matrix[3][1],LEFT),rec_3.animate.move_to(ma.mob_matrix[3][1]))
        self.play(arrow_0.animate.next_to(ma.mob_matrix[3][2],LEFT),rec_3.animate.move_to(ma.mob_matrix[3][2]))
        self.play(Transform(arrow_0,arrow_t3),FadeIn(text_pivot_3),FadeOut(rec_3,shift=RIGHT))
        self.play(kun.animate.close_eyes().smile().set_anim_args(rate_func=there_and_back))
        self.wait()
        self.remove(kun,ma,text_pivot_0,text_pivot_1,text_pivot_2,text_pivot_3,
            arrow_0,rec_0,rec_1,rec_2)
        frame.reorient(0, 0, 0, (12.09, -2.49, 0.0), 7.92)
        # but this is not the formal definition
        # kun_yellow=YellowChicken().fix_in_frame().to_corner(DR,buff=0.1)
        # content_thisisnot=Textch("这个定义大致是对的",t2c={"大致":RED})
        # rec=SurroundingRectangle(VGroup(ma,text_pivot_0,text_pivot_1,text_pivot_2,text_pivot_3),stroke_color=RED)
        # bubble_right=Bubble(content_thisisnot).flip().pin_to(kun_yellow.left_eye).fix_in_frame()
        # self.play(FadeIn(kun_yellow,shift=LEFT),FadeOut(arrow_0),
        #     kun.animate.look_at(kun_yellow),frame.animate.shift(RIGHT*2))
        # self.play(kun_yellow.animate.look_at(kun),
        #     Write(bubble_right),frame.animate.reorient(0, 0, 0, (31.08, -3.83, 0.0), 8.90),
        #     ShowCreation(rec))
        # self.play(kun.animate.close_eyes().set_anim_args(rate_func=there_and_back))
        # self.play(kun_yellow.animate.close_eyes().set_anim_args(rate_func=there_and_back))
        # content2=Textch("这个矩阵必须在行阶梯形式下",t2c={"行阶梯形":YELLOW},t2s={"这个矩阵":ITALIC})
        # bubble_right2=Bubble(content2).flip().pin_to(kun_yellow.left_eye).fix_in_frame()
        # self.remove(bubble_right) 
        # self.play(Write(bubble_right2)) 
        # self.play(TransformFromCopy(ma,content2["这个矩阵"][0]),run_time=2)      
        # self.play(TransformFromCopy(content2["这个矩阵"][0],ma),run_time=1)
        # content_row_echlon=Textch("什么是行阶梯形？")
        # bubble_left=Bubble(content_row_echlon).pin_to(kun.right_eye).fix_in_frame()
        # self.play(FadeOut(bubble_right2),Write(bubble_left),kun.animate.shock()) 
        
        # content_youwillsee=Textch("你会在之后视频后面看到")
        # bubble_right3=Bubble(content_youwillsee).flip().pin_to(kun_yellow.left_eye).fix_in_frame()
        # self.wait()
        # self.play(FadeOut(bubble_left),kun.animate.peace(),
        #     kun_yellow.animate.raise_hand(),Write(bubble_right3))
        # self.wait()
        # kun.unfix_from_frame()
        # kun_yellow.unfix_from_frame()
        # self.remove(kun,kun_yellow,bubble_right3,rec,ma,rec_0,rec_1,rec_2,text_pivot_0,text_pivot_1,text_pivot_2,text_pivot_3)
        

        # move back to matrix elimination
        rec_pivot0_aug0=SurroundingRectangle(matrix_Grp[0].mob_matrix[0][0])
        rec_pivot0_aug1=SurroundingRectangle(matrix_step1[0].mob_matrix[0][0])
        operations1_right=VGroup(
            Tex(R"r2-\frac{-3}{2}\,\,r1",font_size=30),
            Tex(R"r3-\frac{-2}{2}\,\,r1",font_size=30),
            ).arrange(DOWN).next_to(right_arrows[0],RIGHT)
        frac_patn_right=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step1_right=VGroup(
            SurroundingRectangle(operations1_right[0][frac_patn],stroke_width=2,buff=REC_BUFF),
            SurroundingRectangle(operations1_right[1][frac_patn],stroke_width=2,buff=REC_BUFF),
            )
        numerator1_step00_right,frac_symbol1_step00_right,denominator1_step00_right=self.extract_fraction_parts(operations1_right[0],frac_patn)
        numerator1_step01_right,frac_symbol1_step01_right,denominator1_step01_right=self.extract_fraction_parts(operations1_right[1],frac_patn)
        text_row=TextCustom(en="row",ch="行",direction=RIGHT,buff=0.1,
            en_config={"t2c":{"r":RED}}).scale(1.5)
        text_row.next_to(right_rects[0],RIGHT,buff=1)
        ar=ArrowCustom().point_to(rec_pivot0_aug0.get_left()).set_color(YELLOW)
        s1=SurroundingRectangle(VGroup(
            matrix_Grp[0].get_row(0),
            matrix_Grp[3].mob_matrix[0][0]))
        s1.set_stroke(RED,2,1).set_fill(RED,0.2)
        tilt1=Line(stroke_color=RED).match_width(matrix_Grp[0].mob_matrix[1][0])\
                .rotate(-PI/4).move_to(matrix_Grp[0].mob_matrix[1][0])
        tilt2=Line(stroke_color=RED).match_width(matrix_Grp[0].mob_matrix[2][0])\
                .rotate(-PI/4).move_to(matrix_Grp[0].mob_matrix[2][0])
        self.wait()
        self.play(GrowArrow(ar),ShowCreation(rec_pivot0_aug0))
        self.wait()
        self.play(ShowCreation(s1),FadeOut(ar),)
        self.play(
            TransformFromCopy(s1,tilt1),
            ReplacementTransform(s1,tilt2),
            )
        self.play(FadeOut(tilt1),FadeOut(tilt2))
        self.wait()
        self.play(TransformFromCopy(
            VGroup(right_matrices[0][0].brackets,right_matrices[0][1],right_matrices[0][2],right_matrices[0][3].brackets),
            VGroup(right_matrices[1][0].brackets,right_matrices[1][1],right_matrices[1][2],right_matrices[1][3].brackets),
            ))
        self.play(TransformFromCopy(
            VGroup(rec_pivot0_aug0,right_matrices[0][0].get_row(0),right_matrices[0][3].get_row(0)),
            VGroup(rec_pivot0_aug1,right_matrices[1][0].get_row(0),right_matrices[1][3].get_row(0)),
            ))
        self.wait()
        self.play(Write(operations1_right[0]["r2-"]))
        self.play(ShowCreation(recs_step1_right[0]))
        self.play(Write(operations1_right[0]["r1"]))
        
        # show row
        self.play(Write(text_row))
        self.play(LaggedStart(
            *[TransformFromCopy(text_row.en["r"],operations1_right[j]["r"][i]) for i in [0,-1] for j in range(1)],
            *[operations1_right[j]["r"][i].animate.set_color(RED).set_anim_args(rate_func=there_and_back) for i in [0,-1] for j in range(1)],
            FadeOut(text_row),lag_ratio=0.2),run_time=2)
        self.wait()
        self.play(ShowCreation(frac_symbol1_step00_right),
            LaggedStart(
            TransformFromCopy(right_matrices[0][0].mob_matrix[1][0],numerator1_step00_right,path_arc=PI/2),
            TransformFromCopy(right_matrices[0][0].mob_matrix[0][0],denominator1_step00_right,path_arc=PI/2),
            lag_ratio=0.2,),run_time=2)
        COLORS=itertools.cycle([RED,BLUE,GREEN,TEAL])
        self.play(LaggedStart(
            *[TransformFromCopy(Dot(operations1_right[0].get_center(),fill_color=next(COLORS)),right_matrices[1][0].mob_matrix[1][i],) for i in range(3)],
            TransformFromCopy(Dot(operations1_right[0].get_center(),fill_color=next(COLORS)),right_matrices[1][3].get_row(1),),
            lag_ratio=0.1),run_time=2)
        self.play(Write(operations1_right[1]["r3-"]))
        self.play(ShowCreation(recs_step1_right[1]))
        self.play(Write(operations1_right[1]["r1"]))
        self.play(ShowCreation(frac_symbol1_step01_right),
            LaggedStart(
            TransformFromCopy(right_matrices[0][0].mob_matrix[2][0],numerator1_step01_right,path_arc=PI/2),
            TransformFromCopy(right_matrices[0][0].mob_matrix[0][0],denominator1_step01_right,path_arc=PI/2),
            lag_ratio=0.2,),run_time=2)
        self.play(LaggedStart(
            *[TransformFromCopy(Dot(operations1_right[1].get_center(),fill_color=next(COLORS)),right_matrices[1][0].mob_matrix[2][i],) for i in range(3)],
            TransformFromCopy(Dot(operations1_right[1].get_center(),fill_color=next(COLORS)),right_matrices[1][3].get_row(2),),
            lag_ratio=0.1),run_time=2)
        
        # compare with left eqns
        ghost_eqn_left_step1=VGroupCustom(
            Tex("2x+1y-1z=8",isolate=pattern),
            Tex(R"0x+\frac{1}{2}y+\frac{1}{2}z=1",isolate=pattern),
            Tex("0x+2y+1z=5",isolate=pattern),
            reference_eqn=eqns_step0.reference_eqn
            ).arrange(DOWN).next_to(arrow_step1,DOWN).align_eqns()
        ghost_eqn_left_step0=VGroupCustom(
            Tex("2x+1y-1z=8",isolate=pattern),
            Tex(R"-3x-1y+2z=-11",isolate=pattern),
            Tex("-2x+1y+2z=-3",isolate=pattern),
            reference_eqn=eqns_step0.reference_eqn
            ).arrange(DOWN).move_to(eqns_step0).align_eqns()
        coeffi_ptn=[
            re.compile(r"([-]?\d+|[-]|[-]?\\frac{\d+}{\d+})(?=x)"),
            re.compile(r"([-]?\d+|[-]|[-]?\\frac{\d+}{\d+})(?=y)"),
            re.compile(r"([-]?\d+|[-]|[-]?\\frac{\d+}{\d+})(?=z)")]
        # compare0.scale(1.5).stretch(2,0)
        # self.add(compare0)
        b1=back_rec0.copy().set_color(TEAL)
        b2=right_rects[0].copy().set_color(TEAL)
        lrar=Tex(r"\Leftrightarrow").set_color(TEAL).match_y(b1)
        lrar.scale(2)
        lrar.move_to((b1.get_right()+b2.get_left())/2)
        def updater(mob):
            mob.match_y(b1)
        self.play(frame.animate.reorient(0, 0, 0, (4.8, -2.58, 0.0), 8.83))
        self.play(ShowCreation(b1),ShowCreation(b2),
            FadeIn(lrar),
            run_time=2)
        lrar.add_updater(updater)
        self.play(
            LaggedStart(
            *[AnimationGroup(*[
              TransformFromCopy(right_matrices[0][0].mob_matrix[i][j],
              ghost_eqn_left_step0[i][coeffi_ptn[j]],path_arc=PI/3)
            for i in range(3)]) for j in range(3)],
            AnimationGroup(*[TransformFromCopy(right_matrices[0][3].mob_matrix[i][0],
              ghost_eqn_left_step0[i][-1],path_arc=PI/3)
            for i in range(3)]),
            lag_ratio=0.1))
        self.play(LaggedStart(
            AnimationGroup(*[ReplacementTransform(ghost_eqn_left_step0[i][-1],
              right_matrices[0][3].mob_matrix[i][0],path_arc=-PI/3)
            for i in range(3)]),
            *[AnimationGroup(*[
              ReplacementTransform(ghost_eqn_left_step0[i][coeffi_ptn[j]],
              right_matrices[0][0].mob_matrix[i][j],path_arc=-PI/3)
            for i in range(3)]) for j in range(2, -1, -1)],
            lag_ratio=0.1) )
        self.wait()
        self.play(
            b1.animate.surround(VGroup(operations)),
            b2.animate.surround(VGroup(operations1_right)),
            )
        self.wait()
        self.play(
            b1.animate.replace(back_rec1,stretch=True),
            b2.animate.replace(right_rects[1],stretch=True),
            )
        self.wait()
        self.play(
            LaggedStart(
            *[AnimationGroup(*[
              TransformFromCopy(right_matrices[1][0].mob_matrix[i][j],
              ghost_eqn_left_step1[i][coeffi_ptn[j]],path_arc=PI/3)
            for i in range(3)]) for j in range(3)],
            AnimationGroup(*[TransformFromCopy(right_matrices[1][3].mob_matrix[i][0],
              ghost_eqn_left_step1[i][-1],path_arc=PI/3)
            for i in range(3)]),
            lag_ratio=0.1))
        self.play(LaggedStart(
            AnimationGroup(*[ReplacementTransform(ghost_eqn_left_step1[i][-1],
              right_matrices[1][3].mob_matrix[i][0],path_arc=-PI/3)
            for i in range(3)]),
            *[AnimationGroup(*[
              ReplacementTransform(ghost_eqn_left_step1[i][coeffi_ptn[j]],
              right_matrices[1][0].mob_matrix[i][j],path_arc=-PI/3)
            for i in range(3)]) for j in range(2, -1, -1)],
            lag_ratio=0.1) )
        self.play(FadeOut(b1),FadeOut(b2),FadeOut(lrar))
        self.wait()
        
        # notice sth not change and throw
        def move_to_frame_corner(mob,direction,buff:float=0.3):
            mob.move_to(self.frame.get_corner(direction))
            shift_vec=mob.get_center()-mob.get_corner(direction)
            mob.shift(shift_vec)
            mob.shift(-direction*buff)
        self.play(frame.animate.reorient(0, 0, 0, (12.67, -2.41, 0.0), 8.83))
        self.play(TransformFromCopy(VGroup(right_matrices[0][1:3]),
            VGroup(right_matrices[1][1:3]),rate_func=there_and_back),run_time=5)
        trashcan=TrashCan()
        move_to_frame_corner(trashcan,DR,buff=0.7)
        self.play(FadeIn(trashcan,shift=LEFT))
        self.play(trashcan.animate.open(PI/4))
        self.play(
            ThrowTo(VGroup(right_matrices[0][1:3]),trashcan.body),
            ThrowTo(VGroup(right_matrices[1][1:3]),trashcan.body),
                )
        self.play(trashcan.animate.open(-PI/4))
        self.play(LaggedStartMap(FadeOut,
            VGroup(trashcan,right_matrices[0][1:3],right_matrices[1][1:3]),
            shift=RIGHT,lag_ratio=0))
        self.wait()
        
        # become augmented matrix
        aug0=generate_mobmatrix(eqns_step0,True,element_alignment_corner=ORIGIN)
        def align_right_matrix(matrix,eqn_left):
            matrix.match_y(eqn_left)
            matrix.match_height(eqn_left,stretch=False)
            matrix.set_x(XCOORD)
        align_right_matrix(aug0,eqns_step0)
        self.play(FadeTransform(matrix_Grp[0].brackets[1],aug0.line),
            FadeTransform(matrix_Grp[3].brackets[0],aug0.line),)
        self.play(
            ReplacementTransform(matrix_Grp[0].brackets[0], aug0.brackets[0]),
            ReplacementTransform(matrix_Grp[3].brackets[1], aug0.brackets[1]),
            *[
                ReplacementTransform(a, b)
                for a, b in zip(
                    itertools .chain.from_iterable([row for row in matrix_Grp[0].mob_matrix]), 
                    itertools .chain.from_iterable([row[:-1] for row in aug0.mob_matrix])
                )
            ],
            *[ReplacementTransform(*matrix_Grp[3].mob_matrix[i],aug0.mob_matrix[i][3]) for i in range(3)],
            rec_pivot0_aug0.animate.move_to(aug0.mob_matrix[0][0])
        )
        aug1=generate_mobmatrix(eqns_step1,True,element_alignment_corner=ORIGIN)
        align_right_matrix(aug1,eqns_step1)
        self.play(FadeTransform(right_matrices[1][0].brackets[1],aug1.line),
            FadeTransform(right_matrices[1][3].brackets[0],aug1.line),)
        self.play(
            ReplacementTransform(right_matrices[1][0].brackets[0], aug1.brackets[0]),
            ReplacementTransform(right_matrices[1][3].brackets[1], aug1.brackets[1]),
            *[
                ReplacementTransform(a, b)
                for a, b in zip(
                    itertools .chain.from_iterable([row for row in right_matrices[1][0].mob_matrix]), 
                    itertools .chain.from_iterable([row[:-1] for row in aug1.mob_matrix])
                )
            ],
            *[ReplacementTransform(*right_matrices[1][3].mob_matrix[i],aug1.mob_matrix[i][3]) for i in range(3)],
            rec_pivot0_aug1.animate.move_to(aug1.mob_matrix[0][0])
        )
        
        # called augmented matrix
        text_aug=TextCustom(ch="增广矩阵",en="Augmented Matrix",
            direction=DOWN,buff=0.1,aligned_edge=LEFT).scale(1.5)
        text_aug.next_to(right_rects[0],RIGHT,buff=1)
        rec_text_aug=SurroundingRectangle(text_aug,stroke_color=WHITE,stroke_width=2,buff=0.2)
        tempen=text_aug.en.copy().set_submobject_colors_by_gradient(TEAL_A,GREEN_D)
        tempch=text_aug.ch.copy().set_submobject_colors_by_gradient(TEAL_A,GREEN_D)
        self.play(
            LaggedStart(
            TransformFromCopy(right_rects[0],rec_text_aug),
            TransformFromCopy(right_rects[1],rec_text_aug),
            FadeIn(text_aug),
            Write(tempen.sort(lambda p:abs(p[0]-text_aug.en.get_center()[0]))),
            Write(tempch.sort(lambda p:abs(p[0]-text_aug.en.get_center()[0]))),
            lag_ratio=0.05
            ))
        self.play(
            TransformFromCopy(rec_text_aug,right_rects[0]),
            ReplacementTransform(rec_text_aug,right_rects[1]),
            FadeOut(tempen,shift=LEFT*2),
            FadeOut(tempch,shift=LEFT*2),
            FadeOut(text_aug,shift=LEFT*2),
            aug0.sort().animate.set_submobject_colors_by_gradient(GREEN_D,TEAL_A),
            aug1.sort().animate.set_submobject_colors_by_gradient(GREEN_D,TEAL_A),
            )
        self.wait()
        
        # step2
        aug2=generate_mobmatrix(eqns_step2,True,element_alignment_corner=ORIGIN)
        align_right_matrix(aug2,eqns_step2)
        note_step2_right=VGroup(
            Textch("第二步"),
            Textch("寻找第二行的主元",t2c={"主元":YELLOW}),
            Textch("将主元之下的元素消为0",t2c={"主元":YELLOW,"0":YELLOW},t2f={"0":"Mongolian Baiti"}),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step2_right.next_to(right_arrows[1],RIGHT,buff=NOTE_BUFF)
        note_step2_right_line=Underline(note_step2_right[0],stroke_color=YELLOW).reverse_points()
        note_step2_right[1]["找"].set_fill(WHITE,1,0)
        note_step2_right[2]["为"].set_fill(WHITE,1,0)
        rec_pivot1_aug1=SurroundingRectangle(aug1.mob_matrix[1][0])
        arrow_pivot=ArrowCustom(fill_color=YELLOW).point_to(rec_pivot1_aug1.get_left())
        self.play(FadeIn(note_step2_right,shift=LEFT*2),
            ShowCreation(note_step2_right_line),
            frame.animate.reorient(0, 0, 0, (12.67, -6.95, 0.0), 8.83),
            GrowArrow(right_arrows[1]),
            ShowCreation(right_rects[2]))
        self.wait()
        self.play(GrowArrow(arrow_pivot),ShowCreation(rec_pivot1_aug1))
        arrow_pivot.f_always.point_to(rec_pivot1_aug1.get_left)
        self.play(rec_pivot1_aug1.animate.surround(aug1.mob_matrix[1][1]))
        self.play(FadeOut(arrow_pivot))
        self.wait()
        
        # step2 to step3
        rec_pivot0_aug2=SurroundingRectangle(aug2.mob_matrix[0][0])
        rec_pivot1_aug2=SurroundingRectangle(aug2.mob_matrix[1][1])
        operation_aug_step2=Tex(R"r3-\frac{2}{1/2}\,\,r2",font_size=30)\
                    .next_to(right_arrows[1],RIGHT)
        rec_step2_frac=SurroundingRectangle(operation_aug_step2[frac_patn],
            stroke_width=2,buff=REC_BUFF)
        numer,frac,denom=self.extract_fraction_parts(operation_aug_step2,frac_patn)
        self.play(
            TransformFromCopy(aug1.brackets,aug2.brackets),
            TransformFromCopy(aug1.line,aug2.line),
            TransformFromCopy(aug1.get_row(0),aug2.get_row(0)),
            TransformFromCopy(aug1.get_row(1),aug2.get_row(1)),
            TransformFromCopy(rec_pivot0_aug1,rec_pivot0_aug2),
            TransformFromCopy(rec_pivot1_aug1,rec_pivot1_aug2),
            )
        self.play(Write(operation_aug_step2["r3-"]))
        self.play(ShowCreation(rec_step2_frac))
        self.play(Write(operation_aug_step2["r2"]),Write(frac))
        self.play(LaggedStart(
            TransformFromCopy(aug1.mob_matrix[1][1],denom,path_arc=PI/2),
            TransformFromCopy(aug1.mob_matrix[2][1],numer,path_arc=PI/2),
            lag_ratio=0.7),run_time=2)
        self.play(LaggedStart(*[TransformFromCopy(
            Dot(operation_aug_step2.get_center(),fill_color=next(COLORS)),
            aug2.mob_matrix[2][i],) for i in range(4)],lag_ratio=0.1))
        self.wait()
        
        # step3
        note_step3_right=VGroup(
            Textch("第三步"),
            Textch("寻找第三行的主元",t2c={"主元":YELLOW}),
            Textch("将主元之下的元素消为0",t2c={"主元":YELLOW,"0":YELLOW},t2f={"0":"Mongolian Baiti"}),
            Textch("归一化第三行",),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step3_right.next_to(right_arrows[2],RIGHT,buff=NOTE_BUFF)
        note_step3_right_line=Underline(note_step3_right[0],stroke_color=YELLOW).reverse_points()
        note_step3_right[1]["找"].set_fill(WHITE,1,0)
        note_step3_right[2]["为"].set_fill(WHITE,1,0)
        rec_pivot2_aug2=SurroundingRectangle(aug2.mob_matrix[2][0])
        arrow_pivot=ArrowCustom(fill_color=YELLOW).point_to(rec_pivot2_aug2.get_left())
        operation=Tex(R"\frac{1}{-1}\,\,r3",font_size=30).next_to(right_arrows[2],RIGHT)
        oper_rec=SurroundingRectangle(operation[0:4])
        self.play(
            frame.animate.reorient(0, 0, 0, (12.67, -11.8, 0.0), 8.83),
            GrowArrow(right_arrows[2]),
            ShowCreation(right_rects[3]),)
        self.play(LaggedStart(
            FadeIn(note_step3_right[0],shift=LEFT*2),
            ShowCreation(note_step3_right_line),
            FadeIn(note_step3_right[1:3],shift=LEFT*2),
            ))
        self.play(GrowArrow(arrow_pivot),ShowCreation(rec_pivot2_aug2))
        arrow_pivot.f_always.point_to(rec_pivot2_aug2.get_left)
        self.play(rec_pivot2_aug2.animate.surround(aug2.mob_matrix[2][1]))
        self.play(rec_pivot2_aug2.animate.surround(aug2.mob_matrix[2][2]))
        self.play(FadeOut(arrow_pivot))
        self.wait()

        # create aug3
        aug3=generate_mobmatrix(eqns_step3,True,element_alignment_corner=ORIGIN)
        align_right_matrix(aug3,eqns_step3)
        rec_pivot0_aug3=SurroundingRectangle(aug3.mob_matrix[0][0])
        rec_pivot1_aug3=SurroundingRectangle(aug3.mob_matrix[1][1])
        rec_pivot2_aug3=SurroundingRectangle(aug3.mob_matrix[2][2])
        cross_line=Line().insert_n_curves(20).set_stroke(RED,[3,6,3]).replace(note_step3_right[2],stretch=True)
        copied_aug2=VGroup(aug2,rec_pivot0_aug2,rec_pivot1_aug2,rec_pivot2_aug2).copy().match_y(aug3)
        self.play(ShowCreation(cross_line))
        self.wait()
        self.play(FadeIn(note_step3_right[3],shift=RIGHT))
        self.play(TransformFromCopy(VGroup(aug2,rec_pivot0_aug2,rec_pivot1_aug2,rec_pivot2_aug2),copied_aug2))
        self.wait()
        strip=self.get_rec(aug3,2)
        self.play(FadeIn(strip,shift=RIGHT))
        self.play(ReplacementTransform(copied_aug2,VGroup(aug3,rec_pivot0_aug3,rec_pivot1_aug3,rec_pivot2_aug3)))
        self.play(ReplacementTransform(strip,oper_rec),Write(operation))
        self.wait()

        # compare and back substitute
        aug3_2=generate_mobmatrix(eqns_step3_2,True,element_alignment_corner=ORIGIN)
        align_right_matrix(aug3_2,eqns_step3_2)
        note_step3_2_right=VGroup(
            Textch("用第三个主元所在行",t2c={"主元":YELLOW}),
            Textch("将它之上的元素消为0",t2f={"0":"Mongolian Baiti"}),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step3_2_right.next_to(right_arrows[3],RIGHT,buff=NOTE_BUFF)
        note_step3_2_right[1]["为"].set_fill(WHITE,1,0)
        operation1=Tex(R"r2-\frac{1}{2}\,\,r3",font_size=30)
        operation2=Tex(R"r1--1\,\,r3",font_size=30)
        operations=VGroup(operation1,operation2).arrange(DOWN).next_to(right_arrows[3],RIGHT)
        rec_operation1=SurroundingRectangle(operation1[frac_patn],stroke_width=2,buff=REC_BUFF)
        rec_operation2=SurroundingRectangle(operation2["-1"],stroke_width=2,buff=REC_BUFF)
        rec_pivot0_aug3_2=SurroundingRectangle(aug3_2.mob_matrix[0][0])
        rec_pivot1_aug3_2=SurroundingRectangle(aug3_2.mob_matrix[1][1])
        rec_pivot2_aug3_2=SurroundingRectangle(aug3_2.mob_matrix[2][2])
        self.play(frame.animate.reorient(0, 0, 0, (6.39, -12.98, 0.0), 14.86),)
        self.play(LaggedStart(
            GrowArrow(right_arrows[3]),
            ShowCreation(right_rects[4]),lag_ratio=0.2),
            LaggedStart(
            FadeIn(note_step3_2_right[0]),
            FadeIn(note_step3_2_right[1]),lag_ratio=0.2))
        # add left right arrow(lrar)
        b1.replace(VGroup(back_rec3,back_rec3_2),stretch=True)
        b2.replace(VGroup(right_rects[3],right_rects[4]),stretch=True)
        self.play(ShowCreation(b1),ShowCreation(b2),FadeIn(lrar))
        
        self.play(TransformFromCopy(aug3.brackets,aug3_2.brackets),
            TransformFromCopy(aug3.line,aug3_2.line),
            TransformFromCopy(aug3.get_row(2),aug3_2.get_row(2)),
            # TransformFromCopy(aug3.mob_matrix[0][0],aug3_2.mob_matrix[0][0]),
            # TransformFromCopy(aug3.mob_matrix[1][0],aug3_2.mob_matrix[1][0]),
            # TransformFromCopy(aug3.mob_matrix[1][1],aug3_2.mob_matrix[1][1]),
            # TransformFromCopy(rec_pivot0_aug3,rec_pivot0_aug3_2),
            # TransformFromCopy(rec_pivot1_aug3,rec_pivot1_aug3_2),
            TransformFromCopy(rec_pivot2_aug3,rec_pivot2_aug3_2),
            )
        self.play(LaggedStart(
            Write(operation1["r2-"]),
            ShowCreation(rec_operation1),
            Write(operation1["r3"]),
            TransformFromCopy(aug3.mob_matrix[1][1],operation1[frac_patn]),
            lag_ratio=.5))
        self.play(LaggedStart(*[TransformFromCopy(
            Dot(operation1.get_center(),fill_color=next(COLORS)),
            aug3_2.mob_matrix[1][i],) for i in range(4)],
            ShowCreation(rec_pivot1_aug3_2),
            lag_ratio=0.1))
        self.play(LaggedStart(
            Write(operation2["r1-"]),
            ShowCreation(rec_operation2),
            Write(operation2["r3"]),
            TransformFromCopy(aug3.mob_matrix[0][2],operation2["-1"]),
            lag_ratio=.5))
        self.play(LaggedStart(*[TransformFromCopy(
            Dot(operation2.get_center(),fill_color=next(COLORS)),
            aug3_2.mob_matrix[0][i],) for i in range(4)],
            ShowCreation(rec_pivot0_aug3_2),
            lag_ratio=0.1))
        self.wait()
        
        # aug4
        aug4=generate_mobmatrix(eqns_step4,True,element_alignment_corner=ORIGIN)
        align_right_matrix(aug4,eqns_step4)
        note_step4_right=VGroup(
            Textch("第四步"),
            Textch("归一化第二个主元",t2c={"主元":YELLOW}),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step4_right.next_to(right_arrows[4],RIGHT,buff=NOTE_BUFF)
        underline_step4_right=Underline(note_step4_right[0],stroke_color=YELLOW).reverse_points()
        operation1=Tex(R"\frac{1}{1/2}\,\,r3",font_size=30)
        operation1.next_to(right_arrows[4],RIGHT)
        nu,frac,den=self.extract_fraction_parts(operation1,frac_patn)
        rec_operation1=SurroundingRectangle(operation1[frac_patn],stroke_width=2,buff=REC_BUFF)
        rec_pivot0_aug4=SurroundingRectangle(aug4.mob_matrix[0][0])
        rec_pivot1_aug4=SurroundingRectangle(aug4.mob_matrix[1][1])
        rec_pivot2_aug4=SurroundingRectangle(aug4.mob_matrix[2][2])
        self.play(frame.animate.reorient(0, 0, 0, (6.39, -17, 0.0), 14.86),)
        self.play(LaggedStart(
            GrowArrow(right_arrows[4]),
            ShowCreation(right_rects[5]),
            lag_ratio=0.2),
            LaggedStart(
            FadeIn(note_step4_right[0]),
            ShowCreation(underline_step4_right),
            FadeIn(note_step4_right[1]),
            b1.animate.replace(VGroup(back_rec4,back_rec3_2),stretch=True),
            b2.animate.replace(VGroup(right_rects[5],right_rects[4]),stretch=True),
            lag_ratio=0.2),)
        self.play(TransformFromCopy(aug3_2.brackets,aug4.brackets),
            TransformFromCopy(aug3_2.line,aug4.line),
            TransformFromCopy(aug3_2.get_row(0),aug4.get_row(0)),
            TransformFromCopy(aug3_2.get_row(2),aug4.get_row(2)),
            TransformFromCopy(aug3_2.mob_matrix[0][0],aug4.mob_matrix[0][0]),
            TransformFromCopy(rec_pivot0_aug3_2,rec_pivot0_aug4),
            TransformFromCopy(rec_pivot2_aug3_2,rec_pivot2_aug4),
            )
        self.play(LaggedStart(
            Write(nu),Write(frac),
            ShowCreation(rec_operation1),
            Write(operation1["r3"]),
            TransformFromCopy(aug3_2.mob_matrix[1][1],den),
            lag_ratio=.5))
        self.play(LaggedStart(*[TransformFromCopy(
            Dot(operation1.get_center(),fill_color=next(COLORS)),
            aug4.mob_matrix[1][i],) for i in range(4)],
            ShowCreation(rec_pivot1_aug4),
            lag_ratio=0.1))
        self.wait()
        
        # aug 4_2
        aug4_2=generate_mobmatrix(eqns_step4_2,True,element_alignment_corner=ORIGIN)
        align_right_matrix(aug4_2,eqns_step4_2)
        note_step4_2_right=VGroup(
            Textch("用第二个主元所在行",t2c={"主元":YELLOW}),
            Textch("将它之上的元素消为0",t2f={"0":"Mongolian Baiti"}),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step4_2_right.next_to(right_arrows[5],RIGHT,buff=NOTE_BUFF)
        note_step4_2_right[1]["为"].set_fill(WHITE,1,0)
        operation1=Tex(R"r1-\frac{1}{1}\,\,r2",font_size=30)
        num=operation1[3]
        frac=operation1[4]
        deno=operation1[5]
        operation1.next_to(right_arrows[5],RIGHT)
        rec=SurroundingRectangle(operation1[R"\frac{1}{1}"])
        rec_pivot0_aug4_2=SurroundingRectangle(aug4_2.mob_matrix[0][0])
        rec_pivot1_aug4_2=SurroundingRectangle(aug4_2.mob_matrix[1][1])
        rec_pivot2_aug4_2=SurroundingRectangle(aug4_2.mob_matrix[2][2])
        self.play(frame.animate.reorient(0, 0, 0, (6.39, -21.3, 0.0), 14.86),)
        self.play(LaggedStart(
            GrowArrow(right_arrows[5]),
            ShowCreation(right_rects[6]),lag_ratio=0.2),
            LaggedStart(
            FadeIn(note_step4_2_right[0]),
            FadeIn(note_step4_2_right[1]),
            b1.animate.replace(VGroup(back_rec4,back_rec4_2),stretch=True),
            b2.animate.replace(VGroup(right_rects[5],right_rects[6]),stretch=True),
            lag_ratio=0.2))
        self.play(TransformFromCopy(aug4.brackets,aug4_2.brackets),
            TransformFromCopy(aug4.line,aug4_2.line),
            TransformFromCopy(aug4.get_row(1),aug4_2.get_row(1)),
            TransformFromCopy(aug4.get_row(2),aug4_2.get_row(2)),
            # TransformFromCopy(aug4.mob_matrix[0][0],aug4_2.mob_matrix[0][0]),
            # TransformFromCopy(rec_pivot0_aug4,rec_pivot0_aug4_2),
            TransformFromCopy(rec_pivot1_aug4,rec_pivot1_aug4_2),
            TransformFromCopy(rec_pivot2_aug4,rec_pivot2_aug4_2),
            )
        self.play(LaggedStart(
            Write(operation1["r1-"]),
            Write(operation1["r2"]),
            TransformFromCopy(aug4.mob_matrix[1][1],deno),
            ShowCreation(rec),
            Write(frac),
            TransformFromCopy(aug4.mob_matrix[0][1],num),
            lag_ratio=.5))
        self.play(LaggedStart(*[TransformFromCopy(
            Dot(operation1.get_center(),fill_color=next(COLORS)),
            aug4_2.mob_matrix[0][i],) for i in range(4)],
            ShowCreation(rec_pivot0_aug4_2),
            lag_ratio=0.1))
        self.wait()
        
        # aug5
        aug5=generate_mobmatrix(eqns_step5,True,element_alignment_corner=ORIGIN)
        align_right_matrix(aug5,eqns_step5)
        note_step5_right=VGroup(
            Textch("第五步"),
            Textch("归一化第一个主元",t2c={"主元":YELLOW}),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step5_right.next_to(right_arrows[6],RIGHT,buff=NOTE_BUFF)
        underline_step5_right=Underline(note_step5_right[0],stroke_color=YELLOW).reverse_points()
        operation1=Tex(R"\frac{1}{2}\,\,r1",font_size=30)
        operation1.next_to(right_arrows[6],RIGHT)
        nu,frac,den=self.extract_fraction_parts(operation1,frac_patn)
        rec_operation1=SurroundingRectangle(operation1[frac_patn],stroke_width=2,buff=REC_BUFF)
        rec_pivot0_aug5=SurroundingRectangle(aug5.mob_matrix[0][0])
        rec_pivot1_aug5=SurroundingRectangle(aug5.mob_matrix[1][1])
        rec_pivot2_aug5=SurroundingRectangle(aug5.mob_matrix[2][2])
        self.play(frame.animate.reorient(0, 0, 0, (6.39, -26.5, 0.0), 14.86),)
        self.play(LaggedStart(
            GrowArrow(right_arrows[6]),
            ShowCreation(right_rects[7]),lag_ratio=0.2),
            LaggedStart(
            FadeIn(note_step5_right[0]),
            ShowCreation(underline_step5_right),
            FadeIn(note_step5_right[1]),
            b1.animate.replace(VGroup(back_rec5,back_rec4_2),stretch=True),
            b2.animate.replace(VGroup(right_rects[7],right_rects[6]),stretch=True),
            lag_ratio=0.2))
        self.play(TransformFromCopy(aug4_2.brackets,aug5.brackets),
            TransformFromCopy(aug4_2.line,aug5.line),
            TransformFromCopy(aug4_2.get_row(1),aug5.get_row(1)),
            TransformFromCopy(aug4_2.get_row(2),aug5.get_row(2)),
            TransformFromCopy(rec_pivot1_aug4_2,rec_pivot1_aug5),
            TransformFromCopy(rec_pivot2_aug4_2,rec_pivot2_aug5),
            )
        self.play(LaggedStart(
            Write(nu),Write(frac),
            ShowCreation(rec_operation1),
            Write(operation1["r1"]),
            TransformFromCopy(aug4_2.mob_matrix[0][0],den),
            lag_ratio=.5))
        self.play(LaggedStart(*[TransformFromCopy(
            Dot(operation1.get_center(),fill_color=next(COLORS)),
            aug5.mob_matrix[0][i],) for i in range(4)],
            ShowCreation(rec_pivot0_aug5),
            lag_ratio=0.1))
        self.play(frame.animate.reorient(0, 0, 0, (-6.94, -15.17, 0.0), 34.72))
        self.wait()


        





    def play_equation_steps(self,frame, kun, eqns_steps, refer, pattern,time):
        each_time=time/(len(eqns_steps)+2)
        current_eqn = eqns_steps[0]
        for i,eqns in enumerate(eqns_steps):
            current_eqn = eqns
            self.play(LaggedStart(*self.process_equations(eqns, refer, pattern)), run_time=each_time)
    def process_equations(self,eqns_step2, refer, pattern):
        """
        处理方程列表，补全缺失的 x、y、z，并应用动画效果。

        :param eqns_step2: 需要处理的方程列表
        :param refer: 参考方程对象
        :param pattern: 用于 `isolate` 参数的正则模式
        """
        non_change_pattern = re.compile(r"=|x|y|z")
        anims = []

        for eqn in eqns_step2:
            original_string = eqn.string
            
            # **拆分等号**
            if "=" in original_string:
                left_part, right_part = original_string.split("=", 1)
            else:
                left_part, right_part = original_string, "0"  # 防止无等号情况

            # **检查变量 x, y, z 是否存在**
            has_x = "x" in left_part
            has_y = "y" in left_part
            has_z = "z" in left_part

            # **补全缺失变量**
            if not has_x and not has_y and not has_z:
                left_part = "0x+0y+0z"  # 三个变量都缺失

            elif not has_x and not has_y:
                left_part = "0x+0y+" + left_part  # 缺失 x 和 y

            elif not has_y and not has_z:
                left_part = left_part + "+0y+0z"  # 缺失 y 和 z

            else:
                # **处理单个变量缺失的情况**
                if not has_x:
                    left_part = "0x+" + left_part  # x 缺失，补在最前

                if not has_y:
                    if re.search(r"[-+]\s*z", left_part):  # 若 `z` 之前有 `+/-`
                        left_part = left_part.replace("z", "0y+z", 1)
                    else:
                        left_part = left_part + "+0y"  # y 缺失，补在 `z` 之前

                if not has_z:
                    left_part = left_part + "+0z"  # z 缺失，补在最后

            # **修正 `++` 或 `+-`**
            left_part = re.sub(r"\+\+", "+", left_part)
            left_part = re.sub(r"\+-", "-", left_part)

            # **拼接回去**
            new_string = left_part + "=" + right_part

            # **生成新 Tex 对象并对齐**
            if new_string != original_string:
                new_tex = TexEqn(new_string, isolate=pattern).align_eqn(refer).match_y(eqn).set_color(TEAL)
                for part in new_tex[re.compile(r"0x\+|0y\+|0y|0z|\+0z|\+0y")]:
                    anims.append(FadeIn(part, rate_func=there_and_back))

            for part in eqn[non_change_pattern]:
                anims.append(part.animate.set_color(TEAL).set_anim_args(rate_func=there_and_back))

        return anims

class TrashCan(SVGMobject):
    def __init__(self,_file_name="SVG/TrashCan",**kwargs):
        super().__init__(
        file_name=_file_name,**kwargs)
        self.body=self[0]
        self.top=self[1]
        self._rotation_angle = 0
    def open(self,angle):
        self.top.rotate(-angle,about_point=self.top.get_corner(DR))
        self._rotation_angle += angle
        return self
    def close(self):
        self.top.rotate(self._rotation_angle, about_point=self.top.get_corner(DR))
        self._rotation_angle = 0
        return self

        
        
class ThrowTo(Animation):
    def __init__(
        self, mob: Mobject, target, 
        height=2,              # 控制抛物线的最高点高度
        final_scale=0.5,       # 最终缩放比例（1表示不缩放，0.5表示缩小50%）
        rotation_angle=2*np.pi,# 投掷过程旋转的总角度（这里设置为一整圈）
        **kwargs
    ):
        # 如果 target 是 Mobject，则取其中心；否则认为 target 就是一个坐标
        if isinstance(target, Mobject):
            self.target_point = target.get_center()
        else:
            self.target_point = target
        self.height = height
        self.final_scale = final_scale
        self.rotation_angle = rotation_angle
        super().__init__(mob, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        # 先使用速率函数调整 alpha
        alpha = self.rate_func(alpha)
        # 重置为起始状态（这样旋转和缩放不会累积）
        self.mobject.become(self.starting_mobject)
        
        # 获取起始点和目标点
        start_point = self.starting_mobject.get_center()
        end_point = self.target_point
        
        # 计算直线插值的中间位置
        new_center = start_point + alpha * (end_point - start_point)
        # 添加垂直方向的抛物线偏移，公式 4*alpha*(1-alpha) 保证在 alpha=0.5 时达到最大偏移
        new_center += self.height * 4 * alpha * (1 - alpha) * UP
        # 移动对象到新位置
        self.mobject.move_to(new_center)
        
        # 对象在移动过程中旋转：旋转角度随 alpha 线性变化
        current_rotation = alpha * self.rotation_angle
        self.mobject.rotate(current_rotation, about_point=new_center)
        
        # 对象逐渐缩小：线性插值从 1 缩放到 final_scale
        scale_factor = 1 - (1 - self.final_scale) * alpha
        self.mobject.scale(scale_factor, about_point=new_center)

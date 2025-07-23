from _2025.gauss.elimination import Elimination
from manim_imports_custom import *
from _2025.gauss.kun_character import Kun
class test_dir(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        from manimlib.config import parse_cli
        os.getcwd()
        current_file_path =os.path.abspath(__file__) 
        os.path.dirname(current_file_path)
        t=Tex("a")
        self.add(t)
        get_cache_dir()
        get_output_dir()
        self.play(Write(t))
        kun=Kun()
        self.add(kun)
        manim_config
class test_bullet(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        import xml.etree.ElementTree as ET
        xml_data = "<book><title>Python</title></book>"
        root = ET.fromstring(xml_data)
        print(root.tag)  #
        print(root[0].text)  

        a1=Tex("八八八哈哈哈123")
        a2=Tex("abc")
        a1.svg_string
        a2.svg_string
        self.add(a1)
        a=Text("a")
        # SVGMobject().file_name_to_svg_string()
        t=SVGMobject(svg_string=a.svg_string)
        self.add(t)
        t.match_style(a)
        b=BulletedList("hah","lala","我","oo")
        self.add(b)
        self.play(b.animate.fade_all_but(3))
        
        
class ReadNames(InteractiveScene):
    def read_names(self,filename):
        if not filename.endswith('.txt'):
                filename += '.txt'
        base_dir = get_directories()["base"]
        file_path = os.path.join(base_dir, "names", filename)
        names = []  
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                names.append(line.strip())
        return names
    def is_chinese(self,char):
        """
        判断一个字符是否为中文字符
        中文字符范围大致在：\u4e00 - \u9fff
        """
        return '\u4e00' <= char <= '\u9fff'

    def create_name_grp(self,file_identifier):
        names_list = self.read_names(file_identifier)
        all_names_vgroup = VGroup() 
        for name in names_list:
            if any(self.is_chinese(char) for char in name):
                name_mobject = Textch(name)
            else:
                name_mobject = Texten(name)
            all_names_vgroup.add(name_mobject)
        all_names_vgroup.arrange(DOWN, buff=0.5,aligned_edge=LEFT)
        all_names_vgroup.set_height(FRAME_HEIGHT)
        return all_names_vgroup
    def construct(self):
        # init
        frame=self.frame
        # start
        grp=self.create_name_grp("charge")
        self.add(grp)



class RotateSubMobs(Animation):
    def __init__(self, vg,angle=-2*PI, **kwargs):
        self._angle=angle
        super().__init__(vg, **kwargs)

    def interpolate_submobject(self,submobject,starting_submobject ,alpha):
        submobject.become(starting_submobject)
        submobject.rotate(self._angle*alpha,about_point=submobject.get_center())

class RotateScaleSubs(Animation):
    def __init__(self, vg,angle=PI,initial_scale=0.1 ,**kwargs):
        self.angle=angle
        self.initial_scale=initial_scale
        super().__init__(vg, **kwargs)
    def create_starting_mobject(self) -> Mobject:
        for sub in self.mobject.family_members_with_points():
            sub.rotate(-self.angle,about_point=sub.get_center())
            sub.scale(self.initial_scale,about_point=sub.get_center())
        return self.mobject.copy()
    def interpolate_submobject(self,submobject,starting_submobject ,alpha):
        submobject.become(starting_submobject)
        submobject.rotate(self.angle*alpha,about_point=submobject.get_center())
        new_scale = self.initial_scale + (1 - self.initial_scale) * alpha
        submobject.scale(new_scale / self.initial_scale,
            about_point=submobject.get_center())

class OneClickTripleIcon(VGroup):
    def __init__(self, svg_name: str="triples.svg", **kwargs):
        super().__init__(**kwargs)
        t = SVGMobject(svg_name)
        self.thumb =t[7:10]
        self.coin = t[5:7] 
        self.star = t[0:5]
        self.add(self.thumb, self.coin, self.star) # type: ignore
        self.arrange(RIGHT, buff=1.5) 

class RotateScale(Animation):
    def __init__(self, mobject,angle=PI,initial_scale=0.1 ,**kwargs):
        super().__init__(mobject, **kwargs)
        self.angle = angle
        self.initial_scale = initial_scale
        """ 
           !!! 这里必须通过np创建一个深拷贝 !!! 
           或者：self.mobject.deepcopy().get_center() 
        """
        self.fixed_center = np.array(self.mobject.get_center())
    def create_starting_mobject(self) -> Mobject:
        start = self.mobject.copy()
        start.rotate(-self.angle, about_point=self.fixed_center)
        start.scale(self.initial_scale, about_point=self.fixed_center)
        return start
    def interpolate_mobject(self,alpha):
        alpha=self.rate_func(alpha)
        new_scale = self.initial_scale + (1 - self.initial_scale) * alpha
        self.mobject.become(self.starting_mobject)
        self.mobject.rotate(self.angle*alpha,
            about_point=self.fixed_center)
        self.mobject.scale(new_scale / self.initial_scale,
            about_point=self.fixed_center)

class OneClick(ReadNames):
    """
    One Click Triple
    three unions
    triple action
    triple combination
    like, share, follow(subscribe),comment
    """
    def construct(self):
        # init
        frame=self.frame
        # start
        get_output_dir()
        get_vector_image_dir()
        circle_scale_factor=0.5
        text=Textch("感谢充电").scale(1.5)
        text.set_stroke("#729dad",2)
        text.to_corner(UL)
        names=self.create_name_grp("charge")
        names.arrange(DOWN,buff=0.4)
        names.set_height(FRAME_HEIGHT-text.get_height()-1)
        names.next_to(text,DOWN)
        names.to_edge(LEFT)
        names.set_color_by_gradient(GREEN_A,TEAL_A)
        icons=OneClickTripleIcon()
        icons.arrange(RIGHT,buff=1)
        icons.to_corner(UR,buff=1)
        kun=Kun()
        kun.scale(1.2).next_to(icons,DOWN,buff=1,aligned_edge=LEFT)
        kun.smile()
        content=Textch("一键三连哦")
        bubble=Bubble(content,buff=1).pin_to(kun.cheek2)
        self.add(kun)
        # self.add(bubble)
        # self.add(names)
        # self.add(icons)
        self.add(text)
        self.wait(2)
        self.play(LaggedStartMap(FadeIn,names,shift=RIGHT*2),
            kun.animate.look_at(names[0]),
            run_time=3)
        self.play(kun.animate.look_at(names[-1]),
            LaggedStartMap(Flash,names,flash_radius=1),
            run_time=3)
        self.play(
            RotateScale(icons.thumb[0],angle=0,initial_scale=circle_scale_factor),
            Rotate(icons.thumb[1:3],angle=-PI/6,rate_func=there_and_back),
            RotateScale(icons.coin[0],angle=0,initial_scale=circle_scale_factor),
            Write(icons.coin[1]),
            RotateScale(icons.star[0],angle=0,initial_scale=circle_scale_factor),
            RotateScale(icons.star[1:],angle=PI*2,
                initial_scale=0.3),
            kun.animate.look(UP),
            run_time=3)
        self.play(kun.animate.look_at(bubble),
            Write(bubble))
        self.wait()
        self.play(kun.animate.close_eyes().set_anim_args(rate_func=there_and_back))
        self.wait()



class gauss_profile(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        gauss=SVGMobject("ga7").scale(3)
        self.wait()
        self.play(Write(gauss),run_time=10)
        self.wait()
        # gauss.sor

        # self.play(Write(gauss.sort(
        #     lambda p:abs(p[0]-gauss.get_center()[0])
        #     )),run_time=10)
        # self.add(gauss)

class gauss_title(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        matrix=Matrix2(np.eye(9, dtype=int))
        gauss=SVGMobject("t2")
        indices_up=[0,1,3,2,4,6,7,8,5,9,10]
        indices_up.reverse()
        indices_middle=[11,12,13,14,15,17,16,19,18]
        indices_down=[22,21,20,23,26,24,25,27,28,29,30,31,32]
        up=VGroup(gauss.submobjects[i] for i in indices_up)
        middle=VGroup(gauss.submobjects[i] for i in indices_middle)
        down=VGroup(gauss.submobjects[i] for i in indices_down)
        # up=VGroup(*gauss.submobjects[0:11]).reverse_submobjects()
        # middle=VGroup(*gauss.submobjects[11:20])
        # down=VGroup(*gauss.submobjects[20:33])
        # index=index_labels(gauss)
        # brs=BracketsForMobject(gauss,h_buff=0.3,tip_length=0.3,v_buff=0.5)
        matrix.match_height(brs)
        matrix.get_off_diagonal().set_opacity(0.3)
        matrix.scale(2)
        gauss.sort().set_color_by_gradient(TEAL_A,WHITE)
        frame.reorient(0, 0, 0, (0.3, 0.13, 0.0), 8.00)
        self.add(gauss)
        self.wait()
        self.play(LaggedStart(
                    *[FadeOut(part,shift=DOWN)
                    for part in down],
                    *[FadeOut(part,shift=UP)
                    for part in up],
                    *[FadeTransform(a,b)
                    for a,b in zip(middle,matrix.get_diagonal())],
                    FadeIn(matrix.get_off_diagonal()),
                    FadeIn(matrix.brackets[0],shift=RIGHT),
                    FadeIn(matrix.brackets[1],shift=LEFT),
                run_time=5))
        self.wait()
        
class Matrix2(Matrix):
    def __init__(self, matrix, **kwargs):
        super().__init__(matrix,**kwargs)
        self.n_rows = len(self.mob_matrix)
        self.n_cols = len(self.mob_matrix[0])

    def get_diagonal(self):
        diag_elements = [
            self.mob_matrix[i][i]
            for i in range(min(self.n_rows, self.n_cols))
        ]
        return VGroup(*diag_elements)

    def get_off_diagonal(self):
        off_diag_elements = []
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                if i != j:
                    off_diag_elements.append(self.mob_matrix[i][j])
        return VGroup(*off_diag_elements)

class BracketsForMobject(VGroup):
    def __init__(self, mobject, h_buff=0.2, v_buff=0.2, tip_length=0.2, **kwargs):
        super().__init__(**kwargs)
        self.mobject=mobject
        
        height = self.mobject.get_height() + v_buff
        left_bracket = self.create_bracket(height, tip_length, buff=h_buff,direction='left')
        right_bracket = self.create_bracket(height, tip_length, buff=h_buff,direction='right')
        self.add(left_bracket, right_bracket)
    
    def create_bracket(self, height, tip_length,buff, direction='left'):
        baseline = self.create_baseline(height,buff, direction)
        bracket = self.add_horizontal_lines(baseline, tip_length, direction)
        return bracket
    def create_baseline(self, height,buff, direction='left'):
        baseline = Line(
            np.array([0, -height/2, 0]),
            np.array([0, height/2, 0])
        )
        if direction == 'left':
            baseline.next_to(self.mobject, LEFT, buff)
        else:  # direction == 'right'
            baseline.next_to(self.mobject, RIGHT, buff)
        return baseline
    def add_horizontal_lines(self, baseline, tip_length, direction='left'):
        if direction == 'left':
            top_line = Line(
                baseline.get_end(),
                baseline.get_end() + np.array([tip_length, 0, 0])
            )
            bottom_line = Line(
                baseline.get_start(),
                baseline.get_start() + np.array([tip_length, 0, 0])
            )
        else:  # direction == 'right'
            top_line = Line(
                baseline.get_end(),
                baseline.get_end() + np.array([-tip_length, 0, 0])
            )
            bottom_line = Line(
                baseline.get_start(),
                baseline.get_start() + np.array([-tip_length, 0, 0])
            )
        return VGroup(baseline, top_line, bottom_line)



class SVGMobject2(SVGMobject):
    def file_name_to_svg_string(self, file_name: str) -> str:
        return Path(get_full_vector_image_path(file_name)).read_text(encoding="utf-8")
        
class start_framework(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        recs=Rectangle(16,9).replicate(3).arrange(RIGHT,buff=0.3)
        recs.set_width(FRAME_WIDTH*0.99)
        titles=VGroup(
            Textch("力学"),
            Textch("电路"),
            Textch("统计"),
            )
        for title,rec in zip(titles,recs):
            title.next_to(rec,UP)
        grp=VGroup(titles,recs).to_edge(UP)
        titles[2]["计"].set_fill(WHITE,1,0)
        text_solve=Textch("解线性方程组").next_to(recs,DOWN,buff=2)
        ars=VGroup(
            Arrow(recs[0].get_bottom(),text_solve.get_corner(UL),buff=0.1), 
            Arrow(recs[1].get_bottom(),text_solve.get_top(),buff=0.1), 
            Arrow(recs[2].get_bottom(),text_solve.get_corner(UR),buff=0.1), 
            )
        t_copy=text_solve.copy().set_color_by_gradient(TEAL,WHITE,TEAL)
        t_copy.sort(lambda p:abs(p[0]-t_copy.get_center()[0]))
        self.add(grp)
        self.wait(1)
        self.play(LaggedStart(
            *[GrowArrow(ars[i]) for i in range(3)],
            FadeIn(text_solve),
            lag_ratio=0.2
            ))
        self.play(Write(t_copy),FlashUnder(t_copy,color=TEAL),run_time=2)
        self.wait(2)

class statistics(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        
        # statistics
        ax=Axes((-2,10),(-2,10))
        a = 0.5  # 斜率
        b = 2  # 截距
        x = np.linspace(*ax.x_range[0:2] ,400)
        y = a * x + b
        np.random.seed(626)
        noise = np.random.normal(0, 0.5, size=x.shape)  # 均值为 0，标准差为 3
        y_noisy = y + noise
        dots1=Group()
        dots1.add(*[TrueDot(ax.c2p(x,y,0)) for x,y in zip(x,y_noisy)])
        line=ax.get_graph(lambda x:a*x+b)
        dots1.set_submobject_colors_by_gradient(TEAL,WHITE)
        line.set_color(RED)
        strings=[]
        for x,y in zip(x,y_noisy):
            strings.append(f"{x:.2f}a+b={y:.2f}") # x is slope,y is intercept
        points_eqns=VGroup(*[Tex(string,t2c={"a":RED,"b":RED}) for string in strings[:5]])
        points_eqns.add(Tex(R"\vdots"))
        points_eqns.add(*[Tex(string,t2c={"a":RED,"b":RED}) for string in strings[-5:]])
        points_eqns.arrange(DOWN)
        points_eqns.set_submobject_colors_by_gradient(TEAL,WHITE)
        for eqn in points_eqns:
            eqn["a"].set_color(RED)
            eqn["b"].set_color(RED)
            eqn["+"].set_color(WHITE)
            eqn["="].set_color(WHITE)
        line_label=Tex("ax+b=y",t2c={"a":RED,"b":RED,"x":TEAL,"y":TEAL}).scale(1.5).next_to(line.get_end(),RIGHT,buff=0.8)
        points_eqns.next_to(line_label,DOWN)
        frame.reorient(0, 0, 0, (1.09, 0.06, 0.0), 12.40)
        self.add(ax)
        dots1.set_z(20).set_opacity(0)
        self.play(
            LaggedStart(*[d.animate.set_z(0).set_opacity(1) for d in dots1.shuffle()])
            ,run_time=2)
        self.play(ShowCreation(line),Write(line_label),
            frame.animate.reorient(0, 0, 0, (2.07, 0.04, 0.0), 12.40),
            run_time=1)
        self.play(
            LaggedStart(
                *[ReplacementTransform(VectorizedPoint(d.get_center()),eqn)
                for d,eqn in zip(dots1[0:5],points_eqns[0:5])],
                Write(points_eqns[5]),
                *[ReplacementTransform(VectorizedPoint(d.get_center()),eqn)
                for d,eqn in zip(dots1[-5:],points_eqns[-5:])])
            ,run_time=3)
        self.wait()

        # fitting a plane
        ax2=ThreeDAxes(x_range=(-2, 10), y_range=(-2, 10), z_range=(-2, 10))
        a = 0.5  # x的系数
        b = 1.0  # y的系数
        c = 2.0  # z的系数
        d = 3.0  # 平面偏移
        x_vals = np.linspace(*ax2.x_range[0:2], 20)
        y_vals = np.linspace(*ax2.y_range[0:2], 20)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = a * X + b * Y + c
        np.random.seed(626)
        noise = np.random.normal(0, 0.5, size=Z.shape)
        Z_noisy = Z + noise
        dots2 = Group()
        for x, y, z in zip(X.flatten(), Y.flatten(), Z_noisy.flatten()):
            dots2.add(TrueDot(ax2.c2p(x, y, z), color=WHITE))
        dots2.set_submobject_colors_by_gradient(TEAL,WHITE)
        plane = ax2.get_graph(lambda x, y: a*x + b*y + c, u_range=[-2, 10], v_range=[-2, 10])
        plane.set_color(RED).set_opacity(0.5)
        plane_eqn = Tex(f"ax + by + c=z", t2c={"a": RED, "b": RED, "c": RED,"x":TEAL,"y":TEAL,"z":TEAL})
        plane_eqn.to_corner(UR)
        strings2=[]
        for x,y,z in zip(X.flatten(), Y.flatten(), Z_noisy.flatten()):
            strings2.append(f"{x:.1f}a+{y:.1f}b+c={z:.1f}") # x is slope,y is intercept
        num=16
        points_eqns2=VGroup(*[Tex(string) for string in strings2[:num]])
        points_eqns2.add(Tex(R"\vdots"))
        points_eqns2.arrange(DOWN)
        points_eqns2.set_submobject_colors_by_gradient(TEAL,WHITE)
        points_eqns2.match_width(plane_eqn)
        points_eqns2.next_to(plane_eqn,DOWN)
        for eqn in points_eqns2:
            eqn["a"].set_color(RED)
            eqn["b"].set_color(RED)
            eqn["c"].set_color(RED)
            eqn["+"].set_color(WHITE)
            eqn["="].set_color(WHITE)
        eqns=VGroup(plane_eqn,points_eqns2).fix_in_frame()
        self.add(ax2[0:2])
        self.remove(ax)
        self.play(
            FadeOut(line),
            FadeOut(line_label),FadeOut(points_eqns),
            frame.animate.reorient(44, 71, 0, (1.38, 1.3, 5.77), 12.15),
            ShowCreation(ax2[2]),
            LaggedStart(
            *[d1.animate.move_to(d2) for d1,d2 in zip(dots1,dots2)]
            ),run_time=3,rate_func=linear)
        self.add(dots2)
        self.remove(dots1)
        self.play(ShowCreation(plane,time_span=[0,1]),
            LaggedStart(Write(plane_eqn),
                *[ReplacementTransform(VectorizedPoint(p.get_center()),eqn) 
                for p,eqn in zip(dots2[:num],points_eqns2[:num])],
                Write(points_eqns2[-1])),
            frame.animate.reorient(88, 59, 0, (0.42, 1.23, 7.46), 10.38),run_time=3)
        self.wait()
        
        # fadeout
        self.play(
            VGroup(plane_eqn,points_eqns2).animate.to_edge(LEFT).set_anim_args(time_span=[0.5,1.5]),
            LaggedStartMap(FadeOut,Group(ax2,plane,dots2),shift=-ax2.y_axis.get_unit_vector()),
            run_time=2)
        
        # font
        eqns.unfix_from_frame()
        frame.to_default_state()
        rec=SurroundingRectangle(eqns,stroke_color=WHITE)
        text=Textch("线性方程组").scale(2.5).to_edge(RIGHT)
        ar=Arrow(rec.get_right(),text.get_left())
        t_copy=text.copy().set_color_by_gradient(TEAL,WHITE,TEAL)
        t_copy.sort(lambda p:abs(p[0]-t_copy.get_center()[0]))
        self.play(LaggedStart(
            ShowCreation(rec),GrowArrow(ar),FadeIn(text),
            lag_ratio=0.1
            ))
        self.play(Write(t_copy),FlashUnder(t_copy,color=TEAL))
        self.wait(2)
        
class circuit(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # circuit
        frame.reorient(0, 0, 0, (-1.4, 0.06, 0.0), 12.40)
        r1=Rectangle(4,1)
        r2=Rectangle(4,1)
        r3=Rectangle(4,1)
        resistances=VGroup(r1,r2,r3).arrange(DOWN,buff=3)
        short_line=Line().rotate(PI/2)
        long_line=Rectangle(3.5,0.1,fill_color=WHITE,fill_opacity=1).rotate(PI/2)
        source1=VGroup(long_line,short_line).arrange(RIGHT,buff=0.5).scale(0.5)
        source1.next_to(r2,LEFT,buff=4)
        source2=source1.copy().flip().next_to(r3,LEFT,buff=4)
        dot1=Dot(radius=0.15).next_to(source1,LEFT,buff=4)
        dot2=Dot(radius=0.15).next_to(r2,RIGHT,buff=4)
        circuit_up=VGroup(
            source1,
            Line(source1.get_left(),dot1.get_center()),
            dot1,
            Line(dot1.get_center(),np.array([dot1.get_x(),r1.get_y(),0])),
            Line(np.array([dot1.get_x(),r1.get_y(),0]),r1.get_left()),
            r1,
            Line(r1.get_right(),np.array([dot2.get_x(),r1.get_y(),0])),
            Line(np.array([dot2.get_x(),r1.get_y(),0]),dot2.get_center()),
            dot2,
            Line(dot2.get_center(),r2.get_right()),
            r2,
            Line(r2.get_left(),source1.get_right()),)
        circuit_down=VGroup(
            Line(dot2.get_center(),np.array([dot2.get_x(),r3.get_y(),0])),
            Line(np.array([dot2.get_x(),r3.get_y(),0]),r3.get_right()),
            r3,
            Line(r3.get_left(),source2.get_right())  ,
            source2,
            Line(source2.get_left(),np.array([dot1.get_x(),r3.get_y(),0]))  ,
            Line(np.array([dot1.get_x(),r3.get_y(),0]),dot1.get_center())  ,
            )
        
        scale_factor=2
        r1_label=Tex("R1").scale(scale_factor).next_to(r1,UP,buff=0.5)
        r2_label=Tex("R2").scale(scale_factor).next_to(r2,UP,buff=0.5)
        r3_label=Tex("R3").scale(scale_factor).next_to(r3,UP,buff=0.5)
        epsilon1=Tex(R"\epsilon_1").scale(scale_factor).next_to(source1,UP,buff=0.5)
        epsilon2=Tex(R"\epsilon_2").scale(scale_factor).next_to(source2,UP,buff=0.5)
        labels=VGroup(r1_label,r2_label,r3_label,epsilon1,epsilon2)
        circuit=VGroup(labels,circuit_up,circuit_down,r1,r2,r3,dot1,dot2,source1,source2)

        self.add(circuit_up,circuit_down)
        self.play(LaggedStartMap(Write,labels),run_time=2)
        
        # i1,i2,i3
        i1=Arrow(dot2.get_center()+np.array([0,3,0]),dot2.get_center(),tip_width_ratio=10)
        i2=Arrow(dot2.get_center(),dot2.get_center()+np.array([-3,0,0]),tip_width_ratio=10)
        i3=Arrow(dot2.get_center(),dot2.get_center()+np.array([0,-3,0]),tip_width_ratio=10)
        i1.set_color(RED)
        i2.set_color(YELLOW)
        i3.set_color(BLUE)
        i1.shift(RIGHT*0.2)
        i2.shift(UP*0.2)
        i3.shift(RIGHT*0.2)        
        i1_label=Tex("i_1").scale(2).next_to(i1,RIGHT).match_color(i1)
        i2_label=Tex("i_2").scale(2).next_to(i2,UP).match_color(i2)
        i3_label=Tex("i_3").scale(2).next_to(i3,RIGHT).match_color(i3)
        # self.add(i1_label,i2_label,i3_label)

        self.play(LaggedStart(
                (line.animate.set_color(BLUE)
                 .set_anim_args(rate_func=there_and_back)
                 for line in circuit_up[0:9]
                ),lag_ratio=0.2
            ),Write(i1,time_span=[0.5,1]),run_time=1)
        self.play(LaggedStart(
                (line.animate.set_color(BLUE)
                 .set_anim_args(rate_func=there_and_back)
                 for line in circuit_up[9:]
                ),lag_ratio=0.2,
            ),
                LaggedStart(
                (line.animate.set_color(BLUE)
                 .set_anim_args(rate_func=there_and_back)
                 for line in circuit_down
                ),lag_ratio=0.2,
            ),Write(i2,time_span=[0.5,1]),Write(i3,time_span=[0.5,1]),run_time=1)
        self.play(Write(i1_label),Write(i2_label),Write(i3_label))
        self.wait()


        # circuit eqn
        kcl=Tex(R"i_1-i_2-i_3=0",t2c={"i_1":RED,"i_2":YELLOW,"i_3":BLUE})
        kvl1=Tex(R"-R_2i_2+\epsilon_1-R_1i_1=0",t2c={"i_1":RED,"i_2":YELLOW,"i_3":BLUE})
        kvl2=Tex(R"-R_3i_3-\epsilon_2-\epsilon_1+R_2i_2=0",t2c={"i_1":RED,"i_2":YELLOW,"i_3":BLUE})
        circuit_eqns=VGroup(kcl,kvl1,kvl2).arrange(DOWN,aligned_edge=RIGHT)
        circuit_eqns.scale(3).next_to(circuit,DOWN,buff=2)
        self.play(
            frame.animate.reorient(0, 0, 0, (-0.97, -1.64, 0.0), 16.31).set_anim_args(time_span=[0,1]),
            LaggedStart(
            FadeTransform(i1_label.copy(),kcl["i_1"]),
            FadeTransform(i2_label.copy(),kcl["i_2"]),
            FadeTransform(i3_label.copy(),kcl["i_3"]),lag_ratio=0.2
            ),Write(kcl["-"],time_span=[1,2]),Write(kcl["=0"],time_span=[1,2]),run_time=2)
        self.play(
            frame.animate.reorient(0, 0, 0, (-0.98, -2.59, 0.0), 17.70).set_anim_args(time_span=[0,1]),
            LaggedStart(
            FadeTransform(r2_label.copy(),kvl1["R_2"]),
            FadeTransform(i2_label.copy(),kvl1["i_2"]),
            FadeTransform(epsilon1.copy(),kvl1[R"\epsilon_1"]),
            FadeTransform(r1_label.copy(),kvl1["R_1"]),
            FadeTransform(i1_label.copy(),kvl1["i_1"]),
            lag_ratio=0.2),
            Write(kvl1["-"],time_span=[1,2]),
            Write(kvl1["+"],time_span=[1,2]),
            Write(kvl1["=0"],time_span=[1,2]),
            run_time=2)
        self.play(
            frame.animate.reorient(0, 0, 0, (-0.98, -2.85, 0.0), 20.86).set_anim_args(time_span=[0,1]),
            LaggedStart(
            FadeTransform(r3_label.copy(),kvl2["R_3"]),
            FadeTransform(i3_label.copy(),kvl2["i_3"]),
            FadeTransform(epsilon1.copy(),kvl2[R"\epsilon_1"]),
            FadeTransform(epsilon2.copy(),kvl2[R"\epsilon_2"]),
            FadeTransform(r2_label.copy(),kvl2["R_2"]),
            FadeTransform(i2_label.copy(),kvl2["i_2"]),
            lag_ratio=0.2),
            Write(kvl2["-"],time_span=[1,2]),
            Write(kvl2["+"],time_span=[1,2]),
            Write(kvl2["=0"],time_span=[1,2]),
            run_time=2)
        self.wait()
        # text
        rec=SurroundingRectangle(circuit_eqns,stroke_color=WHITE)
        text=Textch("线性方程组").scale(4).next_to(circuit_eqns,DOWN,buff=4)
        ar=Arrow(rec.get_bottom(),text.get_top())
        t_copy=text.copy().set_color_by_gradient(TEAL,WHITE,TEAL)
        t_copy.sort(lambda p:abs(p[0]-t_copy.get_center()[0]))
        self.play(LaggedStart(
            frame.animate.reorient(0, 0, 0, (-0.69, -12.82, 0.0), 17.85),
            ShowCreation(rec),GrowArrow(ar),FadeIn(text),
            lag_ratio=0.1
            ))
        self.play(Write(t_copy),FlashUnder(t_copy,color=TEAL))
        self.wait()

class newton_force(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # physics
        def get_closest_point_index(points,deg=225):
            target_vector=np.array([[np.cos(deg*DEGREES)],[np.sin(deg*DEGREES)],[0]])
            to_compare=[ np.dot(point,target_vector) for point in points]
            index=np.argmax(to_compare)
            return index
        pin=SVGMobject('pin.svg',height=1)
        pin.set_fill(YELLOW,1)
        pin.set_stroke(RED,1,1)
        path=pin.submobjects[0]
        points=path.get_points()    
        index=get_closest_point_index(points,225)  # 45
        shift_vector=-points[index-1]

        ax=NumberPlane().set_opacity(0.5)
        pin0=pin.copy()
        pin1=pin.copy()
        pin2=pin.copy()
        coord0=ax.c2p(0,0,0)
        coord1=ax.c2p(-4,4,0)
        coord2=ax.c2p(3,3*math.sqrt(3),0)
        coord3=ax.c2p(0,-5,0)
        pin0.move_to(coord0).shift(shift_vector)
        pin1.move_to(coord1).shift(shift_vector)
        pin2.move_to(coord2).shift(shift_vector)
        # self.add(ax,pin0,pin1,pin2)
        frame.reorient(0, 0, 0, (0.99, 1.05, 0.0), 11.40)
        self.play(LaggedStartMap(FadeIn,Group(pin0,pin1,pin2),shift=LEFT,lag_ratio=0.1))

        # hanging things
        line_left=Line(coord1,coord0)
        line_right=Line(coord2,coord0)
        line_down=Line(coord0,coord3)
        ball=Sphere(radius=0.3).move_to(coord3)
        # self.add(line_left,line_right,line_down)
        # self.add(ball)
        self.play(LaggedStartMap(ShowCreation,Group(line_left,line_right,line_down),time_span=[0,1.5]),
            ShowCreation(ball,time_span=[1,2]),
            frame.animate.reorient(0, 0, 0, (1.27, -0.41, 0.0), 13.44),run_time=2)

        # dashedline
        dashedline1=DashedLine(coord1,coord1+RIGHT*1.5)
        dashedline2=DashedLine(coord2,coord2+LEFT*1.5)
        arc1=Circle(stroke_color=WHITE).reverse_points().move_to(coord1)
        arc2=Circle(stroke_color=WHITE).move_to(coord2)
        arc1=arc1.get_subcurve(0,45/360)
        arc2=arc2.get_subcurve(180/360,(180+60)/360)
        arc1_label=Tex(R"45^\circ")
        arc2_label=Tex(R"60^\circ")
        arc1_label.move_to(arc1).shift(np.array([0.5,-0.1,0]))
        arc2_label.move_to(arc2).shift(np.array([-0.5,-0.3,0]))
        # self.add(arc1,arc2)
        # self.add(arc1_label,arc2_label)
        # self.add(dashedline1,dashedline2)
        self.play(LaggedStartMap(ShowCreation,VGroup(dashedline1,dashedline2,arc1,arc2) ))
        self.play(Write(arc1_label),Write(arc2_label))

        # force analysis
        f_mg=Arrow(coord0,(coord0+coord3)*1/2,tip_width_ratio=10,buff=0).set_color(YELLOW_B)
        f_t1=Arrow(coord0,(coord0+coord1)*1/2,tip_width_ratio=10,buff=0).set_color(BLUE)
        f_t2=Arrow(coord0,(coord0+coord2)*1/2,tip_width_ratio=10,buff=0).set_color(RED)
        f_mg_label=Tex("mg").match_color(f_mg).scale(1.5).next_to(f_mg.get_end(),LEFT)
        f_t1_label=Tex("T_1").match_color(f_t1).scale(1.5).next_to(f_t1.get_end(),LEFT)
        f_t2_label=Tex("T_2").match_color(f_t2).scale(1.5).next_to(f_t2.get_end(),RIGHT)
        # self.add(f_mg,f_t1,f_t2)
        # self.add(f_mg_label,f_t1_label,f_t2_label)
        self.play(LaggedStart(GrowArrow(f_mg),Write(f_mg_label),lag_ratio=0.5))
        self.play(LaggedStart(GrowArrow(f_t1),Write(f_t1_label),lag_ratio=0.5))
        self.play(LaggedStart(GrowArrow(f_t2),Write(f_t2_label),lag_ratio=0.5))

        # force decomposition
        dash_t1_x=DashedLine(f_t1.get_end(),np.array([f_t1.get_end()[0],0,0])) 
        dash_t1_y=DashedLine(f_t1.get_end(),np.array([coord0[0],f_t1.get_end()[1],0]))
        dash_t2_x=DashedLine(f_t2.get_end(),np.array([f_t2.get_end()[0],0,0])) 
        dash_t2_y=DashedLine(f_t2.get_end(),np.array([coord0[0],f_t2.get_end()[1],0]))
        decomp_t1_x=Arrow(coord0,dash_t1_x.get_end(),buff=0,tip_width_ratio=8).match_color(f_t1)
        decomp_t1_y=Arrow(coord0,dash_t1_y.get_end(),buff=0,tip_width_ratio=8).match_color(f_t1)
        decomp_t2_x=Arrow(coord0,dash_t2_x.get_end(),buff=0,tip_width_ratio=8).match_color(f_t2)
        decomp_t2_y=Arrow(coord0,dash_t2_y.get_end(),buff=0,tip_width_ratio=8).match_color(f_t2)
        label_decomp_t1_x=Tex(R"T_1\cos(45^\circ)").match_color(f_t1).next_to(decomp_t1_x.get_end(),DOWN)
        label_decomp_t1_y=Tex(R"T_1\sin(45^\circ)").match_color(f_t1).next_to(decomp_t1_y.get_end(),UP).shift(LEFT*1)
        label_decomp_t2_x=Tex(R"T_2\cos(60^\circ)").match_color(f_t2).next_to(decomp_t2_x.get_end(),DOWN)
        label_decomp_t2_y=Tex(R"T_2\sin(60^\circ)").match_color(f_t2).next_to(decomp_t2_y.get_end(),UP).shift(RIGHT*0.5)
        # self.add(dash_t1_x,dash_t1_y,dash_t2_x,dash_t2_y) 
        # self.add(decomp_t1_x,decomp_t1_y,decomp_t2_x,decomp_t2_y) 
        # self.add(label_decomp_t1_x,label_decomp_t1_y,label_decomp_t2_x,label_decomp_t2_y)
        self.play(ShowCreation(dash_t1_x),ShowCreation(dash_t1_y))
        self.play(TransformFromCopy(f_t1,decomp_t1_x),TransformFromCopy(f_t1,decomp_t1_y),
            f_t1.animate.set_opacity(0.3))
        self.play(Write(label_decomp_t1_x),Write(label_decomp_t1_y))
        self.play(ShowCreation(dash_t2_x),ShowCreation(dash_t2_y))
        self.play(TransformFromCopy(f_t2,decomp_t2_x),TransformFromCopy(f_t2,decomp_t2_y),
            f_t2.animate.set_opacity(0.3))
        self.play(Write(label_decomp_t2_x),Write(label_decomp_t2_y))

        # force eqn
        horizontal_eqn=Tex(R"T_1\cos(45^\circ)=T_2\cos(60^\circ)",t2c={"T_1":BLUE,"T_2":RED})
        vertical_eqn=Tex(R"T_1\sin(45^\circ)+T_2\sin(60^\circ)=mg",t2c={"T_1":BLUE,"T_2":RED})
        force_eqns=VGroup(horizontal_eqn,vertical_eqn).scale(1.5).arrange(DOWN,aligned_edge=RIGHT)
        force_eqns.next_to(ball,DOWN)
        # self.add(force_eqns)
        self.play(frame.animate.reorient(0, 0, 0, (1.49, -0.79, 0.0), 14.59),
            FadeTransform(label_decomp_t1_x.copy(),horizontal_eqn[R"T_1\cos(45^\circ)"]),
            FadeTransform(label_decomp_t2_x.copy(),horizontal_eqn[R"T_2\cos(60^\circ)"]),
            Write(horizontal_eqn[R"="]),
            label_decomp_t1_x.animate.set_opacity(0.3),
            label_decomp_t2_x.animate.set_opacity(0.3),run_time=2)
        self.play(
            FadeTransform(label_decomp_t1_y.copy(),vertical_eqn[R"T_1\sin(45^\circ)"]),
            FadeTransform(label_decomp_t2_y.copy(),vertical_eqn[R"T_2\sin(60^\circ)"]),
            FadeTransform(f_mg_label.copy(),vertical_eqn[R"mg"]),
            label_decomp_t1_y.animate.set_opacity(0.3),
            label_decomp_t2_y.animate.set_opacity(0.3),
            f_mg_label.animate.set_opacity(0.3),
            Write(vertical_eqn[R"="]),Write(vertical_eqn[R"+"]),run_time=2)
        self.wait()

        # text
        rec=SurroundingRectangle(force_eqns,stroke_color=WHITE)
        text=Textch("线性方程组").scale(3)
        text.next_to(force_eqns,DOWN,buff=3)
        ar=Arrow(rec.get_bottom(),text.get_top())
        t_copy=text.copy().set_color_by_gradient(TEAL,WHITE,TEAL)
        t_copy.sort(lambda p:abs(p[0]-t_copy.get_center()[0]))
        self.play(LaggedStart(
            frame.animate.reorient(0, 0, 0, (1.18, -7.55, 0.0), 12.00),
            ShowCreation(rec),GrowArrow(ar),FadeIn(text),
            lag_ratio=0.1
            ))
        self.play(Write(t_copy),FlashUnder(t_copy,color=TEAL))
        self.wait()
        
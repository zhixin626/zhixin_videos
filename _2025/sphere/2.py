from manim_imports_custom import *
class archi_method(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        # t=Text("Archimedes’ Method").scale(2)
        t=Textch("阿基米德的方法").scale(2)
        self.add(t)

class archi_saying_ch(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        # t=Text("Give me a place to stand, and I will move the Earth")
        t=Textch("给我一个支点，我能翘起整个地球！")
        bubble=Bubble(content=t,direction=RIGHT,buff=2,fill_color=WHITE,fill_opacity=0.2)
        self.wait(2)
        self.play(
            GrowFromPoint(bubble.body,bubble.get_tip()),
            GrowFromPoint(bubble.content,bubble.get_tip()))
        self.wait(2)
class timeline_ch(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        frame.reorient(0, 0, 0, (0.05, 0.57, 0.0), 10.14)
        numbers=[10,5,0,-2,-7.5]
        up_mutiple=1.5
        line=NumberLine((-25,25,0.5),
            big_tick_numbers=numbers,longer_tick_multiple=3)
        line.next_to(frame.get_top(),DOWN*4)
        times=VGroup(
            Text("2025").next_to(line.n2p(10),UP*up_mutiple),
            Text("1000").next_to(line.n2p(5),UP*up_mutiple),
            Text("1AD").next_to(line.n2p(0),UP*up_mutiple),
            Text("-200BC").next_to(line.n2p(-2),UP*up_mutiple),
            Text("-1500BC").next_to(line.n2p(-7.5),UP*up_mutiple)
            )
        x_target=times[3].get_center()
        tri=Triangle(fill_color=BLUE,fill_opacity=0.8,stroke_opacity=0)
        tri.scale(0.3).next_to(line.n2p(10),DOWN*up_mutiple)
        grp=VGroup(line,times,tri).match_x(
            frame.get_center()-tri.get_center())
        self.play(FadeIn(tri),FadeIn(times),FadeIn(line))
        self.wait()
        self.play(tri.animate.match_x(line.n2p(-5)),
            frame.animate.match_x(line.n2p(-5)))
        self.wait()

        # Ancient Greek
        rec=SurroundingRectangle(VGroup(line.get_tick(-2),line.get_tick(-7.5)),buff=0)
        rec.set_style(fill_opacity=0.5,stroke_opacity=0,fill_color=BLUE)
        rec.set_height(0.6,stretch=True)
        # title=Text("Ancient Greece").scale(1.5).set_color(BLUE)
        title=Textch("古希腊时期").scale(1.5).set_color(BLUE)
        title.next_to(tri,DOWN)
        self.play(GrowFromPoint(rec,tri.get_top()),
            Write(title))
        self.wait()
        grp.add(rec)
        self.play(FadeOut(grp,shift=UP),
            title.animate.next_to(frame.get_top(),DOWN*1.5),)
        underline=Underline(title,stroke_color=BLUE)
        underline.shift(RIGHT*6)
        self.play(FadeIn(underline,shift=RIGHT),
            title.animate.shift(RIGHT*6))
        self.wait()
class archi(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        frame.reorient(0, 0, 0, (0.05, 0.57, 0.0), 10.14)
        svgs=VGroup(
        SVGMobject("back"),
        SVGMobject("grass"),)
        archi=SVGMobject("archiwhole")
        svgs.match_width(self.frame)
        archi.scale(3)
        archi.scale(1.4).to_edge(LEFT).shift(LEFT*1.3).shift(DOWN*0.3)
        # Group(svgs,archi).move_to(frame.get_center())
        name=Text("Archimedes",font='Freestyle Script').scale(1.5)
        name.shift(UP*2.5+RIGHT*0.5)
        self.play(ShowCreation(svgs),run_time=2)
        self.play(Write(archi[640:],stroke_color=BLACK),run_time=2)
        self.play(Write(name),run_time=2)
        self.play(Write(archi[0:640],stroke_color="#6c3e11"),run_time=2)
        self.wait(2)

class ar(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        ar=Arrow(ORIGIN,RIGHT*3)
        self.play(GrowArrow(ar))
        self.play(FadeOut(ar))
        self.wait()
class Surrounding(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        t=Tex("=")
        self.play(FlashAround(t),run_time=2)
        self.wait()
class frame(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        frame.reorient(0, 0, 0, (0,0,0), 19.11)
        rec=Rectangle(width=16,height=9)\
        .get_grid(2,2,buff=0.5)
        self.add(rec)
        
class thank_ch(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        # thank=Text("Thanks for watching!").scale(2)
        thank=Textch("感谢观看!").scale(2)
        self.play(FadeIn(thank,shift=LEFT),run_time=3)
        self.wait(2)


class cover(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        t=Text("Archimedes’ Sphere Trick").scale(2)
        self.add(t)
        
class complement1_ch(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        # vol=Text("Volume of sphere")
        vol=Textch("球体的体积")
        eqn=Tex(R"=\frac{4}{3} \pi r^3")
        grp=VGroup(vol,eqn).arrange(DOWN,aligned_edge=LEFT).scale(2)
        self.add(grp)
        self.play(LaggedStartMap(FadeIn,grp,shift=RIGHT,lag_ratio=0.2))
        self.wait()
        self.play(Indicate(eqn),run_time=2)
        self.wait()
class complement2(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        eq=Tex("(x-a)^2+y^2=a^2")
        eq.to_corner(UL)
        self.play(FlashAround(eq),run_time=2)
class complement3(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        circle=Circle(fill_opacity=1,fill_color=YELLOW,stroke_opacity=0)
        eq1=Tex(R"\pi r^2")
        self.add(circle)
        self.play(ShowCreation(circle))

        

        
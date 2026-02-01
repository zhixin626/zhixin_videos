import sys
sys.path.append("D:/zhixin_videos")
from manim_imports_custom import *
class cover(InteractiveScene):
    default_camera_config = {"background_color": BLACK}
    def construct(self):
        # start
        if len(sys.argv) >= 8:
            name  = sys.argv[3]
            time  = sys.argv[4]
            color = sys.argv[5]
            year  = sys.argv[6]
        else:
            name  = "不可一世杀手"
            time  = "12月14日"
            color = "#FFFF00"
            year  = "2026"
        # F
        safe_rec  = Safe(y=-2.5).rec
        kwargs    = {"font":"WenYue XinQingNianTi (Authorization Required)"}
        name      = Text(name,**kwargs).set_color(color).scale(1.8)
        time      = Text(time,**kwargs).set_color(WHITE).scale(1.5)
        replay    = Text("直播回放",**kwargs).set_color(WHITE).scale(1)
        grp       = VGroup(name,time,replay).arrange(DOWN)
        max_width  = safe_rec.get_width() - 1
        grp.set_width(max_width)
        max_height = safe_rec.get_height() - 1
        if grp.get_height() > max_height:
            grp.set_height(max_height)
        grp.move_to(safe_rec)
        max_top  = np.array([0,3.4,0])
        name.shift(max_top-name.get_top())
        year     = Text(year,font='Freestyle Script')
        year.scale(2.3).set_color(color)
        line     = Underline(year,stroke_color=color)
        year_grp = VGroup(year,line)
        year_grp.next_to(time,RIGHT,aligned_edge=DOWN)
        self.add(year_grp,grp)

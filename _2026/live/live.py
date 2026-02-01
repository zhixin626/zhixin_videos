from manim_imports_custom import *
class live(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        im=ImageMobject("livefake.jpg")
        im.set_height(FRAME_HEIGHT)
        self.add(im)
        rec1=RoundedRectangle(1,4,corner_radius=0.4)
        rec1.set_stroke(WHITE,0,0)
        rec1.set_fill(WHITE,1)
        grp=rec1.replicate(3).arrange(RIGHT,buff=0.5)
        scale_factor = 0.1
        grp.scale(scale_factor).to_mob_corner(im,UL,buff=0.25)
        grp.add_background_rectangle("#e43472",buff=0.02)
        self.add(grp)

        def liveupdater(mob):
            # 1. 使用 sin 映射：(np.sin(t) + 1) / 2 的范围是 0 到 1
            # 加上 mob.offset 让三根柱子相位不同
            t = 5 * self.time + mob.offset
            percentage = (np.sin(t) + 1) / 2

            # 2. 设定高度范围，例如从 1 到 4 平滑过渡
            h = interpolate(1.0, 4.0, percentage)

            # 3. 重新创建以保持圆角 (Corner Radius)
            new_mob = RoundedRectangle(
                width=1,
                height=h,
                corner_radius=0.4
            ).match_style(rec1).scale(scale_factor)

            new_mob.move_to(mob.get_edge_center(DOWN), aligned_edge=DOWN)
            mob.become(new_mob)

        # 遍历数组，给每个柱子分配不同的初始相位 (Phase Offset)
        for i, bar in enumerate(grp[1:]):
            bar.offset = i * 0.8  # 这里的数值决定了它们跳动的“错位”程度
            bar.add_updater(liveupdater)
        self.wait(5)



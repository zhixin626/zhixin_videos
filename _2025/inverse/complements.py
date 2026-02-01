from manim_imports_custom import *

class Symbols(InteractiveScene):
    def construct(self):
        frame=self.frame
        light=self.camera.light_source

        # 1. 数据准备 (中文, 符号)
        title = Text("Fundamental Concepts of Linear Algebra", font_size=24)
        title.to_edge(UP).fix_in_frame()
        self.add(title)
        concepts = [
            ["Inverse", "逆", "A^{-1}"],
            ["Right Inverse", "右逆", "A^T (A A^T)^{-1}"],
            ["Left Inverse", "左逆", "(A^T A)^{-1} A^T"],
            ["Pseudo-inverse", "伪逆", r"A^{\dagger}"],
            ["Row Space", "行空间", r"\mathcal{C}(A^T)"],
            ["Column Space", "列空间", r"\mathcal{C}(A)"],
            ["Null Space", "零空间", r"\mathcal{N}(A)"],
            ["Left Null Space", "左零空间", r"\mathcal{N}(A^T)"],
        ]

        grp = VGroup()
        for i, (en, cn, sym) in enumerate(concepts):
            item = VGroup(
                Text(en, font_size=36),
                Text(cn, font='WenYue XinQingNianTi (Authorization Required)', font_size=42),
                Tex(sym, font_size=54, color=BLUE)
            ).arrange(DOWN, buff=0.4)
            alpha = i / max(1, len(concepts) - 1)
            item.set_color(interpolate_color(YELLOW,BLUE,alpha))
            grp.add(item)

        grp.arrange_in_grid(2, 4)

        for i, item in enumerate(grp):
            item.save_state()
            # 基础间距随索引增加，产生向四周扩散的透视感
            x_val = i * 0.6 + 1
            y_val = i * 0.3 + 0.1
            # i // 2 两两分组 i % 2 == 0 是左，i % 2 == 1 是右
            # (i // 2) % 2 == 0 是上，(i // 2) % 2 == 1 是下
            item.set_x(-x_val if i % 2 == 0 else x_val)
            item.set_y(y_val if (i // 2) % 2 == 0 else -y_val)
            item.set_z(i * 2)
            item.set_opacity(0.3)
        all_points = np.array([point for item in grp for point in item.get_all_corners()])
        center = all_points.mean(axis=0)
        x_range = all_points[:, 0].max() - all_points[:, 0].min()
        y_range = all_points[:, 1].max() - all_points[:, 1].min()
        max_range = max(x_range, y_range)
        frame_height = max_range * 1.2
        self.add(grp)
        self.frame.match_height(grp[0]).move_to(grp[0])
        self.play(
            self.frame.animate.move_to(center).set_height(frame_height),
            LaggedStart(*[item.animate.set_opacity(1) for item in grp],
                lag_ratio=5/len(grp)),
            run_time=5,rate_func=linear
        )
        self.play(
            *[item.animate.restore() for item in grp],
            self.frame.animate.to_default_state(),
            run_time=2
        )
        self.wait()

class TableOfContents(InteractiveScene):
    def construct(self):
        # start
        kwargs={"font":'WenYue XinQingNianTi (Authorization Required)'}
        items = VGroup(
            Text("Part 1: 输入空间和输出空间",**kwargs),
            Text("Part 2: 线性变换",**kwargs),
            Text("Part 3: 可逆",**kwargs),
            Text("Part 4: 不可逆",**kwargs),
            Text("Part 5: 不可逆中的可逆",**kwargs),
        )
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        items.set_height(FRAME_HEIGHT - 1)
        items.to_edge(LEFT)
        self.play(LaggedStartMap(FadeIn, items, shift=0.5 * LEFT, lag_ratio=0.1))
        self.wait()

        # Slow pan through
        items.save_state()
        highlight_points = Group()

        def update_item(item):
            y_diff = item.get_y() - item.highlight_point.get_y()
            alpha = np.exp(-(2 * y_diff)**2)
            item.set_height(interpolate(0.5, item.start_height, alpha), about_edge=LEFT)
            item.set_opacity(interpolate(0.5, 1, alpha))

        for item in items:
            item.start_height = item.get_height()
            item.highlight_point = Point(item.get_center())
            item.add_updater(update_item)

            highlight_points.add(item.highlight_point)

        self.play(
            *(item.highlight_point.animate.set_y(items[0].get_y()) for item in items),
            run_time=2
        )
        self.play(
            *(item.highlight_point.animate.set_y(-4) for item in items),
            run_time=7,
            rate_func=linear
        )
        self.play(
            *(item.highlight_point.animate.match_y(item) for item in items),
            run_time=2
        )
        self.wait()


        # One by one
        items.clear_updaters()
        for n in range(len(items)):
            items.target = items.generate_target()
            for k, item in enumerate(items.target):
                if k == n:
                    item.set_height(1, about_edge=LEFT).set_opacity(1)
                else:
                    item.set_height(0.5, about_edge=LEFT).set_opacity(0.5)
            self.play(MoveToTarget(items))
            self.wait()
        self.wait(2)
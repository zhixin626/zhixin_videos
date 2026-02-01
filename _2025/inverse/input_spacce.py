from manim_imports_custom import *
def split_group_by_axis(group, cuts, axis="y", descending=True):
    axis_idx = {"x": 0, "y": 1, "z": 2}[axis]
    cuts = sorted(cuts)

    coords = np.array([mob.get_center()[axis_idx] for mob in group])
    indices = np.digitize(coords, cuts)  # 0..len(cuts)

    subgroups = [Group() for _ in range(len(cuts) + 1)]
    for i, mob in zip(indices, group):
        subgroups[i].add(mob)

    if descending:
        subgroups = subgroups[::-1]

    return Group(*subgroups)
def get_random_points_vectorized(rect, n):
    center = rect.get_center()
    width = rect.get_width()
    height = rect.get_height()

    # 在 [-0.5, 0.5] 范围内生成随机矩阵，然后缩放和平移
    # (n, 3) 形状的数组，z 轴保持为 0
    random_offsets = np.random.uniform(-0.5, 0.5, (n, 3))
    random_offsets[:, 0] *= width   # 缩放 x
    random_offsets[:, 1] *= height  # 缩放 y
    random_offsets[:, 2] = 0        # 确保 z 轴为 0

    return center + random_offsets
class inputspace(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        def get_input_slots(matrix,buff=0.15,fill_color=BLUE_D,**kwargs):
            input_slots  = VGroup(Dot(col.get_top(),fill_color=fill_color,**kwargs) for col in matrix.columns)
            input_slots.move_to(matrix.get_top())
            input_slots.shift(UP*buff)
            input_slots.set_z_index(1)
            return input_slots
        def get_output_slots(matrix,buff=0.1,fill_color=ORANGE,**kwargs):
            output_slots = VGroup(Dot(row.get_right()+RIGHT*0.2,fill_color=fill_color,**kwargs) for row in matrix.rows)
            output_slots.move_to(matrix.get_right())
            output_slots.shift(RIGHT*buff)
            output_slots.set_z_index(1)
            return output_slots
        def get_col_rectangles(matrix,**kwargs):
            recs=VGroup(Rectangle(**kwargs).replace(col,stretch=True).scale(1.2) for col in matrix.columns)
            recs.set_fill(BLUE_D,0.5)
            recs.set_stroke(BLUE_D,0,0)
            return recs
        def get_row_rectangles(matrix,**kwargs):
            recs=VGroup(Rectangle(**kwargs).replace(row,stretch=True).scale(1.2) for row in matrix.rows)
            recs.set_fill(ORANGE,0.5)
            recs.set_stroke(ORANGE,0,0)
            return recs
        def get_matrix_body(matrix,color=GREY_A,opacity=0.8):
            rec=Rectangle().replace(matrix,stretch=True)
            rec.set_fill(color,opacity)
            rec.set_stroke(color,0,0)
            return rec

        # matrix
        arr    = np.array([[1,2,3],[4,5,6]])
        matrix = Matrix(arr).scale(2)
        matrix.brackets.set_z_index(1)
        body         = get_matrix_body(matrix,GREY_C).set_z_index(0)
        input_slots  = get_input_slots(matrix,buff=0)
        output_slots = get_output_slots(matrix,buff=0)
        col_rets     = get_col_rectangles(matrix)
        row_rets     = get_row_rectangles(matrix)
        self.add(matrix)
        self.play(LaggedStartMap(FadeIn,col_rets,shift=UP,lag_ratio=0.1),run_time=1)
        self.play(LaggedStart(
            *[ReplacementTransform(ret,slot)
            for ret,slot in zip(col_rets,input_slots)],lag_ratio=0.1,run_time=1))
        self.play(LaggedStartMap(FadeIn,row_rets,shift=RIGHT,lag_ratio=0.1),run_time=1)
        self.play(LaggedStart(
            *[ReplacementTransform(ret,slot)
            for ret,slot in zip(row_rets,output_slots)],lag_ratio=0.1,run_time=1))
        self.play(FadeIn(body))

        # show random vectors
        arrs_in=[
            np.array([[0.6],[0.2],[0.6]]),
            np.array([[1],[2],[1]]),
            np.array([[6],[2],[6]]),
            ]
        element_configs=[dict(num_decimal_places=1),{},{}]
        BUFFS=[0.3,0.3,0.3]
        arrs_out    = [np.dot(arr,arrs_in[i]) for i in range(len(arrs_in))]
        vectors_in  = VGroup(Matrix(arr,element_config=element_config) for arr,element_config in zip(arrs_in,element_configs))
        vectors_out = VGroup(Matrix(arr,element_config=element_config) for arr,element_config in zip(arrs_out,element_configs))
        for vector,buff in zip(vectors_in,BUFFS):
            vector.match_height(matrix)
            vector.next_to(matrix,RIGHT,buff=buff)
        for vector,buff in zip(vectors_out,BUFFS):
            vector.match_height(matrix)
            vector.next_to(matrix,RIGHT,buff=buff)
        for i in range(len(arrs_in)):
            self.play(FadeIn(vectors_in[i]))
            self.play(*[
                row.animate.move_to(slot).scale(0.3).set_anim_args(path_arc=PI*3/4,remover=True)
                for row,slot in zip(vectors_in[i].rows,input_slots)
                ],FadeOut(vectors_in[i].brackets))
            # particle anims
            particles=self.play_emit_particles(
                input_slots,DOWN,
                triangle_height=body.get_height(),
                triangle_base=body.get_width()/3,
                run_time=1)
            self.play(*[
                part.animate.move_to(p).set_color(ORANGE)
                for part, p in zip(particles, get_random_points_vectorized(body,len(particles)),
                    )],run_time=0.5)
            sorted_particles = split_group_by_axis(particles, [0], axis="y")
            self.play_absorb_particles(sorted_particles,output_slots,run_time=1)
            self.play(*[
                GrowFromPoint(row,slot.get_center())
                for row,slot in zip(vectors_out[i].rows,output_slots)
                ],FadeIn(vectors_out[i].brackets))
            self.wait()
            self.remove(vectors_out[i])





    def play_emit_particles(
        self,
        apex_positions,
        directions,
        run_time=1.5,
        flatten=True,
        **kwargs):
        if not isinstance(apex_positions,Group):
            apex_positions=[apex_positions]
        if isinstance(directions,np.ndarray):
            directions=[directions]*len(apex_positions)

        all_animations = []
        all_particle_groups = Group()

        for pos,direct in zip(apex_positions,directions):
            parts, poss = self.get_particles_in_triangle(pos, direct, **kwargs)
            all_particle_groups.add(parts)
            for part, pos in zip(parts, poss):
                all_animations.append(part.animate.move_to(pos).set_opacity(0.5))

        self.add(all_particle_groups)
        self.play(*all_animations, rate_func=rush_from, run_time=run_time)
        if flatten:
            particles=Group(*all_particle_groups.family_members_with_points())
            return particles
        else:
            return all_particle_groups

    def play_absorb_particles(self,
            particles,
            apex_positions,
            run_time=1.5):
        apex_list = list(apex_positions)
        if len(apex_list) < len(particles):
            needed = len(particles) - len(apex_list)
            apex_list += [apex_list[-1]] * needed
        all_animations = []
        for part,pos in zip(particles,apex_list):
            all_animations.append(part.animate.move_to(pos).set_opacity(0).scale(0.1))
        self.play(*all_animations, rate_func=rush_into, run_time=run_time)
        self.remove(particles)

    def get_particles_in_triangle(
        self,
        apex_pos,
        direction,
        num_particles=50,
        particle_color=BLUE_D,
        particle_radius=[0.05, 0.1],
        particle_glow=[0.1, 3],
        triangle_height=3.0,
        triangle_base=2.0
    ):
        """生成在三角形区域内均匀分布的粒子组 (Generate particle groups)"""
        if isinstance(apex_pos,Mobject):
            apex_pos=apex_pos.get_center()
        else:
            apex_pos=np.array(apex_pos)
        direction = normalize(direction)
        perpendicular = np.array([-direction[1], direction[0], 0])
        half_base = triangle_base / 2

        particles = Group()
        target_position = []

        # 参数处理内部函数
        get_color = lambda: particle_color if particle_color != "random" else random_bright_color()
        get_radius = lambda: np.random.uniform(*particle_radius) if isinstance(particle_radius, (list, tuple)) else particle_radius
        get_glow = lambda: np.random.uniform(*particle_glow) if isinstance(particle_glow, (list, tuple)) else particle_glow

        for _ in range(num_particles):
            # 重心坐标生成 (Barycentric coordinates)
            r1, r2 = np.random.random(), np.random.random()
            if r1 + r2 > 1:
                r1, r2 = 1 - r1, 1 - r2

            v1 = np.array([0, 0, 0])
            v2 = direction * triangle_height + perpendicular * half_base
            v3 = direction * triangle_height - perpendicular * half_base

            offset = v1 * (1 - r1 - r2) + v2 * r1 + v3 * r2
            target_position.append(offset+apex_pos)

            p = Group(GlowDot(color=get_color(), radius=get_radius(), glow_factor=get_glow()))
            p.move_to(apex_pos)
            particles.add(p)

        return particles, target_position

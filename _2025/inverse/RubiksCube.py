from manim_imports_custom import *
AXIS_TO_VEC = {"x": RIGHT, "y": UP, "z": OUT}

FACE = {
    "OUT":   0,  # +Z
    "IN":    5,  # -Z
    "RIGHT": 2,  # +X
    "LEFT":  4,  # -X
    "UP":    3,  # +Y
    "DOWN":  1,  # -Y
        }
DEFAULT_FACE_COLORS = {
    "OUT": BLUE,      # 前
    "IN":  GREEN,     # 后
    "RIGHT": RED,     # 右
    "LEFT": ORANGE,   # 左
    "UP": WHITE,      # 上
    "DOWN": YELLOW,   # 下
}

class RubiksCube(Group):
    """
    3x3x3 Rubik's Cube made of 27 cubies.

    Coordinates:
      i -> x (LEFT..RIGHT)  in {-1,0,1}
      j -> y (DOWN..UP)     in {-1,0,1}
      k -> z (IN..OUT)      in {-1,0,1}
    """

    def __init__(
        self,
        cubie_side: float = 2.0,
        gap: float = 0.2,
        face_colors= None,
        internal_color=BLACK,
        shading=(0, 0, 0),
        **kwargs
    ):
        super().__init__()

        self.cubie_side = float(cubie_side)
        self.gap = float(gap)
        self.pitch = self.cubie_side + self.gap
        self.internal_color = internal_color
        self.face_colors = dict(DEFAULT_FACE_COLORS)
        if face_colors:
            self.face_colors.update(face_colors)

        # (i,j,k) -> cubie(VGroup/Cube)
        self.cubies: Dict[Tuple[int, int, int], Cube] = {}

        self._build(shading=shading,**kwargs)

    # -------------------------
    # Build / coloring
    # -------------------------
    def _build(self, shading=(0, 0, 0),**kwargs):
        base = Cube(
            side_length=self.cubie_side,
            shading=shading,
            square_resolution=(5,5),**kwargs)

        # 给 base 六面上色（按 FACE 索引）
        base[FACE["OUT"]].set_color(self.face_colors["OUT"])
        base[FACE["IN"]].set_color(self.face_colors["IN"])
        base[FACE["RIGHT"]].set_color(self.face_colors["RIGHT"])
        base[FACE["LEFT"]].set_color(self.face_colors["LEFT"])
        base[FACE["UP"]].set_color(self.face_colors["UP"])
        base[FACE["DOWN"]].set_color(self.face_colors["DOWN"])

        # 生成 27 个 cubies
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                for k in [-1, 0, 1]:
                    cubie = base.copy()
                    cubie.shift(i * self.pitch * RIGHT + j * self.pitch * UP + k * self.pitch * OUT)
                    cubie.index = (i, j, k)
                    self._black_internal_faces(cubie, i, j, k)
                    self.cubies[(i, j, k)] = cubie
                    self.add(cubie)

    def _black_internal_faces(self, cubie: Cube, i: int, j: int, k: int):
        """
        规则：把“朝向中心”的面染黑；中层的两侧面都黑。
        """
        # x axis
        if i == 1:
            cubie[FACE["LEFT"]].set_color(self.internal_color)
        elif i == -1:
            cubie[FACE["RIGHT"]].set_color(self.internal_color)
        else:
            cubie[FACE["LEFT"]].set_color(self.internal_color)
            cubie[FACE["RIGHT"]].set_color(self.internal_color)

        # y axis
        if j == 1:
            cubie[FACE["DOWN"]].set_color(self.internal_color)
        elif j == -1:
            cubie[FACE["UP"]].set_color(self.internal_color)
        else:
            cubie[FACE["UP"]].set_color(self.internal_color)
            cubie[FACE["DOWN"]].set_color(self.internal_color)

        # z axis
        if k == 1:
            cubie[FACE["IN"]].set_color(self.internal_color)
        elif k == -1:
            cubie[FACE["OUT"]].set_color(self.internal_color)
        else:
            cubie[FACE["OUT"]].set_color(self.internal_color)
            cubie[FACE["IN"]].set_color(self.internal_color)

    def get_cubie(self, i: int, j: int, k: int) -> Cube:
        return self.cubies[(int(i), int(j), int(k))]

    def get_layer(self, axis: str, index: int) -> Group:
        """
        axis: 'x'|'y'|'z'
        index: -1|0|1
        """
        axis = axis.lower()
        assert axis in ("x", "y", "z")
        index = int(index)

        mobs = []
        for (i, j, k), cubie in self.cubies.items():
            if axis == "x" and i == index:
                mobs.append(cubie)
            elif axis == "y" and j == index:
                mobs.append(cubie)
            elif axis == "z" and k == index:
                mobs.append(cubie)

        return Group(*mobs)
    def rotate_layer(
        self,
        axis: str,
        index: int,
        quarter_turns: int = 1,
        clockwise: bool = True,
        about_point=ORIGIN,
        run_time: float = 0.8,
        rate_func=smooth,
    ):
        """
        返回一个 Animation（Rotate），你在 Scene 里 self.play(rubik.rotate_layer(...))
        然后它会在 play 结束后更新 self.cubies 的索引映射（你需要手动调用 finalize）。

        推荐用法：
          anim = rubik.rotate_layer("z", 1, quarter_turns=1, clockwise=True)
          self.play(anim)
          rubik.finalize_rotation("z", 1, quarter_turns=1, clockwise=True)

        这样把“动画”和“数据更新”拆开，最稳定。
        """
        axis = axis.lower()
        assert axis in ("x", "y", "z")
        index = int(index)
        q = int(quarter_turns) % 4
        if q == 0:
            return AnimationGroup()  # 空动画

        layer = self.get_layer(axis, index)

        # 角度：顺时针/逆时针（这里的 clockwise 是“从轴正方向看过去”的顺时针）
        sign = -1 if clockwise else 1
        angle = sign * q * (PI / 2)

        return Rotate(
            layer,
            angle=angle,
            axis=AXIS_TO_VEC[axis],
            about_point=about_point,
            run_time=run_time,
            rate_func=rate_func,
        )

    def finalize_rotation(self, axis: str, index: int, quarter_turns: int = 1, clockwise: bool = True):
        """
        在你 self.play(...) 之后调用：更新 cubies 的 (i,j,k) 索引映射。
        """
        axis = axis.lower()
        assert axis in ("x", "y", "z")
        index = int(index)

        q = int(quarter_turns) % 4
        if q == 0:
            return

        # 计算旋转映射：对 layer 内每个 (i,j,k) 做整数格点旋转
        sign = -1 if clockwise else 1  # 与 rotate_layer 保持一致

        new_map: Dict[Tuple[int, int, int], Cube] = dict(self.cubies)

        # 先找出这一层的 key
        layer_keys = []
        for key in self.cubies.keys():
            i, j, k = key
            if axis == "x" and i == index:
                layer_keys.append(key)
            elif axis == "y" and j == index:
                layer_keys.append(key)
            elif axis == "z" and k == index:
                layer_keys.append(key)

        # 从旧映射里移除 layer keys，重新写入
        for key in layer_keys:
            new_map.pop(key, None)

        def rot_once(i, j, k):
            # 90° 旋转：右手系；sign=-1 表示从轴正向看“顺时针”
            if axis == "x":
                # (j,k) 平面旋转
                return (i, -sign * k, sign * j)
            if axis == "y":
                # (i,k) 平面旋转
                return (sign * k, j, -sign * i)
            # axis == "z"
            return (-sign * j, sign * i, k)

        for key in layer_keys:
            cubie = self.cubies[key]
            i, j, k = key
            ni, nj, nk = i, j, k
            for _ in range(q):
                ni, nj, nk = rot_once(ni, nj, nk)

            ni, nj, nk = int(ni), int(nj), int(nk)
            cubie.index = (ni, nj, nk)
            new_map[(ni, nj, nk)] = cubie

        self.cubies = new_map

    def move(self, move: str, run_time: float = 0.8):
        move = move.strip()

        turns = 2 if move.endswith("2") else 1
        base = move[:-1] if move.endswith("2") else move

        table = {
            "R":  ("x",  1, True),
            "R'": ("x",  1, False),
            "L":  ("x", -1, False),
            "L'": ("x", -1, True),
            "U":  ("y",  1, True),
            "U'": ("y",  1, False),
            "D":  ("y", -1, False),
            "D'": ("y", -1, True),
            "F":  ("z",  1, True),
            "F'": ("z",  1, False),
            "B":  ("z", -1, False),
            "B'": ("z", -1, True),
        }

        if base not in table:
            raise ValueError(f"Unknown move: {move}")

        axis, idx, cw = table[base]

        anim = self.rotate_layer(
            axis,
            idx,
            quarter_turns=turns,
            clockwise=cw,
            run_time=run_time,
        )
        finalize_kwargs = dict(
            axis=axis,
            index=idx,
            quarter_turns=turns,
            clockwise=cw,
        )
        return anim, finalize_kwargs

class cube(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        frame.set_focal_distance(15)
        self.set_floor_plane("xz")
        frame.reorient(40, -32, 0, (0,-1,0), 11.93)
        ax = ThreeDAxesCustom((-8,8,1),(-7,4,1),(-8,8,1))
        ax.add_axis_labels()
        ax.apply_depth_test()
        # self.add(ax)
        rubiks = RubiksCube(cubie_side=2, gap=0.2, shading=(0, 0, 0),
            internal_color=GREY_D)
        self.add(rubiks)
        for cubie in rubiks:
            cubie._position=np.copy(cubie.get_center())
            cubie._angle=random.uniform(0,PI/2)
            cubie._axis=normalize(np.random.random(3))
            cubie.rotate(cubie._angle, cubie._axis)
            cubie.set_opacity(0.3)
        rubiks.space_out_submobjects(3)
        self.wait()
        self.play(*[
                cubie.animate.move_to(cubie._position)\
                .rotate(-cubie._angle, axis=cubie._axis)\
                .set_opacity(1)
                for cubie in rubiks
                ],run_time=2)

        frame.add_ambient_rotation(2*DEG)
        self.play(
            rubiks.get_layer("z", 1).animate.shift(0.5 * OUT),
            rubiks.get_layer("z", 0).animate.shift(0.5 * UP),
            rubiks.get_layer("z", -1).animate.shift(0.5 * IN),
            rate_func=there_and_back)
        self.play(
            rubiks.get_layer("x", 1).animate.shift(0.5 * RIGHT),
            rubiks.get_layer("x", 0).animate.shift(0.5 * UP),
            rubiks.get_layer("x", -1).animate.shift(0.5 * LEFT),
            rate_func=there_and_back)
        self.play(
            rubiks.get_layer("y", 1).animate.shift(0.5 * UP),
            rubiks.get_layer("y", 0).animate.shift(0.5 * OUT),
            rubiks.get_layer("y", -1).animate.shift(0.5 * DOWN),
            rate_func=there_and_back)


        self.play_cube(rubiks,"R U R' U' R' F R2 U' R' U' R U R' F'")
        self.play(frame.animate.increment_theta(1))
        self.wait()
        self.play_cube(rubiks,"F R U' R' U  R U  R2 F' R  U R U' R'")

        # self.play(*[Rotate(s,random.uniform(0,PI/2),axis=normalize(random.random(3)))
        #     for s in rubiks],
        #     rate_func=there_and_back)
        self.wait()
        frame.clear_updaters()


    def play_cube(self, rubiks: RubiksCube, alg, run_time=0.6):
        # alg 可以是 list[str] 或 "R U R' U'" 这种字符串
        if isinstance(alg, str):
            alg = alg.replace("’", "'").split()

        for mv in alg:
            anim, kw = rubiks.move(mv, run_time=run_time)
            self.play(anim)
            rubiks.finalize_rotation(**kw)





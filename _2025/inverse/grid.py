from manim_imports_custom import *
import sympy,scipy
from typing import List
class NumberGrid(ThreeDAxes):
    def __init__(
        self,
        x_range=(-8, 8, 1),
        y_range=(-6, 6, 1),
        z_range=(-6, 6, 1),
        background_line_interval=(8, 6, 6),
        faded_line_ratio=(1,1,1),
        background_line_style=dict(
            stroke_color=BLUE_D,
            stroke_width=3,
            stroke_opacity=0.8),
        faded_line_style=dict(
            stroke_color=BLUE_D,
            stroke_width=1,
            stroke_opacity=0.5),
        **kwargs
    ):
        super().__init__(x_range, y_range, z_range, **kwargs)

        # 处理间隔参数
        if isinstance(background_line_interval, (int, float)):
            self.bg_intervals = [background_line_interval] * 3
        else:
            self.bg_intervals = background_line_interval

        # 处理细分比例
        if isinstance(faded_line_ratio, int):
            self.faded_line_ratio = [faded_line_ratio] * 3
        else:
            self.faded_line_ratio = faded_line_ratio

        self.background_line_style = background_line_style
        self.faded_line_style = faded_line_style

        self.parallel_to_axis = [VGroup() for _ in range(3)]
        self.background_lines = VGroup()
        self.faded_lines = VGroup()

        self.init_grid()

    def init_grid(self):
        ranges = [self.x_range, self.y_range, self.z_range]
        for i in range(3):
            other_dims = [j for j in range(3) if j != i]
            self._generate_lines(
                axis_idx=i,
                range1=ranges[other_dims[0]],
                range2=ranges[other_dims[1]],
                range_main=ranges[i],
                other_indices=other_dims
            )

        self.background_lines.set_style(**self.background_line_style)
        self.faded_lines.set_style(**self.faded_line_style)
        self.add_to_back(self.faded_lines, self.background_lines)

    def _generate_lines(self, axis_idx, range1, range2, range_main, other_indices):
        # 获取对应维度的背景线间隔
        bg_interval1 = self.bg_intervals[other_indices[0]]
        bg_interval2 = self.bg_intervals[other_indices[1]]

        # 获取细分比例
        ratio1 = self.faded_line_ratio[other_indices[0]]
        ratio2 = self.faded_line_ratio[other_indices[1]]

        # 计算实际生成的步长：基于自定义的 bg_interval 而非 range[2]
        step1 = bg_interval1 / (1 + ratio1)
        step2 = bg_interval2 / (1 + ratio2)

        # 确定生成范围
        num1 = int(round((range1[1] - range1[0]) / step1)) + 1
        num2 = int(round((range2[1] - range2[0]) / step2)) + 1
        vals1 = np.linspace(range1[0], range1[1], num1)
        vals2 = np.linspace(range2[0], range2[1], num2)

        for v1 in vals1:
            for v2 in vals2:
                # 跳过原点附近的轴线（由父类处理）
                if abs(v1) < 1e-8 and abs(v2) < 1e-8:
                    continue

                p_start, p_end = np.zeros(3), np.zeros(3)
                p_start[other_indices[0]], p_start[other_indices[1]] = v1, v2
                p_end[other_indices[0]], p_end[other_indices[1]] = v1, v2
                p_start[axis_idx], p_end[axis_idx] = range_main[0], range_main[1]

                line = Line(self.c2p(*p_start), self.c2p(*p_end))
                line.axis_idx = axis_idx
                line.fixed_values = {other_indices[0]: v1, other_indices[1]: v2}

                # 关键修改：使用自定义的 bg_interval 判断是否为背景线
                eps = 1e-8
                is_v1_main = abs(((v1 - range1[0]) / bg_interval1) - round((v1 - range1[0]) / bg_interval1)) < eps
                is_v2_main = abs(((v2 - range2[0]) / bg_interval2) - round((v2 - range2[0]) / bg_interval2)) < eps

                if is_v1_main and is_v2_main:
                    line.line_type = "background"
                    self.background_lines.add(line)
                else:
                    line.line_type = "faded"
                    self.faded_lines.add(line)

                self.parallel_to_axis[axis_idx].add(line)

    def _classify_line(self, line, v1, v2):
        is_v1_main = abs(v1 % 1.0) < 1e-8
        is_v2_main = abs(v2 % 1.0) < 1e-8

        if abs(v1) < 1e-8 and abs(v2) < 1e-8:
            self.grid_axes_lines.add(line)
        elif is_v1_main and is_v2_main:
            self.background_lines.add(line)
        else:
            self.faded_lines.add(line)

    def get_parallel_lines(self, axis, line_type="all"):
        """
        axis: 'x', 'y', 'z' 或 0, 1, 2
        line_type: 'all', 'background' (或 'bg'), 'faded'
        """
        axis_map = {'x': 0, 'y': 1, 'z': 2, 0: 0, 1: 1, 2: 2}
        idx = axis_map.get(str(axis).lower() if isinstance(axis, str) else axis)

        if idx is None:
            raise ValueError("Invalid axis")

        lines = self.parallel_to_axis[idx]

        if line_type == "all":
            return lines

        # 转换为小写并支持简写
        lt = line_type.lower()
        if lt in ["background", "bg"]:
            return VGroup(*[l for l in lines if l.line_type == "background"])
        elif lt == "faded":
            return VGroup(*[l for l in lines if l.line_type == "faded"])
        else:
            raise ValueError("line_type must be 'all', 'background', or 'faded'")


    def get_plane_grid(self, axis, constant_val):
        """
        axis: 垂直于哪个轴 (x, y, 或 z)
        constant_val: 该轴上的固定坐标值
        """
        axis_map = {'x': 0, 'y': 1, 'z': 2, 0: 0, 1: 1, 2: 2}
        idx = axis_map.get(str(axis).lower() if isinstance(axis, str) else axis)

        if idx is None:
            raise ValueError("无效的 axis")

        plane_lines = VGroup()

        # 稍微放宽一点阈值，或者使用 math.isclose
        eps = 1e-7

        # 我们只需要检查平行于另外两个轴的线
        other_dims = [i for i in range(3) if i != idx]

        for d in other_dims:
            for line in self.parallel_to_axis[d]:
                # 检查这条线在‘垂直轴’上的固定坐标是否匹配请求的 constant_val
                if abs(line.fixed_values[idx] - constant_val) < eps:
                    plane_lines.add(line)
        if len(plane_lines) == 0:
            print(f"提示：在 {axis}={constant_val} 处未找到网格线。请检查该坐标是否符合网格步长设定。")
        return plane_lines

    def get_lines_at_point(self, x, y, z):
        """获取交汇于 (x,y,z) 的三条线"""
        point_lines = VGroup()
        coords = [x, y, z]
        for i in range(3): # 平行于 i 轴的线
            other_dims = [j for j in range(3) if j != i]
            for line in self.parallel_to_axis[i]:
                # 检查另外两个维度的固定值是否匹配
                if abs(line.fixed_values[other_dims[0]] - coords[other_dims[0]]) < 1e-8 and \
                   abs(line.fixed_values[other_dims[1]] - coords[other_dims[1]]) < 1e-8:
                    point_lines.add(line)
        return point_lines


def get_rref_history(matrix: sympy.Matrix|np.ndarray)-> List[sympy.Matrix]:
    matrix=_ensure_sympy_matrix(matrix)
    A = matrix.copy()
    rows, cols = A.shape
    history = []
    pivot_row = 0

    for j in range(cols): # 遍历每一列
        if pivot_row >= rows:
            break
        # 1. 寻找当前列绝对值最大的行（为了数值稳定性，符号计算中找首个非0即可）
        target_row = pivot_row
        while target_row < rows and A[target_row, j] == 0:
            target_row += 1
        if target_row == rows: # 当前列全为0，跳过处理下一列
            continue
        # --- 执行行交换 ---
        if target_row != pivot_row:
            A = A.elementary_row_op("n<->m", row1=pivot_row, row2=target_row)
        # --- 执行归一化 (让主元变为 1) ---
        pivot_val = A[pivot_row, j]
        if pivot_val != 1:
            A = A.elementary_row_op("n->kn", row=pivot_row, k=1/pivot_val)
        # --- 执行消元 (让该列其他行变为 0) ---
        for i in range(rows):
            if i != pivot_row:
                factor = A[i, j]
                if factor != 0:
                    A = A.elementary_row_op("n->n+km", row1=i, row2=pivot_row, k=-factor)
        # 完成一列的处理，记录当前矩阵状态
        history.append(A.copy())
        pivot_row += 1

    return history



def create_manim_matrix(sp_mat: sympy.Matrix, **kwargs):
    data = [[Tex(sympy.latex(x)) for x in row] for row in sp_mat.tolist()]
    return Matrix(data, **kwargs)

def _ensure_sympy_matrix(mat):
    if isinstance(mat, np.ndarray):
        return sympy.Matrix(mat)
    return mat

def get_colspace_matrix(sp_mat: sympy.Matrix|np.ndarray):
    sp_mat = _ensure_sympy_matrix(sp_mat)
    basis_vectors = sp_mat.columnspace()
    if not basis_vectors:
        return np.array([[]])
    np_basis = [np.array(v.tolist(), dtype=float) for v in basis_vectors]
    return np.hstack(np_basis)

def get_nullspace_matrix(sp_mat: sympy.Matrix|np.ndarray):
    sp_mat = _ensure_sympy_matrix(sp_mat)
    basis_vectors = sp_mat.nullspace()
    if not basis_vectors:
        return np.zeros((sp_mat.cols, 0))
    np_basis = [np.array(v.tolist(), dtype=float) for v in basis_vectors]
    return np.hstack(np_basis)

def get_rowspace_matrix(sp_mat: sympy.Matrix|np.ndarray):
    sp_mat = _ensure_sympy_matrix(sp_mat)
    basis_vectors = sp_mat.rowspace()
    if not basis_vectors:
        return np.array([[]])
    np_basis = [np.array(v.tolist(), dtype=float).T for v in basis_vectors]
    return np.hstack(np_basis)

class showrref_history(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # sympy
        arr=np.array([[1,2,3],[4,5,6],[7,8,9]])
        matrix=Matrix(arr)
        rref_matrices=VGroup(create_manim_matrix(his) for his in get_rref_history(arr))
        rref_matrices.arrange(RIGHT).next_to(matrix,DOWN)
        self.add(matrix,rref_matrices)
        sympy.pprint(sympy.Matrix(matrix.raw_matrix).rref(pivots=False))

        # svd
        arr = [[3, 0], [0, -2]]
        U,S,V=sympy.Matrix(arr).singular_value_decomposition() # 慎用：超过3*3将巨慢
        svd_grp=VGroup(create_manim_matrix(m) for m in [U,S,V.T])
        svd_grp.arrange(RIGHT).to_edge(UP)
        self.add(svd_grp)

class creategrid(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        grid=get_grid()
        frame.reorient(0, 0, 0, (0.64, 0.2, 0.0), 14.62)
        for line in grid[1].background_lines:
            line.reverse_points()
        self.play(
            Write(grid[0],stroke_color=WHITE),
            Write(grid[1].faded_lines,stroke_color=RED),
            Write(grid[1].background_lines,stroke_color=GREEN),
            Write(grid[1].axes,stroke_color=PURPLE),
            frame.animate.reorient(12, 56, 0, (1.5, 1.12, -1.31), 25.89))
        self.wait()


def get_grid():
    grid3d=NumberGrid(
        x_range=(-10,10,1),
        y_range=(-8,8,1),
        z_range=(-8,8,1),
        background_line_interval=(20,16,8),
        faded_line_ratio=(1,1,1))
    grid2d=NumberPlane(
        x_range=(-10,10,5),
        y_range=(-8,8,4),
        background_line_style=grid3d.background_line_style,
        faded_line_style=grid3d.faded_line_style)
    grid2d.set_opacity(0.5)
    grid3d.add_axis_labels(font_size=100,buff=0.5)
    return VGroup(grid2d,grid3d)


class nullspacce(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        arr1 = np.array([[1, 0,0], [0,1,0], [1,1,0]])
        col_mat = get_colspace_matrix(arr1)
        null_mat= get_nullspace_matrix(arr1)
        leftnull_mat= get_nullspace_matrix(arr1.T)
        row_mat = get_rowspace_matrix(arr1)
        plane=NumberPlane(background_line_style=dict(
            stroke_width=1,stroke_opacity=0.5,
            stroke_color=BLUE_D))
        grid=NumberGrid()
        self.frame.reorient(5, 41, 0, (2.05, 1.38, -0.17), 23.29)
        self.add(grid)
        col_space=plane.copy().apply_matrix(col_mat)
        row_space=plane.copy().apply_matrix(row_mat)
        col_space.set_color(YELLOW)
        row_space.set_color(RED)
        self.add(col_space)
        self.add(row_space)
        self.play(grid.animate.apply_matrix(arr1))
        self.play(row_space.animate.apply_matrix(arr1))

class GridScene(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source

        # grid
        def get_space_vectors(space_array:np.ndarray, color_list=[BLUE, GREEN, RED]):
            num_vectors = space_array.shape[1]
            vectors_grp = VGroup()
            for i in range(num_vectors):
                raw_vec = space_array[:, i]
                norm_vec = normalize(raw_vec)
                v = Vector(norm_vec, fill_color=color_list[i % len(color_list)])
                vectors_grp.add(v)
            if num_vectors >= 2:
                v1 = vectors_grp[0].get_vector()
                v2 = vectors_grp[1].get_vector()
                target_normal = normalize(np.cross(v1, v2))
                for v in vectors_grp:
                    v.apply_matrix(rotation_between_vectors(v.get_unit_normal(), target_normal))
            return vectors_grp
        def get_space(space_array:np.ndarray,**kwargs):
            num_vectors = space_array.shape[1]
            if num_vectors ==1:
                space   = NumberLine(**kwargs)
            elif num_vectors ==2:
                space   = NumberPlane(**kwargs)
            else:
                space   = NumberGrid(**kwargs)
            space.apply_matrix(space_array)
            return space

        # build space
        grid2d,grid3d = grid =get_grid()
        grid2d.save_state()
        arr           = np.array([[1,0,0],[0,1,0],[2,1,0]])
        colspace      = get_colspace_matrix(arr)
        nullspace     = get_nullspace_matrix(arr)
        rowspace      = get_rowspace_matrix(arr)
        leftnullspace = get_nullspace_matrix(arr.T)
        vts_col       = get_space_vectors(colspace)
        vts_null      = get_space_vectors(nullspace)
        vts_row       = get_space_vectors(rowspace)
        vts_leftnull  = get_space_vectors(leftnullspace)
        sp_col        = get_space(colspace)
        sp_null       = get_space(nullspace)
        sp_row        = get_space(rowspace)
        sp_leftnull   = get_space(leftnullspace)

        self.frame.reorient(9, 51, 0, (0.84, 2.25, -0.48), 6.36)
        self.add(grid2d)
        self.add(vts_col)
        self.add(vts_row)
        self.add(vts_null)
        self.add(vts_leftnull)

        self.add(sp_row)
        self.add(sp_col)
        self.add(sp_null)
        self.add(sp_leftnull)

        self.play(grid2d.animate.apply_matrix(arr))
        self.play(grid2d.animate.restore())
        self.play(sp_row.animate.apply_matrix(arr))







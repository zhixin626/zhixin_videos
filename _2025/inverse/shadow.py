from manim_imports_custom import *
from _2025.sphere.useful import ConePatched,CylinderCustom
import scipy
EARTH_TEXTURE="D:/Grant/images/raster/EarthTextureMap.jpg"
NIGHT_EARTH_TEXTURE="D:/Grant/images/raster/NightEarthTextureMap.jpg"
EARTH_TILT_ANGLE = 23.3 * DEG

def get_convex_hull(mobject):
    points = mobject.get_all_points()
    hull = scipy.spatial.ConvexHull(points[:, :2])
    hull_points = points[hull.vertices].copy()  # 建议 copy，避免连带改 points
    hull_points[:, 2] = 0                       # z 投影到 0
    return hull_points

class light_shadow(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        self.light=self.camera.light_source
        # setup
        axis_config={
            "stroke_color":GREY_A,
            "stroke_width":0.2,
            "stroke_opacity":0.2}
        grid=NumberPlane((-8,8,1),
            axis_config=axis_config,
            background_line_style=axis_config,
            faded_line_style={
            "stroke_color":GREY_A,
            "stroke_width":0.05,
            "stroke_opacity":0.05}
            )
        plane=Surface(color=GREY_A,opacity=0.3,resolution=(100,100))
        plane.replace(grid,stretch=True)
        frame.reorient(3, 63, 0, (0.67, 0.96, 1.48), 6.71)
        self.add(plane)

        # start
        sphere=Sphere(prefered_creation_axis=0)
        sphere.always_sort_to_camera(self.camera)
        sphere.set_opacity(0.8)
        sphere.shift(OUT*2.5)
        self.add(sphere)
        self.play(ShowCreation(sphere))

        shadow=self.get_shadow_outline(sphere,
            stroke_color=BLUE,stroke_opacity=0.1,
            fill_color=BLUE,fill_opacity=0.1)
        light_lines=self.get_light_lines(shadow,
            opacity=0.2,width=0.2,color=BLUE)
        self.add(light_lines)
        self.play(*[Write(line) for line in light_lines],
            FadeIn(shadow,time_span=[1,1.5]),run_time=1.5)

        # remove sphere
        self.play(FadeOut(sphere))

        # show cannot recover
        cone=ConePatched(1).move_to(sphere)
        hyp1s=Hyperboloid1S().move_to(sphere)
        cylinder=CylinderCustom(1).move_to(sphere)

        frame.add_ambient_rotation(1*DEG)
        self.wait()
        self.add(cone)
        self.remove(sphere)
        self.wait()
        self.add(cylinder)
        self.remove(cone)
        self.wait()
        self.add(hyp1s)
        self.remove(cylinder)
        self.wait()
        frame.clear_updaters()

    def get_shadow_outline(self,mob, stroke_width=1,**kwargs):
        outline = VMobject()
        outline.set_style(**kwargs)
        hull_points = get_convex_hull(mob)          # (N,3)，z 已经是 0
        outline.set_points_as_corners(hull_points).close_path()
        return outline
    def get_light_lines(
            self,outline,
            inf_light=True,
            n_lines=100,
            only_vertices=False,
            **kwargs
        ):
        def update_lines(lines):
            lp = self.light.get_center()
            if only_vertices:
                points = outline.get_vertices()
            else:
                points = [outline.pfp(a) for a in np.linspace(0, 1, n_lines)]
            for line, point in zip(lines, points):
                if inf_light:
                    line.set_points_as_corners([point + 10 * OUT, point])
                else:
                    line.set_points_as_corners([lp, point])
        line = Line(IN, OUT)
        line.insert_n_curves(100)
        light_lines = line.replicate(n_lines)
        light_lines.set_stroke(**kwargs)
        update_lines(light_lines)
        return light_lines

class Hyperboloid1S(ParametricSurface):
    # 核心：指向你创建的新文件夹
    # shader_folder: str = "custom"

    def __init__(
        self,
        waist_R=0.5,
        top_R=1.0,
        height=1.0,
        u_range=None,
        v_range=(0, TAU),
        **kwargs
    ):
        self.waist_R = waist_R
        self.top_R = top_R
        self.height = height

        # 计算数学参数
        self.u_max = np.arccosh(top_R / waist_R)
        actual_u_range = u_range if u_range else (-self.u_max, self.u_max)
        self.c_param = height / np.sinh(self.u_max)

        # 初始化父类，传入参数化函数
        super().__init__(
            uv_func=self.uv_func,
            u_range=actual_u_range,
            v_range=v_range,
            **kwargs
        )
    def uv_func(self, u, v):
        x = self.waist_R * np.cosh(u) * np.cos(v)
        y = self.waist_R * np.cosh(u) * np.sin(v)
        z = self.c_param * np.sinh(u)
        return np.array([x, y, z])




class earth(light_shadow):
    def construct(self):
        # init
        frame=self.frame
        light=self.camera.light_source
        # start
        ax=ThreeDAxes()
        ax.add_axis_labels()
        self.add(ax)
        glow=GlowDot()
        glow.always.move_to(light)
        self.add(glow)
        def get_earth(radius=1.0):
            sphere = Sphere()
            earth = TexturedSurface(sphere, EARTH_TEXTURE,NIGHT_EARTH_TEXTURE)
            earth.rotate(-EARTH_TILT_ANGLE, UP)
            return earth
        def get_celestial_sphere(radius=1000, constellation_opacity=0.1,
            t1="D:/Grant/images/raster/hiptyc_2020_8k",
            t2="D:/Grant/images/raster/constellation_figures"):
            sphere = Group(
                TexturedSurface(Sphere(radius=radius, clockwise=True), t1),
                TexturedSurface(Sphere(radius=0.99 * radius, clockwise=True), t2),
            )
            sphere.set_shading(0, 0, 0)
            sphere[1].set_opacity(constellation_opacity)
            sphere.rotate(-EARTH_TILT_ANGLE, UP)
            return sphere
        earth=get_earth()
        earth_axis = rotate_vector(OUT, -EARTH_TILT_ANGLE,UP)
        earth.add_updater(lambda m, dt: m.rotate(dt * 10 * DEG, axis=earth_axis))
        axis=Line(ORIGIN,earth_axis*1000)
        light.move_to(LEFT*10)
        universe=get_celestial_sphere()
        self.frame.reorient(3, 70, 0, (-0.09, 0.17, 0.36), 3.50)
        self.add(universe)
        self.add(earth)
        self.add(axis)
        self.wait(5)
        self.play(frame.animate.move_to(axis.get_end()),run_time=3)
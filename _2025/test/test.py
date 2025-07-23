from manim_imports_custom import *
class test(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        ax=ThreeDAxesCustom()
        ax.add_axis_labels()
        RANGE=5
        def gauss2d(x, y, mu_x=0, mu_y=0, sigma_x=1, sigma_y=1, A=1):
            x_term = ((x - mu_x) ** 2) / (2 * sigma_x**2)
            y_term = ((y - mu_y) ** 2) / (2 * sigma_y**2)
            return A * np.exp(-(x_term + y_term))
        sf=ax.get_parametric_surface(
            lambda u, v: ax.c2p(u, v, gauss2d(u, v, mu_x=0, mu_y=0, sigma_x=1, sigma_y=1)),
            u_range=(-RANGE,RANGE),
            v_range=(-RANGE,RANGE),
            opacity=0.6)
        N=5
        sfs=Group(
            *[ax.get_parametric_surface(
            lambda u, v: ax.c2p(u, v, gauss2d(u, v, mu_x=0, mu_y=0, sigma_x=sigma, sigma_y=sigma)),
            u_range=(-RANGE,RANGE),
            v_range=(-RANGE,RANGE),
            opacity=0.6)
            for sigma in [i / N for i in range(1, N + 1)]])
        frame.reorient(30, 56, 0, (-0.01, 0.23, 0.2), 9.43)
        self.add(ax)
        self.add(sf)
        # for i in range(N):
        #     self.play(Transform(sf,sfs[i]))
class spiral_of_archimedes(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        ax=ThreeDAxesCustom()
        a = 0.2
        func=lambda t: [
                a * t * np.cos(t),
                a * t * np.sin(t),
                0
            ]
        spiral = ParametricCurve(
            lambda t:ax.c2p(*func(t)),
            t_range=(0, 6 * PI, 0.05),
            color=YELLOW
        )
        self.add(spiral)
        self.add(ax)
        self.play(ShowCreation(spiral))
class cardioid(InteractiveScene): # 心形线
    def construct(self):
        # init
        frame=self.frame
        # start
        a=2
        def func(t):
            x=a*(np.cos(t)+np.cos(t)**2)
            y=a*(np.sin(t)+np.sin(t)*np.cos(t))
            z=0
            return x,y,z
        ax=ThreeDAxesCustom()
        cardioid = ParametricCurve(
            lambda t:ax.c2p(*func(t)),
            t_range=(0, 2 * PI, 0.05),
            color=YELLOW
        )
        self.add(cardioid,ax)

class CartesianHeart(InteractiveScene): # 心形线
    def construct(self):
        # init
        frame=self.frame
        # start
        def heart_function(x, y):
            return (x**2 + y**2 - 1)**3 - x**2 * y**3
        ax=ThreeDAxesCustom()
        heart_curve = ImplicitFunction(
            func=heart_function,
            color=RED,
            stroke_width=2,
        )
        self.add(heart_curve,ax)
from manim_imports_custom import *
class col_space(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        camera=self.camera
        # start
        ax=ThreeDAxesCustom()
        ax.add_axis_labels()
        self.add(ax)
        sf=ParametricSurface(
            uv_func=lambda a,b:ax.c2p(
                a,b,-a+2*b),
            u_range=(-5,5),
            v_range=(-5,5),
            resolution=(100,100),
            opacity=0.5
            )
        self.add(sf)
        cube=Cube(side_length=10,opacity=0.3,square_resolution=(20,20))
        self.add(cube)
        frame.reorient(37, 66, 0, (0.34, 0.18, -0.69), 20.29)

        # clip plane
        sf.set_clip_plane(np.array([0,0,1
            ]),threshold=5)




from manim_imports_custom import*

class testcomplex(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        def cos(theta):
            return np.cos(theta)
        def sin(theta):
            return np.sin(theta)
        def exp(theta):
            return [theta,cos(theta),sin(theta)]

        ax=ThreeDAxesCustom()
        ax.add_axis_labels()
        points=np.array([*[exp(theta) for theta in np.arange(0,2*TAU,0.1)]])
        curve=VMobject()
        curve.set_points_as_corners(ax.c2p(*points.T))
        self.add(ax)
        self.add(curve)
        self.play(frame.animate.reorient(0, 90, 0))
        self.play(frame.animate.reorient(90, 90, 0))
        self.play(frame.animate.set_focal_distance(1000))
        self.play(frame.animate.to_default_state())
        self.play(frame.animate.reorient(0, 90, 0))
        self.play(frame.animate.reorient(90, 90, 0))

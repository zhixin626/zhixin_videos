from manim_imports_custom import *

class video1(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame

        # init_func
        T=5
        W=TAU*0.5    # w/TAU circles every T seconds
        def get_phi(mob):
            phi=mob.get_x()
            return phi
        def f(t,phi):
            w=W/T
            return w*t+phi
        def updater(mob,alpha):   # z = sin( w*t+f(x) )
            t=alpha*T
            phi=get_phi(mob)
            x=f(t,phi)
            # mob.set_x(x)
            mob.set_z(np.sin(x))
        def updater2(mob,dt):   # dt updater form
            mob.wtime+=dt
            t=mob.wtime
            phi=get_phi(mob)
            x=f(t,phi)
            # mob.set_x(x)
            mob.set_z(np.sin(x))
        # mat_init
        np.random.seed(41)
        arr=np.random.randint(-20,20,(20,20))
        mat=Matrix(arr,height=6.28)
        mat.set_color(TEAL)
        mat.set_width(10)
        def mat_set_z(mob):
            return mob.animate.set_z(np.sin(mob.get_x()))
        def generate_shift1():
            np.random.seed(None)
            random_vector = 2 * np.random.rand(2) - 1
            normalized_vector = random_vector / np.linalg.norm(random_vector) 
            return np.array([*normalized_vector * 2, 0]) 
        def generate_shift2():
            np.random.seed(None)
            random_vector = 2 * np.random.rand(3) - 1
            normalized_vector = random_vector / np.linalg.norm(random_vector) 
            return normalized_vector*2 
        grp=[]
        for submob in VGroup(*mat.elements).shuffle():
            rand_vec=generate_shift2()
            grp.append(FadeIn(submob,shift=rand_vec))
        self.wait()
        self.play(AnimationGroup(*grp,lag_ratio=0.02),
            FadeIn(mat.brackets[0],shift=RIGHT),
            FadeIn(mat.brackets[1],shift=LEFT),run_time=5)

        # add updater

        self.play(LaggedStartMap(mat_set_z,mat.elements,run_time=2),
                  LaggedStartMap(mat_set_z,mat.brackets,run_time=2),
                  frame.animate.reorient(-1, 25, 0, (-0.51, -0.24, -0.57), 8.00),
                  run_time=1)
        for submob in mat:
            submob.wtime=0
            submob.add_updater(updater2)
        self.wait(5)

        # text
        text=TextCustom(en='Matrix',ch='矩阵')
        text.scale(2)
        self.play(frame.animate.to_default_state())
        self.play(Write(text.en),Write(text.ch),run_time=2)
        self.wait(2)
        self.play(FadeOut(mat,shift=RIGHT*3),text.animate.to_edge(LEFT).scale(0.7))


        # svgs
        text1=TextCustom(en='Data Repository',ch='数据仓库',aligned_edge=LEFT)
        text2=TextCustom(en='Architect of Spaces',ch='空间建筑师',aligned_edge=LEFT)
        text3=TextCustom(en='Linear Transformation Wizard',ch='线性变换魔法师',aligned_edge=LEFT)
        text1.scale(0.6)
        text2.scale(0.6)
        text3.scale(0.6)
        grp_texts=VGroup(text1,text2,text3)
        grp_texts.arrange(DOWN)

        svg1=SVGMobject('warehouse.svg',stroke_color=WHITE,stroke_opacity=1,stroke_width=3,
            fill_color=PURPLE_B,fill_opacity=0.3)
        svg2=SVGMobject('hypercube.svg',stroke_color=WHITE,stroke_opacity=1,stroke_width=3,
            fill_color=WHITE,fill_opacity=0.1)
        svg3=SVGMobject('magician.svg',stroke_color=WHITE,stroke_opacity=1,stroke_width=3,
            fill_color=PURPLE_B,fill_opacity=0.3)

        grp_svgs=VGroup(svg1,svg2,svg3)
        grp_svgs.arrange(DOWN)
        grp_svgs.center().shift(LEFT)
        svg1.scale(0.7)
        svg2.scale(0.8)
        svg3.scale(0.9)
        grp_texts.to_edge(RIGHT)
        text1.next_to(svg1,RIGHT,buff=0.8)
        text2.next_to(svg2,RIGHT,buff=0.8).align_to(text1,LEFT)
        text3.next_to(svg3,RIGHT,buff=0.8).align_to(text1,LEFT)
        ax=ThreeDAxesCustom()
        floor=VMobject().set_points_as_corners([ax.c2p(-3,2,0),ax.c2p(0,4,0),ax.c2p(3,2,0)])
        floor.add_arc_to(ax.c2p(3.25,2.25,0),angle=PI)
        floor.add_line_to(ax.c2p(0,4.5,0))
        floor.add_line_to(ax.c2p(-3.25,2.25,0))
        floor.add_arc_to(ax.c2p(-3,2,0),angle=PI)
        sq1=Square(1)
        sq1.move_to(np.array([0,0.5,0]))
        sq2=sq1.copy()
        sq2.shift(RIGHT*1.5)
        sq3=sq1.copy()
        sq3.shift(LEFT*1.5)
        sq4=sq1.copy()
        sq4.move_to(np.array([-0.75,2,0]))
        sq5=sq1.copy()
        sq5.move_to(np.array([0.75,2,0]))
        goods=VGroup(sq1,sq2,sq3,sq4,sq5)
        repo=VGroup(floor,goods)
        repo.scale(0.3)
        repo.move_to(svg1)

        self.play( LaggedStart(DrawBorderThenFill(repo),Write(text1),lag_ratio=0.3) )
        self.play(sq1.animate.move_to(sq3),sq3.animate.move_to(sq4),
            sq4.animate.move_to(sq5),sq5.animate.move_to(sq2),sq2.animate.move_to(sq1))
        self.play(sq1.animate.move_to(sq3),sq3.animate.move_to(sq4),
            sq4.animate.move_to(sq5),sq5.animate.move_to(sq2),sq2.animate.move_to(sq1))


        # hyper_cube
        def get_cube(length):
            ax=ThreeDAxesCustom()
            point1=ax.c2p(-length/2,-length/2,length/2)
            point2=ax.c2p(-length/2,length/2,length/2)
            point3=ax.c2p(length/2,length/2,length/2)
            point4=ax.c2p(length/2,-length/2,length/2)
            point5=ax.c2p(-length/2,-length/2,-length/2)
            point6=ax.c2p(-length/2,length/2,-length/2)
            point7=ax.c2p(length/2,length/2,-length/2)
            point8=ax.c2p(length/2,-length/2,-length/2)
            line1=Line(point1,point2)
            line2=Line(point2,point3)
            line3=Line(point3,point4)
            line4=Line(point4,point1)
            line5=Line(point5,point6)
            line6=Line(point6,point7)
            line7=Line(point7,point8)
            line8=Line(point8,point5)
            line9=Line(point1,point5)
            line10=Line(point2,point6)
            line11=Line(point3,point7)
            line12=Line(point4,point8)
            points=[point1,point2,point3,point4,point5,point6,point7,point8]
            cube=VGroup(line1,line2,line3,line4,line5,line6,line7,line8,line9,line10,line11,line12)
            return cube,points
        cube1,points1=get_cube(1)     
        cube2,points2=get_cube(2)
        hyberlines=VGroup()
        hyber_lines=VGroup(*[ Line(points1[i],points2[i])for i in range(len(points1))])
        for i,line in enumerate(hyber_lines):
            line.add_updater(lambda m,i=i:m.put_start_and_end_on(cube1[i].get_start(),cube2[i].get_start()))
        hybercube=VGroup(cube1,cube2,hyber_lines)
        hybercube.move_to(svg2)
        hybercube.scale(0.5)
        hybercube2=hybercube.deepcopy()
        hybercube.add_updater(lambda m,dt:m.rotate(dt*PI/10,axis=DOWN))
        hybercube.add_updater(lambda m,dt:m.rotate(dt*PI/10,axis=LEFT))
        self.wait()
        hybercube.suspend_updating()
        self.play(ShowCreation(hybercube),run_time=0.5)
        hybercube.resume_updating()
        self.play(Write(text2))
        self.wait()
        self.play(cube2.animate.scale(0.5),cube1.animate.scale(2),run_time=2,rate_func=there_and_back)
        self.play( LaggedStart(DrawBorderThenFill(svg3),Write(text3),lag_ratio=0.5) )
        self.wait()

        # fadeout
        self.play(LaggedStartMap(FadeOut,VGroup(text,repo),shift=LEFT),
                  AnimationGroup(
                 LaggedStartMap(FadeOut,VGroup(hybercube,text2,svg3,text3),shift=RIGHT),
                 text1.animate.scale(2/0.8).center().arrange(DOWN),lag_ratio=0.5))
        hybercube.clear_updaters()
        self.wait()
        self.play(FadeOut(text1.en,shift=RIGHT),FadeOut(text1.ch,shift=LEFT))
        self.wait()

        # picture
        rec=Rectangle(width=FRAME_HEIGHT*4/3,height=FRAME_HEIGHT)
        # self.add(rec)
        cube1,points1=get_cube(1)     
        cube2,points2=get_cube(2)
        hyberlines=VGroup()
        hyber_lines=VGroup(*[ Line(points1[i],points2[i])for i in range(len(points1))])
        for i,line in enumerate(hyber_lines):
            line.add_updater(lambda m,i=i:m.put_start_and_end_on(cube1[i].get_start(),cube2[i].get_start()))
        hybercube=VGroup(cube1,cube2,hyber_lines)
        mat=np.array([[ 9.58561009e-01, -2.84887333e-01, -1.94289029e-16],                                        
                       [ 3.79927988e-02,  1.27834450e-01,  9.91067556e-01],                                        
                       [-2.82342593e-01, -9.49998716e-01,  1.33360786e-01]])
        hybercube.apply_matrix(mat) 
        hybercube.rotate(-PI/10,axis=LEFT)
        svg=SVGMobject('kun.svg',stroke_width=3,stroke_color=YELLOW,stroke_opacity=1,fill_opacity=0)
        sf=Sphere(radius=1.5)
        mesh=SurfaceMesh(sf,resolution=(10,10))
        mesh.rotate(PI/4,axis=LEFT)
        mesh[:10].set_color(YELLOW)
        cube1.set_color(YELLOW)
        cube2.set_color(WHITE)
        svg.scale(1.3)
        text=TextCustom(en='Matrix',ch='矩阵的三重身份')
        # ,font='Mongolian Baiti'
        text=Text('The triple identity \nof the matrix',alignment='center')
        text2=Text('矩阵的三重身份',font='WenCang')
        text.scale(2)
        text2.scale(2)
        text2.next_to(text,DOWN,buff=0.8)
        rec1=Rectangle(width=FRAME_WIDTH/3,height=FRAME_HEIGHT,stroke_opacity=0,fill_opacity=0.5,fill_color=WHITE)
        rec2=Rectangle(width=FRAME_WIDTH/3,height=FRAME_HEIGHT,stroke_opacity=0,fill_opacity=0.5,fill_color=BLUE)
        rec3=Rectangle(width=FRAME_WIDTH/3,height=FRAME_HEIGHT,stroke_opacity=0,fill_opacity=0.5,fill_color=GREEN)
        grp_rec=VGroup(rec1,rec2,rec3).arrange(RIGHT,buff=0)
        hybercube.scale(0.7)
        svg.scale(0.7)
        mesh.scale(0.6)
        rec_back=Rectangle(FRAME_WIDTH,FRAME_HEIGHT,fill_color=WHITE,fill_opacity=0.5)
        grp=Group(svg,hybercube,mesh).arrange(RIGHT,buff=2).to_edge(UP,buff=0.1)
        self.add(grp_rec)
        self.add(grp)
        self.add(text)
        self.add(text2)
        # self.bring_to_back(rec_back)

        


class video2(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame

        # write title
        title=TextCustom(en='Data Repository',ch='数据仓库')
        title.scale(1.5)
        # self.play(FadeIn(title.en,shift=RIGHT),FadeIn(title.ch,shift=LEFT))
        # self.wait()
        # self.play(FadeOut(title.en,shift=RIGHT),FadeOut(title.ch,shift=LEFT))
        # self.wait()
        # equation_init
        tex_mat=Tex(R"""
            \left[\enspace
            \begin{matrix}
            1&2&3\\
            4&5&6\\
            7&8&9
            \end{matrix}
            \enspace\right]""",font_size=60,)
        tex_mat_aug=Tex(R"""
            \left[\enspace
            \begin{matrix}
            1&2&3\\
            4&5&6\\
            7&8&9
            \end{matrix}
            \enspace\right.
            \left|\enspace
            \begin{matrix}6\\15\\24
            \end{matrix}
            \enspace\right]""",font_size=60)
        tex_eqn=TexText(R"""
            \begin{alignat*}{6}
             1\,&x+&&\,2\,&&y\,+&&\,3\,&&z&&=6  \\
            4\,&x+&&\,5\,&&y\,+&&\,6\,&&z&&=15\\
            7\,&x+&&\,8\,&&y\,+&&\,9\,&&z&&=24
            \end{alignat*}
            """,
            t2c={"x":BLUE_A,"y":BLUE_B,"z":BLUE_C},
            isolate=["+"])
        grp=VGroup(tex_mat_aug,tex_eqn).arrange(RIGHT,buff=1)
        text1=TextCustom('Matrix','矩阵',DOWN,buff=0.4).next_to(tex_mat_aug,UP)
        text2=TextCustom('Augmented Matrix','增广矩阵',DOWN,buff=0.2).next_to(tex_mat_aug,UP)
        saved_state=tex_mat_aug[22:24].copy()           # bracket original position
        tex_mat_aug[22:24].move_to(tex_mat_aug[11:17])  # move bracket
        
        # matrix and augmented matrix
        kw=dict(path_arc=30*DEGREES,run_time=1)
        tex_eqn.save_state()
        self.play(Write(tex_eqn.center().scale(1.3)))
        self.wait()
        self.play(tex_eqn.animate.restore())
        self.play(Write(tex_mat_aug[22:24]),Write(tex_mat_aug[0:2]))
        Animations=[
        TransformFromCopy(VGroup(tex_eqn[0],tex_eqn[10],tex_eqn[21]),
          VGroup(tex_mat_aug[2],tex_mat_aug[5],tex_mat_aug[8]),**kw),
        VGroup(tex_eqn[0],tex_eqn[10],tex_eqn[21]).animate.set_opacity(0.5),
        TransformFromCopy(VGroup(tex_eqn[3],tex_eqn[13],tex_eqn[24]),
          VGroup(tex_mat_aug[3],tex_mat_aug[6],tex_mat_aug[9]), **kw),
        VGroup(tex_eqn[3],tex_eqn[13],tex_eqn[24]).animate.set_opacity(0.5),
        TransformFromCopy(VGroup(tex_eqn[6],tex_eqn[16],tex_eqn[27]),
          VGroup(tex_mat_aug[4],tex_mat_aug[7],tex_mat_aug[10]), **kw),
        VGroup(tex_eqn[6],tex_eqn[16],tex_eqn[27]).animate.set_opacity(0.5),
                   ]
        self.play(LaggedStart(Animations,lag_ratio=0.1))
        self.play(Write(text1))
        self.wait()
        self.play(tex_mat_aug[22:24].animate.move_to(saved_state)
            ,FadeIn(tex_mat_aug[11:17]))
        self.play(
            TransformFromCopy(VGroup(tex_eqn[9],tex_eqn[19:21],tex_eqn[30:32]),
          VGroup(tex_mat_aug[17],tex_mat_aug[18:20],tex_mat_aug[20:22]), **kw),
            VGroup(tex_eqn[9],tex_eqn[19:21],tex_eqn[30:32]).animate.set_opacity(0.5))
        self.play(
            ReplacementTransform(text1.en.get_part_by_text('Matrix'),
                text2.en.get_part_by_text('Matrix')),
            ReplacementTransform(text1.ch.get_part_by_text('矩阵'),
                text2.ch.get_part_by_text('矩阵')),
            Write(text2.en.get_part_by_text('Augmented')),
            Write(text2.ch.get_part_by_text('增广'))
            )
        self.play(FadeOut(tex_eqn),VGroup(tex_mat_aug,text2).animate.center())
        self.play(LaggedStartMap(FadeOut,VGroup(text2.en,text2.ch,tex_mat_aug),shift=RIGHT*2))

        # vectorized--kun
        def get_cloud_grp(points,slices):
            grp=Group()
            for i in range(slices):
                cloud=DotCloud(points[i::slices,:],radius=0.05)
                grp.add(cloud)
            # grp.arrange(RIGHT)
            return grp
        ax=ThreeDAxesCustom()
        ax.add_axis_labels()
        ax.add_coordinate_labels()
        ax.remove(ax.z_axis)
        ax.set_opacity(0.7)
        svg=SVGMobject('kun.svg',stroke_color=WHITE,stroke_opacity=1,stroke_width=2,)
        svg.scale(2)
        points=svg.get_all_points()             # 1518
        clouds=get_cloud_grp(points,slices=66)  # 1518=23*66
        # clouds.scale(2)
        cloud_0_points=np.round(clouds[0].get_all_points().T,2)[:2,:]
        mat=Matrix(cloud_0_points)

        # matrix -- store image data 
        title=TextCustom(en='For Example',ch='举个栗子')
        title.scale(1.5)
        self.play(FadeIn(title.en,shift=RIGHT),FadeIn(title.ch,shift=LEFT))
        self.wait()
        self.play(FadeOut(title.en,shift=RIGHT),FadeOut(title.ch,shift=LEFT))

        # matrix_init
        mat.to_corner(UL)
        mat.set_opacity(1)
        mat.clear_updaters()
        self.play(Write(mat))
        self.play(mat.animate.to_corner(UR),run_time=5,rate_func=there_and_back)
        self.wait()
        self.play(Write(ax))

        # animations_init
        the_points_grp=Group()
        def grow_dots_anim(cloud,i,run_time=1):
            the_point=cloud.copy().pointwise_become_partial(clouds[0],0,(i+1)/num_of_points)
            the_col=mat.get_column(i)
            the_coord=cloud.get_all_points()[i,:]
            arrow=Arrow(start=ORIGIN,end=the_coord,buff=0)
            mat.get_column(i).set_opacity(0.5)
            self.play(TransformFromCopy(the_col,arrow),run_time=run_time/2)
            self.play(FadeOutToPoint(arrow,the_coord),FadeIn(the_point),run_time=run_time/2)
            the_points_grp.add(the_point)

        # compute whole_time
        num_of_points=cloud_0_points.shape[1]
        whole_time=0
        def func(i):
            return 2/math.sqrt(i)
        for i in np.arange(5,num_of_points):
            run_time=func(i)
            whole_time+=run_time
        print(f"whole time is {whole_time}")

        # anims
        velocity=(mat.get_right()[0]-frame.get_shape()[0]/2)/(whole_time+1.8*3)
        grow_dots_anim(clouds[0],0,run_time=2)
        grow_dots_anim(clouds[0],1,run_time=2)
        mat.add_updater(lambda m,dt:m.shift(dt*LEFT*velocity))
        grow_dots_anim(clouds[0],2,run_time=1.8)
        grow_dots_anim(clouds[0],3,run_time=1.8)
        grow_dots_anim(clouds[0],4,run_time=1.8)

        # anims_2
        for i in np.arange(5,num_of_points):
            run_time=func(i)
            grow_dots_anim(clouds[0],i,run_time=run_time)
        mat.clear_updaters()

        # many many points
        left_bracket=Tex(R"[")
        number=Tex('2',font_size=48)
        times=Tex(R'\times')
        decimal_number=DecimalNumber(23,num_decimal_places=0,color=TEAL)
        decimal_number.scale(0.7)
        right_bracket=Tex(R"]")
        grp=VGroup(left_bracket,number,times,decimal_number,right_bracket).arrange(RIGHT)
        grp.match_height(mat)
        grp.to_edge(UP)
        # self.add(grp)
        self.play(FadeTransform(mat.brackets[0],left_bracket),
            FadeTransform(mat.brackets[1],right_bracket),
            ReplacementTransform(VGroup(mat.elements),VGroup(number,times,decimal_number)),
            run_time=2)

        # shuffle clouds
        clouds_shuffled=clouds[1:].shuffle()
        def add_cloud(i,clouds,number,value):
            value=value+value*(i+1)
            self.play( number.animate.set_value(value),
                ShowCreation(clouds_shuffled[i]) ,run_time=1)

        for i in np.arange(0,10):
            add_cloud(i,clouds_shuffled,decimal_number,num_of_points)

        self.play(LaggedStartMap(ShowCreation,clouds_shuffled[10:],run_time=8),
            decimal_number.animate.set_value(len(points)).set_anim_args(run_time=2),
            right_bracket.animate.shift(RIGHT).set_anim_args(run_time=2))

        # fadeout drawborder
        self.play(LaggedStartMap(FadeOut,grp,shift=UP),FadeOut(ax))
        self.play(
            LaggedStart(
            AnimationGroup(*map(FadeOut,Group(the_points_grp,clouds_shuffled))), 
            DrawBorderThenFill(svg),lag_ratio=0.02,run_time=10
            ))

        # back rectangle
        rec=BackgroundRectangle(svg,color=WHITE,buff=0,fill_opacity=1)
        svg.set_fill(color=BLACK,opacity=1)
        rec.next_to(svg,UP)

        # image
        im=ImageMobject('kun.jpg')
        im.rescale_to_fit(rec.get_width(),0)
        im.set_opacity(1)

        # rec animation
        rec.stretch_to_fit_height(im.get_height())
        self.play(FadeIn(rec),run_time=0.3)
        self.bring_to_back(rec)
        self.play(rec.animate.move_to(svg,aligned_edge=DOWN),run_time=3)


        # image anim
        im.move_to(rec)
        self.play(FadeTransform(Group(rec,svg),im),run_time=2,rate_func=smooth)


        # r,g,b
        im_r=ImageMobject('red_channel.jpg')
        im_g=ImageMobject('green_channel.jpg')
        im_b=ImageMobject('blue_channel.jpg')
        im_grp=Group(im_r,im_g,im_b)
        positions=im_grp.copy().arrange(RIGHT)
        im_r.shift(LEFT*2)
        im_b.shift(RIGHT*2)
        im_r.rotate(-PI/4,axis=UP)
        im_g.rotate(-PI/4,axis=UP)
        im_b.rotate(-PI/4,axis=UP)
        
        for subim in im_grp:
            subim.apply_depth_test().set_opacity(0.5)
        
        # self.play(FadeIn(im),rate_func=linear)
        self.play(im.animate.rotate(-PI/4,axis=UP))
        self.play(FadeTransform(im,im_g),FadeTransform(im.copy(),im_r),
                FadeTransform(im.copy(),im_b))
        self.play(LaggedStart(
            [im_r.animate.rotate(PI/4,axis=UP).move_to(positions[0]),
            im_g.animate.rotate(PI/4,axis=UP).move_to(positions[1]),
            im_b.animate.rotate(PI/4,axis=UP).move_to(positions[2])],lag_ratio=0.1))

        # image_matrix
        image_r=Image.open(get_full_raster_image_path('red_channel.jpg'))
        image_g=Image.open(get_full_raster_image_path('green_channel.jpg'))
        image_b=Image.open(get_full_raster_image_path('blue_channel.jpg'))
        r_arr=np.array(image_r)[:,:,0]
        g_arr=np.array(image_g)[:,:,1]
        b_arr=np.array(image_b)[:,:,2]
        mat_r=Matrix(r_arr[:15,:10],ellipses_col=9,ellipses_row=14)
        mat_g=Matrix(g_arr[:15,:10],ellipses_col=9,ellipses_row=14)
        mat_b=Matrix(b_arr[:15,:10],ellipses_col=9,ellipses_row=14)
        mat_grp=VGroup(mat_r,mat_g,mat_b)
        mat_r.move_to(im_r).match_width(im_r).set_color(RED)
        mat_g.move_to(im_g).match_width(im_r).set_color(GREEN)
        mat_b.move_to(im_b).match_width(im_r).set_color("#6666FF")
        
        self.play(LaggedStart(
                im_r.animate.set_opacity(0.3),
                Write(mat_r),
                im_g.animate.set_opacity(0.3),
                Write(mat_g),
                im_b.animate.set_opacity(0.3),
                Write(mat_b),run_time=2
            ))
        self.wait()
        # write some text
        text=TextCustom(en='Pixel Matrices of Red, Green, and Blue Channels',
                        ch='红绿蓝三色通道像素矩阵',
                        font_size_en=30,font_size_ch=30,
                        en_config={'t2c':{'Red':RED,'Green':GREEN,'Blue':BLUE}},
                        ch_config={'t2c':{'红':RED,'绿':GREEN,'蓝':BLUE}})
        text.next_to(im_g,UP)
        # self.add(text)
        self.play(LaggedStartMap(Write,VGroup(text.en,text.ch),lag_ratio=0.02),run_time=2)
        self.wait()
        # fadeout
        self.play(
            LaggedStartMap(FadeOut,Group(im_r,mat_r),shift=LEFT),
            LaggedStartMap(FadeOut,Group(im_b,mat_b),shift=RIGHT),
            LaggedStartMap(FadeOut,Group(im_g,mat_g),shift=UP),
            LaggedStartMap(FadeOut,text,shift=UP*2))
        self.wait()

        pass
class video3(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        
        # 2. Builder of Spaces---text
        title2=TextCustom(en='Architect of Spaces',ch='空间建构师')
        title2.scale(1.5)
        self.play(FadeIn(title2.en,shift=RIGHT),FadeIn(title2.ch,shift=LEFT))
        self.wait()
        self.play(FadeOut(title2.en,shift=RIGHT),FadeOut(title2.ch,shift=LEFT))

        # 2d matrix --- rank
        mat2d=MatrixCustom(np.array([[1,0],[0,1]]))
        ax=ThreeDAxesCustom()
        ax.add_coordinate_labels()
        ax.add_axis_labels()
        comb2d=mat2d.get_linear_combination()
        arrow1,arrow2=mat2d.get_column_arrows(ax)
        change_parts=mat2d.get_changeable_parts()
        mat2d.save_state()
        mat2d.center().scale(2)
        self.play(Write(mat2d))
        self.play(LaggedStartMap(FlashAround,VGroup(mat2d.get_column(0),mat2d.get_column(1)),
            lag_ratio=0.5),run_time=2)
        self.wait()

        # write rank
        text=TextCustom(en="Rank",ch="秩")
        tex=Tex(R"=")
        number=DecimalNumber(1,num_decimal_places=0)
        number.set_color(mat2d.color_palette[0])
        number.scale(1.5)
        tex.scale(1.5)
        text.next_to(mat2d,RIGHT)
        tex.next_to(text,RIGHT)
        number.always.next_to(tex,RIGHT)
        rank_grp=VGroup(text,tex)
        number_copy=DecimalNumber(1,num_decimal_places=0,include_sign=True)
        number_copy.move_to(tex)
        number_copy.match_style(number)
        self.play(LaggedStartMap(Write,VGroup(text,tex)))
        self.play(VGroup(mat2d,rank_grp).animate.arrange(RIGHT,buff=1))
        self.play(TransformFromCopy(mat2d.get_column(0),number,path_arc=-3))
        self.play(TransformFromCopy2(mat2d.get_column(1),number_copy,path_arc=-3),
            number.animate.set_value(2))        
        self.wait()
        self.play(LaggedStartMap(FadeOut,VGroup(text,tex,number),shift=RIGHT*2),
            mat2d.animate.restore())

        # 2d comb ; grow arrow 
        animations=[AnimationGroup(TransformFromCopy(mat2d.brackets,
                mat2d.vector_matrices[0].brackets,path_arc=1),
            TransformFromCopy(mat2d.get_column(0),
                mat2d.vector_matrices[0].get_column(0),path_arc=1)),
                    AnimationGroup(TransformFromCopy(mat2d.brackets,
                mat2d.vector_matrices[1].brackets,path_arc=1),
            TransformFromCopy(mat2d.get_column(1),
                mat2d.vector_matrices[1].get_column(0),path_arc=1))]
        self.play(LaggedStart(*animations,lag_ratio=0.7))
        self.play(Write(mat2d.parts),run_time=2)
        ax.x_axis.set_opacity(0.5)
        ax.y_axis.set_opacity(0.5)
        self.play(Write(ax.x_axis),Write(ax.y_axis))
        self.play(LaggedStart(
         [TransformFromCopy2(mat2d.vector_matrices[0].elements[0],ax.x_axis.numbers[6].copy()),
         ShrinkToPoint(mat2d.vector_matrices[0].elements[1].copy(),point=ax.c2p(0,0,0))],
         lag_ratio=0.5))
        self.play(GrowArrow(arrow1))
        self.play(LaggedStart(
         [ShrinkToPoint(mat2d.vector_matrices[1].elements[0].copy(),point=ax.c2p(0,0,0)),
         TransformFromCopy2(mat2d.vector_matrices[1].elements[1],ax.y_axis.numbers[3].copy()),]
         ,lag_ratio=0.5))
        self.play(GrowArrow(arrow2))

        # add two arrows
        nbp=NumberPlaneCustom()
        arrow3=get_added_arrow(arrow1,arrow2,axis=ax)
        changeable_parts=mat2d.get_changeable_parts()
        arrow2copy=arrow2.copy().set_opacity(0.5)
        self.play(arrow2copy.animate.shift(arrow1.get_vector()),arrow2.animate.set_opacity(0.5))
        self.play(GrowArrow(arrow3))
        self.play(FadeOut(arrow2copy),arrow1.animate.set_opacity(0.5))
        self.play(*map(FlashAround,mat2d.parts))
        self.play(ReplacementTransform(mat2d.parts,changeable_parts))

        # span 2d plane
        vt1=ValueTracker(1)
        vt2=ValueTracker(1)
        changeable_parts[0].always.set_color(mat2d.color_palette[0])
        changeable_parts[1].always.set_color(mat2d.color_palette[1])
        changeable_parts[0].f_always.set_value(lambda:vt1.get_value())
        changeable_parts[1].f_always.set_value(lambda:vt2.get_value())
        def get_span2d_animation(x,y,nbp):
            return [
            AnimationGroup(vt1.animate.set_value(x),vt2.animate.set_value(y)),
            AnimationGroup(Write(nbp.index_lines(x,y)),nbp.index_lines(x,y).animate.set_opacity(0.3))]
        def get_span2d_animation2(x,y,nbp):
            return [
            AnimationGroup(vt1.animate.set_value(x),vt2.animate.set_value(y)),
            AnimationGroup(Write(nbp.index_lines(x,y)[1]),
                nbp.index_lines(x,y)[1].animate.set_opacity(0.3))]
        arrow1.add_updater(get_updater(arrow1.nparr,vt1,ax))
        arrow2.add_updater(get_updater(arrow2.nparr,vt2,ax))
        arrow3.add_updater(get_added_arrow_updater(vt1,vt2,arrow1.nparr,arrow2.nparr,ax))
        self.play(LaggedStart(get_span2d_animation(-2,-2,nbp)))
        self.play(LaggedStart(get_span2d_animation(-5,1,nbp)))
        self.play(LaggedStart(get_span2d_animation(1,3,nbp)))
        self.play(LaggedStart(get_span2d_animation(4,-3,nbp)),run_time=0.9)
        self.play(LaggedStart(get_span2d_animation(-6,2,nbp)),run_time=0.9)
        self.play(LaggedStart(get_span2d_animation(2,-1,nbp)),run_time=0.8)
        self.play(LaggedStart(get_span2d_animation(-4,0,nbp)),run_time=0.8)
        self.play(LaggedStart(get_span2d_animation2(3,3,nbp)),run_time=0.7)
        self.play(LaggedStart(get_span2d_animation2(-3,2,nbp)),run_time=0.7)
        self.play(LaggedStart(get_span2d_animation2(5,1,nbp)),run_time=0.6)
        self.play(LaggedStart(get_span2d_animation2(-1,-1,nbp)),run_time=0.6)
        self.play(LaggedStart(get_span2d_animation2(6,-2,nbp)),run_time=0.6)
        self.play(LaggedStart(get_span2d_animation2(0,0,nbp)),run_time=0.6)
        self.play(Write(nbp.faded_lines.set_opacity(0.4)),
            nbp.background_lines.animate.set_opacity(0.5))
        self.play(ax.x_axis.animate.set_opacity(1),ax.y_axis.animate.set_opacity(1),)

        # fadeout
        self.remove(arrow1,arrow2,arrow3)
        self.play(LaggedStartMap(FadeOut,
            VGroup(mat2d.vector_matrices,changeable_parts),shift=RIGHT*2),
                LaggedStartMap(FadeOut,
            VGroup(ax.x_axis,ax.y_axis,nbp,mat2d),shift=LEFT*2))

        # 3d text
        text=TextCustom(en="Three-dimensional Space",
            ch="三维空间")
        self.play(FadeIn(text.en,shift=RIGHT),FadeIn(text.ch,shift=LEFT))
        self.wait()
        self.play(FadeOut(text.en,shift=RIGHT),FadeOut(text.ch,shift=LEFT))

        # mat 3d ---- rank
        mat3d=MatrixCustom(np.array([[1,0,0],[0,1,0],[0,0,1]]))
        comb3d=mat3d.get_linear_combination()
        mat3d.scale(0.7,about_point=mat3d.get_corner(UL))
        comb3d.scale(0.7,about_point=comb3d.get_corner(UR))
        mat3d.save_state()
        mat3d.center().scale(2)
        self.play(Write(mat3d))
        # rank
        text=TextCustom(en="Rank",ch="秩")
        tex=Tex(R"=")
        number=DecimalNumber(1,num_decimal_places=0)
        number.set_color(mat3d.color_palette[0])
        number.scale(1.5)
        tex.scale(1.5)
        text.next_to(mat3d,RIGHT)
        tex.next_to(text,RIGHT)
        number.always.next_to(tex,RIGHT)
        rank_grp=VGroup(text,tex)
        number_copy=DecimalNumber(1,num_decimal_places=0,include_sign=True)
        number_copy.move_to(tex)
        number_copy.match_style(number)
        self.play(LaggedStartMap(Write,VGroup(text,tex)))
        self.play(VGroup(mat3d,rank_grp).animate.arrange(RIGHT,buff=1))
        self.play(TransformFromCopy(mat3d.get_column(0),number,path_arc=-3))
        self.play(TransformFromCopy2(mat3d.get_column(1),number_copy,path_arc=-3),
            number.animate.set_value(2))        
        self.play(TransformFromCopy2(mat3d.get_column(2),number_copy,path_arc=-3),
            number.animate.set_value(3))
        self.wait()
        self.play(LaggedStartMap(FadeOut,VGroup(text,tex,number),shift=RIGHT*2),
            mat3d.animate.restore())

        # 3d mat_comb
        animations=[AnimationGroup(TransformFromCopy(mat3d.brackets,
                mat3d.vector_matrices[0].brackets,path_arc=1),
            TransformFromCopy(mat3d.get_column(0),
                mat3d.vector_matrices[0].get_column(0),path_arc=1)),
                    AnimationGroup(TransformFromCopy(mat3d.brackets,
                mat3d.vector_matrices[1].brackets,path_arc=1),
            TransformFromCopy(mat3d.get_column(1),
                mat3d.vector_matrices[1].get_column(0),path_arc=1)),
                    AnimationGroup(TransformFromCopy(mat3d.brackets,
                mat3d.vector_matrices[2].brackets,path_arc=1),
            TransformFromCopy(mat3d.get_column(1),
                mat3d.vector_matrices[2].get_column(0),path_arc=1))]
        self.play(LaggedStart(*animations,lag_ratio=0.5,run_time=2))
        self.play(Write(mat3d.parts),run_time=1)

        # write three d axis
        changeable_parts=mat3d.get_changeable_parts(font_size=25)
        changeable_parts.fix_in_frame()
        mat3d.fix_in_frame()
        comb3d.fix_in_frame()
        ax=ThreeDAxesCustom()
        ax.set_opacity(0.5)
        ax.add_axis_labels()
        ax.add_coordinate_labels()
        ax.set_opacity(0.5)
        
        self.play(Write(ax),frame.animate.reorient(16, 30, 0, (0.41, 0.41, 0.11), 8.00))
        arrow1,arrow2,arrow3=mat3d.get_column_arrows(ax)
        self.play(frame.animate.reorient(15, 29, 0, (0.49, 0.17, -0.03), 4.55))

        # grow 3 arrows
        zero=Tex('0').move_to(ax.c2p(0,0,0)).scale(0.1)
        self.play(TransformFromCopy2(
                mat3d.vector_matrices[0].elements[0],ax.x_axis.numbers[6]),
            TransformFromCopy2(mat3d.vector_matrices[0].elements[1],zero),
            TransformFromCopy2(mat3d.vector_matrices[0].elements[2],zero))
        self.play(GrowArrow(arrow1))
        self.play(TransformFromCopy2(
                mat3d.vector_matrices[1].elements[0],zero),
            TransformFromCopy2(mat3d.vector_matrices[1].elements[1],ax.y_axis.numbers[3]),
            TransformFromCopy2(mat3d.vector_matrices[1].elements[2],zero))
        self.play(GrowArrow(arrow2))
        self.play(TransformFromCopy2(
                mat3d.vector_matrices[2].elements[0],zero),
            TransformFromCopy2(mat3d.vector_matrices[2].elements[1],zero),
            TransformFromCopy2(mat3d.vector_matrices[2].elements[2],ax.z_axis.numbers[4]))
        self.play(GrowArrow(arrow3))

        # added_arrow
        frame.save_state()
        arrow4=get_added_arrow(arrow1,arrow2,arrow3,axis=ax)
        arrow2copy=arrow2.copy().set_opacity(0.5)
        self.play(frame.animate.reorient(34, 66, 0, (0.41, 0.3, 0.32), 3.53))
        self.play(arrow2copy.animate.shift(arrow1.get_vector()))
        arrow3copy=arrow3.copy().set_opacity(0.5)
        self.play(arrow3copy.animate.shift(arrow1.get_vector()),run_time=0.5,rate_func=linear)
        self.play(arrow3copy.animate.shift(arrow2.get_vector()),run_time=0.5,rate_func=linear)
        self.play(GrowArrow(arrow4))    
        self.play(LaggedStartMap(FadeOut,VGroup(arrow2copy,arrow3copy)),frame.animate.restore())

        # indicate;get added arrow
        mat3d.parts.fix_in_frame()
        self.play(*map(FlashAround,mat3d.parts))
        self.play(ReplacementTransform(mat3d.parts,changeable_parts))
        
        # span 3d space
        self.play(frame.animate.reorient(15, 29, 0, (0.78, 0.34, 0.02), 7.86))
        frame.add_ambient_rotation(angular_speed=1 * DEG)
        vt1=ValueTracker(1)
        vt2=ValueTracker(1)
        vt3=ValueTracker(1)
        arrow1.add_updater(get_updater(arrow1.nparr,vt1,ax))
        arrow2.add_updater(get_updater(arrow2.nparr,vt2,ax))
        arrow3.add_updater(get_updater(arrow3.nparr,vt3,ax))
        arrow4.add_updater(get_added_arrow_updater2(vt1,vt2,vt3,arrow1.nparr,arrow2.nparr,arrow3.nparr,ax))
        changeable_parts[0].f_always.set_value(lambda:vt1.get_value())
        changeable_parts[0].always.set_color(mat3d.color_palette[0])
        changeable_parts[1].f_always.set_value(lambda:vt2.get_value())
        changeable_parts[1].always.set_color(mat3d.color_palette[1])
        changeable_parts[2].f_always.set_value(lambda:vt3.get_value())
        changeable_parts[2].always.set_color(mat3d.color_palette[2])
        grp=get_lines_grp(ax)
        self.play(Write(VGroup(*grp_index(ax,grp,[1,1,1]))))
        coord=[-1,-1,-1]
        self.play(LaggedStart(
                  frame.animate.reorient(-21, 74, 0, (0.78, 0.34, 0.02), 7.86),
                  AnimationGroup( vt1.animate.set_value(coord[0]),
                                  vt2.animate.set_value(coord[1]),
                                  vt3.animate.set_value(coord[2])
                                ),
                  Write(VGroup(*grp_index(ax,grp,[coord[0],coord[1],coord[2]]))),
                  lag_ratio=0.2)
                  )
        coord=[2,-1,2]
        self.play(LaggedStart(
                  frame.animate.reorient(-19, 30, 0, (0.4, -0.12, -0.0), 8.00),
                  AnimationGroup( vt1.animate.set_value(coord[0]),
                                  vt2.animate.set_value(coord[1]),
                                  vt3.animate.set_value(coord[2])
                                ),
                  Write(VGroup(*grp_index(ax,grp,[coord[0],coord[1],coord[2]]))),
                  lag_ratio=0.2)
                  )
        coord=[-2,-2,-2]
        self.play(LaggedStart(
                  frame.animate.reorient(-16, 75, 0, (-0.91, -0.58, 0.33), 8.00),
                  AnimationGroup( vt1.animate.set_value(coord[0]),
                                  vt2.animate.set_value(coord[1]),
                                  vt3.animate.set_value(coord[2])
                                ),
                  Write(VGroup(*grp_index(ax,grp,[coord[0],coord[1],coord[2]]))),
                  lag_ratio=0.2)
                  )
        coord=[-2,2,3]
        self.play(LaggedStart(
                  frame.animate.reorient(-40, 49, 0, (-0.64, 0.0, 1.05), 8.00),
                  AnimationGroup( vt1.animate.set_value(coord[0]),
                                  vt2.animate.set_value(coord[1]),
                                  vt3.animate.set_value(coord[2])
                                ),
                  Write(VGroup(*grp_index(ax,grp,[coord[0],coord[1],coord[2]]))),
                  lag_ratio=0.2)
                  )
        self.play(frame.animate.reorient(-26, 50, 0, (-0.03, -0.04, 1.27), 11.73),
                    Write(grp))
        frame.add_ambient_rotation(angular_speed=3 * DEG)
        coord=[-6,-3,4]
        glow1=GlowDot(ax.c2p(*coord),radius=0.3)
        self.play(AnimationGroup(vt1.animate.set_value(coord[0]),
                                 vt2.animate.set_value(coord[1]),
                                 vt3.animate.set_value(coord[2])),
                                ShowCreation(glow1))
        coord=[6,-3,4]
        glow2=GlowDot(ax.c2p(*coord),radius=0.3)
        self.play(AnimationGroup(vt1.animate.set_value(coord[0]),
                                 vt2.animate.set_value(coord[1]),
                                 vt3.animate.set_value(coord[2])),
                                ShowCreation(glow2))
        coord=[-6,3,-4]
        glow3=GlowDot(ax.c2p(*coord),radius=0.3)
        self.play(AnimationGroup(vt1.animate.set_value(coord[0]),
                                 vt2.animate.set_value(coord[1]),
                                 vt3.animate.set_value(coord[2])),
                                ShowCreation(glow3))
        coord=[6,3,-4]
        glow4=GlowDot(ax.c2p(*coord),radius=0.3)
        self.play(AnimationGroup(vt1.animate.set_value(coord[0]),
                                 vt2.animate.set_value(coord[1]),
                                 vt3.animate.set_value(coord[2])),
                                ShowCreation(glow4))
        coord=[-6,3,4]
        glow5=GlowDot(ax.c2p(*coord),radius=0.3)
        self.play(AnimationGroup(vt1.animate.set_value(coord[0]),
                                 vt2.animate.set_value(coord[1]),
                                 vt3.animate.set_value(coord[2])),
                                ShowCreation(glow5))
        coord=[6,3,4]
        glow6=GlowDot(ax.c2p(*coord),radius=0.3)
        self.play(AnimationGroup(vt1.animate.set_value(coord[0]),
                                 vt2.animate.set_value(coord[1]),
                                 vt3.animate.set_value(coord[2])),
                                ShowCreation(glow6))
        coord=[-6,-3,-4]
        glow7=GlowDot(ax.c2p(*coord),radius=0.3)
        self.play(AnimationGroup(vt1.animate.set_value(coord[0]),
                                 vt2.animate.set_value(coord[1]),
                                 vt3.animate.set_value(coord[2])),
                                ShowCreation(glow7))
        coord=[6,-3,-4]
        glow8=GlowDot(ax.c2p(*coord),radius=0.3)
        self.play(frame.animate.reorient(7, 50, 0, (0.51, -0.06, 1.16), 13.82),
                AnimationGroup(vt1.animate.set_value(coord[0]),
                                 vt2.animate.set_value(coord[1]),
                                 vt3.animate.set_value(coord[2])),
                                ShowCreation(glow8))
        self.wait(2)
        self.play(LaggedStartMap(FadeOut,VGroup(mat3d),shift=LEFT),
                LaggedStartMap(FadeOut,VGroup(changeable_parts,mat3d.vector_matrices),shift=RIGHT),
                *map(FadeOut,VGroup(ax,arrow1,arrow2,arrow3,arrow4,grp)),
                *map(FadeOut,Group(glow1,glow2,glow3,glow4,glow5,glow6,glow7,glow8)))
        frame.clear_updaters()

        # 4d_text
        frame.to_default_state()
        text=TextCustom(en="Four-dimensional Space",
            ch="四维空间")
        self.play(FadeIn(text.en,shift=RIGHT),FadeIn(text.ch,shift=LEFT))
        self.wait()
        self.play(FadeOut(text.en,shift=RIGHT),FadeOut(text.ch,shift=LEFT))

        # 4d_rank
        mat4d=MatrixCustom(np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]))
        mat4d.fix_in_frame()
        comb4d=mat4d.get_linear_combination()
        comb4d.fix_in_frame()
        mat4d.scale(0.7,about_point=mat4d.get_corner(UL))
        comb4d.scale(0.7,about_point=comb4d.get_corner(UR))
        changeable_parts=mat4d.get_changeable_parts(font_size=25)
        changeable_parts.fix_in_frame()
        mat4d.save_state()
        mat4d.scale(2)
        mat4d.center()
        text=TextCustom(en="Rank",ch="秩")
        tex=Tex(R"=")
        number=DecimalNumber(1,num_decimal_places=0)
        number.set_color(mat4d.color_palette[0])
        number.scale(1.5)
        tex.scale(1.5)
        text.next_to(mat4d,RIGHT)
        tex.next_to(text,RIGHT)
        number.fix_in_frame()
        number.always.next_to(tex,RIGHT)
        rank_grp=VGroup(text,tex).fix_in_frame()
        number_copy=DecimalNumber(1,num_decimal_places=0,include_sign=True)
        number_copy.move_to(tex)
        number_copy.match_style(number)
        self.play(Write(mat4d))
        self.play(LaggedStartMap(Write,VGroup(text,tex)))
        self.play(VGroup(mat4d,rank_grp).animate.arrange(RIGHT,buff=1))
        self.play(TransformFromCopy(mat4d.get_column(0),number,path_arc=-2))
        self.play(TransformFromCopy2(mat4d.get_column(1),number_copy,path_arc=-2),
            number.animate.set_value(2))        
        self.play(TransformFromCopy2(mat4d.get_column(2),number_copy,path_arc=-2),
            number.animate.set_value(3))
        self.play(TransformFromCopy2(mat4d.get_column(3),number_copy,path_arc=-2),
            number.animate.set_value(4))
        self.wait()
        self.play(LaggedStartMap(FadeOut,VGroup(text,tex,number),shift=RIGHT*2),
            mat4d.animate.restore())

        # show 4d comb
        animations=[AnimationGroup(TransformFromCopy(mat4d.brackets,
                mat4d.vector_matrices[0].brackets,path_arc=1),
            TransformFromCopy(mat4d.get_column(0),
                mat4d.vector_matrices[0].get_column(0),path_arc=1)),
                    AnimationGroup(TransformFromCopy(mat4d.brackets,
                mat4d.vector_matrices[1].brackets,path_arc=1),
            TransformFromCopy(mat4d.get_column(1),
                mat4d.vector_matrices[1].get_column(0),path_arc=1)),
                    AnimationGroup(TransformFromCopy(mat4d.brackets,
                mat4d.vector_matrices[2].brackets,path_arc=1),
            TransformFromCopy(mat4d.get_column(1),
                mat4d.vector_matrices[2].get_column(0),path_arc=1)),
                    AnimationGroup(TransformFromCopy(mat4d.brackets,
                mat4d.vector_matrices[3].brackets,path_arc=1),
            TransformFromCopy(mat4d.get_column(0),
                mat4d.vector_matrices[3].get_column(0),path_arc=1))]
        self.play(LaggedStart(*animations,lag_ratio=0.5))
        self.play(Write(mat4d.parts),run_time=1)
        
        # write 4d axis
        ax=FourDAxesCustom(show_w_axis=True)
        ax.add_coordinate_labels()
        ax.add_axis_labels()
        ax.set_opacity(0.5)
        arrow1,arrow2,arrow3,arrow4=mat4d.get_column_arrows(ax)
        arrow4.set_perpendicular_to_camera(ax.frame)
        self.play(LaggedStartMap(Write,VGroup(ax.x_axis,ax.y_axis,ax.z_axis)),
            frame.animate.set_orientation(ax.frame.get_orientation()))

        # grow arrow 4d(1st 2nd 3rd arrows)
        zero=Tex('0').move_to(ax.c2p_4d(0,0,0,0)).scale(0.1)
        frame.add_ambient_rotation(angular_speed=2 * DEG)
        self.play(TransformFromCopy2(
                mat4d.vector_matrices[0].elements[0],ax.x_axis.numbers[6]),
            TransformFromCopy2(mat4d.vector_matrices[0].elements[1],zero),
            TransformFromCopy2(mat4d.vector_matrices[0].elements[2],zero),
            TransformFromCopy2(mat4d.vector_matrices[0].elements[3],zero),
            mat4d.parts[0].animate.set_opacity(0.3),
            mat4d.vector_matrices[0].animate.set_opacity(0.3),)
        self.play(GrowArrow(arrow1))
        self.play(TransformFromCopy2(
                mat4d.vector_matrices[1].elements[0],zero),
            TransformFromCopy2(mat4d.vector_matrices[1].elements[1],ax.y_axis.numbers[3]),
            TransformFromCopy2(mat4d.vector_matrices[1].elements[2],zero),
            TransformFromCopy2(mat4d.vector_matrices[1].elements[3],zero),
            mat4d.parts[1].animate.set_opacity(0.3),
            mat4d.vector_matrices[1].animate.set_opacity(0.3),)
        self.play(GrowArrow(arrow2))
        self.play(TransformFromCopy2(
                mat4d.vector_matrices[2].elements[0],zero),
            TransformFromCopy2(mat4d.vector_matrices[2].elements[1],zero),
            TransformFromCopy2(mat4d.vector_matrices[2].elements[2],ax.z_axis.numbers[4]),
            TransformFromCopy2(mat4d.vector_matrices[2].elements[3],zero),
            mat4d.parts[2].animate.set_opacity(0.3),
            mat4d.vector_matrices[2].animate.set_opacity(0.3),)
        self.play(GrowArrow(arrow3))

        # question ?
        tex=Tex('?')
        tex.fix_in_frame()
        tex.scale(3)
        tex.match_color(mat4d.vector_matrices[3])
        tex.next_to(mat4d.vector_matrices[3],DOWN,buff=0.5)
        tex_3d=Tex(R"3D")
        tex_3d.scale(2)
        tex_3d.to_corner(DL)
        tex_3d_number=tex_3d.make_number_changeable('3')
        tex_3d.fix_in_frame()
        tex_3d_number.fix_in_frame()
        self.play(FlashAround(VGroup(mat4d.vector_matrices[3],mat4d.parts[3])),run_time=3)
        self.play(Write(tex),run_time=2)
        self.wait(2)
        self.play(FadeOut(tex,shift=RIGHT))
        self.wait(2)
        frame.clear_updaters()
        self.play(frame.animate.set_orientation(ax.frame.get_orientation()))
        sf=get_current_frame_surface(frame)
        sf.set_opacity(0.3)
        self.play(ShowCreation(sf),Write(tex_3d))
        for axis in VGroup(ax.x_axis,ax.y_axis,ax.z_axis):
            axis.save_state()
        ax.make_xyz_flat()
        for arrow in VGroup(arrow1,arrow2,arrow3):
            arrow.save_state()
            arrow.apply_function(ax.projection_function)
        self.wait(2)

        # rotation to 4d
        enter_point_frame=frame.copy()
        frame.save_state()
        rotation_mat=FourDAxesCustom.get_rotation_matrix(frame.get_implied_camera_location())
        self.play(Write(ax.w_axis),
            frame.animate.set_orientation(Rotation.from_matrix(rotation_mat)),
            tex_3d_number.animate.set_value(4),
            run_time=3)
        self.wait()
        self.play(ax.w_axis.animate.set_opacity(1),rate_func=there_and_back,run_time=2)
        self.wait()
        self.play(frame.animate.rotate(30*DEGREES,axis=ax.z_axis.get_vector()),)
        self.wait()
        self.play(frame.animate.scale(0.6))
        self.wait()

        # grow 4th arrow
        self.play(TransformFromCopy2(
                mat4d.vector_matrices[3].elements[0],zero),
            TransformFromCopy2(mat4d.vector_matrices[3].elements[1],zero),
            TransformFromCopy2(mat4d.vector_matrices[3].elements[2],zero),
            TransformFromCopy2(mat4d.vector_matrices[3].elements[3],ax.w_axis.numbers[6]),
            mat4d.parts[3].animate.set_opacity(0.3),
            mat4d.vector_matrices[3].animate.set_opacity(0.3),)
        self.play(GrowArrow(arrow4))
        self.play(frame.animate.scale(1/0.6))
        self.wait()

        # go back to 3d
        self.play(LaggedStart(
            frame.animate.restore(),
            AnimationGroup(*map(FadeOut,Group(ax.w_axis,arrow4)),
            AnimationGroup(FadeOut(sf),tex_3d_number.animate.set_value(3))
            ),lag_ratio=0.8 ) ,run_time=3)
        restore_grp=VGroup(ax.x_axis,ax.y_axis,ax.z_axis,arrow1,arrow2,arrow3)
        for sth in restore_grp:
            sth.restore()
        frame.add_ambient_rotation(angular_speed=-8 * DEG)
        self.play(frame.animate.reorient(19, 28, 0, (0,0,0), 3.93),)
        self.wait(4)
        
        # comb opacity 1
        fadeout_grp=Group(sf,ax.w_axis,arrow4)
        apply_grp=VGroup(arrow1,arrow2,arrow3,ax.x_axis,ax.y_axis,ax.z_axis)
        self.play(comb4d.animate.set_opacity(1))
        mat4d.parts.fix_in_frame()
        frame.clear_updaters()

        # add the first three arrows
        added_arrow=get_added_arrow(arrow1,arrow2,arrow3,axis=ax.ghost)
        arrow2copy=arrow2.copy().set_opacity(0.5)
        self.play(frame.animate.reorient(34, 66, 0, (0.41, 0.3, 0.32), 3.53))
        self.play(arrow2copy.animate.shift(arrow1.get_vector()))
        arrow3copy=arrow3.copy().set_opacity(0.5)
        self.play(arrow3copy.animate.shift(arrow1.get_vector()),run_time=0.5,rate_func=linear)
        self.play(arrow3copy.animate.shift(arrow2.get_vector()),run_time=0.5,rate_func=linear)
        self.play(GrowArrow(added_arrow),run_time=0.5)    
        self.play(LaggedStartMap(FadeOut,VGroup(arrow2copy,arrow3copy)),
            frame.animate.restore(),
            VGroup(mat4d.parts[0:3],mat4d.vector_matrices[0:3]).animate.set_opacity(0.5))
        
        # go to 4d 
        self.play(FadeIn(sf),tex_3d_number.animate.set_value(4))
        apply_grp.add(added_arrow)
        for sth in apply_grp:
            sth.save_state()
            sth.apply_function(ax.projection_function)
        self.play(FadeIn(ax.w_axis),FadeIn(arrow4),
            frame.animate.reorient(-48, 55, 54, (0.18, 0.18, 0.51), 12.75))
        
        # add 4th arrow
        frame.save_state()
        final_added_arrow=Arrow(start=ax.c2p_4d(0,0,0,0),end=ax.c2p_4d(1,1,1,1),buff=0)
        added_arrow_copy=added_arrow.copy().set_opacity(0.5)
        self.play(frame.animate.reorient(-75, 50, 53, (0.46, 0.75, 1.28), 3.77),run_time=1.5)
        self.play(added_arrow_copy.animate.shift(arrow4.get_vector()))
        self.play(GrowArrow(final_added_arrow))
        self.play(FadeOut(added_arrow_copy),FadeOut(added_arrow),
            mat4d.parts[-1].animate.set_opacity(0.5),
            mat4d.vector_matrices[-1].animate.set_opacity(0.5))
        self.play(Flash(final_added_arrow.get_end()),Indicate(final_added_arrow),run_time=2)
        self.play(frame.animate.restore(),run_time=1.5)

        # flash around
        self.play(LaggedStartMap(FlashAround,VGroup(*mat4d.parts)))
        self.play(ReplacementTransform(mat4d.parts,changeable_parts))

        # 4d updater
        vt1=ValueTracker(1)
        vt2=ValueTracker(1)
        vt3=ValueTracker(1)
        vt4=ValueTracker(1)
        changeable_parts[0].f_always.set_value(lambda:vt1.get_value())
        changeable_parts[1].f_always.set_value(lambda:vt2.get_value())
        changeable_parts[2].f_always.set_value(lambda:vt3.get_value())
        changeable_parts[3].f_always.set_value(lambda:vt4.get_value())
        changeable_parts[0].always.set_color(mat4d.color_palette[0])
        changeable_parts[1].always.set_color(mat4d.color_palette[1])
        changeable_parts[2].always.set_color(mat4d.color_palette[2])
        changeable_parts[3].always.set_color(mat4d.color_palette[3])
        arrow1.add_updater(lambda m:m.put_start_and_end_on(ax.c2p_4d(0,0,0,0),ax.c2p_4d(vt1.get_value(),0,0,0)))
        arrow2.add_updater(lambda m:m.put_start_and_end_on(ax.c2p_4d(0,0,0,0),ax.c2p_4d(0,vt2.get_value(),0,0)))
        arrow3.add_updater(lambda m:m.put_start_and_end_on(ax.c2p_4d(0,0,0,0),ax.c2p_4d(0,0,vt3.get_value(),0)))
        arrow4.add_updater(lambda m:m.put_start_and_end_on(ax.c2p_4d(0,0,0,0),ax.c2p_4d(0,0,0,vt4.get_value())))
        arrow4.always.set_perpendicular_to_camera(ax.frame)
        final_added_arrow.add_updater(lambda m:m.put_start_and_end_on(ax.c2p_4d(0,0,0,0),ax.c2p_4d(vt1.get_value(),vt2.get_value(),vt3.get_value(),vt4.get_value())))


        # 4d space spanning
        sf_grp=SGroup()
        for i in np.concatenate((np.arange(-6, 0, 1), np.arange(1, 7, 1))):
            sf_grp.add(sf.copy().move_to(ax.c2p_4d(0,0,0,i)))

        # stickers
        def get_xyz_sticker(position,axis=ax,remove_ticks=False,remove_numbers=True,remove_label=True):
            ax_sticker=axis[0:3].copy()
            ax_sticker.shift(ax.c2p_4d(*position))
            if remove_ticks:
                ax_sticker[0].remove(ax_sticker[0].ticks)
                ax_sticker[1].remove(ax_sticker[1].ticks)
                ax_sticker[2].remove(ax_sticker[2].ticks)
            if remove_numbers:
                ax_sticker[0].remove(ax_sticker[0].numbers)
                ax_sticker[1].remove(ax_sticker[1].numbers)
                ax_sticker[2].remove(ax_sticker[2].numbers)
            if remove_label:
                ax_sticker[0].remove(ax_sticker[0][-1])
                ax_sticker[1].remove(ax_sticker[1][-1])
                ax_sticker[2].remove(ax_sticker[2][-1])
            return ax_sticker
        def get_w_sticker(position,axis=ax,remove_ticks=True,remove_numbers=True,remove_label=True):
            w_sticker=axis.w_axis.copy()
            sf_right=normalize(cross(axis.z_axis.get_vector(),axis.w_axis.get_vector()))
            sf_left=-sf_right
            sf_down=normalize(cross(sf_right,axis.w_axis.get_vector()))
            sf_up=-sf_down
            if remove_ticks:
                w_sticker.remove(w_sticker.ticks)
            if remove_numbers:
                w_sticker.remove(w_sticker.numbers)
            if remove_label:
                w_sticker.remove(w_sticker[-1])
            w_sticker.shift(sf_left*position[0])
            w_sticker.shift(sf_up*position[1])
            return w_sticker

        lines=VGroup(get_w_sticker([sf.u_range[1],sf.v_range[0]]),          
                     get_w_sticker([sf.u_range[1],sf.v_range[1]]),          
                     get_w_sticker([sf.u_range[0],sf.v_range[0]]),          
                     get_w_sticker([sf.u_range[0],sf.v_range[1]]),
                     get_w_sticker([-7.11,0]),
                     get_w_sticker([7.11,0]),
                     get_w_sticker([0,4]),
                     get_w_sticker([0,-4]),)
        axes=VGroup()
        for i in np.concatenate((np.arange(-6, 0, 1), np.arange(1, 7, 1))):
            axes.add(get_xyz_sticker([0,0,0,i],remove_ticks=True))

        def z_axis_updater(angular_speed=1 * DEG,axis=ax.z_axis):
            def updater(m,dt):
                m.rotate(angular_speed*dt,axis=axis.get_vector())
            return updater
       
        # w=6
        frame.clear_updaters()
        frame.add_updater(z_axis_updater(angular_speed=-2* DEG,axis=ax.z_axis))
        def span_4d_animation(w,run_time=1,deg=-10,remove_label=True,remove_ticks=True):
            mapping = {-6: 0, -5: 1, -4: 2, -3: 3, -2: 4, -1: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 10, 6: 11}
            xyz_sticker=get_xyz_sticker([0,0,0,w],
                remove_label=remove_label,remove_ticks=remove_ticks)
            xyz_sticker.set_opacity(0.3)
            self.play(frame.animate.rotate(deg*DEG,axis=ax.z_axis.get_vector()),
                    vt1.animate.set_value(0),
                    vt2.animate.set_value(0),
                    vt3.animate.set_value(0),
                    vt4.animate.set_value(w),FadeIn(sf_grp[mapping.get(w)]),
                    rate_func=linear,run_time=run_time)
            self.play(vt1.animate.set_value(-6),run_time=run_time)
            self.play(Write(xyz_sticker[0]),vt1.animate.set_value(6),run_time=run_time)
            self.play(vt1.animate.set_value(0),vt2.animate.set_value(-3),run_time=run_time/2)
            self.play(Write(xyz_sticker[1]),vt2.animate.set_value(3),run_time=run_time)
            self.play(vt2.animate.set_value(0),vt3.animate.set_value(-4),run_time=run_time/2)
            self.play(Write(xyz_sticker[2]),vt3.animate.set_value(4),run_time=run_time)

        span_4d_animation(6,run_time=1,deg=20,remove_label=False,remove_ticks=False)

        span_4d_animation(5,run_time=0.8,deg=-20)

        span_4d_animation(4,run_time=0.7,deg=-2)

        span_4d_animation(3,run_time=0.5,deg=0)

        span_4d_animation(2,run_time=0.2,deg=0)

        span_4d_animation(1,run_time=0.2,deg=0)

        frame.clear_updaters()
        frame.add_updater(z_axis_updater(angular_speed=-3* DEG,axis=ax.z_axis))

        span_4d_animation(-1,run_time=0.2,deg=0)

        span_4d_animation(-2,run_time=0.2,deg=0)

        span_4d_animation(-3,run_time=0.2,deg=0)

        span_4d_animation(-4,run_time=0.2,deg=0)

        span_4d_animation(-5,run_time=0.2,deg=0)

        span_4d_animation(-6,run_time=0.2,deg=0)

        self.play(frame.animate.reorient(-49, 56, 54, (0.23, 0.23, 0.62), 15.86),
            Write(lines,stroke_color=WHITE),
            rate_func=linear,run_time=3)

        # fade out and clear updaters
        self.wait()
        frame.clear_updaters()
        self.play(
            AnimationGroup(*map(Uncreate,lines)),
            LaggedStartMap(FadeOut,VGroup(mat4d,tex_3d),shift=LEFT),
            LaggedStartMap(FadeOut,VGroup(changeable_parts,mat4d.vector_matrices),shift=RIGHT),
            LaggedStartMap(FadeOut,Group(self.mobjects)) )
        # 

class magician_of_transformation(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        # write title
        title=TextCustom(en='Magician of Transformation',ch='古希腊掌管变化的神')
        title.scale(1.5)
        self.play(FadeIn(title.en,shift=RIGHT),FadeIn(title.ch,shift=LEFT))
        self.wait(2)
        self.play(FadeOut(title.en,shift=RIGHT),FadeOut(title.ch,shift=LEFT))

        pass

def get_frame_position(frame):
    frame = frame
    center = frame.get_center()
    height = frame.get_height()
    angles = frame.get_euler_angles()

    call = f"reorient("
    theta, phi, gamma = (angles / DEG).astype(int)
    call += f"{theta}, {phi}, {gamma}"
    if any(center != 0):
        call += f", {tuple(np.round(center, 2))}"
    if height != FRAME_HEIGHT:
        call += ", {:.2f}".format(height)
    call += ")"
    return call
        

def grp_index(ax,grp,target_xyz):
    x_min=ax.x_axis.x_min
    y_min=ax.y_axis.x_min            
    z_min=ax.z_axis.x_min
    x=target_xyz[0]
    y=target_xyz[1]
    z=target_xyz[2]
    z_index=int(z-z_min)
    x_index=int(x-x_min)
    y_index=int(y-y_min)
    x_line=grp[0][z_index][y_index]
    y_line=grp[1][z_index][x_index]
    z_line=grp[2][y_index][x_index]
    return x_line,y_line,z_line
def get_lines_grp(ax):
    x_min=ax.x_axis.x_min
    x_max=ax.x_axis.x_max
    y_min=ax.y_axis.x_min
    y_max=ax.y_axis.x_max
    z_min=ax.z_axis.x_min
    z_max=ax.z_axis.x_max
    step=1
    # x-lines
    x_grp=VGroup()
    for z in np.arange(z_min,z_max+1,step):
        x_subgrp=VGroup()
        for y in np.arange(y_min,y_max+1,step):
            line=Line(ax.c2p(x_min,y,z),ax.c2p(x_max,y,z))
            x_subgrp.add(line)
        x_subgrp.set_opacity(0.2)
        x_grp.add(x_subgrp)
    # y-lines
    y_grp=VGroup()
    for z in np.arange(z_min,z_max+1,step):
        y_subgrp=VGroup()
        for x in np.arange(x_min,x_max+1,step):
            line=Line(ax.c2p(x,y_min,z),ax.c2p(x,y_max,z))
            y_subgrp.add(line)
        y_subgrp.set_opacity(0.2)
        y_grp.add(y_subgrp)
    # z-lines
    z_grp=VGroup()
    for y in np.arange(y_min,y_max+1,step):
        z_subgrp=VGroup()
        for x in np.arange(x_min,x_max+1,step):
            line=Line(ax.c2p(x,y,z_min),ax.c2p(x,y,z_max))
            z_subgrp.add(line)
        z_subgrp.set_opacity(0.2)
        z_grp.add(z_subgrp)
    xyz_grp=VGroup(x_grp,y_grp,z_grp)
    return xyz_grp
def get_added_arrow_updater(vt1,vt2,arr1,arr2,ax):
    def updater(m):
        factor1=vt1.get_value()
        factor2=vt2.get_value()
        arr=vt1.get_value()*arr1+vt2.get_value()*arr2
        m.put_start_and_end_on(ax.c2p(0,0,0),ax.c2p(*arr))
    return updater
def get_added_arrow_updater2(vt1,vt2,vt3,arr1,arr2,arr3,ax):
    def updater(m):
        factor1=vt1.get_value()
        factor2=vt2.get_value()
        factor3=vt3.get_value()
        arr=vt1.get_value()*arr1+vt2.get_value()*arr2+vt3.get_value()*arr3
        m.put_start_and_end_on(ax.c2p(0,0,0),ax.c2p(*arr))
    return updater       
def get_updater(arr,vt,ax):
    def updater(m):
        factor=vt.get_value()
        m.put_start_and_end_on(ax.c2p(0,0,0),ax.c2p(*factor*arr)) 
    return updater        

def get_added_arrow(*arrows,axis):
    coord=np.zeros(3)
    for arrow in arrows:
        coord += np.array(axis.p2c(arrow.get_end())) 
    added_arrow=Arrow(axis.c2p(0,0,0),axis.c2p(*coord),buff=0)
    colors = [arrow.get_color() for arrow in arrows]
    added_arrow.set_color(average_color(*colors))
    return added_arrow

class ShrinkToPoint(Transform):
    def __init__(self,mobject,point,**kwargs):
        mobject=mobject
        target_mobject=mobject.copy().scale(0,about_point=point)
        super().__init__(mobject,target_mobject,remover=True,**kwargs)

class FourDAxesCustom(ThreeDAxesCustom):
    def __init__(
        self,
        x_range=(-6.0, 6.0, 1.0),
        y_range=(-3.0, 3.0, 1.0),
        z_range=(-4.0, 4.0, 1.0),
        w_range=(-6.0, 6.0, 1.0),
        frame=None,
        show_w_axis=False,
        **kwargs):
        super().__init__(x_range, y_range, z_range,**kwargs)
        self.w_range=w_range
        self.ghost=ThreeDAxesCustom(x_range, y_range, z_range,**kwargs) 
        self.init_w_axis(frame)
        self.show_w_axis=show_w_axis
        if show_w_axis:
            self.add_w_axis()
    def get_projection_plane(self):
        rec=Rectangle(width=FRAME_WIDTH,
            height=FRAME_HEIGHT,
            fill_color=WHITE,fill_opacity=0.3,stroke_opacity=0)
        mat=self.frame.get_inv_view_matrix()[:3,:3]
        rec.apply_matrix(mat)
        rec.move_to(self.frame.get_center())
        rec.set_height(self.frame.get_height())
        return rec
    def make_xyz_flat(self,frame=None):
        if frame is None:
            frame=self.frame
        else : frame=frame
        def projection_wrapper(point):
            return FourDAxesCustom.get_projection_point(point,frame)
        self[0:3].apply_function(projection_wrapper)
        self.projection_function=projection_wrapper
        return self
    def c2p_4d(self,*coords):
        # ax.c2p_4d(1,1,1,1) --> array([1,12,0.89,1.39])
        ax2=self.ghost
        func=FourDAxesCustom.get_projection_point
        point=self.w_axis.n2p(coords[-1])+func(ax2.c2p(*coords[:3]),self.frame)
        return point
    # overrides
    def add_coordinate_labels(self, 
        x_values=None, 
        y_values=None, 
        excluding=[0], 
        z_values=None, font_size=18, **kwargs):
        super().add_coordinate_labels(
            x_values=x_values, y_values=y_values, 
            excluding=excluding, z_values=z_values,font_size=font_size, **kwargs)
        if self.show_w_axis:
            self.add_w_axis_numbers()
        return self.coordinate_labels
    def add_axis_labels(self, *args, **kwargs):
        super().add_axis_labels(*args, **kwargs)
        if self.show_w_axis:
            self.add_w_axis_label()
    # sub functions
    def add_w_axis(self):
        if not self.show_w_axis:
            self.show_w_axis=True
        self.add(self.w_axis)
        self.axes.add(self.w_axis)
    def add_w_axis_label(self):
        self.axis_labels.add(self.w_label)
        self.w_axis.add(self.w_label)
    def add_w_axis_numbers(self):
        self.w_axis.add(self.w_numbers)
        self.w_axis.numbers=self.w_numbers

    def init_w_axis(self,frame):
        # w-axis
        if frame is None:
            rot=Rotation.from_quat(
                np.array([0.24558994, 0.04225083, 0.16419859, 0.95443139]))
            self.frame=CameraFrame().set_orientation(rot)
        else:
            self.frame=frame
        w_axis =  NumberLine(self.w_range)
        w_axis.shift(w_axis.n2p(0))
        w_axis.ticks.remove(w_axis.ticks[int(w_axis.x_max)])
        w_axis_ghost=w_axis.copy()
        # w-label
        w_label=Tex('w',font_size=70)
        w_label.next_to(w_axis,RIGHT,0.3)
        w_axis_ghost.add(w_label)
        # w-numbers
        w_numbers=w_axis_ghost.add_numbers(excluding=[0])
        # w-colors
        w_axis.set_color(PURPLE_B)
        w_axis.ticks.set_color(YELLOW)
        w_label.set_color(YELLOW)
        w_numbers.set_color(YELLOW)
        # get matrix
        camera_position=self.frame.get_implied_camera_location()
        mat=FourDAxesCustom.get_rotation_matrix(camera_position)
        w_axis.apply_matrix(mat)
        w_axis_ghost.apply_matrix(mat)
        # make smooth
        w_axis.make_smooth()
        w_label.make_smooth()
        w_numbers.make_smooth()
        self.w_axis=w_axis
        self.w_label=w_label
        self.w_numbers=w_numbers

    @staticmethod
    def get_projection_point(point,frame): # perspective 
        #convert list to numpy column vector
        camera_postion=frame.get_implied_camera_location()
        frame_center=frame.get_center()
        frame_center=np.array([frame_center]).T
        point=np.array([point]).T
        camera_postion=np.array([camera_postion]).T
        # codes:
        point=point-frame_center
        n=camera_postion-frame_center 
        proj_mat=np.dot(n,n.T)/np.dot(n.T,n)
        proj_point=np.dot(proj_mat,point)
        dirc_vector=point-proj_point
        scale_factor=get_norm(n)/(get_norm(n-proj_point))
        target_point=scale_factor*dirc_vector
        final_point=target_point+frame_center
        return final_point.T[0]   # column --> row --> first row (a list)
    @staticmethod
    def get_xyz(camera_position,z1=OUT):
        # x_vector=camera_position
        # y_vector=in the plane (z_axis and x_vector)
        # z_vector=cross product of x_vector and y_vector
        x=camera_position
        y=np.cross(np.cross(x,z1),x)
        z=np.cross(x,y)
        return normalize(x),normalize(y),normalize(z)
    @staticmethod
    def get_rotation_matrix(camera_postion): # combine new basis
        x,y,z=FourDAxesCustom.get_xyz(camera_postion)
        B=np.array([x,y,z]).T
        return B   
def split_rgb_channels(image_path, save=False):
    from PIL import Image
    """
    拆分图像为红、绿、蓝三个通道并返回对应的图像。

    参数：
    - image_path: str，输入图像路径。
    - save: bool，是否保存分离后的图像（默认不保存）。

    返回：
    - r_image: 仅保留红色通道的图像。
    - g_image: 仅保留绿色通道的图像。
    - b_image: 仅保留蓝色通道的图像。
    """
    # 打开并转换为 RGB 模式
    image_path = get_full_raster_image_path(image_path)
    img = Image.open(image_path).convert("RGB")

    # 转换为 NumPy 数组
    pixels = np.array(img)

    # 创建红色通道图像
    r_pixels = pixels.copy()
    r_pixels[:, :, 1] = 0  # 设置 G 通道为 0
    r_pixels[:, :, 2] = 0  # 设置 B 通道为 0
    r_image = Image.fromarray(r_pixels)

    # 创建绿色通道图像
    g_pixels = pixels.copy()
    g_pixels[:, :, 0] = 0  # 设置 R 通道为 0
    g_pixels[:, :, 2] = 0  # 设置 B 通道为 0
    g_image = Image.fromarray(g_pixels)

    # 创建蓝色通道图像
    b_pixels = pixels.copy()
    b_pixels[:, :, 0] = 0  # 设置 R 通道为 0
    b_pixels[:, :, 1] = 0  # 设置 G 通道为 0
    b_image = Image.fromarray(b_pixels)

    # 保存图像（如果需要）
    if save:
        output_dir = get_raster_image_dir()
        os.makedirs(output_dir, exist_ok=True)

        r_image.save(os.path.join(output_dir, "red_channel.jpg"))
        g_image.save(os.path.join(output_dir, "green_channel.jpg"))
        b_image.save(os.path.join(output_dir, "blue_channel.jpg"))

    return r_image, g_image, b_image
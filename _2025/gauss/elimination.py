from manim_imports_custom import *
from fractions import Fraction
from scipy.sparse import random 
from pydub import AudioSegment
class MatrixAug(Matrix):
    def __init__(self,matrix,add_augmented_line=True,**kwargs):
        super().__init__(matrix,**kwargs)
        if add_augmented_line:
            self.add_augmented_line()

    def add_augmented_line(self):
        line=Line()
        line_position=(self.get_columns()[-1].get_center()+self.get_columns()[-2].get_center())/2
        line.rotate(PI/2).match_height(self.brackets).move_to(line_position)
        self.line=line
        self.add(line)
class DecimalNumber2(DecimalNumber):
    def __init__(self,number,**kwargs):
        self.rec=False
        super().__init__(number,**kwargs)
    def set_value(self, number: float | complex):
        if self.rec :
            rec=self.submobjects[-1]
            self.remove(rec)
            super().set_value(number)
            self.add(rec)
            new_rec=SurroundingRectangle(VGroup(self.submobjects[:-1]))
            rec.become(new_rec)
            return self
        else:
            super().set_value(number)
            return self
    def copy(self,*args,**kwargs):
        copy_obj  =super().copy(*args,**kwargs)
        if self.rec==True:
            copy_obj.rec=True
        return copy_obj

class DecimalMatrix2(DecimalMatrix):
    def __init__(self,
        matrix,
        num_decimal_places=1,
        decimal_config={"edge_to_fix":DOWN},
        add_augmented_line=False,
        add_middle_line=False,
        **kwargs):
        super().__init__(matrix,num_decimal_places,decimal_config,**kwargs)
        if add_augmented_line:
            self.add_augmented_line()
        if add_middle_line:
            self.add_middle_line()
    def element_to_mobject(self, element, **decimal_config) -> DecimalNumber:
        return DecimalNumber2(element, **decimal_config)
    def add_augmented_line(self):
        line=Line()
        line_position=(self.get_columns()[-1].get_center()+self.get_columns()[-2].get_center())/2
        line.rotate(PI/2).match_height(self.brackets).move_to(line_position)
        self.augmented_line=line
        self.add(line)
    def add_middle_line(self):
        line=Line()
        n_cols=len(self.mob_matrix[0])
        m1=int(np.floor(n_cols/2))
        line_position=(self.get_columns()[m1-1].get_center()+self.get_columns()[m1].get_center())/2
        line.rotate(PI/2).match_height(self.brackets).move_to(line_position)
        self.middle_line=line
        self.add(line)
    def refresh_rows(self):
        self.rows = VGroup(*(VGroup(*row) for row in self.mob_matrix))       


class Elimination(InteractiveScene):
    aug1=np.array([
            [2,  1,-1, 8],
            [-3,-1, 2,-11],
            [-2, 1, 2,-3]]) # unique soln
    aug2=np.array([
            [0, 1,-1, 8],
            [3,-1, 2,-11],
            [2, 1, 2,-3]]) # unique soln
    aug3=np.array([
            [1,1,1,1,1,15],
            [2,0,2,2,3,31],
            [3,3,0,3,5,46],
            [0,1,1,1,1,14],
            [4,1,0,1,1,15]]) # page 56 -- unique soln
        
    def play_elimination(self,base,arr,RUN_TIME,aug=0,backsub=True,elimination=True,**kwargs):
        pivots,elim,nor,back=self.get_elimination_steps(arr,aug=aug,**kwargs)
        rows,cols=arr.shape
        if elimination:
            for i in range(min(rows,cols-aug)):
                self.find_pivot_anim(pivots,base,i,aug,RUN_TIME)
                self.exchange_row_anim(pivots,base,i,RUN_TIME)
                self.elimination_anim(elim,base,i,RUN_TIME)
        if backsub:
            for i in reversed(range(min(rows,cols-aug))):
                self.normalize_and_backsub_anim(pivots,nor,back,i,base,RUN_TIME)    
    def get_random_matrix(self,row:int,col:int,size=10,seed=None):
        np.random.seed(seed)
        matrix = np.random.randint(-size, size, size=(row, col)) 
        return matrix
    def generate_augmented_matrix(self,n,seed=None):
        np.random.seed(seed)
        A = np.random.randn(n, n)
        x = np.random.randint(-10, 10, size=(n, 1)) 
        b = np.dot(A, x)  
        augmented_matrix = np.hstack((A, b)) 
        return A, x,b,augmented_matrix
    def generate_random_sparse_matrix(self,n,m,density = 0.2,scale_factor=10, seed=None):
        sparse_matrix = random(n, m, density=density, format='csr', random_state=seed)
        sparse_matrix = sparse_matrix * scale_factor
        return sparse_matrix.toarray()
    def generate_random_sparse_intmatrix(self, n, m, density=0.2, scale_factor=10, seed=None):
        rng = np.random.default_rng(seed)  # 使用 NumPy 的随机数生成器
        # data_rvs 用于生成非零元素，这里生成 1 到 scale_factor 之间的随机整数
        sparse_matrix = random(n, m, density=density, format='csr', random_state=seed,
                               data_rvs=lambda s: rng.integers(1, scale_factor+1, size=s))
        return sparse_matrix.toarray()

    def solve(self,aug):
        aug.astype('float')
        a=aug[:, :-1]
        b=aug[:, -1]
        x=np.linalg.solve(a,b)
        check=np.allclose(np.dot(a, x), b)
        return x,check
    def get_elimination_steps(self,
        matrix,
        integer_algorithm=False,
        aug=0):
        matrix=matrix.astype('float')
        elimination_results={}
        normalize_reuslts={}
        backsub_results={}
        pivots={}
        rows, cols = matrix.shape
        for i in range(min(rows,cols - aug)):
            found=False
            pivots[i]=None
            elimination_results[i]=None
            # find pivot: 
            if i < rows-1: # not the last row
                for t in range(i, cols - aug):
                    for j in range(i , rows):
                        if matrix[j, t] !=0:
                            found = True
                            pivots[i]=(j,t)
                            if j!=i:
                                matrix[[i, j]] = matrix[[j, i]]
                            break
                    if found:
                        break
            else: # lase row
                for j in range(i, cols - aug):
                    if matrix[i,j]!=0:
                        found=True
                        pivots[i]=(i,j)
                        break
                    else:
                        found=False
            # row reduction
            if found and i!=rows-1 and np.any(matrix[i+1:,pivots[i][1]]!=0): # 最后一行不进行row reduction
                index=(i,pivots[i][1])
                pivot_value = matrix[*index]
                for j in range(i + 1, rows):
                    if integer_algorithm==True: # Fraction-Free Integer Gauss Elimination
                        fa, fb = self.get_lcm_multipliers(
                            pivot_value, matrix[j, index[1]])
                        matrix[j] = matrix[j] * fb - matrix[i] * fa
                    else:
                        factor = matrix[j, index[1]] / pivot_value
                        matrix[j] -= factor * matrix[i]
                elimination_results[i]=matrix.copy()

        # normalize and back substitute
        for key in reversed(pivots):
            if pivots[key] is not None:
                c=pivots[key][1]
                r=key
                # normalize
                pivot_value = matrix[r, c]
                if pivot_value!=1:
                    matrix[r, :] = matrix[r, :] / pivot_value
                    normalize_reuslts[r]=matrix.copy()
                else: normalize_reuslts[r]=None
                # back substitute
                if r !=0 and np.any(matrix[:r,c]!=0): # 第一个pivot不进行back substitution
                    for i in range(r-1, -1, -1):  
                        if matrix[i, c] !=0:
                            factor = matrix[i, c]  
                            matrix[i, :] -= factor * matrix[r, :]  
                    backsub_results[r]=matrix.copy()
                else: 
                    backsub_results[r]=None
        # return
        return pivots,elimination_results,normalize_reuslts,backsub_results

    def find_pivot_anim(self,pivots,base,row,aug,RUN_TIME):
        index=pivots[row]
        rows=len(base.mob_matrix)
        cols=len(base.mob_matrix[0])
        rec=SurroundingRectangle(base.mob_matrix[row][row])
        self.wait(RUN_TIME)
        self.add_trimed_sound("stone",RUN_TIME)
        self.play(ShowCreation(rec),run_time=RUN_TIME)
        if (row,row)!=index and index is not None:
            for j in range(row,cols-aug):
                for i in range(row,rows):
                    if (i, j) == (row, row):
                        continue
                    self.remove(rec)
                    rec=SurroundingRectangle(base.mob_matrix[i][j])
                    self.add_trimed_sound("stone",RUN_TIME)
                    self.add(rec)
                    self.wait(RUN_TIME)
                    if (i,j)==index:
                        base.mob_matrix[i][j].add(rec)
                        base.mob_matrix[i][j].rec=True
                        return
        if index is None:
            self.play(FadeOut(rec),run_time=RUN_TIME)
            self.wait(RUN_TIME/2)
            return
        else:
            base.mob_matrix[row][row].add(rec)
            base.mob_matrix[row][row].rec=True
    def get_lcm_multipliers(self,a, b):
        # find least common multiple
        if b == 0:
            return 0,1
        else:
            lcm = abs(a * b) // math.gcd(int(a), int(b))  # 最小公倍数
            return lcm // a, lcm // b
                        
    def exchange_row_anim(self,pivots,base,row,RUN_TIME):
        index=pivots[row]
        if index is None: return
        i=row
        j=index[0]
        def arc_func(x):
            return ((PI*3/5)/x)+PI
        if i !=j:
            angle=arc_func(abs(i-j))
            x1=base.get_row(i).get_x()
            x2=base.get_row(j).get_x()
            self.wait(RUN_TIME/2)
            self.add_trimed_sound("whoosh",RUN_TIME*2)
            self.play(
                base.get_row(i).animate.move_to(base.get_row(j)).set_x(x1).set_anim_args(path_arc=angle),
                base.get_row(j).animate.move_to(base.get_row(i)).set_x(x2).set_anim_args(path_arc=angle),
                run_time=RUN_TIME*2)
            base.mob_matrix[i], base.mob_matrix[j] = base.mob_matrix[j], base.mob_matrix[i]
            base.refresh_rows()
        else: return

    def elimination_anim(self,elim,base,row,RUN_TIME):
        rows=len(base.mob_matrix)
        if elim[row] is None: 
            return
        else:
            dic=self.generate_dict_forward(rows)
            self.number_fly_anim(base,dic,row,RUN_TIME*2)
            anims=self.get_decimal_change_anim(base,elim[row])
            self.add_trimed_sound("ticks",RUN_TIME*2)
            self.play(*anims,run_time=RUN_TIME*2)
            self.set_matrix_color(base,WHITE)
    
    def add_trimed_sound(self,file,trimtime):
        return self.file_writer.add_audio_segment(
            self.load_and_keep_wav(get_full_sound_file_path(file),trimtime),self.get_time())

    def load_and_keep_wav(self,filepath: str, time: float) -> AudioSegment:
        audio = AudioSegment.from_wav(filepath)
        total_duration_ms = len(audio)
        keep_duration_ms = int(time * 1000)
        if keep_duration_ms >= total_duration_ms:
            return audio  
        else:
            return audio[:keep_duration_ms]
    def normalize_and_backsub_anim(self,pivots,nor,back,row,base,RUN_TIME):
        rows=len(base.mob_matrix)
        if pivots[row] is None: return
        if nor[row] is not None:
            rec=self.get_rec(base,row)
            self.play(FadeIn(rec,shift=RIGHT),run_time=RUN_TIME)
            self.set_subgrp_color(base.get_row(row),TEAL)
            self.play(FadeOut(rec,shift=RIGHT),run_time=RUN_TIME)
            anims=self.get_decimal_change_anim(base,nor[row])
            self.add_trimed_sound("ticks",RUN_TIME*2)
            self.play(*anims,run_time=RUN_TIME*2)
            self.set_matrix_color(base,WHITE)
        if back[row] is not None:
            dic=self.generate_dict_backward(rows)
            self.number_fly_anim(base,dic,row,RUN_TIME*2)
            anims=self.get_decimal_change_anim(base,back[row])
            self.add_trimed_sound("ticks",RUN_TIME*2)
            self.play(*anims,run_time=RUN_TIME*2)
            self.set_matrix_color(base,WHITE)
    def number_fly_anim(self,base,_dict,i,RUN_TIME):
        used_row_index=i
        to_rows_indices=_dict[i]
        used_row=base.get_row(used_row_index)
        trans2=VGroup( base.get_row(i) for i in to_rows_indices)
        trans1=VGroup()
        for i in range(len(trans2)):
            trans1.add(used_row.copy())
        anims=[]
        for elem,pos in zip(trans1,trans2):
            for a,b in zip(elem,pos):
                if a.rec==True:
                    copied_a=a[:-1].copy()
                else:
                    copied_a=a.copy()
                anim=copied_a.set_color(TEAL).animate.move_to(b).scale(0.5).set_anim_args(path_arc=PI/2,remover=True)
                anims.append(anim)
        self.add_trimed_sound("fly",RUN_TIME)        
        self.play(LaggedStart(*anims,lag_ratio=0.01),run_time=RUN_TIME)
        self.set_grp_color(trans2,TEAL)

    def get_decimal_change_anim(self,base,result):
        anims=[]
        for row,row_values in zip(base.mob_matrix,result):
            for number,value in zip(row,row_values):
                anim=ChangeDecimalToValue(number,value)
                anims.append(anim)
        return anims
        
    def set_subgrp_color(self,grp,color):
        for mob in grp:
            if mob.rec==True:
                mob[:-1].set_color(color)
            else:
                mob.set_color(color)
    def set_matrix_color(self,matrix,color):
        # matrix.set_color(color)
        for row in matrix.mob_matrix:
            for mob in row:
                if mob.rec==True:
                    mob[:-1].set_color(color)
                else:
                    mob.set_color(color)
    def set_grp_color(self,grp,color):
        for row in grp:
            for mob in row:
                if mob.rec==True:
                    mob[:-1].set_color(color)
                else:
                    mob.set_color(color)
    def generate_dict_forward(self,n):
         return {i: tuple(range(i + 1, n )) for i in range(n-1)}
    def generate_dict_backward(self,n):
         return {i: tuple(range(i - 1, -1, -1)) for i in range(n-1, 0, -1)}
    
    def get_rec(self,matrix,row):
        the_row=matrix.get_row(row)
        rec=Rectangle(fill_color=TEAL,fill_opacity=0.5,stroke_opacity=0)
        rec.set_width(matrix.get_width()*1.5,stretch=True)
        rec.set_height(the_row.get_height()/2,stretch=True)
        rec.move_to(the_row)
        self.bring_to_back(rec)
        return rec

class Easteregg2(Elimination):
    def construct(self):
        # init
        frame=self.frame
        # start
        inv=np.linalg.inv
        det=np.linalg.det
        rank=np.linalg.matrix_rank
        
        # find rank
        n=4
        arr0=self.get_random_matrix(n,n,seed=626)
        arr=np.hstack((arr0,np.eye(n)))
        base=DecimalMatrix2(arr0,num_decimal_places=2,add_middle_line=False)
        t_rank=VGroup(
            Textch("秩"),
            Tex("="),
            DecimalNumber(1,num_decimal_places=0)).scale(1.3).arrange(RIGHT,buff=0.2)
        t_rank.next_to(base,UP,buff=1)
        ghost_rec=SurroundingRectangle(t_rank[2])
        frame.reorient(0, 0, 0, (-0.02, 0.04, 0.0), 8.22)
        self.add(t_rank[0:2])
        # self.play(ChangeDecimalToValue(t_rank[2],1))
        self.add(base)
        self.wait()
        self.play_elimination(base,arr0,aug=0,RUN_TIME=0.2,backsub=False)
        TIME=0.5
        self.play(TransformFromCopy2( base.mob_matrix[0][0][-1],ghost_rec),
                  FadeIn(t_rank[2]),run_time=TIME)
        self.play(TransformFromCopy2( base.mob_matrix[1][1][-1],ghost_rec),
                  ChangeDecimalToValue(t_rank[2],2),run_time=TIME)
        self.play(TransformFromCopy2( base.mob_matrix[2][2][-1],ghost_rec),
                  ChangeDecimalToValue(t_rank[2],3),run_time=TIME)
        self.play(TransformFromCopy2( base.mob_matrix[3][3][-1],ghost_rec),
                  ChangeDecimalToValue(t_rank[2],4),run_time=TIME)
        self.wait()
        # compute det
        t_det=VGroup(
            Textch("行列式"),
            Tex("=")).scale(1.3).arrange(RIGHT,buff=0.2)
        t_det.next_to(base,UP,buff=1).shift(LEFT*2)
        eqn=Tex("7.00",R"\times","(-9.14)",R"\times","(-9.81)",R"\times","26.26")
        eqn.next_to(t_det[1],RIGHT,buff=0.2)
        result=Tex(f"{det(arr0)}").next_to(t_det[1],RIGHT,buff=0.2)
        self.play(FadeOut(t_rank,shift=UP),FadeIn(t_det,shift=RIGHT))
        self.play(LaggedStart(
            FadeTransform(base.mob_matrix[0][0][0:-1].copy(),eqn["7.00"][0]),
            FadeTransform(base.mob_matrix[1][1][0:-1].copy(),eqn["-9.14"][0]),
            FadeTransform(base.mob_matrix[2][2][0:-1].copy(),eqn["-9.81"][0]),
            FadeTransform(base.mob_matrix[3][3][0:-1].copy(),eqn["26.26"][0]),
            FadeIn(eqn[R"\times"]),
            FadeIn(eqn["("]),
            FadeIn(eqn[")"])
            ))
        self.play(ReplacementTransform(eqn,result))
        self.wait()

        # find det
        # def det_gauss(arr): # handle row exchange!!
        #     pivots,a,b,c=self.get_elimination_steps(arr)
        #     pivots_values=[]
        #     sign=1
        #     for i in range(n):
        #         pivots_values.append(a[n-2][i][i])
        #     for key,value in pivots.items():
        #         if key !=value[0]:
        #             sign=sign*-1
        #     result=np.prod(pivots_values)*sign
        #     return result,pivots_values
        # print(det(arr0))
        # result,pivots=det_gauss(arr0)
        # print(result)
        
        # find inverse
        values  = []
        for i in range(4):
            row = []
            for j in range(4):
                val = base.mob_matrix[i][j].get_value()
                row.append(val)
            values.append(row)
        nparr = np.array(values)
        newarr=np.hstack((nparr,np.eye(4)))
        base2=DecimalMatrix2(newarr,num_decimal_places=2,add_middle_line=True)
        for i in range(4):
            base2.mob_matrix[i][i].add(SurroundingRectangle(base2.mob_matrix[i][i]))
            base2.mob_matrix[i][i].rec=True
        self.play(
            LaggedStart(
            FadeOut(t_det),FadeOut(result),
            ReplacementTransform(base.brackets,base2.brackets),
            *[base.mob_matrix[i][j].animate.move_to(base2.mob_matrix[i][j])
            for i in range(4) for j in range(4) ],
            *[FadeIn(base2.mob_matrix[j][i],shift=LEFT)
            for i in range(4,8) for j in range(4)],
            ShowCreation(base2.middle_line.reverse_points())
            ))
        self.clear()
        self.add(base2)
        self.play_elimination(base2,newarr,RUN_TIME=0.2,elimination=False)
        # inv_text
        text=Textch("逆矩阵").scale(1.5).next_to(base2,UP,buff=1).shift(RIGHT*3.5)
        arrow=ArrowCustom().point_to(text.get_bottom(),angle=PI/2,length=0.7)
        rec=SurroundingRectangle(base2.get_columns()[4:])
        text.set_stroke(YELLOW,0.1,1)
        self.play(ShowCreation(rec),
                GrowArrow(arrow),
                Write(text))
        self.wait(2)


        
        
class integer(Elimination):
    def construct(self):
        # init
        frame=self.frame
        # start
        n=5
        arr=self.generate_random_sparse_intmatrix(n,n+1,seed=626,
            density=0.7,scale_factor=9)
        base=DecimalMatrix2(arr,num_decimal_places=2,add_augmented_line=True,
            h_buff=1)
        self.add(base)
        self.wait()
        self.play_elimination(base,arr,aug=1,RUN_TIME=0.5,backsub=True,
            integer_algorithm=True) 
        self.wait()

class normal(Elimination):
    def construct(self):
        # init
        frame=self.frame
        # start
        n=5
        arr=self.generate_random_sparse_intmatrix(n,n+1,seed=626,
            density=0.7,scale_factor=9)
        base=DecimalMatrix2(arr,num_decimal_places=2,add_augmented_line=True,
            h_buff=1)
        self.add(base)
        self.wait()
        self.play_elimination(base,arr,aug=1,RUN_TIME=0.5,backsub=True,
            integer_algorithm=False) 
        self.wait()

class Easteregg_frame(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # start
        SCALE=0.65
        line=Line().set_width(FRAME_HEIGHT).rotate(PI/2)
        line2=Line().set_width(FRAME_WIDTH)
        t1=Textch("高斯消元正常算法").scale(1.2)
        t1_down=Textch("缺点：会出现小数或分数").scale(SCALE)
        t2=Textch("高斯消元\n针对整数矩阵的优化算法",alignment="CENTER").scale(1.2)
        t2_y=Textch("优点：不会出现小数或分数").scale(SCALE)
        t2_q=Textch("缺点：但会出现较大的整数").scale(SCALE)
        titles=VGroup(t1,t2).arrange(RIGHT,buff=2.5,aligned_edge=ORIGIN).to_edge(UP)
        line2.next_to(titles,DOWN)
        t2_down=VGroup(t2_y,t2_q).arrange(DOWN)
        downs=VGroup(t1_down,t2_down).arrange(RIGHT,buff=3,aligned_edge=UP).next_to(line2,DOWN)
        # fine tun
        t1.shift(RIGHT)
        self.add(titles,line,line2)
        self.add(downs)
        self.wait(2)


class bigelimination_with_sound(Elimination):
    def construct(self):
        # init
        frame=self.frame
        rank=np.linalg.matrix_rank
        # start
        arr=self.generate_random_sparse_matrix(8,9,density=0.5,seed=626,scale_factor=20)
        base=DecimalMatrix2(arr,num_decimal_places=2,add_augmented_line=True)
        self.wait()
        self.add(base)
        self.wait()
        self.play_elimination(base,arr,aug=1,RUN_TIME=0.5)
        self.wait()
class Soundtest(Elimination):
    def construct(self):
        # init
        frame=self.frame
        rank=np.linalg.matrix_rank
        # start
        arr=self.generate_random_sparse_matrix(8,9,density=0.3,seed=626,scale_factor=20)
        base=DecimalMatrix2(arr,num_decimal_places=2,add_augmented_line=True)
        self.wait()
        self.add(base)
        self.wait()
        self.play_elimination(base,arr,aug=1,RUN_TIME=0.5)
        self.wait()

class bigelimination(Elimination):
    def construct(self):
        # init
        frame=self.frame
        # start
        arr=self.generate_random_sparse_matrix(8,9,density=0.5,seed=626,scale_factor=20)
        base=DecimalMatrix2(arr,num_decimal_places=2,add_augmented_line=True)
        self.wait()
        self.add(base)
        self.wait()
        self.play_elimination(base,arr,aug=1,RUN_TIME=0.2)
        self.wait()

class EliminationOld(InteractiveScene):
    aug1=np.array([
            [2,  1,-1, 8],
            [-3,-1, 2,-11],
            [-2, 1, 2,-3]]) # unique soln
    aug2=np.array([
            [0, 1,-1, 8],
            [3,-1, 2,-11],
            [2, 1, 2,-3]]) # unique soln
    aug3=np.array([
            [1,1,1,1,1,15],
            [2,0,2,2,3,31],
            [3,3,0,3,5,46],
            [0,1,1,1,1,14],
            [4,1,0,1,1,15]]) #page 56 -- unique soln
    aug4=np.array([
            [8, 7, 4, 1],
            [4, 6, 7, 3],
            [6, 3, 4, 6],
            [4, 5, 8, 2]
        ])

    def solve(self,aug):
        aug.astype('float')
        a=aug[:, :-1]
        b=aug[:, -1]
        x=np.linalg.solve(a,b)
        check=np.allclose(np.dot(a, x), b)
        return x,check

    def align_grp_matrices(self,grp):
        widths = [mob.get_width() for mob in grp]  
        max_index = widths.index(max(widths))  # 直接获取最大索引
        widest_matrix = grp[max_index]  
        widest_matrix=grp[max_index]
        for mat in grp:
            mat.brackets[0].replace(widest_matrix.brackets[0])
            mat.brackets[1].replace(widest_matrix.brackets[1])
            for i,row in enumerate(mat.mob_matrix):
                for j,elem in enumerate(row):
                    elem.move_to(widest_matrix.mob_matrix[i][j])
        return grp
    
    def get_elimination_matrices(self,nparr,simple=True,aug=True,**kwargs):
        if simple:
            steps=self.get_elimination_steps(nparr)
        else:
            steps=self.get_elimination_steps(nparr,simple=False)
        matrices_grp=self.create_matrices(steps,**kwargs)
        self.align_grp_matrices(matrices_grp)
        if aug:
            for mat in matrices_grp:
                mat.add_augmented_line()
        return matrices_grp

    def create_matrices(self,matrices_numpy_arr,decimal=True,**kwargs):
        if decimal:
            create_matrix=lambda m: MatrixAug(m,add_augmented_line=False,**kwargs)
        else:
            vfunc=np.vectorize(lambda x: Fraction(x).limit_denominator(),otypes=[str])
            create_matrix=lambda m: MatrixAug(vfunc(m),add_augmented_line=False,**kwargs)
        matrix_grp=VGroup()
        for matrix in matrices_numpy_arr:
            matrix_grp.add(create_matrix(matrix))
        return matrix_grp
    def get_lcm_multipliers(self,a, b):
        # find least common multiple
        lcm = abs(a * b) // math.gcd(a, b)  # 最小公倍数
        return lcm // a, lcm // b

    def get_elimination_steps(self,
        matrix,
        simple=True,
        integer_algorithm=False,
        verbose=False,
        return_pivots_dict=False,
        **kwargs):
        # simple_return=True 只返回消元和回代过程中产生的矩阵 (mats2)
        # simple_return=False  返回包含所有操作（消元、回代、行交换、归一化行）的矩阵 (mats1)
        matrix=matrix.astype('float')
        mats1=[matrix.copy()] # complex form
        mats2=[matrix.copy()] # simple form
        if verbose:
            print("original matrix is")
            print(matrix)
        rows, cols = matrix.shape
        pivots_dict={}
        for i in range(rows):
            if verbose:
                print(f"operating on row{i+1}")
            # find pivot:
            if matrix[i,i]!=0:
                found=True
                index=(i,i)
                if verbose:
                    print(f"{i+1}th row pivot is",matrix[i,i])
            else:
                found = False  
                if i< rows-1: # not the last row
                    for j in range(i + 1, rows):
                        if matrix[j, i] != 0:
                            matrix[[i, j]] = matrix[[j, i]]  # 交换行
                            found = True
                            mats1.append(matrix.copy())
                            index=(i,i)
                            print(f"Operating row{i+1} :change row{i+1} and row{j+1}")
                            if verbose:
                                print(f"change row{i+1} and row{j+1}")
                                print(f"{i+1}th row pivot is",matrix[i,i])
                                print(matrix)
                            break
                        if not found:
                            for t in range(i + 1, cols):  # 向右查找
                                if matrix[i, t] != 0:
                                    found=True
                                    index=(i,t)
                                    if verbose:
                                        print(f"{i+1}th row pivot is",matrix[i, t])
                                else:
                                    for j in range(i + 1, rows):
                                        if matrix[j, t] != 0:
                                            matrix[[i, j]] = matrix[[j, i]]  # 交换行
                                            found = True
                                            mats1.append(matrix.copy())
                                            index=(i,t)
                                            print(f"Operating row{i+1} :change row{i+1} and row{j+1}")
                                            if verbose:
                                                print(f"change row{i+1} and row{j+1}")
                                                print(f"{i+1}th row pivot is",matrix[i,t])
                                                print(matrix)
                                            break
                                    if found:
                                        break
                else: # lase row
                    for j in range(i+1,cols):
                        if matrix[i,j]!=0:
                            found=True
                            index=(i,j)
                            if verbose:
                                print(f"{i+1}th row pivot is",matrix[i, j])
                            break
                if not found:
                    index=None
                    if verbose:
                        print(f"{i+1}th row has no pivot")
            
            # row reduction
            pivots_dict[i]=index
            if not found:
                if verbose:
                    print("no reduction")
            else:
                if i!=rows-1: # 最后一行不进行row reduction
                    pivot_value = matrix[*index]
                    for j in range(i + 1, rows):
                        if integer_algorithm==True: # Fraction-Free Integer Gauss Elimination
                            a,b=self.get_lcm_multipliers(pivot_value,matrix[j, index[1]])
                            matrix[j]=matrix[j]*a-matrix[i]*b
                        else:
                            factor = matrix[j, index[1]] / pivot_value
                            matrix[j] -= factor * matrix[i]
                    if verbose:
                        print("after row reduction")
                        print(matrix)
                    mats1.append(matrix.copy())
                    mats2.append(matrix.copy())
        # back substitute
        for key in reversed(pivots_dict):
            if pivots_dict[key] is not None:
                r,c=pivots_dict[key]
                # normalize
                pivot_value = matrix[r, c]
                matrix[r, :] = matrix[r, :] / pivot_value
                mats1.append(matrix.copy())
                if verbose:
                    print(f"after normalize the pivot in position:({r+1},{c+1})")
                    print(matrix)
                if key ==0: # 只有1.第一行 2.有pivot 的时候，mats2加入矩阵
                    mats2.append(matrix.copy())
                # back substitute
                if key !=0: # 第一个pivot不进行back substitution
                    for i in range(r-1, -1, -1):  # 只需修改上面的行
                        if matrix[i, c] != 0:
                            factor = matrix[i, c]  # 当前行该列的值
                            matrix[i, :] -= factor * matrix[r, :]  # 用当前行去消去上面行的元素
                    if verbose:
                        print(f"back substitute above position:({r+1},{c+1})")
                        print(matrix)
                    mats1.append(matrix.copy())
                    mats2.append(matrix.copy()) #just elimination matrices
        # return
        if simple:
            return mats2
        else:
            return mats1        
class test_elimination(EliminationOld):
    aug1=np.array([
            [2,  1,-1, 8],
            [-3,-1, 2,-11],
            [-2, 1, 2,-3]]) # unique soln
    aug2=np.array([
            [0, 1,-1, 8],
            [3,-1, 2,-11],
            [2, 1, 2,-3]]) # unique soln
    aug3=np.array([
            [1,1,1,1,1,15],
            [2,0,2,2,3,31],
            [3,3,0,3,5,46],
            [0,1,1,1,1,14],
            [4,1,0,1,1,15]]) #page 56 -- unique soln
    aug4=np.array([
            [8, 7, 4, 1],
            [4, 6, 7, 3],
            [6, 3, 4, 6],
            [4, 5, 8, 2]
        ])
    def construct(self):
        # init
        frame=self.frame
        # check1
        aug1=np.array([[2,1,-1,8],[-3,-1,2,-11],[-2,1,2,-3]]) # unique soln
        aug2=np.array([[1,3,1,9],[1,1,-1,1],[3,11,5,35]]) # mutiple solns
        aug3=np.array([[0,1,-1,8],[3,-1,2,-11],[2,1,2,-3]]) # unique soln
        aug4=np.array([[0,0,0,0,0,1],[0,2,0,0,0,1],[0,0,0,0,0,1],[0,0,0,0,4,1]]) # no soln
        aug5=np.array([[0,0,0,0],[0,0,3,0],[0,0,6,0],[0,0,0,2]]) # no soln
        aug6=np.array([[2,4,-2,2],[4,9,-3,8],[-2,-3,7,10]]) #page 56 -- unique soln
        aug7=np.array([[1,1,1,1,1,15],[2,0,2,2,3,31],[3,3,0,3,5,46],[0,1,1,1,1,14],[4,1,0,1,1,15]]) #page 56 -- unique soln
        aug8=np.array([[3,4,6,1],[1,3,2,1],[3,6,8,1]])
        aug9=np.array([[1,1,1,1,1,15],[2,1,1,1,1,16],[1,1,2,1,1,18],[3,1,1,1,2,22],[1,1,1,3,1,23]])
        aug10=np.array([[0,3,2,12],[1,4,2,15],[9,54,38,231]])
        mats=self.get_elimination_matrices(aug4)
        self.add(mats.arrange(DOWN))

        self.solve(aug1)

        def add_arrows(grp):
            arrows=VGroup()
            for i in range(len(grp)-1):
                arrow=Arrow(grp[i].get_left(),grp[i+1].get_left(),path_arc=PI)
                arrows.add(arrow)
            return arrows
        def add_texts(grp,arrows):
            texts = VGroup()
            attach = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一"]
            grp_len = len(grp) - 1
            half_len = grp_len // 2
            row_number = 0  # 用于控制 "一, 二, 三..."
            for i in range(half_len):  
                insert = attach[row_number]  # 取对应的汉字
                if i % 2 == 0:
                    t = Textch(f"寻找第{insert}行的主元")
                else:
                    t = Textch(f"用第{insert}行向下消元")
                    row_number += 1  # 只有消元时，行号才前进
                texts.add(t)

            #  生成 "第X行归一化" 和 "第X列回代"（逆序）
            for i in range(half_len, grp_len):  
                insert = attach[row_number]  # 取当前行对应的汉字
                if i % 2 == 0:
                    t = Textch(f"用{insert}行向上回代")  # 按照 t6, t8, t10 逆序
                    row_number -= 1  # 只有回代时，行号才递减
                else:
                    t = Textch(f"第{insert}行归一化")  # 按照 t7, t9 逆序
                texts.add(t)
            for t,arrow in zip(texts,arrows):
                t.next_to(arrow,LEFT)
            return texts


        pivots_dict,mats=self.elimination(aug1,False,height=2)
        arrows=add_arrows(mats)
        texts=add_texts(mats,arrows)
        
        # self.add(texts)
        # self.add(arrows)
        # self.add(mats)
        recs0=VGroup()
        recs1=VGroup()
        recs2=VGroup()
        for mat in mats:
            # first pivot
            rec0=SurroundingRectangle(mat.mob_matrix[pivots_dict[0][0]][pivots_dict[0][1]] )
            rec1=SurroundingRectangle(mat.mob_matrix[pivots_dict[1][0]][pivots_dict[1][1]] )
            rec2=SurroundingRectangle(mat.mob_matrix[pivots_dict[2][0]][pivots_dict[2][1]] )
            recs0.add(rec0)
            recs1.add(rec1)
            recs2.add(rec2)
        # animation
        self.add(mats[0])
        # find first row's privot
        self.play(Write(texts[0]))
        self.play(Write(recs0[0]))
        self.play(ReplacementTransform(mats[0],mats[1]),run_time=0.5)
        # first col elimination
        self.play(FadeOut(texts[0],shift=LEFT),FadeIn(texts[1],shift=LEFT))
        mats[1].get_row(0).set_color(YELLOW)
        self.play(FlashAround(mats[1].get_row(0)))
        self.play(mats[1].get_row(0).copy().animate.move_to(mats[0].get_row(1)).set_anim_args(path_arc=PI/4,remover=True))
        self.play(ReplacementTransform(mats[1].get_row(1),mats[2].get_row(1)))
        self.play(mats[1].get_row(0).copy().animate.move_to(mats[0].get_row(2)).set_anim_args(path_arc=PI/4,remover=True))
        self.play(ReplacementTransform(mats[1].get_row(2),mats[2].get_row(2)))
        





        


        


        # align_equations
        class MyTex(Tex):
            # remindar for alignat:
            # & is left_aligned,next align point should use &&
            tex_environment: str = "alignat*"
            def __init__(self,*args,additional="{20}",**kwargs):
                self.additional = additional
                super().__init__(*args,**kwargs)
            def get_content_prefix_and_suffix(
                self, is_labelled: bool
            ) -> tuple[str, str]:
                prefix_lines = []
                suffix_lines = []
                if not is_labelled:
                    prefix_lines.append(self.get_color_command(
                        color_to_hex(self.base_color)
                    ))
                if self.alignment:
                    prefix_lines.append(self.alignment)
                if self.tex_environment:
                    prefix_lines.append(f"\\begin{{{self.tex_environment}}}")
                    if self.additional is not None:
                        prefix_lines.append(self.additional)
                    suffix_lines.append(f"\\end{{{self.tex_environment}}}")
                return (
                    "".join([line + "\n" for line in prefix_lines]),
                    "".join(["\n" + line for line in suffix_lines])
                )
        # setting eqn
        eqn=MyTex(R"""
         &\,\,  &&x    &\,+\, &&y    &\,+\, &&z    &\,+\, &&w  &\,+\, &&t   &\,= &\,\,&15 \\
         &\,\,  &2&x   &\,\,  &&     &\,+\, &2&z   &\,+\, &2&w &\,+\, &3&t  &\,= &\,\,&31 \\
         &\,\,  &3&x   &\,+\, &3&y   &\,\,  &&     &\,+\, &3&w &\,+\, &5&t  &\,= &\,\,&46 \\
         &\,\,  &&     &\,\,  &&y    &\,+\, &&z    &\,+\, &&w  &\,+\, &&t   &\,= &\,\,&14 \\
         &\,\,  &4&x   &\,+\, &&y    &\,\,  &&     &\,+\, &&w  &\,+\, &&t   &\,= &\,\,&15 
        """,additional="{18}",
        t2c={"x":RED,"y":GREEN,"z":YELLOW,"w":TEAL,"t":BLUE})
        # self.add(eqn)

        # parse eqn
        def parse_latex_equation(eqn_string, variables=['x', 'y', 'z', 'w', 't']):
            # Initialize an empty list for rows of the augmented matrix
            matrix = []

            # Split the input LaTeX equation string by '\\\\' (each equation is separated by this)
            equations = eqn_string.split("\\\\\n")

            # Iterate through each equation
            for eqn in equations:
                # Remove LaTeX commands (e.g., '\\,' and other LaTeX symbols)
                eqn = eqn.replace('\\,', '').replace('\\,\\,', '').replace('&', '').replace(" ","")
                # print(eqn)
                # Split the equation into the left side and right side (constant)
                sides = eqn.split("=")

                # Extract coefficients and the constant term
                left_side = sides[0].strip()
                right_side = float(sides[1].strip())

                # Initialize a list to store the coefficients for this equation
                row = []

                # Regex to extract coefficients for the variables
                # Matches coefficients and variable names such as 3x, -2y, x, -z, etc.
                for var in variables:
                    # Regex: Look for an optional sign, optional digits, and a variable name
                    pattern = rf"([+-]?\d*)(?={var})"  # Look for coefficient before the variable
                    match = re.search(pattern, left_side)

                    # Default coefficient is 1 (or -1 if the sign is negative), and 0 if the variable is absent
                    if match:
                        coeff_str = match.group(0)
                        if coeff_str == '' or coeff_str == '+':  # If no coefficient, assume 1
                            coeff = 1
                        elif coeff_str == '-':  # If just a '-', assume -1
                            coeff = -1
                        else:
                            coeff = float(coeff_str)  # If a number is provided, use it
                    else:
                        coeff = 0  # If the variable doesn't exist in the equation, the coefficient is 0

                    row.append(coeff)

                # Append the coefficients to the row, followed by the constant
                row.append(right_side)

                # Add the row to the matrix
                matrix.append(row)

            # Convert the matrix to a NumPy array
            return np.array(matrix)

        # arr1=parse_latex_equation(eqn.tex_string,variables = ['x', 'y', 'z', 'w', 't'])
        # solve(arr1)
        # grp=elimination(arr1)
        # grp.arrange(DOWN).next_to(eqn,DOWN)
        # self.add(grp)
        # self.remove(eqn)
        # self.remove(grp)

        # test another eqn
        eqn2=MyTex(R"""
            2&x+4&&y-2&&z&&=2\\
            4&x+9&&y-3&&z&&=8\\
            -2&x-3&&y+7&&z&&=10
            """,additional="{6}",t2c={"x":RED,"y":GREEN,"z":YELLOW})
        # self.add(eqn2)
        # arr2=parse_latex_equation(eqn2.tex_string,["x","y","z"])
        # solve(arr2)
        # self.remove(eqn2)
        # grp_eqn2=elimination(arr2).arrange(DOWN)
        # self.add(grp_eqn2.next_to(eqn2,DOWN))

        # numpy to latex
        def arr_to_latex(arr, variables):
            latex_expr = "\n"
            rows, cols = arr.shape
            for i in range(rows):
                for j in range(cols - 1):
                    coef = arr[i, j]
                    var = variables[j]
                    if coef == 0: # no x,y,z just to align
                        latex_expr +=r"&\,\,  &&"
                    elif coef==1:
                        if j !=0:
                            latex_expr +=rf"&\,+\,  &&{var}"
                        else:
                            latex_expr +=rf"&\,\,  &&{var}"
                    elif coef==-1:
                        latex_expr +=rf"&\,-\,  &&{var}"
                    elif coef<0:
                        if coef.is_integer():
                            latex_expr +=rf"&\,-\,  &{-coef:.0f}&{var}"
                        else:
                            frac_coef = Fraction(-coef).limit_denominator()
                            frac_latex=rf"\frac{{{frac_coef.numerator}}}{{{frac_coef.denominator}}}"
                            latex_expr +=rf"&\,-\,  &{frac_latex}&{var}"
                    else :
                        if j !=0:
                            if coef.is_integer():
                                latex_expr +=rf"&\,+\,  &{coef:.0f}&{var}"
                            else:
                                frac_coef = Fraction(coef).limit_denominator()
                                frac_latex=rf"\frac{{{frac_coef.numerator}}}{{{frac_coef.denominator}}}"
                                latex_expr +=rf"&\,+\,  &{frac_latex}&{var}"
                        else:
                            if coef.is_integer():
                                latex_expr +=rf"&\,\,  &{coef:.0f}&{var}"
                            else:
                                frac_coef = Fraction(coef).limit_denominator()
                                frac_latex=rf"\frac{{{frac_coef.numerator}}}{{{frac_coef.denominator}}}"
                                latex_expr +=rf"&\,\,  &{frac_latex}&{var}"
                # equal sign
                latex_expr += r"&\,="
                coef_b = arr[i, -1]
                if coef_b>0:
                    if coef_b.is_integer():
                        latex_expr +=rf"&\,\,&{coef_b:.0f}"
                    else:
                        frac_coef = Fraction(coef_b).limit_denominator()
                        frac_latex=rf"\frac{{{frac_coef.numerator}}}{{{frac_coef.denominator}}}"
                        latex_expr +=rf"&\,\,&{frac_latex}"
                else:
                    if coef_b.is_integer():
                        latex_expr +=rf"&\,-\,&{-coef_b:.0f}"
                    else:
                        frac_coef = Fraction(-coef_b).limit_denominator()
                        frac_latex=rf"\frac{{{frac_coef.numerator}}}{{{frac_coef.denominator}}}"
                        latex_expr +=rf"&\,-\,&{frac_latex}"
                #last row
                if i != rows-1:
                    latex_expr +="\\\\\n"
                else:
                    latex_expr +="\n"
            return latex_expr

        # test
        # arr=np.array([[-2,-0.5,3,-3.5],[1,2,0,4.5],[1.2,-2,1,-4]])
        # eqn=MyTex(arr_to_latex(arr,["x_1","x_2","x_3"]))
        # self.add(eqn)
        # self.remove(eqn)
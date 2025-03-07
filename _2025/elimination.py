from manim_imports_custom import *
from fractions import Fraction
from _2025.kun_character import Kun,YellowChicken 
class elimination(InteractiveScene):
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
            mat.brackets[0].move_to(widest_matrix.brackets[0])
            mat.brackets[1].move_to(widest_matrix.brackets[1])
            for i,row in enumerate(mat.mob_matrix):
                for j,elem in enumerate(row):
                    elem.move_to(widest_matrix.mob_matrix[i][j])
        return grp

    def elimination(self,matrix,integer_algorithm=False,**kwargs):
        matrix=matrix.astype('float')
        vfunc=np.vectorize(lambda x: Fraction(x).limit_denominator(),otypes=[str])
        create_matrix=lambda m: Matrix(vfunc(m),**kwargs)
        mats1=VGroup(create_matrix(matrix))
        mats2=VGroup(create_matrix(matrix))
        rows, cols = matrix.shape
        print("original matrix is")
        print(matrix)
        pivots_dict={}
        for i in range(rows):
            print(f"operating on row{i+1}")
            # find pivot:
            if matrix[i,i]!=0:
                found=True
                mats1.add(create_matrix(matrix))
                index=(i,i)
                print(f"{i+1}th row pivot is",matrix[i,i])
            else:
                found = False  
                if i< rows-1: # not the last row
                    for j in range(i + 1, rows):
                        if matrix[j, i] != 0:
                            matrix[[i, j]] = matrix[[j, i]]  # 交换行
                            found = True
                            mats1.add(create_matrix(matrix))
                            index=(i,i)
                            print(f"{i+1}th row pivot is",matrix[i,i])
                            print(f"change row{i+1} and row{j+1}")
                            print(matrix)
                            break
                        if not found:
                            for t in range(i + 1, cols):  # 向右查找
                                if matrix[i, t] != 0:
                                    found=True
                                    mats1.add(create_matrix(matrix))
                                    index=(i,t)
                                    print(f"{i+1}th row pivot is",matrix[i, t])
                                else:
                                    for j in range(i + 1, rows):
                                        if matrix[j, t] != 0:
                                            matrix[[i, j]] = matrix[[j, i]]  # 交换行
                                            found = True
                                            mats1.add(create_matrix(matrix))
                                            index=(i,t)
                                            print(f"{i+1}th row pivot is",matrix[i,t])
                                            print(f"change row{i+1} and row{j+1}")
                                            print(matrix)
                                            break
                                    if found:
                                        break
                else: # lase row
                    for j in range(i+1,cols):
                        if matrix[i,j]!=0:
                            found=True
                            mats1.add(create_matrix(matrix))
                            index=(i,j)
                            print(f"{i+1}th row pivot is",matrix[i, j])
                            break
                if found==False:
                    index=None
                    print(f"{i+1}th row has no pivot")
            # row reduction
            pivots_dict[i]=index
            if not found:
                print("no reduction")
            else:
                pivot_value = matrix[*index]
                for j in range(i + 1, rows):
                    if integer_algorithm==True: # Fraction-Free Integer Gauss Elimination
                        matrix[j]=matrix[j]*pivot_value-matrix[i]*matrix[j, index[1]]
                    else:
                        factor = matrix[j, index[1]] / pivot_value
                        matrix[j] -= factor * matrix[i]
            print("after row reduction")
            print(matrix)
            if i!=rows-1: # 最后一行不进行row reduction
                mats1.add(create_matrix(matrix) )
                mats2.add(create_matrix(matrix) )
        # back substitute
        for key in reversed(pivots_dict):
            if pivots_dict[key] is not None:
                r,c=pivots_dict[key]
                # normalize
                pivot_value = matrix[r, c]
                matrix[r, :] = matrix[r, :] / pivot_value
                mats1.add(create_matrix(matrix))
                mats2.add(create_matrix(matrix))
                print(f"after normalize pivot{pivot_value}")
                print(matrix)
                # back substitute
                for i in range(r-1, -1, -1):  # 只需修改上面的行
                    if matrix[i, c] != 0:
                        factor = matrix[i, c]  # 当前行该列的值
                        matrix[i, :] -= factor * matrix[r, :]  # 用当前行去消去上面行的元素
            print(f"back substitute for pivot {pivots_dict[key]}")
            print(matrix)
            print(key,pivots_dict[key])
            if key !=0: # 不是第一行的pivot，存在或不存在都算
                mats1.add(create_matrix(matrix))
                mats2.add(create_matrix(matrix)) #just elimination matrices
        return pivots_dict,self.align_grp_matrices(mats1),self.align_grp_matrices(mats2)


class eqn_scene(elimination):
    def construct(self):
        # init
        frame=self.frame
        # start
        eqn1=VGroup(
            Tex("x+y=3"),
            Tex("2x+y=5")).arrange(DOWN)
        eqn2=VGroup(
            Tex("x+y=3"),
            Tex("2x+y=5")).arrange(DOWN)
        eqn2.next_to(eqn1,DOWN,buff=0.5)
        sub1=Tex(R"y=3-x")
        sub1.move_to(eqn2[0])
        brace1=Brace(eqn1,LEFT)
        brace2=Brace(eqn2,LEFT)
        self.add(eqn1)
        self.add(brace1)
        self.play(TransformFromCopy(VGroup(brace1,eqn1),VGroup(brace2,eqn2)),frame.animate.move_to(VGroup(eqn1,eqn2)))
        self.play(TransformMatchingTex(eqn2[0],sub1,key_map={"+":"-"}))
        sub2=Tex(R"2x+3-x=5")
        sub2.move_to(eqn2[1])
        self.play(TransformMatchingTex(eqn2[1],sub2),brace2.animate.shift(LEFT*0.4),
            ReplacementTransform(sub1.copy(),VectorizedPoint(eqn2[1]["y"].get_center())))
        # split
        sub22=Tex(R"x=5-3")
        sub22.move_to(sub2)
        self.play(TransformMatchingTex(sub2,sub22,key_map={"2x":"x"}),brace2.animate.shift(RIGHT*0.4))
        sub11=Tex(R"y=3-2")
        sub111=Tex(R"y=1")
        sub222=Tex(R"x=2")
        sub11.move_to(sub1)
        sub222.move_to(sub22)
        sub111.move_to(sub11)
        self.play(TransformMatchingTex(sub22,sub222))
        self.play(ReplacementTransform(sub222.copy(),VectorizedPoint(sub1["x"].get_center())),
            TransformMatchingTex(sub1,sub11))
        self.play(TransformMatchingTex(sub11,sub111),brace2.animate.shift(RIGHT*0.4))
        # solve!
        mark=Tex(R"\checkmark").set_color(RED)
        brace1.put_at_tip(mark)
        self.play(ReplacementTransform(VGroup(brace2,sub111,sub222),mark))
        self.play(FadeOut(mark),run_time=1)

        # three eqns
        eqn=VGroup(
            Tex("x+y+z=4"),
            Tex("2x+y+z=6"),
            Tex("x+y+2z=5")).arrange(DOWN)
        brace=Brace(eqn,LEFT)
        self.play(TransformMatchingTex(eqn1[0],eqn[0],key_map={"3":"4"}),
            TransformMatchingTex(eqn1[1],eqn[1],key_map={"5":"6"}),
            ReplacementTransform(brace1,brace),
            FadeIn(eqn[2],shift=LEFT,time_span=[0.5,2]),run_time=2)
        eqn_down=VGroup(
            Tex("x+y+z=4"),
            Tex("2x+y+z=6"),
            Tex("x+y+2z=5")).arrange(DOWN).next_to(eqn,DOWN,buff=0.5)
        brace_down=Brace(eqn_down,LEFT)
        self.play(TransformFromCopy(VGroup(brace,eqn),VGroup(brace_down,eqn_down)),
            frame.animate.move_to(VGroup(eqn,eqn_down)),VGroup(brace,eqn).animate.set_opacity(0.5))
        
        # solve
        arrow_right=Arrow(eqn_down[0].get_right(),eqn_down[0].get_right()+RIGHT)
        eqn_right=VGroup(Tex("y+z=4-x"),Tex("x+y=4-z")).arrange(DOWN)
        brace_right=Brace(eqn_right,LEFT)
        VGroup(brace_right,eqn_right).next_to(arrow_right,RIGHT)
        eqn1=VGroup(Tex("2+y+1=4"),Tex("y=4-1-2"),Tex("y=1")).move_to(eqn_down[0])
        eqn2=VGroup(Tex("2x+4-x=6"),Tex("2x-x=6-4"),Tex("x=2")).move_to(eqn_down[1])
        eqn3=VGroup(Tex("4-z+2z=5"),Tex("-z+2z=5-4"),Tex("z=1")).move_to(eqn_down[2])
        mark2=Tex(R"\checkmark").set_color(RED)
        brace.put_at_tip(mark2)
        self.play(LaggedStart([Write(arrow_right),Write(brace_right)]),frame.animate.shift(RIGHT))
        self.play(FlashAround(eqn_down[0]["y+z"]),FlashAround(eqn_down[1]["y+z"]),run_time=2)
        self.play(TransformMatchingTex(eqn_down[0].copy(),eqn_right[0],path_arc=-PI/4))
        self.play(FlashAround(eqn_down[0]["x+y"],color=RED),FlashAround(eqn_down[2]["x+y"],color=RED),run_time=2)
        self.play(TransformMatchingTex(eqn_down[0].copy(),eqn_right[1],path_arc=PI/4))
        self.play(FlashAround(eqn_right[0]["y+z"]),FlashAround(eqn_down[1]["y+z"]),run_time=2)
        self.play(ReplacementTransform(eqn_right[0],VectorizedPoint(eqn_down[1]["y+z"].get_center())),
                TransformMatchingTex(eqn_down[1],eqn2[0]))
        self.play(FlashAround(eqn_right[1]["x+y"]),FlashAround(eqn_down[2]["x+y"]),run_time=2)
        self.play(ReplacementTransform(eqn_right[1],VectorizedPoint(eqn_down[2]["x+y"].get_center())),
                TransformMatchingTex(eqn_down[2],eqn3[0]))
        self.play(FadeOut(arrow_right),FadeOut(brace_right),frame.animate.shift(LEFT))
        self.play(LaggedStart(FlashUnder(eqn_down[1]),FlashUnder(eqn_down[2]),lag_ratio=0.2))
        self.play(LaggedStart(FlashUnder(eqn_down[1]),FlashUnder(eqn_down[2]),lag_ratio=0.2))
        self.play(TransformMatchingTex(eqn2[0],eqn2[1]),
            TransformMatchingTex(eqn3[0],eqn3[1]))
        self.play(TransformMatchingTex(eqn2[1],eqn2[2]),
            TransformMatchingTex(eqn3[1],eqn3[2]))

        self.play(Indicate(VGroup(eqn_down[0]["x"],eqn2[2]["x"]))) 
        self.play(Indicate(VGroup(eqn_down[0]["z"],eqn3[2]["z"]))) 
        self.play(LaggedStart(
            TransformFromCopy(eqn2[2],VectorizedPoint(eqn_down[0]["x"].get_center())),
            TransformFromCopy(eqn3[2],VectorizedPoint(eqn_down[0]["z"].get_center())),lag_ratio=0.1),
            TransformMatchingTex(eqn_down[0],eqn1[0]),run_time=1.5)
        # split
        self.play(TransformMatchingTex(eqn1[0],eqn1[1],path_arc=PI/4))
        self.play(TransformMatchingTex(eqn1[1],eqn1[2],matched_keys={"4-1-2":"1"}),
            brace_down.animate.shift(RIGHT).set_anim_args(time_span=[0.5,1.5]),run_time=1.5)
        self.play(ReplacementTransform(VGroup(brace_down,eqn1[2],eqn2[2],eqn3[2]),mark2))
        self.play(FadeOut(mark2),eqn.animate.set_opacity(1),brace.animate.set_opacity(1),frame.animate.center(),run_time=1)
        # 5 eqns 5 unknows
        eqn_5=VGroup(
            Tex("x+y+z+w+t=15"),
            Tex("2x+y+z+w+t=16"),
            Tex("x+y+2z+w+t=18"),
            Tex("3x+y+z+w+t=22"),
            Tex("x+y+z+3w+t=23")
            ).arrange(DOWN)
        eqn_5_decimal=VGroup(
            Tex("0.1x+0.5y+0.6z+0.7w+0.8t=13.8"),
            Tex("2.2x+2.6y+5,1z+3,2w+0.1t=16.7"),
            Tex("1.2x+3.4y+2.8z+5.8w+0.9t=18.2"),
            Tex("3.5x+6.3y+6.9z+8.8w+9.3t=22.6"),
            Tex("0.3x+7.1y+2.4z+3.7w+0.5t=23.8")
            ).arrange(DOWN)
        br=Brace(eqn_5,LEFT)
        br_decimal=Brace(eqn_5_decimal,LEFT)
        self.play(FadeOut(VGroup(brace,eqn),shift=LEFT),FadeIn(VGroup(br,eqn_5),shift=LEFT))
        self.wait()
        self.play(FadeOut(VGroup(br,eqn_5),shift=LEFT),FadeIn(VGroup(br_decimal,eqn_5_decimal),shift=LEFT))
        self.wait()

class CustomVGroup(VGroup):
    def __init__(self, *vmobjects, reference_eqn=None, **kwargs):
            super().__init__(*vmobjects, **kwargs)
            self.reference_eqn = reference_eqn
    def align_eqns(self):
        self.reference_eqn.move_to(self[0]).shift(UP)
        variables = list(dict.fromkeys(re.findall(r"[a-zA-Z]",self.reference_eqn.string)))
        pattern_LHS = [re.compile(rf"[+-]?(?:\d*|\d*\.\d+|\\frac{{\d+}}{{\d+}}){var}") 
                    for var in variables]
        pattern_RHS = re.compile(r"=[+-]?(?:\d+|\d*\.\d+|\\frac\{\d+\}\{\d+\})")
        for eqn in self:
            # left hand side
            for pattern in pattern_LHS:
                match=pattern.search(eqn.string)
                match_rf=pattern.search(self.reference_eqn.string)

                if not match or not match_rf:
                   continue

                start,end=match.span()
                start_rf,end_rf=match_rf.span()
                eqn[end-1:end].align_to(self.reference_eqn[end_rf-1:end_rf],RIGHT) # align x

                if match.group().startswith(("+","-")):
                    eqn[start].align_to(self.reference_eqn[start_rf],RIGHT)
                    if len(match.group()) > 2:
                        eqn[start+1:end-1].align_to(self.reference_eqn[start_rf+1:end_rf-1],RIGHT)
                else:
                    if len(match.group()) > 1:
                        eqn[start:end-1].align_to(self.reference_eqn[start_rf+1:end_rf-1],RIGHT)
            # right hand side
            match=pattern_RHS.search(eqn.string)
            match_rf=pattern_RHS.search(self.reference_eqn.string)

            if not match or not match_rf:
                continue
            start,end=match.span()
            start_rf,end_rf=match_rf.span()
            eqn[start].align_to(self.reference_eqn[start_rf],RIGHT)
            if match.group().startswith(("+","-"),1):
                eqn[start+1].align_to(self.reference_eqn[start_rf+1],RIGHT)
                eqn[start+2:end].match_x(self.reference_eqn[start_rf+2:end_rf])
            else:
                eqn[start+1:end].match_x(self.reference_eqn[start_rf+2:end_rf])
        return self
class TexEqn(Tex):
    def __init__(self,tex_strings, reference_eqn=None, **kwargs):
            super().__init__(tex_strings, **kwargs)
            self.reference_eqn = reference_eqn
    def align_eqn(self,rf=None):
        if rf is None and self.reference_eqn is not None:
            rf=self.reference_eqn.copy()
        elif rf is not None:
            rf = rf.copy()
        else:
            raise ValueError("align_eqn requires a reference equation, but none was provided.")
        variables = list(dict.fromkeys(re.findall(r"[a-zA-Z]",rf.string)))
        pattern_LHS = [re.compile(rf"[+-]?(\d*|\d*\.\d+|\\frac{{\d+}}{{\d+}}){var}") 
                    for var in variables]
        pattern_RHS =  re.compile(rf"=[+-]?(\d+|\d*\.\d+|\\frac{{\d+}}{{\d+}})")
        # left hand side
        y=self.get_y()
        for pattern in pattern_LHS:

            span=self.find_spans_by_selector(pattern)
            span_rf=rf.find_spans_by_selector(pattern)

            if not span:
                continue

            indices_eqn=self.get_submob_indices_list_by_span(span[0])
            indices_rf=rf.get_submob_indices_list_by_span(span_rf[0])
            start,end=span[0]
            start_rf,end_rf=span_rf[0]
            
            self[indices_eqn[-1]].align_to(rf[indices_rf[-1]],RIGHT) # x,y,z
            if self.string[start:end].startswith(("+","-")) : # to_align有符号
                if rf.string[start_rf:end_rf].startswith(("+","-")): # rf 也有符号  
                    self[indices_eqn[0]].align_to(rf[indices_rf[0]],RIGHT) # 匹配符号
                    if len(indices_eqn)>2 and len(indices_rf)>2:    # 二者都有内容
                        self[indices_eqn[1]:indices_eqn[-1]].align_to(rf[indices_rf[1]:indices_rf[-1]],RIGHT)
                    if len(indices_eqn)>2 and len(indices_rf)==2:  # to_align有内容,rf无内容
                        self[indices_eqn[1]:indices_eqn[-1]].next_to(self[indices_eqn[-1]],LEFT,buff=0.1).set_y(y)
                
                elif not rf.string[start_rf:end_rf].startswith(("+","-")):# to_align有符号 rf 无符号
                    self[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[0]:indices_rf[-1]],RIGHT)

            elif rf.string[start_rf:end_rf].startswith(("+","-")): # __x--->___+x  to_align无符号；参考有符号
                if len(indices_eqn)>1 and len(indices_rf)>2: # 2x --> +2x to_align有内容；参考有内容
                    self[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[1]:indices_rf[-1]],RIGHT)
                if len(indices_eqn)>1 and len(indices_rf)==2: # 2x --> +x  to_align有内容；参考无内容
                    # pass
                    self[indices_eqn[0]:indices_eqn[-1]].next_to(self[indices_eqn[-1]],LEFT,buff=0.1).set_y(y)
                if len(indices_eqn)==1 and len(indices_rf)>=2: # x --> +x  to_align无内容；参考有或无内容
                    pass
            elif not rf.string[start_rf:end_rf].startswith(("+","-")):
                if len(indices_eqn)>1 and len(indices_rf)>1:
                    self[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[0]:indices_rf[-1]],RIGHT)

        # right hand side
        span=self.find_spans_by_selector(pattern_RHS)
        span_rf=rf.find_spans_by_selector(pattern_RHS)

        if span==[]:
            return self
        start,end=span[0]
        start_rf,end_rf=span_rf[0]
        indices_eqn=self.get_submob_indices_list_by_span(span[0])
        indices_rf=rf.get_submob_indices_list_by_span(span_rf[0])

        self[indices_eqn[0]].align_to(rf[indices_rf[0]],RIGHT) # 匹配=
        if self.string[start:end].startswith(("+","-"),1) : # to_align 有符号
            if rf.string[start_rf:end_rf].startswith(("+","-"),1): # rf 也有符号
                self[indices_eqn[1]].align_to(rf[indices_rf[1]],RIGHT) # 匹配符号
                self[indices_eqn[2]:].match_x(rf[indices_rf[2]:]) # 匹配内容
        elif rf.string[start_rf:end_rf].startswith(("+","-"),1): # to_align 无符号 rf有符号
            self[indices_eqn[1]:].match_x(rf[indices_rf[2]:])
        elif not rf.string[start_rf:end_rf].startswith(("+","-"),1):# to_align 无符号 rf无符号
            self[indices_eqn[1]:].match_x(rf[indices_rf[1]:])
        return self

class CustomVGroup2(VGroup):
    def __init__(self, *vmobjects, reference_eqn=None, **kwargs):
            super().__init__(*vmobjects, **kwargs)
            self.reference_eqn = reference_eqn
    def align_eqns(self):
        # re.compile(rf"[+-]?(\\frac{{\d+}}{{\d+}})k")
        rf=self.reference_eqn.copy()
        variables = list(dict.fromkeys(re.findall(r"[a-zA-Z]",rf.string)))
        pattern_LHS = [re.compile(rf"[+-]?(\d*|\d*\.\d+|\\frac{{\d+}}{{\d+}}){var}") 
                    for var in variables]
        pattern_RHS =  re.compile(rf"=[+-]?(\d+|\d*\.\d+|\\frac{{\d+}}{{\d+}})")
        for eqn in self:
            # left hand side
            y=eqn.get_y()
            for pattern in pattern_LHS:

                span=eqn.find_spans_by_selector(pattern)
                span_rf=rf.find_spans_by_selector(pattern)

                if span==[]:
                    continue

                indices_eqn=eqn.get_submob_indices_list_by_span(span[0])
                indices_rf=rf.get_submob_indices_list_by_span(span_rf[0])
                start,end=span[0]
                start_rf,end_rf=span_rf[0]
                
                eqn[indices_eqn[-1]].align_to(rf[indices_rf[-1]],RIGHT) # x,y,z
                if eqn.string[start:end].startswith(("+","-")) : # to_align有符号
                    if rf.string[start_rf:end_rf].startswith(("+","-")): # rf 也有符号  
                        eqn[indices_eqn[0]].align_to(rf[indices_rf[0]],RIGHT) # 匹配符号
                        if len(indices_eqn)>2 and len(indices_rf)>2:    # 二者都有内容
                            eqn[indices_eqn[1]:indices_eqn[-1]].align_to(rf[indices_rf[1]:indices_rf[-1]],RIGHT)
                        if len(indices_eqn)>2 and len(indices_rf)==2:  # to_align有内容,rf无内容
                            eqn[indices_eqn[1]:indices_eqn[-1]].next_to(eqn[indices_eqn[-1]],LEFT,buff=0.1).set_y(y)
                    
                    elif not rf.string[start_rf:end_rf].startswith(("+","-")):# to_align有符号 rf 无符号
                        eqn[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[0]:indices_rf[-1]],RIGHT)

                elif rf.string[start_rf:end_rf].startswith(("+","-")): # __x--->___+x  to_align无符号；参考有符号
                    if len(indices_eqn)>1 and len(indices_rf)>2: # 2x --> +2x to_align有内容；参考有内容
                        eqn[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[1]:indices_rf[-1]],RIGHT)
                    if len(indices_eqn)>1 and len(indices_rf)==2: # 2x --> +x  to_align有内容；参考无内容
                        # pass
                        eqn[indices_eqn[0]:indices_eqn[-1]].next_to(eqn[indices_eqn[-1]],LEFT,buff=0.1).set_y(y)
                    if len(indices_eqn)==1 and len(indices_rf)>=2: # x --> +x  to_align无内容；参考有或无内容
                        pass
                elif not rf.string[start_rf:end_rf].startswith(("+","-")):
                    if len(indices_eqn)>1 and len(indices_rf)>1:
                        eqn[indices_eqn[0]:indices_eqn[-1]].align_to(rf[indices_rf[0]:indices_rf[-1]],RIGHT)

            # right hand side
            span=eqn.find_spans_by_selector(pattern_RHS)
            span_rf=rf.find_spans_by_selector(pattern_RHS)

            if span==[]:
                continue
            start,end=span[0]
            start_rf,end_rf=span_rf[0]
            indices_eqn=eqn.get_submob_indices_list_by_span(span[0])
            indices_rf=rf.get_submob_indices_list_by_span(span_rf[0])

            eqn[indices_eqn[0]].align_to(rf[indices_rf[0]],RIGHT) # 匹配=
            if eqn.string[start:end].startswith(("+","-"),1) : # to_align 有符号
                if rf.string[start_rf:end_rf].startswith(("+","-"),1): # rf 也有符号
                    eqn[indices_eqn[1]].align_to(rf[indices_rf[1]],RIGHT) # 匹配符号
                    eqn[indices_eqn[2]:].match_x(rf[indices_rf[2]:]) # 匹配内容
            elif rf.string[start_rf:end_rf].startswith(("+","-"),1): # to_align 无符号 rf有符号
                eqn[indices_eqn[1]:].match_x(rf[indices_rf[2]:])
            elif not rf.string[start_rf:end_rf].startswith(("+","-"),1):# to_align 无符号 rf无符号
                eqn[indices_eqn[1]:].match_x(rf[indices_rf[1]:])
        return self


class part1(InteractiveScene):
    def extract_fraction_parts(self,vgroup, frac_pattern):
        numerator = VGroup()
        denominator = VGroup()
        fraction_symbol = None
        check = 0  
        for submob in vgroup[frac_pattern][0].submobjects:
            if isinstance(submob, VMobjectFromSVGPath) and check == 0:
                numerator.add(submob)
            elif isinstance(submob, Rectangle):  # 识别分数线
                fraction_symbol = submob
                check = 1
            elif isinstance(submob, VMobjectFromSVGPath) and check == 1:
                denominator.add(submob)
        return numerator, fraction_symbol, denominator
    def construct(self):
        # init
        frame=self.frame
        
        # add eqns_step0
        pattern=re.compile(r"\\frac\{\d+\}\{\d+\}|[a-zA-Z]|\+|\-|=|\d+")
        refer=Tex(R"+2x\,+2y\,+2z\,=+22",isolate=pattern).stretch(1.2,0)
        eqns_right=CustomVGroup2(
            Tex("y+2x-z=8",isolate=pattern),
            Tex("2z-y-3x=-11",isolate=pattern),
            Tex("-2x+2z+y=-3",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN)
        eqns_step0=CustomVGroup2(
            Tex("2x+y-z=8",isolate=pattern),
            Tex("-3x-y+2z=-11",isolate=pattern),
            Tex("-2x+y+2z=-3",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN)
        # define func "get_labels_to"
        def get_labels_to(grp):
            labels=VGroup()
            for i,eqn in enumerate(grp):
                label=Tex(f"({i+1})",font_size=30)
                label.next_to(eqn,RIGHT,buff=0.5)
                labels.add(label)
            for i,label in enumerate(labels):
                if i !=0:
                    label.align_to(labels[0],RIGHT)
            return labels
        self.add(eqns_right)
        self.play(TransformMatchingTex(eqns_right[0],eqns_step0[0],path_arc=PI/2))
        self.play(TransformMatchingTex(eqns_right[1],eqns_step0[1],path_arc=PI/2))
        self.play(TransformMatchingTex(eqns_right[2],eqns_step0[2],path_arc=PI/2,matched_keys={"+2z"}))
        self.play(eqns_step0.animate.align_eqns())
        labels_step0=get_labels_to(eqns_step0.align_eqns())
        self.play(LaggedStartMap(FadeIn,labels_step0,shift=LEFT))

        # eqns_step1
        ARROW_LENGTH=2.3
        REC_BUFF=0.05
        arrow_step1=Arrow(eqns_step0.get_bottom(),eqns_step0.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step1=CustomVGroup2(
            Tex("2x+y-z=8",isolate=pattern),
            Tex(R"\frac{1}{2}y+\frac{1}{2}z=1",isolate=pattern),
            Tex("2y+z=5",isolate=pattern),
            reference_eqn=eqns_step0.reference_eqn
            ).arrange(DOWN).next_to(arrow_step1,DOWN).align_eqns()
        labels_step1=get_labels_to(eqns_step1)
        note_step1=VGroup(
            Textch("第一步"),
            Textch("用方程"),
            Textch("消去它下面的"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step1_insert=VGroup(
            labels_step0[0].copy().next_to(note_step1[1],RIGHT,buff=0.1),
            Tex("x").next_to(note_step1[2],RIGHT,buff=0.1)
            )
        note_step1.add(note_step1_insert)
        note_step1.next_to(arrow_step1,LEFT,buff=3,aligned_edge=UP)
        underline_step1=Underline(note_step1[0],stroke_color=YELLOW)
        operations=VGroup(
            Tex(R"(2)-\frac{-3}{2}(1)",font_size=30),
            Tex(R"(3)-\frac{-2}{2}(1)",font_size=30),
            ).arrange(DOWN).next_to(arrow_step1,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step1=VGroup(
            SurroundingRectangle(operations[0][frac_patn],stroke_width=2,buff=REC_BUFF),
            SurroundingRectangle(operations[1][frac_patn],stroke_width=2,buff=REC_BUFF)
            )
        back_rec0=SurroundingRectangle(VGroup(eqns_step0,labels_step0),
            stroke_color=WHITE,stroke_opacity=0.5,buff=0.2)
        back_rec1=SurroundingRectangle(VGroup(eqns_step1,labels_step1),
            stroke_color=WHITE,stroke_opacity=0.5,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        numerator1,frac_symbol1,denominator1=self.extract_fraction_parts(operations[0],frac_patn)
        numerator2,frac_symbol2,denominator2=self.extract_fraction_parts(operations[1],frac_patn)
        self.play(FadeIn(note_step1[0],shift=RIGHT),ShowCreation(underline_step1),
            frame.animate.reorient(0, 0, 0, (0.0, -2.2, 0.0), 8.00),
            ShowCreation(back_rec0))
        self.wait()
        self.play(FadeIn(note_step1[1:],shift=RIGHT),GrowArrow(arrow_step1),ShowCreation(back_rec1))
        # copy 1st eqn
        tilt_line1=Line(stroke_color=RED).match_width(eqns_step0[1]["-3x"]).rotate(-PI/4).move_to(eqns_step0[1]["-3x"])
        tilt_line2=Line(stroke_color=RED).match_width(eqns_step0[2]["-2x"]).rotate(-PI/4).move_to(eqns_step0[2]["-2x"])
        self.play(TransformFromCopy(eqns_step0[0],eqns_step1[0]),
            TransformFromCopy(labels_step0[0],labels_step1[0]))
        rec=SurroundingRectangle(eqns_step0[0],stroke_color=RED,stroke_opacity=0.5,fill_opacity=0.5,fill_color=RED)
        self.play(Write(rec))
        self.play(TransformFromCopy(rec,tilt_line1,path_arc=-PI/2),
            ReplacementTransform(rec,tilt_line2,path_arc=-PI/2))
        self.play(FadeOut(tilt_line1),FadeOut(tilt_line2))
        self.play(
            TransformFromCopy(labels_step0[1],operations[0][0:3]),
            FadeIn(operations[0][3]),FadeIn(recs_step1[0]),
            TransformFromCopy(labels_step0[0],operations[0][-1:-4:-1].reverse_submobjects()),
            )
        self.play(
            TransformFromCopy(labels_step0[2],operations[1][0:3]),
            FadeIn(operations[1][3]),FadeIn(recs_step1[1]),
            TransformFromCopy(labels_step0[0],operations[1][-1:-4:-1].reverse_submobjects()),
            )
        self.play(LaggedStart(
            TransformFromCopy(eqns_step0[1][0:2],numerator1,path_arc=PI/2),
            TransformFromCopy(eqns_step0[0][0],denominator1[0],path_arc=PI/2),
            Write(frac_symbol1),
            lag_ratio=0.2),run_time=2)
        self.play(LaggedStart(
            TransformFromCopy(eqns_step0[2][0:2],numerator2,path_arc=PI/2),
            TransformFromCopy(eqns_step0[0][0],denominator2[0],path_arc=PI/2),
            Write(frac_symbol2),
            lag_ratio=0.2),run_time=2)
        
        # messy calculation
        arrow_to_right=Arrow(operations[0].get_right(),operations[0].get_right()+RIGHT*2.3)
        m1=TexEqn("-3x-y+2z=-11",isolate=pattern)
        m2=TexEqn("2x+y-z=8",isolate=pattern)
        m2_change=TexEqn(R"3x+\frac{3}{2}y-\frac{3}{2}z=12",isolate=pattern)
        result=TexEqn(R"\frac{1}{2}y+\frac{1}{2}z=1",isolate=pattern)
        messy=VGroup(m1,VGroup(m2,m2_change),result).arrange(DOWN)
        m1.align_eqn(refer)
        m2.align_eqn(refer)
        m2_change.align_eqn(refer)
        result.align_eqn(refer)
        messy.next_to(arrow_to_right,RIGHT,buff=2)
        left_br=Tex("(").next_to(m2_change,LEFT)
        right_br=Tex(")").next_to(m2_change,RIGHT)
        l_factor=Tex(R"\frac{-3}{2}",isolate=pattern).next_to(left_br,LEFT)
        minus=Tex("-").next_to(l_factor,LEFT)
        d_line=Line(minus.get_left(),right_br.get_right()).next_to(m2,DOWN,buff=0.5)
        symbols=VGroup(minus,left_br,right_br,l_factor,d_line)
        rec_whole=SurroundingRectangle(VGroup(messy,minus,d_line),buff=0.2,stroke_color=WHITE,
            fill_color=GREY,fill_opacity=0.2)
        dont_worry=Textch("一些琐碎的计算，不必关心细节！").next_to(rec_whole,UP)
        self.play(GrowArrow(arrow_to_right),
            frame.animate.reorient(0, 0, 0, (5.2, -2.2, 0.0), 8.00))
        self.play(FadeIn(rec_whole),FadeIn(dont_worry))
        self.play(LaggedStart(
            TransformFromCopy(operations[0][0:3],m1,path_arc=-PI/2),
            TransformFromCopy(operations[0][3],minus,path_arc=-PI/2),
            TransformFromCopy(operations[0][4:8],l_factor,path_arc=-PI/2),
            TransformFromCopy(operations[0][8:],m2,path_arc=-PI/2),
            Write(left_br),Write(right_br),ShowCreation(d_line)
            ,lag_ratio=0.5))
        self.play(LaggedStart(
            ReplacementTransform(VGroup(minus.copy(),l_factor.copy(),m2[0:2]),m2_change[0:2],path_arc=-PI/2),
            ReplacementTransform(VGroup(minus.copy(),l_factor.copy(),m2[2:4]),m2_change[2:7],path_arc=-PI/2),
            ReplacementTransform(VGroup(minus.copy(),l_factor.copy(),m2[4:6]),m2_change[7:12],path_arc=-PI/2),
            ReplacementTransform(VGroup(minus,l_factor,m2[6:]),m2_change[12:],path_arc=-PI/2),
            FadeOut(VGroup(left_br,right_br)),
            lag_ratio=0.5))
        self.play(LaggedStart(
            TransformFromCopy(VGroup(m1[0:3],m2_change[0:2]),VectorizedPoint(result.get_left()+LEFT)),
            TransformFromCopy(VGroup(m1[3:5],m2_change[2:7]),result[0:4]),
            TransformFromCopy(VGroup(m1[5:8],m2_change[7:12]),result[4:9]),
            TransformFromCopy(VGroup(m1[8],m2_change[12]),result[9]),
            TransformFromCopy(VGroup(m1[9:],m2_change[13:]),result[10]),
            lag_ratio=0.3))
        # go_back
        self.play(LaggedStartMap(FadeOut,VGroup(arrow_to_right,m1,m2_change,d_line,dont_worry,rec_whole),shift=RIGHT),
            TransformMatchingStrings(result,eqns_step1[1],time_span=[0,1.3]),
            frame.animate.reorient(0, 0, 0, (0.0, -2.2, 0.0)),
            FadeIn(labels_step1[1],shift=LEFT,time_span=[1,1.5]),run_time=1.5)
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(operations[1],eqns_step1[2]),
            FadeIn(labels_step1[2],shift=LEFT),lag_ratio=0.3
            ))

        # eqns_step2
        arrow_step2=Arrow(eqns_step1.get_bottom(),eqns_step1.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step2=CustomVGroup2(
            Tex("2x+y-z=8",isolate=pattern),
            Tex(R"\frac{1}{2}y+\frac{1}{2}z=1",isolate=pattern),
            Tex("-z=1",isolate=pattern),
            reference_eqn=eqns_step0.reference_eqn
            ).arrange(DOWN).next_to(arrow_step2,DOWN).align_eqns()
        labels_step2=get_labels_to(eqns_step2)
        note_step2=VGroup(
            Textch("第二步"),
            Textch("用方程"),
            Textch("消去它下面的"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step2_insert=VGroup(
            labels_step1[1].copy().next_to(note_step2[1],RIGHT,buff=0.1),
            Tex("y").next_to(note_step2[2],RIGHT,buff=0.1)
            )
        note_step2.add(note_step2_insert)
        note_step2.next_to(arrow_step2,LEFT,buff=3,aligned_edge=UP)
        underline_step2=Underline(note_step2[0],stroke_color=YELLOW)
        operations2=Tex(R"(3)-\frac{2}{1/2}(2)",font_size=30).next_to(arrow_step2,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step2=SurroundingRectangle(operations2[frac_patn],stroke_width=2,buff=REC_BUFF)
        numerator2,frac_symbol2,denominator2=self.extract_fraction_parts(operations2,frac_patn)
        back_rec1=SurroundingRectangle(VGroup(eqns_step2,labels_step2),
            stroke_color=WHITE,stroke_opacity=0.5,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step2,eqns_step2,labels_step2,note_step2,underline_step2,operations2,recs_step2)
        self.play(frame.animate.reorient(0, 0, 0, (0.0, -6.97, 0.0), 8.00))
        self.play(FadeIn(note_step2[0],shift=RIGHT),ShowCreation(underline_step2))
        self.play(FadeIn(note_step2[1:],shift=RIGHT))
        self.play(GrowArrow(arrow_step2),ShowCreation(back_rec1))
        self.play(
            TransformFromCopy(eqns_step1[0],eqns_step2[0]),
            TransformFromCopy(labels_step1[0],labels_step2[0]),
            TransformFromCopy(eqns_step1[1],eqns_step2[1]),
            TransformFromCopy(labels_step1[1],labels_step2[1])
            )
        # cross out
        rec=SurroundingRectangle(eqns_step1[1],stroke_color=RED,stroke_opacity=0.5,fill_opacity=0.5,fill_color=RED)
        tilt_line3=Line(stroke_color=RED).match_width(eqns_step1[2]["2y"]).rotate(-PI/4).move_to(eqns_step1[2]["2y"])
        self.play(Write(rec))
        self.play(ReplacementTransform(rec,tilt_line3,path_arc=-PI/2),)
        self.play(FadeOut(tilt_line3))
        self.play(
            TransformFromCopy(labels_step1[2],operations2[0:3]),
            FadeIn(operations2[3]),FadeIn(recs_step2),
            TransformFromCopy(labels_step1[1],operations2[-1:-4:-1].reverse_submobjects()),
            )
        self.play(LaggedStart(
            TransformFromCopy(eqns_step1[2][0],numerator2[0],path_arc=PI/2),
            TransformFromCopy(eqns_step1[1][0:3],denominator2,path_arc=PI/2),
            Write(frac_symbol2),
            lag_ratio=0.2),run_time=2)
        self.play(TransformFromCopy(operations2,eqns_step2[2]),
            FadeIn(labels_step2[2],shift=LEFT))
        # we can now solve
        ar1=Arrow(labels_step2[2].get_right(),labels_step2[2].get_right()+RIGHT,buff=0.05)
        ar2=Arrow(labels_step2[1].get_right(),labels_step2[1].get_right()+RIGHT,buff=0.05)
        ar3=Arrow(labels_step2[0].get_right(),labels_step2[0].get_right()+RIGHT,buff=0.05)
        s1=Tex("z=-1").next_to(ar1,RIGHT)
        s2=Tex("y=3").next_to(ar2,RIGHT)
        s3=Tex("x=4").next_to(ar3,RIGHT)
        u1=Arrow(s1.get_top(),s1.get_top()+UP*0.5,buff=0.01)
        u2=Arrow(s2.get_top(),s2.get_top()+UP*0.5,buff=0.01).match_x(u1)
        u3=Arrow(s1.get_right(),s3.get_bottom(),path_arc=PI/2)
        self.play(LaggedStart(
            GrowArrow(ar1),
            FadeIn(s1,shift=RIGHT*1.5)
            ))
        self.play(FadeOut(ar1))
        self.play(LaggedStart(
            GrowArrow(ar2),
            GrowArrow(u1),
            FadeIn(s2,shift=RIGHT*1.5)
            ))
        self.play(FadeOut(u1),FadeOut(ar2))
        self.play(LaggedStart(
            GrowArrow(ar3),
            GrowArrow(u2),GrowArrow(u3),
            FadeIn(s3,shift=RIGHT*1.5)
            ))
        self.play(FadeOut(u2),FadeOut(ar3),FadeOut(u3))

        # called gaussian elimination
        frame.save_state()
        big_br=Brace(VGroup(eqns_step0,eqns_step2,note_step1),LEFT,buff=0.8)
        gaussian=TextCustom(en="Gaussian Elimination",ch="高斯消元",
            font_size_en=80,font_size_ch=80)
        big_br.put_at_tip(gaussian)
        self.play(frame.animate.reorient(0, 0, 0, (-3.07, -4.56, 0.0), 13.42),)
        self.play(LaggedStartMap(FadeIn,
            VGroup(big_br,gaussian),shift=RIGHT,lag_ratio=0.02))
        self.wait()
        self.play(frame.animate.restore())

        # dont want solve this way
        line_out=VGroup(
            Line().insert_n_curves(20).set_stroke(RED,[3,6,0]).replace(s1,stretch=True),
            Line().insert_n_curves(20).set_stroke(RED,[3,6,0]).replace(s2,stretch=True),
            Line().insert_n_curves(20).set_stroke(RED,[3,6,0]).replace(s3,stretch=True),
            )
        self.play(*map(ShowCreation,line_out))
        self.play(LaggedStartMap(FadeOut,VGroup(line_out,s3,s2,s1),shift=RIGHT))

        # jordan continue--step3
        arrow_step3=Arrow(eqns_step2.get_bottom(),eqns_step2.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step3=CustomVGroup2(
            TexEqn("2x+y-z=8",isolate=pattern),
            TexEqn(R"\frac{1}{2}y+\frac{1}{2}z=1",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=eqns_step0.reference_eqn
            ).arrange(DOWN).next_to(arrow_step3,DOWN).align_eqns()
        labels_step3=get_labels_to(eqns_step3)
        note_step3=VGroup(
            Textch("第三步"),
            Textch("归一化"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step3_insert=VGroup(
            labels_step2[2].copy().next_to(note_step3[1],RIGHT,buff=0.1),
            )
        note_step3.add(note_step3_insert)
        note_step3.next_to(arrow_step3,LEFT,buff=3,aligned_edge=UP).align_to(note_step2,LEFT)
        underline_step3=Underline(note_step3[0],stroke_color=YELLOW)
        operations3=Tex(R"\frac{1}{-1}\cdot(3)",font_size=30).next_to(arrow_step3,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step3=SurroundingRectangle(operations3[frac_patn],stroke_width=2,buff=REC_BUFF)
        numerator3,frac_symbol3,denominator3=self.extract_fraction_parts(operations3,frac_patn)
        back_rec3=SurroundingRectangle(VGroup(eqns_step3,labels_step3),
            stroke_color=WHITE,stroke_opacity=0.5,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step3,eqns_step3,labels_step3)
        # self.add(note_step3,underline_step3,operations3,recs_step3,back_rec3)
        self.play(frame.animate.reorient(0, 0, 0, (0.0, -11.7, 0.0), 8),
            )
        self.play(FadeIn(note_step3[0],shift=RIGHT),ShowCreation(underline_step3))
        self.play(FadeIn(note_step3[1:],shift=RIGHT))
        self.play(GrowArrow(arrow_step3),ShowCreation(back_rec3))
        self.play(
            TransformFromCopy(eqns_step2[0],eqns_step3[0]),
            TransformFromCopy(eqns_step2[1],eqns_step3[1]),
            TransformFromCopy(labels_step2[0],labels_step3[0]),
            TransformFromCopy(labels_step2[1],labels_step3[1]),
            )
        self.play(TransformFromCopy(labels_step2[2],operations3["(3)"][0]),
            FadeIn(operations3[R"\cdot"][0]),FadeIn(frac_symbol3),
                FadeIn(numerator3))
        self.play(ShowCreation(recs_step3))
        self.play(TransformFromCopy(eqns_step2[2]["-"],denominator3))
        self.play(TransformFromCopy(operations3,eqns_step3[2]),FadeIn(labels_step3[2],shift=LEFT))

        # step3_2
        arrow_step3_2=Arrow(eqns_step3.get_bottom(),eqns_step3.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step3_2=CustomVGroup2(
            TexEqn("2x+y=7",isolate=pattern),
            TexEqn(R"\frac{1}{2}y=\frac{3}{2}",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN).next_to(arrow_step3_2,DOWN).align_eqns()
        labels_step3_2=get_labels_to(eqns_step3_2)
        note_step3_2=VGroup(
            Textch("用方程"),
            Textch("消去它上面的"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step3_2_insert=VGroup(
            labels_step3[2].copy().next_to(note_step3_2[0],RIGHT,buff=0.1),
            Tex("z").next_to(note_step3_2[1],RIGHT,buff=0.1),
            )
        note_step3_2.add(note_step3_2_insert)
        note_step3_2.next_to(arrow_step3_2,LEFT,buff=3,aligned_edge=UP).align_to(note_step3,LEFT)
        operations3_2=VGroup(
            Tex(R"(2)-\frac{1}{2}(3)",font_size=30).next_to(arrow_step3_2,RIGHT),
            Tex(R"(1)--1(3)",font_size=30).next_to(arrow_step3_2,RIGHT),
        ).arrange(DOWN,aligned_edge=LEFT).next_to(arrow_step3_2,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step3_2=VGroup(
            SurroundingRectangle(operations3_2[0][frac_patn],stroke_width=2,buff=REC_BUFF),
            SurroundingRectangle(operations3_2[1]["-1"],stroke_width=2,buff=REC_BUFF),
            )
        numerator3_2,frac_symbol3_2,denominator3_2=self.extract_fraction_parts(operations3_2[0],frac_patn)
        back_rec3_2=SurroundingRectangle(VGroup(eqns_step3_2,labels_step3_2),
            stroke_color=WHITE,stroke_opacity=0.5,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step3_2,eqns_step3_2,labels_step3_2,note_step3_2,operations3_2,
        #     recs_step3_2,back_rec3_2)
        self.play(frame.animate.reorient(0, 0, 0, (0, -15.88, 0.0), 8.00))
        self.play(FadeIn(note_step3_2[0],shift=RIGHT),
            FadeIn(note_step3_2_insert[0],shift=RIGHT)
            )
        self.play(FadeIn(note_step3_2[1],shift=RIGHT),
            FadeIn(note_step3_2_insert[1],shift=RIGHT)
            )
        self.play(GrowArrow(arrow_step3_2),ShowCreation(back_rec3_2))
        self.play(
            TransformFromCopy(eqns_step3[2],eqns_step3_2[2]),
            TransformFromCopy(labels_step3[2],labels_step3_2[2]),
            )
        self.play(
            TransformFromCopy(labels_step3[2],operations3_2[0]["(3)"][0]),
            TransformFromCopy(labels_step3[1],operations3_2[0]["(2)"][0]),
            FadeIn(operations3_2[0]["-"][0]),
            )
        self.play(ShowCreation(recs_step3_2[0]),
            TransformFromCopy(eqns_step3[1][5:8],operations3_2[0][R"\frac{1}{2}"][0])
            )
        self.play(FadeTransform(operations3_2[0].copy(),eqns_step3_2[1]),
            FadeIn(labels_step3_2[1],shift=LEFT))
        self.play(TransformFromCopy(labels_step3[2],operations3_2[1]["(3)"][0]),
            TransformFromCopy(labels_step3[0],operations3_2[1]["(1)"][0]),
            FadeIn(operations3_2[1]["-"][0]),FadeIn(recs_step3_2[1]),)
        self.play(TransformFromCopy(eqns_step3[0]["-"][0],operations3_2[1]["-1"][0]))
        self.play(FadeTransform(operations3_2[1].copy(),eqns_step3_2[0]),
            FadeIn(labels_step3_2[0],shift=LEFT))

        # step4
        arrow_step4=Arrow(eqns_step3_2.get_bottom(),eqns_step3_2.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step4=CustomVGroup2(
            TexEqn("2x+y=7",isolate=pattern),
            TexEqn("y=3",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN).next_to(arrow_step4,DOWN).align_eqns()
        labels_step4=get_labels_to(eqns_step4)
        note_step4=VGroup(
            Textch("第四步"),
            Textch("归一化"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step4_insert=VGroup(
            labels_step3_2[1].copy().next_to(note_step4[1],RIGHT,buff=0.1),
            )
        note_step4.add(note_step4_insert)
        note_step4.next_to(arrow_step4,LEFT,buff=3,aligned_edge=UP).align_to(note_step2,LEFT)
        underline_step4=Underline(note_step4[0],stroke_color=YELLOW)
        operations4=Tex(R"\frac{1}{1/2}\cdot(2)",font_size=30).next_to(arrow_step4,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step4=SurroundingRectangle(operations4[frac_patn],stroke_width=2,buff=REC_BUFF)
        numerator4,frac_symbol4,denominator4=self.extract_fraction_parts(operations4,frac_patn)
        back_rec4=SurroundingRectangle(VGroup(eqns_step4,labels_step4),
            stroke_color=WHITE,stroke_opacity=0.5,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step4,eqns_step4,labels_step4)
        # self.add(note_step4,underline_step4,operations4,recs_step4,back_rec4)
        self.play(frame.animate.reorient(0, 0, 0, (0.0, -20.6, 0.0), 8),
            )
        self.play(FadeIn(note_step4[0],shift=RIGHT),ShowCreation(underline_step4))
        self.play(FadeIn(note_step4[1:],shift=RIGHT))
        self.play(GrowArrow(arrow_step4),ShowCreation(back_rec4))
        self.play(
            TransformFromCopy(eqns_step3_2[0],eqns_step4[0]),
            TransformFromCopy(eqns_step3_2[2],eqns_step4[2]),
            TransformFromCopy(labels_step3_2[0],labels_step4[0]),
            TransformFromCopy(labels_step3_2[2],labels_step4[2]),
            )
        self.play(TransformFromCopy(labels_step3_2[1],operations4["(2)"][0]),
            FadeIn(operations3[R"\cdot"][0]),FadeIn(frac_symbol4),
                FadeIn(numerator4))
        self.play(ShowCreation(recs_step4))
        self.play(TransformFromCopy(eqns_step3_2[1][R"\frac{1}{2}"][0],denominator4))
        self.play(FadeTransform(operations4,eqns_step4[1]).copy(),FadeIn(labels_step4[1],shift=LEFT))

        # step4_2
        arrow_step4_2=Arrow(eqns_step4.get_bottom(),eqns_step4.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step4_2=CustomVGroup2(
            TexEqn("2x=4",isolate=pattern),
            TexEqn("y=3",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN).next_to(arrow_step4_2,DOWN).align_eqns()
        labels_step4_2=get_labels_to(eqns_step4_2)
        note_step4_2=VGroup(
            Textch("用方程"),
            Textch("消去它上面的"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step4_2_insert=VGroup(
            labels_step4[1].copy().next_to(note_step4_2[0],RIGHT,buff=0.1),
            Tex("y").next_to(note_step4_2[1],RIGHT,buff=0.1),
            )
        note_step4_2.add(note_step4_2_insert)
        note_step4_2.next_to(arrow_step4_2,LEFT,buff=3,aligned_edge=UP).align_to(note_step3,LEFT)
        operations4_2=Tex(R"(1)-(2)",font_size=35).next_to(arrow_step3_2,RIGHT)\
            .next_to(arrow_step4_2,RIGHT)
        back_rec4_2=SurroundingRectangle(VGroup(eqns_step4_2,labels_step4_2),
            stroke_color=WHITE,stroke_opacity=0.5,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step4_2,eqns_step4_2,labels_step4_2,note_step4_2,operations4_2,
        #     recs_step4_2,back_rec4_2)
        self.play(frame.animate.reorient(0, 0, 0, (0, -24.5, 0.0), 8.00))
        self.play(FadeIn(note_step4_2[0],shift=RIGHT),
            FadeIn(note_step4_2_insert[0],shift=RIGHT)
            )
        self.play(FadeIn(note_step4_2[1],shift=RIGHT),
            FadeIn(note_step4_2_insert[1],shift=RIGHT)
            )
        self.play(GrowArrow(arrow_step4_2),ShowCreation(back_rec4_2))
        self.play(
            TransformFromCopy(eqns_step4[1],eqns_step4_2[1]),
            TransformFromCopy(labels_step4[1],labels_step4_2[1]),
            TransformFromCopy(eqns_step4[2],eqns_step4_2[2]),
            TransformFromCopy(labels_step4[2],labels_step4_2[2]),
            )
        self.play(
            TransformFromCopy(labels_step4[0],operations4_2["(1)"][0]),
            TransformFromCopy(labels_step4[1],operations4_2["(2)"][0]),
            FadeIn(operations4_2[3])
            )

        self.play(FadeTransform(operations4_2.copy(),eqns_step4_2[0]),
            FadeIn(labels_step4_2[0],shift=LEFT))

        # step5
        arrow_step5=Arrow(eqns_step4_2.get_bottom(),eqns_step4_2.get_bottom()+DOWN*ARROW_LENGTH)
        eqns_step5=CustomVGroup2(
            TexEqn("x=2",isolate=pattern),
            TexEqn("y=3",isolate=pattern),
            TexEqn("z=-1",isolate=pattern),
            reference_eqn=refer
            ).arrange(DOWN).next_to(arrow_step5,DOWN).align_eqns()
        labels_step5=get_labels_to(eqns_step5)
        note_step5=VGroup(
            Textch("第五步"),
            Textch("归一化"),
            ).arrange(DOWN,aligned_edge=LEFT)
        note_step5_insert=VGroup(
            labels_step5[0].copy().next_to(note_step5[1],RIGHT,buff=0.1),
            )
        note_step5.add(note_step5_insert)
        note_step5.next_to(arrow_step5,LEFT,buff=3,aligned_edge=UP).align_to(note_step2,LEFT)
        underline_step5=Underline(note_step5[0],stroke_color=YELLOW)
        operations5=Tex(R"\frac{1}{2}\cdot(1)",font_size=30).next_to(arrow_step5,RIGHT)
        frac_patn=re.compile(r"\\frac\{[+-]?(\d+|\d+/\d+)\}\{[+-]?(\d+|\d+/\d+)\}")
        recs_step5=SurroundingRectangle(operations5[frac_patn],stroke_width=2,buff=REC_BUFF)
        numerator5,frac_symbol5,denominator5=self.extract_fraction_parts(operations5,frac_patn)
        back_rec5=SurroundingRectangle(VGroup(eqns_step5,labels_step5),
            stroke_color=WHITE,stroke_opacity=0.5,buff=0.2).match_width(back_rec0).match_x(back_rec0)
        # self.add(arrow_step4,eqns_step4,labels_step4)
        # self.add(note_step4,underline_step4,operations4,recs_step4,back_rec4)
        self.play(frame.animate.reorient(0, 0, 0, (0.0, -28.5, 0.0), 8),
            )
        self.play(FadeIn(note_step5[0],shift=RIGHT),ShowCreation(underline_step5))
        self.play(FadeIn(note_step5[1:],shift=RIGHT))
        self.play(GrowArrow(arrow_step5),ShowCreation(back_rec5))
        self.play(
            TransformFromCopy(eqns_step4_2[1],eqns_step5[1]),
            TransformFromCopy(eqns_step4_2[2],eqns_step5[2]),
            TransformFromCopy(labels_step4_2[1],labels_step5[1]),
            TransformFromCopy(labels_step4_2[2],labels_step5[2]),
            )
        self.play(TransformFromCopy(labels_step4_2[0],operations5["(1)"][0]),
            FadeIn(operations5[R"\cdot"][0]),FadeIn(frac_symbol5),
            FadeIn(numerator5),ShowCreation(recs_step5))
        self.play(TransformFromCopy(eqns_step4_2[0][0],denominator5[0]))
        self.play(FadeTransform(operations5.copy(),eqns_step5[0]),FadeIn(labels_step5[0],shift=LEFT))
        # align variables
        eqns_step5.save_state()
        self.play(
            eqns_step5[0][0].animate.match_x(eqns_step5[2][0]),
            eqns_step5[1][0].animate.match_x(eqns_step5[2][0]),
            )
        self.wait()
        self.play(eqns_step5.animate.restore())

        # show gaussian jordan elimination
        big_br2=Brace(VGroup(eqns_step5,eqns_step0,gaussian),LEFT,buff=0.8)
        jordan=TextCustom(en="Gauss–Jordan Elimination",ch="高斯-若尔当消元",
            font_size_ch=200,font_size_en=200,buff=1)
        big_br2.put_at_tip(jordan)
        self.play(frame.animate.reorient(0, 0, 0, (-8.53, -14.74, 0.0), 35.05),)
        self.play(LaggedStartMap(FadeIn,
            VGroup(big_br2,jordan),shift=RIGHT*2,lag_ratio=0.02))
        self.wait()

        # let frame go to original position
        self.play(frame.animate.reorient(0, 0, 0, (0.15, -1.45, 0.0), 7.21)
            ,run_time=2)

        # go to right board
        SHIFT=10.5
        eqn_matrix=eqns_step0.copy().shift(RIGHT*SHIFT)
        labels_eqn_matrix=labels_step0.copy().shift(RIGHT*SHIFT)
        # self.add(eqn_matrix,labels_eqn_matrix)
        self.play(TransformFromCopy(eqns_step0,eqn_matrix),
            TransformFromCopy(labels_step0,labels_eqn_matrix),
            frame.animate.match_x(eqn_matrix),
            run_time=2)

        # write notes
        s1=SurroundingRectangle(VGroup(eqn_matrix,labels_eqn_matrix))
        ar_s1=ArrowCustom().point_to(s1.get_corner(DL),PI/4).set_color(YELLOW)
        text_original=Textch("原始方程组").move_to(ar_s1.get_start())\
        .shift(-ar_s1.get_vector()*0.5)
        text_redifine=Textch("用矩阵的形式\n重新定义这个方程组").move_to(ar_s1.get_start())\
        .shift(-ar_s1.get_vector()*0.8)
        self.add(s1,ar_s1)
        self.add(text_original)
        self.play(ShowCreation(s1),GrowArrow(ar_s1),FadeIn(text_original))
        self.wait()
        self.play(FadeOut(text_original,shift=RIGHT),
            FadeIn(text_redifine,shift=RIGHT))

        # you may ask why??
        kun=Kun().next_to(text_redifine,RIGHT).shift(DOWN)
        bubble=Bubble(Textch("为什么非要写成矩阵形式？")).pin_to(kun.right_eye)
        self.play(FadeIn(kun,shift=LEFT))
        self.play(LaggedStart(
            kun.animate.look_at(bubble).shock(),
            ShowCreation(bubble),lag_ratio=0.3
            ))
        self.wait()
        self.play(FadeOut(bubble,shift=LEFT+DOWN),kun.animate.peace().look_at(eqns_step0))

        # define function
        def process_equations(eqns_step2, refer, pattern):
            """
            处理方程列表，补全缺失的 x、y、z，并应用动画效果。

            :param eqns_step2: 需要处理的方程列表
            :param refer: 参考方程对象
            :param pattern: 用于 `isolate` 参数的正则模式
            """
            non_change_pattern = re.compile(r"=|x|y|z")
            anims = []

            for eqn in eqns_step2:
                original_string = eqn.string
                
                # **拆分等号**
                if "=" in original_string:
                    left_part, right_part = original_string.split("=", 1)
                else:
                    left_part, right_part = original_string, "0"  # 防止无等号情况

                # **检查变量 x, y, z 是否存在**
                has_x = "x" in left_part
                has_y = "y" in left_part
                has_z = "z" in left_part

                # **补全缺失变量**
                if not has_x and not has_y and not has_z:
                    left_part = "0x+0y+0z"  # 三个变量都缺失

                elif not has_x and not has_y:
                    left_part = "0x+0y+" + left_part  # 缺失 x 和 y

                elif not has_y and not has_z:
                    left_part = left_part + "+0y+0z"  # 缺失 y 和 z

                else:
                    # **处理单个变量缺失的情况**
                    if not has_x:
                        left_part = "0x+" + left_part  # x 缺失，补在最前

                    if not has_y:
                        if re.search(r"[-+]\s*z", left_part):  # 若 `z` 之前有 `+/-`
                            left_part = left_part.replace("z", "0y+z", 1)
                        else:
                            left_part = left_part + "+0y"  # y 缺失，补在 `z` 之前

                    if not has_z:
                        left_part = left_part + "+0z"  # z 缺失，补在最后

                # **修正 `++` 或 `+-`**
                left_part = re.sub(r"\+\+", "+", left_part)
                left_part = re.sub(r"\+-", "-", left_part)

                # **拼接回去**
                new_string = left_part + "=" + right_part

                # **生成新 Tex 对象并对齐**
                if new_string != original_string:
                    new_tex = TexEqn(new_string, isolate=pattern).align_eqn(refer).match_y(eqn).set_color(TEAL)
                    for part in new_tex[re.compile(r"0x\+|0y\+|0y|0z|\+0z|\+0y")]:
                        anims.append(FadeIn(part, rate_func=there_and_back))

                for part in eqn[non_change_pattern]:
                    anims.append(part.animate.set_color(TEAL).set_anim_args(rate_func=there_and_back))

            return anims
        # go through steps
        eqns_steps = [eqns_step1, eqns_step2, eqns_step3, eqns_step3_2, 
                      eqns_step4, eqns_step4_2, eqns_step5]
        self.play(frame.animate.scale(1.6).move_to(eqns_step0).shift(DOWN*3),
            kun.animate.next_to(eqns_step0,buff=1) )
        self.play(LaggedStart(*process_equations(eqns_step0, refer, pattern)),
            kun.animate.look([-1,-0.2,0]),run_time=1)
        TIME=10
        DISTANCE1=frame.get_top()[1]-eqns_step5.get_bottom()[1]
        DISTANCE2=DISTANCE1+10
        VELOCITY1=DISTANCE1/TIME
        VELOCITY2=DISTANCE2/TIME
        def updater1(mob,dt):
            mob.shift(DOWN*VELOCITY1*dt)
        def updater2(mob,dt):
            mob.shift(DOWN*VELOCITY2*dt)
        def play_equation_steps(frame, kun, eqns_steps, refer, pattern,time=TIME):
            frame.add_updater(updater1)
            kun.add_updater(updater2)
            each_time=TIME/(len(eqns_steps)+2)
            current_eqn = eqns_steps[0]
            for i,eqns in enumerate(eqns_steps):
                current_eqn = eqns
                if i == len(eqns_steps)-1:
                    frame.clear_updaters()
                    kun.clear_updaters()
                self.play(LaggedStart(*process_equations(eqns, refer, pattern)), run_time=each_time)
                
        play_equation_steps(frame, kun, eqns_steps, refer, pattern)
        self.play(kun.animate.close_eyes().set_anim_args(rate_func=there_and_back))

        # go back
        frame.reorient(0, 0, 0, (10.26, -1.73, 0.0), 7.15)
        self.remove(kun)
        s1_change=SurroundingRectangle(VGroup(eqn_matrix[0],labels_eqn_matrix[0]),buff=0.15)
        ar_s1_change=ArrowCustom().point_to(s1_change.get_left()).set_color(YELLOW)
        self.play(FadeOut(text_redifine,shift=LEFT),
            Transform(s1,s1_change),Transform(ar_s1,ar_s1_change),
            VGroup(eqn_matrix[1:],labels_eqn_matrix[1:]).animate.set_opacity(0.5))






        



        
        
        
        




        


        
        



        


        
class test_scene(elimination):
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
        pivots_dict,mats1,mats2=self.elimination(self.aug4,True)
        self.add(mats2.arrange(DOWN))

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

class statistics(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        
        # statistics
        ax=Axes((-2,10),(-2,10))
        a = 0.5  # 斜率
        b = 2  # 截距
        x = np.linspace(*ax.x_range[0:2] ,400)
        y = a * x + b
        np.random.seed(626)
        noise = np.random.normal(0, 0.5, size=x.shape)  # 均值为 0，标准差为 3
        y_noisy = y + noise
        dots1=Group()
        dots1.add(*[TrueDot(ax.c2p(x,y,0)) for x,y in zip(x,y_noisy)])
        line=ax.get_graph(lambda x:a*x+b)
        dots1.set_submobject_colors_by_gradient(YELLOW,TEAL)
        line.set_color(RED)
        strings=[]
        for x,y in zip(x,y_noisy):
            strings.append(f"{x:.2f}a+b={y:.2f}") # x is slope,y is intercept
        points_eqns=VGroup(*[Tex(string,t2c={"a":RED,"b":RED}) for string in strings[:5]])
        points_eqns.add(Tex(R"\vdots"))
        points_eqns.add(*[Tex(string,t2c={"a":RED,"b":RED}) for string in strings[-5:]])
        points_eqns.arrange(DOWN)
        points_eqns.set_submobject_colors_by_gradient(YELLOW,TEAL)
        for eqn in points_eqns:
            eqn["a"].set_color(RED)
            eqn["b"].set_color(RED)
            eqn["+"].set_color(WHITE)
            eqn["="].set_color(WHITE)
        line_label=Tex("ax+b=y",t2c={"a":RED,"b":RED,"x":YELLOW,"y":YELLOW}).scale(1.5).next_to(line.get_end(),RIGHT,buff=0.8)
        points_eqns.next_to(line_label,DOWN)
        frame.reorient(0, 0, 0, (1.09, 0.06, 0.0), 12.40)
        self.add(ax)
        dots1.set_z(20).set_opacity(0)
        self.play(
            LaggedStart(*[d.animate.set_z(0).set_opacity(1) for d in dots1.shuffle()])
            ,run_time=2)
        self.play(ShowCreation(line),Write(line_label),
            frame.animate.reorient(0, 0, 0, (2.07, 0.04, 0.0), 12.40),
            run_time=1)
        self.play(
            LaggedStart(
                *[ReplacementTransform(VectorizedPoint(d.get_center()),eqn)
                for d,eqn in zip(dots1[0:5],points_eqns[0:5])],
                Write(points_eqns[5]),
                *[ReplacementTransform(VectorizedPoint(d.get_center()),eqn)
                for d,eqn in zip(dots1[-5:],points_eqns[-5:])])
            ,run_time=3)
        self.wait()

        # fitting a plane
        ax2=ThreeDAxes(x_range=(-2, 10), y_range=(-2, 10), z_range=(-2, 10))
        a = 0.5  # x的系数
        b = 1.0  # y的系数
        c = 2.0  # z的系数
        d = 3.0  # 平面偏移
        x_vals = np.linspace(*ax2.x_range[0:2], 20)
        y_vals = np.linspace(*ax2.y_range[0:2], 20)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = a * X + b * Y + c
        np.random.seed(626)
        noise = np.random.normal(0, 0.5, size=Z.shape)
        Z_noisy = Z + noise
        dots2 = Group()
        for x, y, z in zip(X.flatten(), Y.flatten(), Z_noisy.flatten()):
            dots2.add(TrueDot(ax2.c2p(x, y, z), color=WHITE))
        dots2.set_submobject_colors_by_gradient(YELLOW,TEAL)
        plane = ax2.get_graph(lambda x, y: a*x + b*y + c, u_range=[-2, 10], v_range=[-2, 10])
        plane.set_color(RED).set_opacity(0.5)
        plane_eqn = Tex(f"ax + by + c=z", t2c={"a": RED, "b": RED, "c": RED,"x":YELLOW,"y":YELLOW,"z":YELLOW})
        plane_eqn.to_corner(UR)
        plane_eqn.fix_in_frame()
        strings2=[]
        for x,y,z in zip(X.flatten(), Y.flatten(), Z_noisy.flatten()):
            strings2.append(f"{x:.1f}a+{y:.1f}b+c={z:.1f}") # x is slope,y is intercept
        num=16
        points_eqns2=VGroup(*[Tex(string) for string in strings2[:num]])
        points_eqns2.add(Tex(R"\vdots"))
        points_eqns2.arrange(DOWN)
        points_eqns2.set_submobject_colors_by_gradient(YELLOW,TEAL)
        points_eqns2.fix_in_frame()
        points_eqns2.match_width(plane_eqn)
        points_eqns2.next_to(plane_eqn,DOWN)
        for eqn in points_eqns2:
            eqn["a"].set_color(RED)
            eqn["b"].set_color(RED)
            eqn["c"].set_color(RED)
            eqn["+"].set_color(WHITE)
            eqn["="].set_color(WHITE)
        self.add(ax2[0:2])
        self.remove(ax)
        self.play(
            FadeOut(line),
            FadeOut(line_label),FadeOut(points_eqns),
            frame.animate.reorient(44, 71, 0, (1.38, 1.3, 5.77), 12.15),
            ShowCreation(ax2[2]),
            LaggedStart(
            *[d1.animate.move_to(d2) for d1,d2 in zip(dots1,dots2)]
            ),run_time=3,rate_func=linear)
        self.add(dots2)
        self.remove(dots1)
        self.play(ShowCreation(plane,time_span=[0,1]),
            LaggedStart(Write(plane_eqn),
                *[ReplacementTransform(VectorizedPoint(p.get_center()),eqn) 
                for p,eqn in zip(dots2[:num],points_eqns2[:num])],
                Write(points_eqns2[-1])),
            frame.animate.reorient(88, 59, 0, (0.42, 1.23, 7.46), 10.38),run_time=3)
        self.wait()
        
        # fadeout
        self.play(
            VGroup(plane_eqn,points_eqns2).animate.to_edge(LEFT).set_anim_args(time_span=[0.5,1.5]),
            LaggedStartMap(FadeOut,Group(ax2,plane,dots2),shift=-ax2.y_axis.get_unit_vector()),
            run_time=2)
        
        # font
        text=Text("线性方程组",font="Microsoft JhengHei")
        text.fix_in_frame().scale(1.5).center()
        self.add(text)
        
class circuit(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # circuit
        frame.reorient(0, 0, 0, (-1.4, 0.06, 0.0), 12.40)
        r1=Rectangle(4,1)
        r2=Rectangle(4,1)
        r3=Rectangle(4,1)
        resistances=VGroup(r1,r2,r3).arrange(DOWN,buff=3)
        short_line=Line().rotate(PI/2)
        long_line=Rectangle(3.5,0.1,fill_color=WHITE,fill_opacity=1).rotate(PI/2)
        source1=VGroup(long_line,short_line).arrange(RIGHT,buff=0.5).scale(0.5)
        source1.next_to(r2,LEFT,buff=4)
        source2=source1.copy().flip().next_to(r3,LEFT,buff=4)
        dot1=Dot(radius=0.15).next_to(source1,LEFT,buff=4)
        dot2=Dot(radius=0.15).next_to(r2,RIGHT,buff=4)
        circuit_up=VGroup(
            source1,
            Line(source1.get_left(),dot1.get_center()),
            dot1,
            Line(dot1.get_center(),np.array([dot1.get_x(),r1.get_y(),0])),
            Line(np.array([dot1.get_x(),r1.get_y(),0]),r1.get_left()),
            r1,
            Line(r1.get_right(),np.array([dot2.get_x(),r1.get_y(),0])),
            Line(np.array([dot2.get_x(),r1.get_y(),0]),dot2.get_center()),
            dot2,
            Line(dot2.get_center(),r2.get_right()),
            r2,
            Line(r2.get_left(),source1.get_right()),)
        circuit_down=VGroup(
            Line(dot2.get_center(),np.array([dot2.get_x(),r3.get_y(),0])),
            Line(np.array([dot2.get_x(),r3.get_y(),0]),r3.get_right()),
            r3,
            Line(r3.get_left(),source2.get_right())  ,
            source2,
            Line(source2.get_left(),np.array([dot1.get_x(),r3.get_y(),0]))  ,
            Line(np.array([dot1.get_x(),r3.get_y(),0]),dot1.get_center())  ,
            )
        
        scale_factor=2
        r1_label=Tex("R1").scale(scale_factor).next_to(r1,UP,buff=0.5)
        r2_label=Tex("R2").scale(scale_factor).next_to(r2,UP,buff=0.5)
        r3_label=Tex("R3").scale(scale_factor).next_to(r3,UP,buff=0.5)
        epsilon1=Tex(R"\epsilon_1").scale(scale_factor).next_to(source1,UP,buff=0.5)
        epsilon2=Tex(R"\epsilon_2").scale(scale_factor).next_to(source2,UP,buff=0.5)
        labels=VGroup(r1_label,r2_label,r3_label,epsilon1,epsilon2)
        circuit=VGroup(labels,circuit_up,circuit_down,r1,r2,r3,dot1,dot2,source1,source2)

        self.add(circuit_up,circuit_down)
        self.play(LaggedStartMap(Write,labels))
        
        # i1,i2,i3
        i1=Arrow(dot2.get_center()+np.array([0,3,0]),dot2.get_center(),tip_width_ratio=10)
        i2=Arrow(dot2.get_center(),dot2.get_center()+np.array([-3,0,0]),tip_width_ratio=10)
        i3=Arrow(dot2.get_center(),dot2.get_center()+np.array([0,-3,0]),tip_width_ratio=10)
        i1.set_color(RED)
        i2.set_color(YELLOW)
        i3.set_color(BLUE)
        i1.shift(RIGHT*0.2)
        i2.shift(UP*0.2)
        i3.shift(RIGHT*0.2)        
        i1_label=Tex("i_1").scale(2).next_to(i1,RIGHT).match_color(i1)
        i2_label=Tex("i_2").scale(2).next_to(i2,UP).match_color(i2)
        i3_label=Tex("i_3").scale(2).next_to(i3,RIGHT).match_color(i3)
        # self.add(i1_label,i2_label,i3_label)

        self.play(LaggedStart(
                (line.animate.set_color(BLUE)
                 .set_anim_args(rate_func=there_and_back)
                 for line in circuit_up[0:9]
                ),lag_ratio=0.2
            ),Write(i1,time_span=[0.5,1]),run_time=1)
        self.play(LaggedStart(
                (line.animate.set_color(BLUE)
                 .set_anim_args(rate_func=there_and_back)
                 for line in circuit_up[9:]
                ),lag_ratio=0.2,
            ),
                LaggedStart(
                (line.animate.set_color(BLUE)
                 .set_anim_args(rate_func=there_and_back)
                 for line in circuit_down
                ),lag_ratio=0.2,
            ),Write(i2,time_span=[0.5,1]),Write(i3,time_span=[0.5,1]),run_time=1)
        self.play(Write(i1_label),Write(i2_label),Write(i3_label))


        # circuit eqn
        kcl=Tex(R"i_1-i_2-i_3=0",t2c={"i_1":RED,"i_2":YELLOW,"i_3":BLUE})
        kvl1=Tex(R"-R_2i_2+\epsilon_1-R_1i_1=0",t2c={"i_1":RED,"i_2":YELLOW,"i_3":BLUE})
        kvl2=Tex(R"-R_3i_3-\epsilon_2-\epsilon_1+R_2i_2=0",t2c={"i_1":RED,"i_2":YELLOW,"i_3":BLUE})
        circuit_eqns=VGroup(kcl,kvl1,kvl2).arrange(DOWN,aligned_edge=RIGHT)
        circuit_eqns.scale(3).next_to(circuit,DOWN,buff=2)
        self.play(
            frame.animate.reorient(0, 0, 0, (-0.97, -1.64, 0.0), 16.31).set_anim_args(time_span=[0,1]),
            LaggedStart(
            FadeTransform(i1_label.copy(),kcl["i_1"]),
            FadeTransform(i2_label.copy(),kcl["i_2"]),
            FadeTransform(i3_label.copy(),kcl["i_3"]),lag_ratio=0.2
            ),Write(kcl["-"],time_span=[1,2]),Write(kcl["=0"],time_span=[1,2]),run_time=2)
        self.play(
            frame.animate.reorient(0, 0, 0, (-0.98, -2.59, 0.0), 17.70).set_anim_args(time_span=[0,1]),
            LaggedStart(
            FadeTransform(r2_label.copy(),kvl1["R_2"]),
            FadeTransform(i2_label.copy(),kvl1["i_2"]),
            FadeTransform(epsilon1.copy(),kvl1[R"\epsilon_1"]),
            FadeTransform(r1_label.copy(),kvl1["R_1"]),
            FadeTransform(i1_label.copy(),kvl1["i_1"]),
            lag_ratio=0.2),
            Write(kvl1["-"],time_span=[1,2]),
            Write(kvl1["+"],time_span=[1,2]),
            Write(kvl1["=0"],time_span=[1,2]),
            run_time=2)
        self.play(
            frame.animate.reorient(0, 0, 0, (-0.98, -2.85, 0.0), 20.86).set_anim_args(time_span=[0,1]),
            LaggedStart(
            FadeTransform(r3_label.copy(),kvl2["R_3"]),
            FadeTransform(i3_label.copy(),kvl2["i_3"]),
            FadeTransform(epsilon1.copy(),kvl2[R"\epsilon_1"]),
            FadeTransform(epsilon2.copy(),kvl2[R"\epsilon_2"]),
            FadeTransform(r2_label.copy(),kvl2["R_2"]),
            FadeTransform(i2_label.copy(),kvl2["i_2"]),
            lag_ratio=0.2),
            Write(kvl2["-"],time_span=[1,2]),
            Write(kvl2["+"],time_span=[1,2]),
            Write(kvl2["=0"],time_span=[1,2]),
            run_time=2)
        self.wait()

class newton_force(InteractiveScene):
    def construct(self):
        # init
        frame=self.frame
        # physics
        def get_closest_point_index(points,deg=225):
            target_vector=np.array([[np.cos(deg*DEGREES)],[np.sin(deg*DEGREES)],[0]])
            to_compare=[ np.dot(point,target_vector) for point in points]
            index=np.argmax(to_compare)
            return index
        pin=SVGMobject('pin.svg',height=1)
        pin.set_fill(YELLOW,1)
        pin.set_stroke(RED,1,1)
        path=pin.submobjects[0]
        points=path.get_points()    
        index=get_closest_point_index(points,225)  # 45
        shift_vector=-points[index-1]

        ax=NumberPlane().set_opacity(0.5)
        pin0=pin.copy()
        pin1=pin.copy()
        pin2=pin.copy()
        coord0=ax.c2p(0,0,0)
        coord1=ax.c2p(-4,4,0)
        coord2=ax.c2p(3,3*math.sqrt(3),0)
        coord3=ax.c2p(0,-5,0)
        pin0.move_to(coord0).shift(shift_vector)
        pin1.move_to(coord1).shift(shift_vector)
        pin2.move_to(coord2).shift(shift_vector)
        # self.add(ax,pin0,pin1,pin2)
        frame.reorient(0, 0, 0, (0.99, 1.05, 0.0), 11.40)
        self.play(LaggedStartMap(FadeIn,Group(pin0,pin1,pin2),shift=LEFT,lag_ratio=0.1))

        # hanging things
        line_left=Line(coord1,coord0)
        line_right=Line(coord2,coord0)
        line_down=Line(coord0,coord3)
        ball=Sphere(radius=0.3).move_to(coord3)
        # self.add(line_left,line_right,line_down)
        # self.add(ball)
        self.play(LaggedStartMap(ShowCreation,Group(line_left,line_right,line_down),time_span=[0,1.5]),
            ShowCreation(ball,time_span=[1,2]),
            frame.animate.reorient(0, 0, 0, (1.27, -0.41, 0.0), 13.44),run_time=2)

        # dashedline
        dashedline1=DashedLine(coord1,coord1+RIGHT*1.5)
        dashedline2=DashedLine(coord2,coord2+LEFT*1.5)
        arc1=Circle(stroke_color=WHITE).reverse_points().move_to(coord1)
        arc2=Circle(stroke_color=WHITE).move_to(coord2)
        arc1=arc1.get_subcurve(0,45/360)
        arc2=arc2.get_subcurve(180/360,(180+60)/360)
        arc1_label=Tex(R"45^\circ")
        arc2_label=Tex(R"60^\circ")
        arc1_label.move_to(arc1).shift(np.array([0.5,-0.1,0]))
        arc2_label.move_to(arc2).shift(np.array([-0.5,-0.3,0]))
        # self.add(arc1,arc2)
        # self.add(arc1_label,arc2_label)
        # self.add(dashedline1,dashedline2)
        self.play(LaggedStartMap(ShowCreation,VGroup(dashedline1,dashedline2,arc1,arc2) ))
        self.play(Write(arc1_label),Write(arc2_label))

        # force analysis
        f_mg=Arrow(coord0,(coord0+coord3)*1/2,tip_width_ratio=10,buff=0).set_color(YELLOW_B)
        f_t1=Arrow(coord0,(coord0+coord1)*1/2,tip_width_ratio=10,buff=0).set_color(BLUE)
        f_t2=Arrow(coord0,(coord0+coord2)*1/2,tip_width_ratio=10,buff=0).set_color(RED)
        f_mg_label=Tex("mg").match_color(f_mg).scale(1.5).next_to(f_mg.get_end(),LEFT)
        f_t1_label=Tex("T_1").match_color(f_t1).scale(1.5).next_to(f_t1.get_end(),LEFT)
        f_t2_label=Tex("T_2").match_color(f_t2).scale(1.5).next_to(f_t2.get_end(),RIGHT)
        # self.add(f_mg,f_t1,f_t2)
        # self.add(f_mg_label,f_t1_label,f_t2_label)
        self.play(LaggedStart(GrowArrow(f_mg),Write(f_mg_label),lag_ratio=0.5))
        self.play(LaggedStart(GrowArrow(f_t1),Write(f_t1_label),lag_ratio=0.5))
        self.play(LaggedStart(GrowArrow(f_t2),Write(f_t2_label),lag_ratio=0.5))

        # force decomposition
        dash_t1_x=DashedLine(f_t1.get_end(),np.array([f_t1.get_end()[0],0,0])) 
        dash_t1_y=DashedLine(f_t1.get_end(),np.array([coord0[0],f_t1.get_end()[1],0]))
        dash_t2_x=DashedLine(f_t2.get_end(),np.array([f_t2.get_end()[0],0,0])) 
        dash_t2_y=DashedLine(f_t2.get_end(),np.array([coord0[0],f_t2.get_end()[1],0]))
        decomp_t1_x=Arrow(coord0,dash_t1_x.get_end(),buff=0,tip_width_ratio=8).match_color(f_t1)
        decomp_t1_y=Arrow(coord0,dash_t1_y.get_end(),buff=0,tip_width_ratio=8).match_color(f_t1)
        decomp_t2_x=Arrow(coord0,dash_t2_x.get_end(),buff=0,tip_width_ratio=8).match_color(f_t2)
        decomp_t2_y=Arrow(coord0,dash_t2_y.get_end(),buff=0,tip_width_ratio=8).match_color(f_t2)
        label_decomp_t1_x=Tex(R"T_1\cos(45^\circ)").match_color(f_t1).next_to(decomp_t1_x.get_end(),DOWN)
        label_decomp_t1_y=Tex(R"T_1\sin(45^\circ)").match_color(f_t1).next_to(decomp_t1_y.get_end(),UP).shift(LEFT*1)
        label_decomp_t2_x=Tex(R"T_2\cos(60^\circ)").match_color(f_t2).next_to(decomp_t2_x.get_end(),DOWN)
        label_decomp_t2_y=Tex(R"T_2\sin(60^\circ)").match_color(f_t2).next_to(decomp_t2_y.get_end(),UP).shift(RIGHT*0.5)
        # self.add(dash_t1_x,dash_t1_y,dash_t2_x,dash_t2_y) 
        # self.add(decomp_t1_x,decomp_t1_y,decomp_t2_x,decomp_t2_y) 
        # self.add(label_decomp_t1_x,label_decomp_t1_y,label_decomp_t2_x,label_decomp_t2_y)
        self.play(ShowCreation(dash_t1_x),ShowCreation(dash_t1_y))
        self.play(TransformFromCopy(f_t1,decomp_t1_x),TransformFromCopy(f_t1,decomp_t1_y),
            f_t1.animate.set_opacity(0.3))
        self.play(Write(label_decomp_t1_x),Write(label_decomp_t1_y))
        self.play(ShowCreation(dash_t2_x),ShowCreation(dash_t2_y))
        self.play(TransformFromCopy(f_t2,decomp_t2_x),TransformFromCopy(f_t2,decomp_t2_y),
            f_t2.animate.set_opacity(0.3))
        self.play(Write(label_decomp_t2_x),Write(label_decomp_t2_y))

        # force eqn
        horizontal_eqn=Tex(R"T_1\cos(45^\circ)=T_2\cos(60^\circ)",t2c={"T_1":BLUE,"T_2":RED})
        vertical_eqn=Tex(R"T_1\sin(45^\circ)+T_2\sin(60^\circ)=mg",t2c={"T_1":BLUE,"T_2":RED})
        force_eqns=VGroup(horizontal_eqn,vertical_eqn).scale(1.5).arrange(DOWN,aligned_edge=RIGHT)
        force_eqns.next_to(ball,DOWN)
        # self.add(force_eqns)
        self.play(frame.animate.reorient(0, 0, 0, (1.49, -0.79, 0.0), 14.59),
            FadeTransform(label_decomp_t1_x.copy(),horizontal_eqn[R"T_1\cos(45^\circ)"]),
            FadeTransform(label_decomp_t2_x.copy(),horizontal_eqn[R"T_2\cos(60^\circ)"]),
            Write(horizontal_eqn[R"="]),
            label_decomp_t1_x.animate.set_opacity(0.3),
            label_decomp_t2_x.animate.set_opacity(0.3),run_time=2)
        self.play(
            FadeTransform(label_decomp_t1_y.copy(),vertical_eqn[R"T_1\sin(45^\circ)"]),
            FadeTransform(label_decomp_t2_y.copy(),vertical_eqn[R"T_2\sin(60^\circ)"]),
            FadeTransform(f_mg_label.copy(),vertical_eqn[R"mg"]),
            label_decomp_t1_y.animate.set_opacity(0.3),
            label_decomp_t2_y.animate.set_opacity(0.3),
            f_mg_label.animate.set_opacity(0.3),
            Write(vertical_eqn[R"="]),Write(vertical_eqn[R"+"]),run_time=2)
        self.wait()
        










        
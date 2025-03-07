高斯消元

开头：

在物理（力学平衡问题），

化学（方程式配平），(https://en.wikipedia.org/wiki/Chemical_equation)

电路（kcl，kvl），(https://en.wikipedia.org/wiki/Kirchhoff%27s_circuit_laws#Kirchhoff's_voltage_law)

![image-20250226212307468](C:\Users\zhixin\AppData\Roaming\Typora\typora-user-images\image-20250226212307468.png)

统计学（线性回归），

各个领域，我们总是会不可避免遇到解线性方程的问题。高斯消元是解线性方程组的方法之一，但是我们为什么要通过这种方法解方程？高斯消元相比我们高中时候的消元代入法有什么优势？高斯消元的具体步骤是什么？这个视频我将帮你搞明白这些问题。

回想一下高中时期，我们是如何解线性方程的？比如这个方程：（动画举例，先消元，再代入），我们可以解出答案，但是当方程个数多了之后，我们往往会陷入迷茫，（比较依赖一些灵感式的技巧，没有固定的步骤和规范的操作），会有点随意和不系统。有时候我们解到最后发现其实这个方程组无解（很难百分之百确定）

我们需要一种系统化的步骤和方法，让我们方便系统地去解线性方程组，这就轮到高斯消元法登场了。

举个例子：eqn（1）
$$
\begin{aligned}
2 x +4 y -2 z= & 2 \\
4 x +9 y -3 z= & 8 \\
-2 x -3 y +7 z= & 10
\end{aligned}
$$
$$
\begin{alignat}{4}
            2&x+4&&y-2&&z&&=2\\
            4&x+9&&y-3&&z&&=8\\
            -2&x-3&&y+7&&z&&=10
\end{alignat}
$$

$$
\begin{alignat}{20}
&\,-\,  &2&x_1&\,-\,  &\frac{1}{2}&x_2&\,+\,  &3&x_3&\,=&\,-\,&\frac{17}{5}\\           
&\,\,  &&x_1&\,+\,  &2&x_2&\,\,  &&&\,=&\,\,&\frac{23}{5}\\     
&\,\,  &\frac{6}{5}&x_1&\,-\,  &2&x_2&\,+\,  &&x_3&\,=&\,\,&4
\end{alignat}
$$



step1:使用方程1,消去方程一下面的所有x
$$
\begin{aligned}
2 x +4 y -2 z= & 2 \\
y +z= & 4 \\
y +5 z= & 12
\end{aligned}
$$
step2:使用方程2，消去方程2下面所有的y
$$
\begin{aligned}
2 x +4 y -2 z= & 2 \\
y +z= & 4 \\
4z= & 8
\end{aligned}
$$
然后，我们就可以通过第三个方程接触z，然后将z代入第二个方程解出y，然后将y，z代入第一个方程解除x。

这个方法无论方程有多少个，或是未知数有多少个，我们都可以遵循这个步骤，一步一步解出来。（举一个5 by 5的例子）
$$
\begin{aligned}
 &x    &&+y    &&+z    &&+w  &&+t   &&=15 \\
 &2x   &&\quad &&+2z   &&+2w &&+3t  &&=31 \\
 &3x   &&+3y   &&\quad &&+3w  &&+5t  &&=46 \\
 &\quad&&y     &&+z    &&+w  &&+t   &&=14 \\
 &4x   &&+y    &&\quad &&+w  &&+t   &&=15
\end{aligned}
$$
solution is 1,2,3,4,5
$$
\begin{array}{rrrrrrr}
 &x    &+y    &+z    &+w  &+t   &=15 \\
 &2x   &\quad &+2z   &+2w &+3t  &=31 \\
 &3x   &+3y   &\quad &+3w  &+5t  &=46 \\
 &\quad&y     &+z    &+w  &+t   &=14 \\
 &4x   &+y    &\quad &+w  &+t   &=15
\end{array}
$$

$$
\begin{alignat*}{15}
         &&x    &\,+\, &&y    &\,+\, &&z    &\,+\, &&w  &\,+\, &&t   &=15 \\
         &2&x   &\,\,  &&     &\,+\, &2&z   &\,+\, &2&w &\,+\, &3&t  &=31 \\
         &3&x   &\,+\, &3&y   &\,\,  &&     &\,+\, &3&w &\,+\, &5&t  &=46 \\
         &&     &\,\,  &&y    &\,+\, &&z    &\,+\, &&w  &\,+\, &&t   &=14 \\
         &4&x   &\,+\, &&y    &\,\,  &&     &\,+\, &&w  &\,+\, &&t   &=15 
\end{alignat*}
$$



整个过程其实很符合直觉，高斯只是将我们解方程的步骤进行了系统化地规范，如果你早于高斯出生，或许这个方法就是你来命名了。

但是毕竟写一大堆系数，未知数，加减号等于号还是太麻烦了。所以我们不妨进行一些简化。

比如这个方程
$$
\begin{aligned}
2 x +4 y -2 z= & 2
\end{aligned}
$$
我把系数和未知数分开：我规定这个乘法和方程是一样的，叫做点积
$$
\begin{bmatrix}
2 & 4 &-2  \\
\end{bmatrix}
\begin{bmatrix}
x \\
 y\\
z
\end{bmatrix}=2
$$

$$
\begin{bmatrix}
4 & 9 &-3  \\
\end{bmatrix}
\begin{bmatrix}
x \\
 y\\
z
\end{bmatrix}=8
$$

$$
\begin{bmatrix}
-2 & -3 & 7  \\
\end{bmatrix}
\begin{bmatrix}
x \\
 y\\
z
\end{bmatrix}=10
$$

然而我是个懒人，我觉得写了三遍x，y，z还是麻烦，所以我把这三个合并为一个：
$$
\begin{bmatrix}
2 & 4 &-2  \\
4& 9 & -3 \\
-2&-3& 7
\end{bmatrix}
\begin{bmatrix}
x \\
 y\\
z
\end{bmatrix}=
\begin{bmatrix}
 2\\
 8\\
10
\end{bmatrix}
$$
这和我上面地方程是完全等价的，因为我定义一行乘一列叫做点积，也规定了点积的运算规则，所以这样是完全等价的；

我给他们起个名字，左边的叫做矩阵A，中间的叫做未知数矩阵，右边的叫做矩阵b。

然后我要像刚才一样进行高斯消元。对照着刚才的步骤（动画分为两列）
$$
\begin{bmatrix}
2 & 4 &-2  \\
0& 1 & 1 \\
0& 1 & 5
\end{bmatrix}
\begin{bmatrix}
x \\
 y\\
z
\end{bmatrix}=
\begin{bmatrix}
 2\\
 4\\
12
\end{bmatrix}
$$

$$
\begin{bmatrix}
2 & 4 &-2  \\
0& 1 & 1 \\
0& 0 & 4
\end{bmatrix}
\begin{bmatrix}
x \\
 y\\
z
\end{bmatrix}=
\begin{bmatrix}
 2\\
 4\\
8
\end{bmatrix}
$$

但依然，我是个懒人，我不想每次都写x，y，z矩阵，因为它在我消元过程中没影响，所以我将A矩阵和b矩阵合并一下[A|b],起个名字叫做增广矩阵。
$$
\left[\begin{array}{ccc|c}
2 & 4 & -2 & 2 \\
4 & 9 & -3 & 8 \\
-2 & -3 & 7 & 10
\end{array}\right]
$$
那么高斯消元就变为了
$$
\left[\begin{array}{ccc|c}
2 & 4 & -2 & 2 \\
0 & 1 & 1 & 4 \\
0 & 1 & 5 & 12
\end{array}\right]
$$

$$
\left[\begin{array}{ccc|c}
2 & 4 & -2 & 2 \\
0 & 1 & 1 & 4 \\
0 & 0 & 4 & 8
\end{array}\right]
$$

其中第一步 r2-2r1，表示第二行减两倍的第一行，r来自英语单词Row的首字母

然后我们就可以解方程了，解出z=2，在左边的矩阵形式就是将第三行归一化
$$
\left[\begin{array}{ccc|c}
2 & 4 & -2 & 2 \\
0 & 1 & 1 & 4 \\
0 & 0 & 1 & 2
\end{array}\right]
$$
我们有了z的值，所以将z的值代入第一第二个方程，在左边的矩阵形式就是消去“这个”元素头顶的元素
$$
\left[\begin{array}{ccc|c}
2 & 4 & 0 & 6 \\
0 & 1 & 0 & 2 \\
0 & 0 & 1 & 2
\end{array}\right]
$$
我们下面要解y，很幸运，z前面的系数已经是1了，不需要归一化，我们得到了y的值，把y的值代入到第一个方程，在左边的矩阵形式，意味着将这个值头顶的元素消去
$$
\left[\begin{array}{ccc|c}
2 & 0 & 0 & -2 \\
0 & 1 & 0 & 2 \\
0 & 0 & 1 & 2
\end{array}\right]
$$
然后我们解x，归一化x即可
$$
\left[\begin{array}{ccc|c}
1 & 0 & 0 & -1 \\
0 & 1 & 0 & 2 \\
0 & 0 & 1 & 2
\end{array}\right]
$$
这整个过程就叫做高斯消元*Gaussian elimination*，或高斯若尔当消元Gauss–Jordan elimination ，高斯将消元进行到上三角矩阵的时候停下来了，然后通过回代求解x，y，z，而若尔当指出，我们可以直接将矩阵化为单位矩阵，则增广矩阵右边就直接给出了结果。

然而高斯消元过程中可能会遇到一些特殊情况，比如第一个元素为0，这时候我们要进行 行交换，有时候方程组无解，有时候方程组无解，
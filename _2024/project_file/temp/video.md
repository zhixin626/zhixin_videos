# 矩阵的三种作用

## 1. 存储数据

- 方程

$$
\begin{aligned}
& 1 x+2 y+3 z=6 \\
& 4 x+5 y+6 z=15 \\
& 7 x+8 y+9 z=24
\end{aligned}
$$

- 矩阵
  $$
  \left[\enspace\begin{matrix}
  1&2&3\\
  4&5&6\\
  7&8&9
  \end{matrix}\enspace\right|\enspace
  \left.\begin{matrix}
  6\\15\\24
  \end{matrix}\enspace\right]
  $$
  

## 2. 线性变换：

- 旋转

  - 二维旋转
    $$
    R=\left[\enspace\begin{matrix}
    \cos \theta & -\sin \theta \\
    \sin \theta & \cos \theta
    \end{matrix}\enspace
    \right]
    $$

    $$
    \left[\begin{array}{l}
    x^{\prime} \\
    y^{\prime}
    \end{array}\right]=\left[\begin{array}{cc}
    \cos \theta & -\sin \theta \\
    \sin \theta & \cos \theta
    \end{array}\right]\left[\begin{array}{l}
    x \\
    y
    \end{array}\right] .
    $$

    

  - 三维旋转
    
    
    $$
    \begin{aligned}
    & R_x(\theta)=\left[\begin{array}{ccc}
    1 & 0 & 0 \\
    0 & \cos \theta & -\sin \theta \\
    0 & \sin \theta & \cos \theta
    \end{array}\right] \\
    & R_y(\theta)=\left[\begin{array}{ccc}
    \cos \theta & 0 & \sin \theta \\
    0 & 1 & 0 \\
    -\sin \theta & 0 & \cos \theta
    \end{array}\right] \\
    & R_z(\theta)=\left[\begin{array}{ccc}
    \cos \theta & -\sin \theta & 0 \\
    \sin \theta & \cos \theta & 0 \\
    0 & 0 & 1
    \end{array}\right]
    \end{aligned}
    $$
    
    
    

- 投影（垂直投影）（到$A$的列空间）
  $$
  \mathbf{P}=\mathbf{A}\left(\mathbf{A}^{\top} \mathbf{A}\right)^{-1} \mathbf{A}^{\top} 
  $$
  

  - 点投影到线
  - 三维物体投影到平面

## 3. 线性空间： 2D 3D 4D

$$
A_1=\left[\enspace\begin{matrix}
1&0\\
0&1
\end{matrix}\enspace\right]
$$

$$
A_2=\left[\enspace\begin{matrix}
1&0&0\\
0&1&0\\
0&0&1
\end{matrix}\enspace\right]
$$

$$
A_3=\left[\enspace\begin{matrix}
1&0&0&0\\
0&1&0&0\\
0&0&1&0\\
0&0&0&1
\end{matrix}\enspace\right]
$$

- 秩为2的矩阵，可以表示二维空间

  $A_1$的列向量 $\begin{bmatrix}1\\0\end{bmatrix}$ 和 $\begin{bmatrix}0\\1\end{bmatrix}$ 可以线性组合出二维平面的所有点。

- 秩为3的矩阵，可以表示三维空间

  $A_2$的列向量 $\begin{bmatrix}1\\0\\0\end{bmatrix}$ 和 $\begin{bmatrix}0\\1\\0\end{bmatrix}$和$\begin{bmatrix}0\\0\\1\end{bmatrix}$ 可以线性组合出三维空间的所有点。

- 秩为4的矩阵，可以表示四维空间

  $A_3$的列向量 $\begin{bmatrix}1\\0\\0\\0\end{bmatrix}$ 和 $\begin{bmatrix}0\\1\\0\\0\end{bmatrix}$和$\begin{bmatrix}0\\0\\1\\0\end{bmatrix}$和$\begin{bmatrix}0\\0\\0\\1\end{bmatrix}$ 可以线性组合出四维空间的所有点。
  
  
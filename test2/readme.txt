算法：
对于一个N个变量的24点计算，我们可以将运算的过程写成如下形式：

共有N个初始变量及N-1个中间变量
n个初始化等式
INPUT1=V1
INPUT2=V2
...
INPUTN=VN

n-1次中间运算
VX OP VY=VZ
VX OP VY=VZ
...
VX OP VY=VZ

一个结果要求
V2N-1=24

同时满足每个变量在等式左边和右边各出现一次，一个变量在等式左边出现前必须先在等式右边出现。
如对于1,2,3,4，可以写成如下形式：
1=V1
2=V2
3=V3
4=V4
V1+V2=V5
V5+V3=V6
V6*V4=V7
V7=24

具体实现：
采用三个Z3数组left1_array,left2_array,right_array表示每个等式的三个变量下标，一个数组op表示运算符，一个Z3数组value表示变量的值，两个数组leftp,rightp表示每个变量在左、右出现的位置。
需要加的条件有：
初始值和结果正确
leftp,rightp与left1_array,left2_array,right_array记录的信息不矛盾
rightp[i] < leftp[i]
运算正确
具体可参见程序
（输出部分采用简单的宏替换思想即可）

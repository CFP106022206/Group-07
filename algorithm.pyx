import numpy as np
cimport numpy as np
 
# 使用Numpy-C-API
np.import_array()
 
# cdefine C 函数
cdef extern from "main.h":
    void mul (double *a,double *r,double t);
    void plu (double *a,double *b,double *r);
    void minus (double *a,double *b,double *r);
    double dot (double *a,double *b);
    double lenth (double *a);
    void write1(double *a,double a1,double a2,double a3);
    void DP (double *a,double *res,int n,int m,double G,double time);
    void collision(double *a,double *r,int n,int m,double e);
    void main (double *a,double *res, int n, int m,double G,double time,double e);
 
"""
# 定义一个"包装函数", 用于调用C语言的main函数，调用范例：plus_fun(a, b, r)
# 在这里要注意函数传入的参数的类型声明，double表示数组的元素是double类型的，
# ndim = 2表示数组的维度是2
# 在调用main函数时，要把python的变量强制转化成相应的类型（以确保无误），比如<int>
# 当然，基本类型如int，可以不显式地写出来，如下面的a.shape[0]、a.shape[1]
"""
def main_func(np.ndarray[double, ndim=2, mode="c"] a not None,
                     np.ndarray[double, ndim=2, mode="c"] res not None,
                     G not None,time not None,e not None):
    main(<double*> np.PyArray_DATA(a),
                <double*> np.PyArray_DATA(res),
                a.shape[0],
                a.shape[1],
                <double> G,
                <double> time,
                <double> e)
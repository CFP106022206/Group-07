#ifndef _MAIN_H
#define _MAIN_H
void mul (double *a,double *r,double t);
void plu (double *a,double *b,double *r);
void minus (double *a,double *b,double *r);
double dot (double *a,double *b);
double lenth (double *a);
void write1(double *a,double a1,double a2,double a3);
void DP (double *a,double *res,int n,int m,double G,double time);
void collision(double *a,double *r,int n,int m,double e);
void main (double *a,double *res, int n, int m,double G,double time,double e);
#endif


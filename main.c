#include <stdio.h>
#include <math.h>
void mul(double *a,double *r,double t,int n)
{
    int i;
    for(i = 0; i < n; i++)
    {
        *(r + i) = *(a + i) * t;
    }
}
void plu(double *a, double *b, double *r, int n)
{
    int i;
    for(i = 0; i < n; i++)
    {
        *(r + i) = *(a + i) + *(b + i);
    }
}
void minus(double *a, double *b, double *r, int n)
{
    int i;
    for(i = 0; i < n; i++)
    {
        *(r + i) = *(a + i) - *(b + i);
    }
}

void plu1(double *a,double *r,double t,int n)
{
    int i;
    for(i = 0; i < n; i++)
    {
        *(r + i) = *(a + i) + t;
    }
}

double lenth(double *a,int n)
{
    int i;
    double l=0;
    for (i=0;i<n;i++)
    {
        l = l+pow(*(a+i),2);
    }
    return sqrt(l);
}
void write1(double *a,double a1,double a2,double a3)
{
    *(a)   = a1;
    *(a+1) = a2;
    *(a+2) = a3;
}
void dot(double *a, double *b, double *r)
{
    int i;
    for(i = 0; i < 3; i++)
    {
        *(r + i) = *(a + i) * *(b + i);
    }
}

void collision(double *a,double *r,int n,int m,double e)
{
    int i,j;
    double s[3];
    double s1[3];
    double v1[3];
    double v2[3];
    double v11[3];
    double v21[3];
    double v1v[3];
    double v2v[3];
    double v1vf[3];
    double v2vf[3];
    double cm[3];
    double l;
    for (i=0;i<n;i++)
    {
        for (j=i+1;j<n;j++)
        {
            write1(s,*(a+i*m),*(a+i*m+1),*(a+i*m+2));
            write1(s1,*(a+j*m),*(a+j*m+1),*(a+j*m+2));
            minus(s,s1,s,3);
            l = lenth(s,3);
            if (l<*(a+i*m+7)+*(a+j*m+7))
            {
                mul(s,s,1/lenth(s,3),3);

                write1(v2,*(a+j*m+3),*(a+j*m+4),*(a+j*m+5));
                dot(v2,s,v2v);
                minus(v2,v2v,v2,3);

                write1(v1,*(a+i*m+3),*(a+i*m+4),*(a+i*m+5));
                mul(s,s,-1,3);
                dot(v1,s,v1v);
                minus(v1,v1v,v1,3);

                minus(v2v,v1v,v1vf,3);
                mul(v1vf,v1vf,e**(a+j*m+6),3);
                mul(v1,v11,*(a+i*m+6),3);
                mul(v2,v21,*(a+j*m+6),3);
                plu(v1vf,v11,v1vf,3);
                plu(v1vf,v21,v1vf,3);
                mul(v1vf,v1vf,1/(*(a+i*m+6)+*(a+j*m+6)),3);
                plu(v1vf,v1,v1vf,3);

                minus(v1v,v2v,v2vf,3);
                mul(v2vf,v2vf,e**(a+i*m+6),3);
                plu(v2vf,v11,v2vf,3);
                plu(v2vf,v21,v2vf,3);
                mul(v2vf,v2vf,1/(*(a+i*m+6)+*(a+j*m+6)),3);
                plu(v2vf,v2,v2vf,3);

                *(r+i*m+3)=v1vf[0];*(r+i*m+4)=v1vf[1];*(r+i*m+5)=v1vf[2];
                *(r+j*m+3)=v2vf[0];*(r+j*m+4)=v2vf[1];*(r+j*m+5)=v2vf[2];

                write1(v1,*(a+i*m),*(a+i*m+1),*(a+i*m+2));
                write1(v2,*(a+j*m),*(a+j*m+1),*(a+j*m+2));
                mul(v1,v1v,*(a+i*m+6),3);
                mul(v2,v2v,*(a+j*m+6),3);
                plu(v1v,v2v,cm,3);
                mul(cm,cm,1/(*(a+i*m+6)+*(a+j*m+6)),3);
                mul(s,v2v,*(a+i*m+6)/(*(a+i*m+6)+*(a+j*m+6))*0.99,3);
                plu(v2v,cm,v2,3);
                mul(s,v1v,-1**(a+i*m+6)/(*(a+i*m+6)+*(a+j*m+6))*0.99,3);
                plu(v1v,cm,v1,3);
                *(r+i*m+0)=v1[0];*(r+i*m+1)=v1[1];*(r+i*m+2)=v1[2];
                *(r+j*m+0)=v2[0];*(r+j*m+1)=v2[1];*(r+j*m+2)=v2[2];
                *(r+j*m+6)=*(a+j*m+6);*(r+j*m+7)=*(a+j*m+7);
                *(r+i*m+6)=*(a+i*m+6);*(r+i*m+7)=*(a+i*m+7);
            }
        }
    }
}
void DP(double *a,double *res, int n, int m,double G,double time)
{
    int i, j;
    for(i = 0; i < n; i++)
    {

    double m1[3] = {0};
    double m2[3] = {0};
    double m3[3] = {0};
    double m4[3] = {0};
    double m5[3] = {0};
    double m6[3] = {0};
    double m7[3] = {0};
    double mass;
    double r[3];
    double re[3];
    double s[3];
    double l[3];

    double k1[3] = {*(a+i*m+3),*(a+i*m+4),*(a+i*m+5)};
    double r1[3] = {*(a+i*m+0),*(a+i*m+1),*(a+i*m+2)};
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r,3);
        if (j != i && lenth(r,3)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r1,s,3);
            mul(s,re,G*mass/pow(lenth(s,3),2),3);
            mul(re,re,1/lenth(s,3),3);
            plu(m1,re,m1,3);
        }
    }
    double k2[3];
    double r2[3];
    mul(m1,r,time/5.0,3);plu(k1,r,k2,3);
    mul(k1,r,time/5.0,3);plu(r1,r,r2,3);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r,3);
        if (j != i && lenth(r,3)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r2,s,3);
            mul(s,re,G*mass/pow(lenth(s,3),2),3);
            mul(re,re,1/lenth(s,3),3);
            plu(m2,re,m2,3);
        }
    }
    double k3[3];
    double r3[3];
    mul(m1,r,time*3.0/40.0,3);plu(k1,r,k3,3);
    mul(m2,r,time*9.0/40.0,3);plu(k3,r,k3,3);
    mul(k1,r,time*3.0/40.0,3);plu(r1,r,r3,3);
    mul(k2,r,time*9.0/40.0,3);plu(r3,r,r3,3);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r,3);
        if (j != i && lenth(r,3)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r3,s,3);
            mul(s,re,G*mass/pow(lenth(s,3),2),3);
            mul(re,re,1/lenth(s,3),3);
            plu(m3,re,m3,3);
        }
    }
    double k4[3];
    double r4[3];
    mul(m1,r,time*44.0/45.0,3);   plu(k1,r,k4,3);
    mul(m2,r,time*(-56.0/15.0),3);plu(k4,r,k4,3);
    mul(m3,r,time*32.0/9.0,3);    plu(k4,r,k4,3);
    mul(k1,r,time*44.0/45.0,3);   plu(r1,r,r4,3);
    mul(k2,r,time*(-56.0/15.0),3);plu(r4,r,r4,3);
    mul(k3,r,time*32.0/9.0,3);    plu(r4,r,r4,3);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r,3);
        if (j != i && lenth(r,3)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r4,s,3);
            mul(s,re,G*mass/pow(lenth(s,3),2),3);
            mul(re,re,1/lenth(s,3),3);
            plu(m4,re,m4,3);
        }
    }
    double k5[3];
    double r5[3];
    mul(m1,r,time*19372.0/6561.0,3);   plu(k1,r,k5,3);
    mul(m2,r,time*(-25360.0/2187.0),3);plu(k5,r,k5,3);
    mul(m3,r,time*64448.0/6561.0,3);   plu(k5,r,k5,3);
    mul(m4,r,time*(-212.0/729.0),3);   plu(k5,r,k5,3);
    mul(k1,r,time*19372.0/6561.0,3);   plu(r1,r,r5,3);
    mul(k2,r,time*(-25360.0/2187.0),3);plu(r5,r,r5,3);
    mul(k3,r,time*64448.0/6561.0,3);   plu(r5,r,r5,3);
    mul(k4,r,time*(-212.0/729.0),3);   plu(r5,r,r5,3);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r,3);
        if (j != i && lenth(r,3)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r5,s,3);
            mul(s,re,G*mass/pow(lenth(s,3),2),3);
            mul(re,re,1/lenth(s,3),3);
            plu(m5,re,m5,3);
        }
    }
    double k6[3];
    double r6[3];
    mul(m1,r,time*9017.0/3168.0,3);    plu(k1,r,k6,3);
    mul(m2,r,time*(-355.0/33.0),3);    plu(k6,r,k6,3);
    mul(m3,r,time*46732.0/5247.0,3);   plu(k6,r,k6,3);
    mul(m4,r,time*49.0/176.0,3);       plu(k6,r,k6,3);
    mul(m5,r,time*(-5103.0/18656.0),3);plu(k6,r,k6,3);
    mul(k1,r,time*9017.0/3168.0,3);    plu(r1,r,r6,3);
    mul(k2,r,time*(-355.0/33.0),3);    plu(r6,r,r6,3);
    mul(k3,r,time*46732.0/5247.0,3);   plu(r6,r,r6,3);
    mul(k4,r,time*49.0/176.0,3);       plu(r6,r,r6,3);
    mul(k5,r,time*(-5103.0/18656.0),3);plu(r6,r,r6,3);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r,3);
        if (j != i && lenth(r,3)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r6,s,3);
            mul(s,re,G*mass/pow(lenth(s,3),2),3);
            mul(re,re,1/lenth(s,3),3);
            plu(m6,re,m6,3);
        }
    }
    double k7[3];
    double r7[3];
    mul(m1,r,time*35.0/384.0,3);       plu(k1,r,k7,3);
    mul(m3,r,time*500.0/1113.0,3);     plu(k7,r,k7,3);
    mul(m4,r,time*125.0/192.0,3);      plu(k7,r,k7,3);
    mul(m5,r,time*(-2187.0/6784.0),3); plu(k7,r,k7,3);
    mul(m6,r,time*11.0/84.0,3);        plu(k7,r,k7,3);
    mul(k1,r,time*35.0/384.0,3);       plu(r1,r,r7,3);
    mul(k3,r,time*500.0/1113.0,3);     plu(r7,r,r7,3);
    mul(k4,r,time*125.0/192.0,3);      plu(r7,r,r7,3);
    mul(k5,r,time*(-2187.0/6784.0),3); plu(r7,r,r7,3);
    mul(k6,r,time*11.0/84.0,3);        plu(r7,r,r7,3);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r,3);
        if (j != i && lenth(r,3)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r7,s,3);
            mul(s,re,G*mass/pow(lenth(s,3),2),3);
            mul(re,re,1/lenth(s,3),3);
            plu(m7,re,m7,3);
        }
    }
    *(res+i*m+0) = *(a+i*m+0)+5179.0/57600.0*time*k1[0]+7571.0/16695.0*time*k3[0]+393.0/640.0*time*k4[0]-92097.0/339200.0*time*k5[0]+187.0/2100.0*time*k6[0]+1.0/40.0*time*k7[0];
    *(res+i*m+1) = *(a+i*m+1)+5179.0/57600.0*time*k1[1]+7571.0/16695.0*time*k3[1]+393.0/640.0*time*k4[1]-92097.0/339200.0*time*k5[1]+187.0/2100.0*time*k6[1]+1.0/40.0*time*k7[1];
    *(res+i*m+2) = *(a+i*m+2)+5179.0/57600.0*time*k1[2]+7571.0/16695.0*time*k3[2]+393.0/640.0*time*k4[2]-92097.0/339200.0*time*k5[2]+187.0/2100.0*time*k6[2]+1.0/40.0*time*k7[2];
    *(res+i*m+3) = *(a+i*m+3)+5179.0/57600.0*time*m1[0]+7571.0/16695.0*time*m3[0]+393.0/640.0*time*m4[0]-92097.0/339200.0*time*m5[0]+187.0/2100.0*time*m6[0]+1.0/40.0*time*m7[0];
    *(res+i*m+4) = *(a+i*m+4)+5179.0/57600.0*time*m1[1]+7571.0/16695.0*time*m3[1]+393.0/640.0*time*m4[1]-92097.0/339200.0*time*m5[1]+187.0/2100.0*time*m6[1]+1.0/40.0*time*m7[1];
    *(res+i*m+5) = *(a+i*m+5)+5179.0/57600.0*time*m1[2]+7571.0/16695.0*time*m3[2]+393.0/640.0*time*m4[2]-92097.0/339200.0*time*m5[2]+187.0/2100.0*time*m6[2]+1.0/40.0*time*m7[2];
    *(res+i*m+6) = *(a+i*m+6);
    *(res+i*m+7) = *(a+i*m+7);
    }
}
void main(double *a,double *res, int n, int m,double G,double time,double e)
{
    DP(a,res,n,m,G,time);
    collision(a,res,n,m,e);
}

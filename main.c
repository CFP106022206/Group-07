#include <stdio.h>
#include <math.h>
void mul(double *a,double *r,double t)
{
    int i;
    for(i = 0; i < 3; i++)
    {
        *(r + i) = *(a + i) * t;
    }
}
void plu(double *a, double *b, double *r)
{
    int i;
    for(i = 0; i < 3; i++)
    {
        *(r + i) = *(a + i) + *(b + i);
    }
}
void minus(double *a, double *b, double *r)
{
    int i;
    for(i = 0; i < 3; i++)
    {
        *(r + i) = *(a + i) - *(b + i);
    }
}

double lenth(double *a)
{
    int i;
    double l=0;
    for (i=0;i<3;i++)
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
double dot(double *a, double *b)
{
    int i;
    double ans = 0;
    for(i = 0; i < 3; i++)
    {
        ans += *(a + i) * *(b + i);
    }
    return ans;
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
    //double cm[3];
    double l;
    for (i=0;i<n;i++)
    {
        for (j=i+1;j<n;j++)
        {
            write1(s,*(a+i*m),*(a+i*m+1),*(a+i*m+2));
            write1(s1,*(a+j*m),*(a+j*m+1),*(a+j*m+2));
            minus(s1,s,s);
            l = lenth(s);
            if (l<*(a+i*m+7)+*(a+j*m+7))
            {
                mul(s,s,1.0/lenth(s));
                write1(v2,*(a+j*m+3),*(a+j*m+4),*(a+j*m+5));
                mul(s,v2v,dot(v2,s));
                minus(v2,v2v,v2);

                write1(v1,*(a+i*m+3),*(a+i*m+4),*(a+i*m+5));
                mul(s,v1v,dot(v1,s));
                minus(v1,v1v,v1);

                minus(v2v,v1v,v1vf);
                if (dot(v1vf,s)<0)
                {
                    //write1(ini_momentum,*(a+i*m+6)**(a+i*m+3)+*(a+j*m+6)**(a+j*m+3),*(a+i*m+6)**(a+i*m+4)+*(a+j*m+6)**(a+j*m+4),*(a+i*m+6)**(a+i*m+5)+*(a+j*m+6)**(a+j*m+5));
                    mul(v1vf,v1vf,e*(*(a+j*m+6)));
                    mul(v1v,v11,*(a+i*m+6));
                    mul(v2v,v21,*(a+j*m+6));
                    plu(v1vf,v11,v1vf);
                    plu(v1vf,v21,v1vf);
                    mul(v1vf,v1vf,1/(*(a+i*m+6)+*(a+j*m+6)));
                    plu(v1vf,v1,v1vf);

                    minus(v1v,v2v,v2vf);
                    mul(v2vf,v2vf,e*(*(a+i*m+6)));
                    plu(v2vf,v11,v2vf);
                    plu(v2vf,v21,v2vf);
                    mul(v2vf,v2vf,1/(*(a+i*m+6)+*(a+j*m+6)));
                    plu(v2vf,v2,v2vf);

                    *(r+i*m+3)=v1vf[0];*(r+i*m+4)=v1vf[1];*(r+i*m+5)=v1vf[2];
                    *(r+j*m+3)=v2vf[0];*(r+j*m+4)=v2vf[1];*(r+j*m+5)=v2vf[2];
/* position correction
                    write1(v1,*(a+i*m),*(a+i*m+1),*(a+i*m+2));
                    write1(v2,*(a+j*m),*(a+j*m+1),*(a+j*m+2));
                    mul(v1,v1v,*(a+i*m+6));
                    mul(v2,v2v,*(a+j*m+6));
                    plu(v1v,v2v,cm);
                    mul(cm,cm,1/(*(a+i*m+6)+*(a+j*m+6)));
                    mul(s,v2v,*(a+i*m+6)/(*(a+i*m+6)+*(a+j*m+6))*0.99);
                    plu(v2v,cm,v2);
                    mul(s,v1v,-1**(a+i*m+6)/(*(a+i*m+6)+*(a+j*m+6))*0.99);
                    plu(v1v,cm,v1);
                    *(r+i*m+0)=v1[0];*(r+i*m+1)=v1[1];*(r+i*m+2)=v1[2];
                    *(r+j*m+0)=v2[0];*(r+j*m+1)=v2[1];*(r+j*m+2)=v2[2];
                */
                    *(r+i*m+0)=*(a+i*m+0);*(r+i*m+1)=*(a+i*m+1);*(r+i*m+2)=*(a+i*m+2);
                    *(r+j*m+0)=*(a+j*m+0);*(r+j*m+1)=*(a+j*m+1);*(r+j*m+2)=*(a+j*m+2);
                    *(r+j*m+6)=*(a+j*m+6);*(r+j*m+7)=*(a+j*m+7);
                    *(r+i*m+6)=*(a+i*m+6);*(r+i*m+7)=*(a+i*m+7);
                }
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
        minus(l,r,r);
        if (j != i && lenth(r)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r1,s);
            mul(s,re,G*mass/pow(lenth(s),3));
            plu(m1,re,m1);
        }
    }
    double k2[3];
    double r2[3];
    mul(m1,r,time/5.0);plu(k1,r,k2);
    mul(k1,r,time/5.0);plu(r1,r,r2);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r);
        if (j != i && lenth(r)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r2,s);
            mul(s,re,G*mass/pow(lenth(s),3));
            plu(m2,re,m2);
        }
    }
    double k3[3];
    double r3[3];
    mul(m1,r,time*3.0/40.0);plu(k1,r,k3);
    mul(m2,r,time*9.0/40.0);plu(k3,r,k3);
    mul(k1,r,time*3.0/40.0);plu(r1,r,r3);
    mul(k2,r,time*9.0/40.0);plu(r3,r,r3);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r);
        if (j != i && lenth(r)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r3,s);
            mul(s,re,G*mass/pow(lenth(s),3));
            plu(m3,re,m3);
        }
    }
    double k4[3];
    double r4[3];
    mul(m1,r,time*44.0/45.0);   plu(k1,r,k4);
    mul(m2,r,time*(-56.0/15.0));plu(k4,r,k4);
    mul(m3,r,time*32.0/9.0);    plu(k4,r,k4);
    mul(k1,r,time*44.0/45.0);   plu(r1,r,r4);
    mul(k2,r,time*(-56.0/15.0));plu(r4,r,r4);
    mul(k3,r,time*32.0/9.0);    plu(r4,r,r4);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r);
        if (j != i && lenth(r)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r4,s);
            mul(s,re,G*mass/pow(lenth(s),3));
            plu(m4,re,m4);
        }
    }
    double k5[3];
    double r5[3];
    mul(m1,r,time*19372.0/6561.0);   plu(k1,r,k5);
    mul(m2,r,time*(-25360.0/2187.0));plu(k5,r,k5);
    mul(m3,r,time*64448.0/6561.0);   plu(k5,r,k5);
    mul(m4,r,time*(-212.0/729.0));   plu(k5,r,k5);
    mul(k1,r,time*19372.0/6561.0);   plu(r1,r,r5);
    mul(k2,r,time*(-25360.0/2187.0));plu(r5,r,r5);
    mul(k3,r,time*64448.0/6561.0);   plu(r5,r,r5);
    mul(k4,r,time*(-212.0/729.0));   plu(r5,r,r5);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r);
        if (j != i && lenth(r)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r5,s);
            mul(s,re,G*mass/pow(lenth(s),3));
            plu(m5,re,m5);
        }
    }
    double k6[3];
    double r6[3];
    mul(m1,r,time*9017.0/3168.0);    plu(k1,r,k6);
    mul(m2,r,time*(-355.0/33.0));    plu(k6,r,k6);
    mul(m3,r,time*46732.0/5247.0);   plu(k6,r,k6);
    mul(m4,r,time*49.0/176.0);       plu(k6,r,k6);
    mul(m5,r,time*(-5103.0/18656.0));plu(k6,r,k6);
    mul(k1,r,time*9017.0/3168.0);    plu(r1,r,r6);
    mul(k2,r,time*(-355.0/33.0));    plu(r6,r,r6);
    mul(k3,r,time*46732.0/5247.0);   plu(r6,r,r6);
    mul(k4,r,time*49.0/176.0);       plu(r6,r,r6);
    mul(k5,r,time*(-5103.0/18656.0));plu(r6,r,r6);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r);
        if (j != i && lenth(r)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r6,s);
            mul(s,re,G*mass/pow(lenth(s),3));
            plu(m6,re,m6);
        }
    }
    double k7[3];
    double r7[3];
    mul(m1,r,time*35.0/384.0);       plu(k1,r,k7);
    mul(m3,r,time*500.0/1113.0);     plu(k7,r,k7);
    mul(m4,r,time*125.0/192.0);      plu(k7,r,k7);
    mul(m5,r,time*(-2187.0/6784.0)); plu(k7,r,k7);
    mul(m6,r,time*11.0/84.0);        plu(k7,r,k7);
    mul(k1,r,time*35.0/384.0);       plu(r1,r,r7);
    mul(k3,r,time*500.0/1113.0);     plu(r7,r,r7);
    mul(k4,r,time*125.0/192.0);      plu(r7,r,r7);
    mul(k5,r,time*(-2187.0/6784.0)); plu(r7,r,r7);
    mul(k6,r,time*11.0/84.0);        plu(r7,r,r7);
    for(j = 0; j < n; j++)
    {
        write1(r,*(a+i*m+0),*(a+i*m+1),*(a+i*m+2));
        write1(l,*(a+j*m+0),*(a+j*m+1),*(a+j*m+2));
        minus(l,r,r);
        if (j != i && lenth(r)>*(a+i*m+7)+*(a+j*m+7))
        {
            mass = *(a+j*m+6);
            minus(l,r7,s);
            mul(s,re,G*mass/pow(lenth(s),3));
            plu(m7,re,m7);
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
    collision(res,res,n,m,e);
}

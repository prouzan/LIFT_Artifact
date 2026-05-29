#include <stdio.h>

int main()
{
    int a, b, x, y, tmp, tmp2;
    scanf("%d%d%d%d", &a, &b, &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (a == b)
    {
        while (x >= 0 || y >= 0)
        {
            printf("a:%d,b:%d,x:%d,y:%d,tmp:%d,tmp2:%d\n", a, b, x, y, tmp, tmp2);
            
            tmp = x + a - b - 1;
            x = y + b - a - 1;
            y = tmp;
            tmp2 = a;
            a = b;
            b = tmp2;
        }
    }
    return 0;
}

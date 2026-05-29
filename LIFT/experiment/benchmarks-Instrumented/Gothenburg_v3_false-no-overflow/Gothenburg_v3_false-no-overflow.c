#include <stdio.h>

int main()
{
    int a, b, x, y, tmp;
    scanf("%d%d%d%d", &a, &b, &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (a == b)
    {
        while (x >= 0 || y >= 0)
        {
            printf("a:%d,b:%d,x:%d,y:%d,tmp:%d\n", a, b, x, y, tmp);

            x = x + a - b - 1;
            y = y + b - a - 1;

            tmp = a;
            a = b;
            b = tmp;
        }
    }
    return 0;
}

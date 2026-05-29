#include <stdio.h>

int main()
{
    int x, y, r;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    r = 1;
    while (y > 0)
    {
        printf("x:%d,y:%d,r:%d\n", x, y, r);
        r = r * x;
        y = y - 1;
    }
    return 0;
}

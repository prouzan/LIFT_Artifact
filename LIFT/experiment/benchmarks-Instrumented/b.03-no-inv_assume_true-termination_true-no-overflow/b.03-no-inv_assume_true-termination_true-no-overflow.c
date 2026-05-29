#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (x > 0)
    {
        while (x > y && y <= 2147483647 - x)
        {
            printf("x:%d,y:%d\n", x, y);
            y = y + x;
        }
    }
    return 0;
}

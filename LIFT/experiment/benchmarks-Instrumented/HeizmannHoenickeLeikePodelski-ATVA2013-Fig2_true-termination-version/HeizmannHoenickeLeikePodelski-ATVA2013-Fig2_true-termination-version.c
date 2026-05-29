#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (x > y)
    {
        while (x >= 0)
        {
            printf("x:%d,y:%d\n", x, y);
            y = 2 * y - x;
            x = (y + x + 1) / 2;
        }
    }
    return 0;
}

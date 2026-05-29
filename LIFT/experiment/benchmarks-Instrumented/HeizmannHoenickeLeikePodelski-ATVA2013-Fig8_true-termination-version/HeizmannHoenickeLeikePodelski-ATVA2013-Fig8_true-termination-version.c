#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (5 * y >= 1)
    {
        while (x >= 0)
        {
            printf("x:%d,y:%d\n", x, y);
            x = x - 4 * y + 3;
        }
    }
    return 0;
}

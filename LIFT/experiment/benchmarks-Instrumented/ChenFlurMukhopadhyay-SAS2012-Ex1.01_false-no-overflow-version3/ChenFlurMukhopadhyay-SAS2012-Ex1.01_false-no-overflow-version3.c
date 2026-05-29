#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (x < 0 && y > 0)
    {
        printf("x:%d,y:%d\n", x, y);
        x = -3 * x - 17;
        y = -4 * y + 8;
    }
    return 0;
}

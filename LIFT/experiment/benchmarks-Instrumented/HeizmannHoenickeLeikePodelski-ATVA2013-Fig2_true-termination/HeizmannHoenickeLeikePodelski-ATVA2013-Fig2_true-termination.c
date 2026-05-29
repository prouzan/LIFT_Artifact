#include <stdio.h>

int main()
{
    int y;
    scanf("%d", &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    int x = y + 42;
    while (x >= 0)
    {
        printf("y:%d,x:%d\n", y, x);
        y = 2 * y - x;
        x = (y + x) / 2;
    }
    return 0;
}

#include <stdio.h>

int main()
{
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    int y = 2;
    while (x >= 0)
    {
        printf("x:%d,y:%d\n", x, y);
        x = x - y;
        y = (y + 1) / 2;
    }
    return 0;
}

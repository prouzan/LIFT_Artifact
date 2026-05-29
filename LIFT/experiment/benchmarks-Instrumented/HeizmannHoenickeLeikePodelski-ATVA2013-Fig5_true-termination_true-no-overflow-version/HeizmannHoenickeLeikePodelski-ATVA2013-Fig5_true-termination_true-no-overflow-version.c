#include <stdio.h>

int main()
{
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    int y = 3;
    while (x >= 0)
    {
        printf("x:%d,y:%d\n", x, y);
        x = x - y;
        y = (y + 2) / 3;
    }
    return 0;
}

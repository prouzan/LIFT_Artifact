#include <stdio.h>

int main()
{
    int x;
    int y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (x + y <= 0)
    {
        while (x > 0)
        {
            printf("x:%d,y:%d\n", x, y);
            x = x + y + 2;
            y = y - 1;
        }
    }
    return 0;
}

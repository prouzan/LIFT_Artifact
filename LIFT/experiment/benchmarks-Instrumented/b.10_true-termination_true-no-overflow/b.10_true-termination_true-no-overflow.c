#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (((x >= 0 && y < 2147483647 - x) || (x < 0 && y > -2147483648 - x)) && x + y > 0)
    {
        printf("x:%d,y:%d\n", x, y);
        if (x > 0)
        {
            x = x - 1;
        }
        else
        {
            if (y > 0)
            {
                y = y - 1;
            }
            else
            {
            }
        }
    }
    return 0;
}

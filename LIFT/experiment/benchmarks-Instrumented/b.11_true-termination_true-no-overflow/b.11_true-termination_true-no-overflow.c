#include <stdio.h>

int main()
{
    int x, y, c;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    c = 0;
    while (((x >= 0 && y < 2147483647 - x) || (x < 0 && y > -2147483648 - x)) && x + y > 0)
    {
        printf("x:%d,y:%d,c:%d\n", x, y, c);
        if (x > y)
        {
            x = x - 1;
        }
        else
        {
            if (x == y)
            {
                x = x - 1;
            }
            else
            {
                y = y - 1;
            }
        }
    }
    return 0;
}

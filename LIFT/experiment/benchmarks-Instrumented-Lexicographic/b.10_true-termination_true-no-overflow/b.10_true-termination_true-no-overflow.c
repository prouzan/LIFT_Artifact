#include <stdio.h>

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (((x >= 0 && y < 2147483647 - x) || (x < 0 && y > -2147483648 - x)) && x + y > 0)
    {
        printf("%d,%d\n", x,y);
        if (x > 0)
        {
printf("L1\n");
            x = x - 1;
        }
        else
        {
printf("L2\n");
            if (y > 0)
            {
printf("L3\n");
                y = y - 1;
            }
            else
            {
printf("L4\n");
            }
        }
    }
    return 0;
}

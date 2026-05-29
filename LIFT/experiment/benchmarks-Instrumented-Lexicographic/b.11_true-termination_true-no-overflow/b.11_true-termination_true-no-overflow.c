#include <stdio.h>

int main()
{
    int x, y, c;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    c = 0;
    while (((x >= 0 && y < 2147483647 - x) || (x < 0 && y > -2147483648 - x)) && x + y > 0)
    {
        printf("%d,%d\n", x,y);
        if (x > y)
        {
printf("L1\n");
            x = x - 1;
        }
        else
        {
printf("L2\n");
            if (x == y)
            {
printf("L3\n");
                x = x - 1;
            }
            else
            {
printf("L4\n");
                y = y - 1;
            }
        }
    }
    return 0;
}

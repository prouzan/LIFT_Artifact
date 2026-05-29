#include <stdio.h>
#include <stdlib.h>

int _nondet_2(void)
{
    return rand() % 2;
}

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (x > 0 && y > 0)
    {
        printf("%d,%d\n", x, y);

        int old_x = x;
        int old_y = y;
        if (0 == _nondet_2())
        {
printf("L1\n");
            x = old_x - 1;
            y = old_x;
        }
        else
        {
printf("L2\n");
            x = old_y - 3;
            y = old_x + 1;
        }
    }
    return 0;
}

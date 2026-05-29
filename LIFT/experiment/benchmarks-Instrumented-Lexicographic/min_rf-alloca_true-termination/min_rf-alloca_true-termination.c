#include <stdio.h>
#include <stdlib.h>

int _nondet_2(void)
{
    return rand() % 2;
}

int main()
{
    int x, y, z;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (y > 0 && x > 0)
    {
        printf("%d,%d\n", x, y);
        if (x > y)
            {
printf("L1\n");z = y;}
        else
            {
printf("L2\n");z = x;}
        if (0 == _nondet_2())
        {
printf("L3\n");
            y = y + x;
            x = z - 1;
            z = y + z;
        }
        else
        {
printf("L4\n");
            x = y + x;
            y = z - 1;
            z = x + z;
        }
    }
}

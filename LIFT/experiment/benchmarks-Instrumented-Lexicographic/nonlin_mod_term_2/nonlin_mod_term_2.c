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

    if (x <= y)
        return 0;
    if (y <= 1)
        return 0;

    while (x > y)
    {
        printf("%d,%d\n", x, y);
        if (0 == _nondet_2())
            {
printf("L1\n");x = x % y;}
        else
            {
printf("L2\n");x = x - y;}
    }
}

#include <stdio.h>
#include <stdlib.h>

int _nondet_2(void)
{
    return rand() % 2;
}
int _nondet_int(void)
{
    return rand()%32;
}
// GF: depointerized

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (x > 0 && y > 0)
    {
        printf("%d,%d\n", x, y);

        if (0 == _nondet_2())
        {
printf("L1\n");
            if (x < y)
            {
printf("L2\n");
                y = x - 1;
            }
            else
            {
printf("L3\n");
                y = y - 1;
            }
            x = _nondet_int();
        }
        else
        {
printf("L4\n");
            if (x < y)
            {
printf("L5\n");
                x = x - 1;
            }
            else
            {
printf("L6\n");
                x = y - 1;
            }
            y = _nondet_int();
        }
    }
}

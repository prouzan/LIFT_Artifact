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
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (x > 0 && y > 0)
    {
        printf("x:%d,y:%d\n", x, y);

        if (0 == _nondet_2())
        {
            if (x < y)
            {
                y = x - 1;
            }
            else
            {
                y = y - 1;
            }
            x = _nondet_int();
        }
        else
        {
            if (x < y)
            {
                x = x - 1;
            }
            else
            {
                x = y - 1;
            }
            y = _nondet_int();
        }
    }
}

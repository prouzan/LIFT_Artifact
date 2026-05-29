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
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (x > y)
    {
        printf("x:%d,y:%d\n", x, y);
        if (0 == _nondet_2())
            x = x - 1;
        else if (0 == _nondet_2())
            y = y + 1;
        else if (0 == _nondet_2())
            x = x - 2;
        else if (0 == _nondet_2())
            y = y + 2;
        else if (0 == _nondet_2())
            x = x - 3;
        else if (0 == _nondet_2())
            y = y + 3;
        else if (0 == _nondet_2())
            x = x - 4;
        else if (0 == _nondet_2())
            y = y + 4;
        else if (0 == _nondet_2())
            x = x - 5;
        else
            y = y + 5;
    }
}

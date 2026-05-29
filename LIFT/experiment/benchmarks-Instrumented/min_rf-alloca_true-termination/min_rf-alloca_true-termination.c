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
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (y > 0 && x > 0)
    {
        printf("x:%d,y:%d,z:%d\n", x, y, z);
        if (x > y)
            z = y;
        else
            z = x;
        if (0 == _nondet_2())
        {
            y = y + x;
            x = z - 1;
            z = y + z;
        }
        else
        {
            x = y + x;
            y = z - 1;
            z = x + z;
        }
    }
}

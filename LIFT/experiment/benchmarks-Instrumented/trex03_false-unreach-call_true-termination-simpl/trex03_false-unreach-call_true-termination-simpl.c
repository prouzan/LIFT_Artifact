#include <stdio.h>
#include <stdlib.h>

int _nondet_3(void)
{
    return rand() % 3;
}
int _nondet_2(void)
{
    return rand() % 2;
}
int main()
{
    int x1, x2, x3;
    scanf("%d%d%d", &x1, &x2, &x3);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (x1 > 0 && x2 > 0 && x3 > 0)
    {
        printf("x1:%d,x2:%d,x3:%d\n", x1, x2, x3);

        if (_nondet_3() == 0)
            x1 = x1 - 1;
        else if (_nondet_2() == 0)
            x2 = x2 - 1;
        else
            x3 = x3 - 1;
    }

    return 0;
}

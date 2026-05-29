#include <stdio.h>
#include <stdlib.h>

int _nondet_int(void){
    return rand();
}

int main()
{
    int x, b;
    scanf("%d%d", &x, &b);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (!(x >= -2147483647))
        return 0;
    while (b != 0)
    {
        printf("x:%d,b:%d\n", x, b);
        b = _nondet_int();
        x = x - 1;
        if (x >= 0)
        {
            b = 1;
        }
        else
        {
            b = 0;
        }
    }
    return 0;
}

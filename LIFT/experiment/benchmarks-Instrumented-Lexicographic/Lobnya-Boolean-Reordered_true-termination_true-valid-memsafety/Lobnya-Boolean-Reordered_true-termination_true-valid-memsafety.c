#include <stdio.h>
#include <stdlib.h>

int _nondet_int(void){
    return rand();
}

int main()
{
    int x, b;
    scanf("%d%d", &x, &b);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (!(x >= -2147483647))
        return 0;
    while (b != 0)
    {
        printf("%d,%d\n", x, b);
        b = _nondet_int();
        x = x - 1;
        if (x >= 0)
        {
printf("L1\n");
            b = 1;
        }
        else
        {
printf("L2\n");
            b = 0;
        }
    }
    return 0;
}

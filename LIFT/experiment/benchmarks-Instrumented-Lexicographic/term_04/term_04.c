#include <stdio.h>
#include <stdlib.h>
int _nondet_2(void)
{
    return rand() % 2;
}
int main()
{
    int j, d;
    scanf("%d%d", &j, &d);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (j > 0 && d > 0)
    {
        printf("%d,%d\n", j, d);
        if (0 == _nondet_2())
        {
printf("L1\n");
            j--;
        }
        else
        {
printf("L2\n");
            d--;
        }
    }
}
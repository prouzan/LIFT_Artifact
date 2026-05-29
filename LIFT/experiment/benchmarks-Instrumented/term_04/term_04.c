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
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (j > 0 && d > 0)
    {
        printf("j:%d,d:%d\n", j, d);
        if (0 == _nondet_2())
        {
            j--;
        }
        else
        {
            d--;
        }
    }
}
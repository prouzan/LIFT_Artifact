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

    if (j <= d)
        return 0;
    if (d <= 1)
        return 0;
    while (j > d)
    {
        printf("%d,%d\n", j, d);
        j = j % 2;
    }
}
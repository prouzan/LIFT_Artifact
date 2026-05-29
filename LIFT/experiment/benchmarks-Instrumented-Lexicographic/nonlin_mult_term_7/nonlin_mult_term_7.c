#include <stdio.h>

int main()
{
    int j, b;
    scanf("%d%d", &j, &b);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (b <= 1)
        return 0;

    while (j < 100)
    {
        printf("%d,%d\n", j, b);
        if (j <= 0)
            {
printf("L1\n");j = 1;}
        else
            {
printf("L2\n");j = j * b;}
    }
}

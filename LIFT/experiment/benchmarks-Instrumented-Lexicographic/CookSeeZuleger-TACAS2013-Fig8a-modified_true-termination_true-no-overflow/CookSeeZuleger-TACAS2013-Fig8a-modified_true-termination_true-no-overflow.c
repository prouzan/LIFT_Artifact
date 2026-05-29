#include <stdio.h>

int main()
{
    int K, x;
    scanf("%d%d", &K, &x);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (x != K)
    {
        printf("%d,%d\n", K, x);

        if (x > K)
        {
printf("L1\n");
            x = x - 1;
        }
        else
        {
printf("L2\n");
            x = x + 1;
        }
    }
    return 0;
}

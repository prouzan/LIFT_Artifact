#include <stdio.h>

int main()
{
    int K, x, y;
    scanf("%d%d%d", &K, &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (y != K)
    {
        printf("%d,%d,%d\n", K, x, y);

        if (x > K)
        {
printf("L1\n");
            x = x - 1;
        }
        else if (x < K)
        {
printf("L2\n");
            x = x + 1;
        }
        if (y > x)
        {
printf("L3\n");
            y = y - 1;
        }
        else if (y < x)
        {
printf("L4\n");
            y = y + 1;
        }
    }
}

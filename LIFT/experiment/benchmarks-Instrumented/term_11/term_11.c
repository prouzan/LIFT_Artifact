#include <stdio.h>

int main()
{
    int K, x, y;
    scanf("%d%d%d", &K, &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    while (x != K || y != K)
    {
        printf("K:%d,x:%d,y:%d\n", K, x, y);

        if (x > K)
        {
            x = x - 1;
        }
        else if (x < K)
        {
            x = x + 1;
        }
        if (y > K)
        {
            y = y - 1;
        }
        else if (y < K)
        {
            y = y + 1;
        }
    }
    return 0;
}

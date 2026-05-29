#include <stdio.h>

int main()
{
    int K, x;
    scanf("%d%d", &K, &x);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (x != K)
    {
        printf("K:%d,x:%d\n", K, x);

        if (x > K)
        {
            x = x - 1;
        }
        else
        {
            x = x + 1;
        }
    }
    return 0;
}

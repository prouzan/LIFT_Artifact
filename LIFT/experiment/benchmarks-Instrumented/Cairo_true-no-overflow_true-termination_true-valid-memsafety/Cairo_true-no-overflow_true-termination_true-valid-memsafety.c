#include <stdio.h>

int main()
{
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (x > 0)
    {
        while (x != 0)
        {
            printf("x:%d\n", x);
            x = x - 1;
        }
    }
    return 0;
}

#include <stdio.h>

int main()
{
    int c, x;
    scanf("%d%d", &c, &x);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (c >= 2)
    {
        while (x + c >= 0)
        {
            printf("c:%d,x:%d\n", c, x);
            x = x - c;
            c = c + 1;
        }
    }
    return 0;
}

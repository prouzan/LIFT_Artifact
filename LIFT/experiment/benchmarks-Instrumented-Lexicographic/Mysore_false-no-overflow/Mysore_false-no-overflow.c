#include <stdio.h>

int main()
{
    int c, x;
    scanf("%d%d", &c, &x);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (c >= 2)
    {
        while (x + c >= 0)
        {
            printf("%d,%d\n", c, x);
            x = x - c;
            c = c + 1;
        }
    }
    return 0;
}

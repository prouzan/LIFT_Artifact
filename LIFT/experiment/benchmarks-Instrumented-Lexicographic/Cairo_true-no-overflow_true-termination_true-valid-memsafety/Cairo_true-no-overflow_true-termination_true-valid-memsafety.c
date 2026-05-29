#include <stdio.h>

int main()
{
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (x > 0)
    {
        while (x != 0)
        {
            printf("%d\n", x);
            x = x - 1;
        }
    }
    return 0;
}

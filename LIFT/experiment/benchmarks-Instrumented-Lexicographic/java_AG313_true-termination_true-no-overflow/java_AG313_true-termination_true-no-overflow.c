#include <stdio.h>

int main()
{
    int _i, x, y;
    _i = 0;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    if (x != 0)
    {
        while (x > 0 && y > 0)
        {
            printf("%d,%d\n", x, y);
            _i = _i + 1;
            x = (x - 1) - (y - 1);
        }
    }
    return 0;
}

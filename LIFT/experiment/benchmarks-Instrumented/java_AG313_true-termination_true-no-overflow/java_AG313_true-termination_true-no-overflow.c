#include <stdio.h>

int main()
{
    int _i, x, y;
    _i = 0;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (x != 0)
    {
        while (x > 0 && y > 0)
        {
            printf("_i:%d,x:%d,y:%d\n", _i, x, y);
            _i = _i + 1;
            x = (x - 1) - (y - 1);
        }
    }
    return 0;
}

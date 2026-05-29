#include <stdio.h>
#include <stdlib.h>

int _nondet_int(void)
{
    return rand();
}

int main()
{
    int _i = 0;
    int x = 0;
    int y = 0;
    int n;
    scanf("%d", &n);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while ( _i < n)
    {
        printf("_i:%d,x:%d,y:%d,n:%d\n", _i, x, y, n);
        x = x - y;
        y = _nondet_int();
        x = x + y;
        _i++;
    }
}
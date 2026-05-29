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
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while ( _i < n)
    {
        printf("%d\n", n);
        x = x - y;
        y = _nondet_int();
        x = x + y;
        _i++;
    }
}
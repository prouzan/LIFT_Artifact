#include <stdio.h>
#include <stdlib.h>

int _nondet_2(void)
{
    return rand() % 2;
}

int main()
{
    int _i, j, a, b;
    scanf("%d%d%d%d", &_i, &j, &a, &b);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (_i + j + a + b == 0)
    {
        printf("%d,%d,%d,%d\n", _i, j, a, b);
        if (_nondet_2() == 0)
            {
printf("L1\n");_i--;}
        else
            {
printf("L2\n");j++;}
        if (_nondet_2() == 0)
            {
printf("L3\n");a = a - 2;}
        else
            {
printf("L4\n");b = b + 2;} 
    }
    return 0;
}

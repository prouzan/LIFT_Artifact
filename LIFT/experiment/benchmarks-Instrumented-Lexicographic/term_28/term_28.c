#include <stdio.h>
#include <stdlib.h>
int _nondet_2(void)
{
    return rand() % 2;
}

int main()
{
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

    while (x > y)
    {
        printf("%d,%d\n", x, y);
        if (0 == _nondet_2())
            {
printf("L1\n");x = x - 1;}
        else if (0 == _nondet_2())
            {
printf("L2\n");y = y + 1;}
        else if (0 == _nondet_2())
            {
printf("L3\n");x = x - 2;}
        else if (0 == _nondet_2())
            {
printf("L4\n");y = y + 2;}
        else if (0 == _nondet_2())
            {
printf("L5\n");x = x - 3;}
        else if (0 == _nondet_2())
            {
printf("L6\n");y = y + 3;}
        else if (0 == _nondet_2())
            {
printf("L7\n");x = x - 4;}
        else if (0 == _nondet_2())
            {
printf("L8\n");y = y + 4;}
        else if (0 == _nondet_2())
            {
printf("L9\n");x = x - 5;}
        else
            {
printf("L10\n");y = y + 5;}
    }
}

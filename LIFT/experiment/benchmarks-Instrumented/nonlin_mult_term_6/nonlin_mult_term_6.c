#include <stdio.h>

int main()
{
    int d, b;
    scanf("%d%d", &d, &b);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    while (d * b > 0)
    {
        printf("d:%d,b:%d\n", d, b);
        b = -b;
    }
}

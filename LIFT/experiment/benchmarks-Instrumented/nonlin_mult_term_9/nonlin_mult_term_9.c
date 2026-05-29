#include <stdio.h>

int main()
{
    int j, b;
    scanf("%d%d", &j, &b);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (b <= 1)
        return 0;
    if (j < 1)
        return 0;

    while (j < 10)
    {
        printf("j:%d,b:%d\n", j, b);
        j = -2 * j * b;
    }
}

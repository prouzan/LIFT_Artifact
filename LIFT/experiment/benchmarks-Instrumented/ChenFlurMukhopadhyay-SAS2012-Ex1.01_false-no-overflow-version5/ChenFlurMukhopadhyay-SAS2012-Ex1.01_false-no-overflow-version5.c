#include <stdio.h>

int main() {
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if (x <= 0 || y <= 0) return 0;

    while (x > 0) {
        printf("x:%d,y:%d\n", x, y);
        x = -5*x - 6*y + 18;
    }
    return 0;
}

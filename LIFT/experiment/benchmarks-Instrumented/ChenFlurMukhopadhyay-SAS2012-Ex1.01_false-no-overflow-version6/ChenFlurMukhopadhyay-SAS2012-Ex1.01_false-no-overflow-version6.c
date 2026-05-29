#include <stdio.h>

int main() {
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    while (x + y > 0) {
        printf("x:%d,y:%d\n", x, y);
        x = -5*x + 18;
        y = -6*y + 13;
    }
    return 0;
}

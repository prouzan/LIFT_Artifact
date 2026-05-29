#include <stdio.h>

int main() {
    int x, y, oldx;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    while (4*x + y > 0) {
        printf("x:%d,y:%d,oldx:%d\n", x, y, oldx);
        oldx = x;
        x = -2*oldx + 4*y;
        y = 4*oldx;
    }
    return 0;
}

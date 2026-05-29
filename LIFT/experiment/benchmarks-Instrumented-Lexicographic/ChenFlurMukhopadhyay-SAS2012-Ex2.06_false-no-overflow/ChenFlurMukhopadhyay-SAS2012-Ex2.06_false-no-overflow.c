#include <stdio.h>

int main() {
    int x, y, oldx;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    while (4*x + y > 0) {
        printf("%d,%d\n", x, y);
        oldx = x;
        x = -2*oldx + 4*y;
        y = 4*oldx;
    }
    return 0;
}

#include <stdio.h>

int main() {
    int x, y, z, n;
    scanf("%d%d%d%d", &x, &y, &z, &n);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    while (x + y >= 0 && x <= n) {
        printf("%d,%d,%d,%d\n", x, y, z, n);
        x = 2*x + y;
        y = z;
        z = z + 1;
    }
    return 0;
}

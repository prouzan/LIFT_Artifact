#include <stdio.h>

int main() {
    int x, y;
    scanf("%d%d", &x, &y);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    while (x + y > 0) {
        printf("%d,%d\n", x, y);
        x = -5*x + 18;
        y = -6*y + 13;
    }
    return 0;
}

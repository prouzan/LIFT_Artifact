#include <stdio.h>

int main() {
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    while (x > 0) {
        printf("%d\n", x);
        x = -2*x + 10;
    }
    return 0;
}

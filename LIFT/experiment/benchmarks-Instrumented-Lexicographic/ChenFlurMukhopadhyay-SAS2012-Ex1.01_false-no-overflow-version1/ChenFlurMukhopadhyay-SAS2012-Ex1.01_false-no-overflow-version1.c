#include <stdio.h>

int main() {
    int x;
    scanf("%d", &x);
    printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
    while (x > 0) {
        printf("%d\n", x);
        x = -5*x + 50;
    }
    return 0;
}

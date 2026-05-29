#include <stdio.h>

int main() {
    int x, y, z, n;
    scanf("%d%d%d%d", &x, &y, &z, &n);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
    while (x + y >= 0 && x <= n) {
        printf("x:%d,y:%d,z:%d,n:%d\n", x, y, z, n);
        x = 2*x + y;
        y = z;
        z = z - 1;
    }
    return 0;
}

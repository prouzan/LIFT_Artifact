#include <stdio.h>

int main() {
  int x, y, z;
  scanf("%d%d%d", &x, &y, &z);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  while (x >= y) {
    printf("%d,%d,%d\n", x, y, z);
    if (z > 1) {
printf("L1\n");
      z = z - 1;
      x = x + z;
    } else {
printf("L2\n");
      y = y + 1;
    }
  }
}

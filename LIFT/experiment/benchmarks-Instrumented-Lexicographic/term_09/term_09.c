#include <stdio.h>

int main() {
  int K, x, y;
  scanf("%d%d%d", &K, &x, &y);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  if (!(x < y)) return 0;

  while (y != K) {
    printf("%d,%d,%d\n", K, x, y);
    if (x == y) {
printf("L1\n");
      if (x > K) {
printf("L2\n");
        x = x - 1;
      } else {
printf("L3\n");
        x = x + 1;
      }
      y = x;
    } else {
printf("L4\n");
      y = y - 1;
    }
  }
  return 0;
}

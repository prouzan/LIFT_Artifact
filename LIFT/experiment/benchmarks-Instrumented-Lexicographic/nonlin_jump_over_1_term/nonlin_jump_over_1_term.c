#include <stdio.h>

int main() {
  int x, y;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  if (y <= 1) return 0;

  while (x >= y) {
    printf("%d,%d\n", x, y);
    if (x % y == 1) {
printf("L1\n");x++;}
      else {
printf("L2\n");x = x - 2;}
  }
  return 0;
}

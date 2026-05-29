#include <stdio.h>

int main() {
  int x, y;
  scanf("%d", &x);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  y = 5;

  if (x <= 10) return 0;

  while (x != 2*y) {
    printf("%d\n", x);
    if (x % 5 == 1) {
printf("L1\n");x++;}
      else {
printf("L2\n");x = x - 2;}
  }
  return 0;
}

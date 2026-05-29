#include <stdio.h>

int main() {
  int x, y, z;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  if (y <= 1) return 0;
  z = 0;
  while (x > 0) {
    printf("%d,%d\n", x, y);
    x = x - y;
    y = y - z;
    if (z == 0) {
printf("L1\n");z = 13;}
      else if (z == 13) {
printf("L2\n");z = -20;}
        else if (z == -20) {
printf("L3\n");z = 7;}
          else {
printf("L4\n");z = 0;}
  }
  return 0;
}

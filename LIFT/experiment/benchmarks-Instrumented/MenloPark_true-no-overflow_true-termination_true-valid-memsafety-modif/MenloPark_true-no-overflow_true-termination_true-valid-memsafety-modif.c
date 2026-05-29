#include <stdio.h>

int main() {
  int x, y, z;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  if (y <= 1) return 0;

  z = 1;
  while (x > 0) {
    printf("x:%d,y:%d,z:%d\n", x, y, z);
    x = x - y;
    y = y - z;
    z = -z;
  }
  return 0;
}

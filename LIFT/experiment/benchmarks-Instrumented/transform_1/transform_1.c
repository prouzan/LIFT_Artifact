#include <stdio.h>

int main() {
  int x, y, z;
  scanf("%d%d", &x, &y);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  if (y <= 1) return 0;
  z = 0;
  while (x > 0) {
    printf("x:%d,y:%d,z:%d\n", x, y, z);
    x = x - y;
    y = y - z;
    if (z == 0) z = 13;
      else if (z == 13) z = -20;
        else if (z == -20) z = 7;
          else z = 0;
  }
  return 0;
}

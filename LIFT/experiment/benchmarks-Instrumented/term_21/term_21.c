#include <stdio.h>

int main() {
  int z;
  scanf("%d", &z);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  while (z >= 0) {
    printf("z:%d\n", z);
    if (z % 5 == 0) z = z - 5;
      else z++;
  }
  return 0;
}

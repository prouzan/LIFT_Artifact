#include <stdio.h>

int main() {
  int z;
  scanf("%d", &z);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  while (z >= 0) {
    printf("%d\n", z);
    if (z % 5 == 0) {
printf("L1\n");z = z - 5;}
      else {
printf("L2\n");z++;}
  }
  return 0;
}

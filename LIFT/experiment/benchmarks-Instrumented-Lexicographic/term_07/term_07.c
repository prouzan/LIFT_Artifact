#include <stdio.h>

int main() {
  int x, y;
  scanf("%d", &x);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  y = 0;
  while (x > 0)
  {
    printf("%d\n", x);
    if (y == 2) {
printf("L1\n");x = x - 3;} else {
printf("L2\n");x = x + 1;}
    if (y == 2) {
printf("L3\n");y = 0;} else {
printf("L4\n");y = y + 1;}
  }
}

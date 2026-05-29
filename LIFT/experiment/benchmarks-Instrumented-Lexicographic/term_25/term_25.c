#include <stdio.h>

int main() {
  int x, y, z, w, c;
  scanf("%d%d%d", &x, &y, &z);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  w = x + y + z;
  c = 0;
  while (w == x + y + z){
    printf("%d,%d,%d\n", x, y, z);
    if (c < 100) {
printf("L1\n");y --;}
    c++;
    x = x + y + c;
    z = z - y;
  }
}

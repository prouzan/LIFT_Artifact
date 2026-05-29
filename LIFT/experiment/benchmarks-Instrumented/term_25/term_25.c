#include <stdio.h>

int main() {
  int x, y, z, w, c;
  scanf("%d%d%d", &x, &y, &z);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");
  w = x + y + z;
  c = 0;
  while (w == x + y + z){
    printf("x:%d,y:%d,z:%d,w:%d,c:%d\n", x, y, z, w, c);
    if (c < 100) y --;
    c++;
    x = x + y + c;
    z = z - y;
  }
}

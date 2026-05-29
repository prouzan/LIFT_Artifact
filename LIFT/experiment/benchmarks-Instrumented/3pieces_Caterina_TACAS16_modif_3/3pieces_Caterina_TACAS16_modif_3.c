#include <stdio.h>

int main(){
  int x,y,N;
  scanf("%d%d%d", &x, &y, &N);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  if (y > 0) return 0;
  if (N <= 0) return 0;
  while (x != 0)
  {
    printf("x:%d,y:%d,N:%d\n", x, y, N);
    if (x < N) x++; else x = y;
  }
}
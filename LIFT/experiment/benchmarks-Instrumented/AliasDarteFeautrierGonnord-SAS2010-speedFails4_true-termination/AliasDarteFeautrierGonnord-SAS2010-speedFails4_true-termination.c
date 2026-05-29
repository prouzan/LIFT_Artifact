#include <stdio.h>

int main(){
  int x,n,b,t;
  scanf("%d%d%d", &x, &n, &b);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  if (b >= 1) t = 1; else t = -1;

  while (x <= n)
  {
    printf("x:%d,n:%d,b:%d,t:%d\n", x, n, b, t);
    if (b >= 1) x = x + t; else x = x - t;
  }
}
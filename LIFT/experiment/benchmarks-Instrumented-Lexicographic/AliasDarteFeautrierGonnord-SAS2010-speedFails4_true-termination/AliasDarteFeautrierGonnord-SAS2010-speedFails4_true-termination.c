#include <stdio.h>

int main(){
  int x,n,b,t;
  scanf("%d%d%d", &x, &n, &b);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  if (b >= 1) t = 1; else t = -1;

  while (x <= n)
  {
    printf("%d,%d,%d\n", x,n,b);
    if (b >= 1) {
printf("L1\n");x = x + t;} else {
printf("L2\n");x = x - t;}
  }
}
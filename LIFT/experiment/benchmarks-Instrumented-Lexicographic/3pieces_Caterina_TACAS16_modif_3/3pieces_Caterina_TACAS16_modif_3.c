#include <stdio.h>

int main(){
  int x,y,N;
  scanf("%d%d%d", &x, &y, &N);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  if (y > 0) return 0;
  if (N <= 0) return 0;
  while (x != 0)
  {
    printf("%d,%d,%d\n", x,y,N);
    if (x < N) {
printf("L1\n");x++;} else {
printf("L2\n");x = y;}
  }
}
#include <stdio.h>
#include <stdlib.h>

int _nondet_3() {
  return rand()%3;
}
int _nondet_2() {
  return rand()%2;
}
int main() {
  int x1, x2, x3;
  scanf("%d%d%d", &x1, &x2, &x3);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  int d1=1, d2=1, d3=1;
  while(x1>0 && x2>0 && x3>0)
  {
    printf("%d,%d,%d\n", x1, x2, x3);
    if (_nondet_3() == 0) {
printf("L1\n");x1=x1-d1;}
    else if (_nondet_2() == 0) {
printf("L2\n");x2=x2-d2;}
    else {
printf("L3\n");x3=x3-d3;}
  }
  return 0;
}

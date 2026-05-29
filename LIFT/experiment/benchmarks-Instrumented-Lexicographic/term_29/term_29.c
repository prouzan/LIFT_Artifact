#include <stdio.h>
#include <stdlib.h>

int _nondet_5() {
  return rand()%5;
}
int _nondet_4() {
  return rand()%4;
}
int _nondet_3() {
  return rand()%3;
}
int _nondet_2() {
  return rand()%2;
}

int main() {
  int x = 0;
  int y = 0;
  int z = 1;
  int N;
  scanf("%d", &N);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (x < N)
  {
    printf("%d\n", N);
    if      (_nondet_5() == 0 && z == 1) {
printf("L1\n"); y = 5; z = 0; }
    else if (_nondet_4() == 0 && z == 0) {
printf("L2\n"); y = -3; z = 1; }
    else if (_nondet_3() == 0 && z == 1) {
printf("L3\n"); y = 7; z = 0; }
    else if (_nondet_2() == 0 && z == 0) {
printf("L4\n"); y = -2; z = 1; }
    else {
printf("L5\n");y = 1;}

    x = x + y;
  }
}

#include <stdio.h>

int main()
{
  int _i, j, k;
  _i = -7;
  j = 2;
  k = 8;
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (_i != j)
  {
    printf("#\n");
    _i = _i + j - k;
    j = j * 2;
    k = k - 1;
  }
  return 0;
}

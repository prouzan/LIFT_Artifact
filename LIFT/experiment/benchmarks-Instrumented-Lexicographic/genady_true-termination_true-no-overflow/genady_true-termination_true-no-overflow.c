#include <stdio.h>

int main()
{
  int _i, j;
  j = 1;
  _i = 10000;
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");
  while (_i - j >= 1)
  {
    printf("#\n");

    j = j + 1;
    _i = _i - 1;
  }
  return 0;
}

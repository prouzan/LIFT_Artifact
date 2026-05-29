#include <stdio.h>

int main()
{
  int a, b, c, d, _e;
  a = 0;
  b = 0;
  c = 0;
  d = 0;
  _e = 0;
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  while (a == 0)
  {
    printf("#\n");
    a = a + b;
    b = b + c;
    c = c + d;
    d = d + _e;
    _e = _e + 1;
  }
  return 0;
}

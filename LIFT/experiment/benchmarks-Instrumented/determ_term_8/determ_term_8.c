#include <stdio.h>

int main()
{
  int a, b, c, d, _e, f;
  a = 0;
  b = 0;
  c = 0;
  d = 0;
  _e = 0;
  f = 0;
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  while (a == 0)
  {
    printf("a:%d,b:%d,c:%d,d:%d,_e:%d,f:%d\n", a, b, c, d, _e, f);
    a = a + b;
    b = b + c;
    c = c + d;
    d = d + _e;
    _e = _e + f;
    f = f + 1;
  }
  return 0;
}

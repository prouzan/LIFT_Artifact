#include <stdio.h>

int main()
{
  int _i, j, m, n;
  scanf("%d%d", &n, &m);
  printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

  if (m > 0 && n > m)
  {
    _i = 0;
    j = 0;
    while (_i < n)
    {
      printf("_i:%d,j:%d,m:%d,n:%d\n", _i, j, m, n);
      if (j < m)
      {
        j = j + 1;
      }
      else
      {
        j = 0;
        _i = _i + 1;
      }
    }
  }
  return 0;
}

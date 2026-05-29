#include <stdio.h>

int main()
{
  int _i, j, m, n;
  scanf("%d%d", &n, &m);
  printf("[Testing] <Interface V3.0TR> (Basic lexical method)\n");

  if (m > 0 && n > m)
  {
    _i = 0;
    j = 0;
    while (_i < n)
    {
      printf("%d,%d\n", n, m);
      if (j < m)
      {
printf("L1\n");
        j = j + 1;
      }
      else
      {
printf("L2\n");
        j = 0;
        _i = _i + 1;
      }
    }
  }
  return 0;
}

function {:existential true} b0(m:int, n:int, _i:int, j:int, i:int %Decl:i%): bool;

procedure main()
{
  var _i, j, m, n, i: int;
  havoc n;
  havoc m;

  assume(m > 0 && n > m);
  _i := 0;
  j := 0;

  assume(%M:i%);
  
  while (_i < n)
  invariant b0(m,n,_i,j,i %Inv:i%);
  {
    assert(i > 0);
    if (j < m) 
    {
      j := j + 1;
    } 
    else 
    {
      j := 0;
      _i := _i + 1;
    }
    i := i - 1;
  }
}

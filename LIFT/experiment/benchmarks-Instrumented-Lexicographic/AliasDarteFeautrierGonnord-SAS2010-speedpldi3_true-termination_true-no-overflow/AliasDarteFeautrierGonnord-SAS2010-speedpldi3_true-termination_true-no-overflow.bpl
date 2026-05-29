function {:existential true} b0(m:int, n:int, _i:int, j:int %FD%, TR1:int, TR2:int): bool;

procedure main()
{
  var _i, j, m, n %VD%, TR1, TR2: int;
  havoc n;
  havoc m;

  assume(m > 0 && n > m);
  _i := 0;
  j := 0;

  %BE%
TR1 := 0;
TR2 := 0;
  
  while (_i < n)
  invariant b0(m,n,_i,j %IC%, TR1, TR2);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (j < m) 
    {
TR1 := 1;
      j := j + 1;
    } 
    else 
    {
TR2 := 1;
      j := 0;
      _i := _i + 1;
    }
    %IT%
  }
}

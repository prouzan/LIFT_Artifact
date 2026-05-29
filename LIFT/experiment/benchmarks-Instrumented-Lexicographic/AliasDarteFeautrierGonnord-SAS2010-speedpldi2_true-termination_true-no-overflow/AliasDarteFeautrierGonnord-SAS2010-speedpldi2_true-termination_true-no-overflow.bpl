function {:existential true} b0(m:int, n:int, v1:int, v2:int %FD%, TR1:int, TR2:int, T1:int): bool;

procedure main()
{
  var m,n,v1,v2 %VD%, TR1, TR2: int;
  havoc n;
  havoc m;

  assume(n >= 0 && m > 0);
  v1 := n;
  v2 := 0;

  %BE%
TR1 := 0;
TR2 := 0;
  
  while (v1 > 0)
  invariant b0(m,n,v1,v2 %IC%, TR1, TR2, 2*v1);
  {
    %BT%
TR1 := 0;
TR2 := 0;
    if (v2 < m) 
    {
TR1 := 1;
      v2 := v2 + 1;
      v1 := v1 - 1;
    } 
    else 
    {
TR2 := 1;
      v2 := 0;
    }
    %IT%
  }
}

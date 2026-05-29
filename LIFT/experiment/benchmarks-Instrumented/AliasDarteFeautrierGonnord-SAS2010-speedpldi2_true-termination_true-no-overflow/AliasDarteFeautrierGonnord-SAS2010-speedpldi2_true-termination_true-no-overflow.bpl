function {:existential true} b0(m:int, n:int, v1:int, v2:int, i:int %Decl:i%, T1:int): bool;

procedure main()
{
  var m,n,v1,v2,i: int;
  havoc n;
  havoc m;

  assume(n >= 0 && m > 0);
  v1 := n;
  v2 := 0;

  assume(%M:i%);
  
  while (v1 > 0)
  invariant b0(m,n,v1,v2,i %Inv:i%, 2*v1);
  {
    assert(i > 0);
    if (v2 < m) 
    {
      v2 := v2 + 1;
      v1 := v1 - 1;
    } 
    else 
    {
      v2 := 0;
    }
    i := i - 1;
  }
}

function {:existential true} b0(n:int, i:int %Decl:i%, ATTM$n$SUB$_i:int): bool;

procedure main()
{
  var _i,x,y,n,i: int;
  _i := 0;
  x := 0;
  y := 0;
  havoc n;
  
  assume(%M:i%);
  
  while (_i < n)
  invariant b0(n,i %Inv:i%, n - _i);
  {
    assert(i > 0);
    x := x - y;
    havoc y;
    x := x + y;
    _i := _i + 1;

    i := i - 1;
  }
}

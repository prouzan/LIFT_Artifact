function {:existential true} b0(x1:int, x2:int, x3:int, d1:int, d2:int, d3:int, i:int %Decl:i%): bool;

procedure main()
{
  var x1,x2,x3,d1,d2,d3,i: int;
  havoc x1;
  havoc x2;
  havoc x3;
  havoc d1;
  havoc d2;
  havoc d3;

  assume(!(d1 < 1 || d2 < 1 || d3 < 1));
  assume(%M:i%);

  while (x1>0 && x2>0 && x3>0)
  invariant b0(x1,x2,x3,d1,d2,d3,i %Inv:i%);
  {
    assert(i > 0);
    if (*) { x1:=x1-d1; }
    else if (*) { x2:=x2-d2; }
    else { x3:=x3-d3; }
    i := i - 1;
  }
}

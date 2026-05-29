function {:existential true} b0(x:int, y:int, oldx:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,oldx,i: int;
  havoc x;
  havoc y;

  assume(%M:i%);

  while (4*x + y > 0)
  invariant b0(x,y,oldx,i %Inv:i%);
  {
    assert(i > 0);
    oldx := x;
    x := -2*oldx + 4*y;
    y := 4*oldx;
    i := i - 1;
  }
}

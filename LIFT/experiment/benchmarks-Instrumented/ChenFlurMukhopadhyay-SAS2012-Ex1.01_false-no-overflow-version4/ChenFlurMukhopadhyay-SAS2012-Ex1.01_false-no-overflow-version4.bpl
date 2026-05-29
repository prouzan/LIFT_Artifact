function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  havoc y;

  assume(!(x <= 0 || y <= 0));
  assume(%M:i%);

  while (x + y > 0)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    x := -4*x + 18;
    y := -6*y + 13;
    i := i - 1;
  }
}

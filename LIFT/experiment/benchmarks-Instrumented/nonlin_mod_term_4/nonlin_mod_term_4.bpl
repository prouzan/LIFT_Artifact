function {:existential true} b0(x:int, y:int, i:int %Decl:i%, ATTM$x_MOD_y:int): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  havoc y;

  assume(!(x <= y));
  assume(!(y <= 1));
  assume(%M:i%);

  while (0 != x mod y)
  invariant b0(x,y,i %Inv:i%, x mod y);
  {
    assert(i > 0);
    y := y - 1;
    i := i - 1;
  }
}

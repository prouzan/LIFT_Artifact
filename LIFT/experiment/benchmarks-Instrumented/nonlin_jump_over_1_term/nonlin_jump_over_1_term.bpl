function {:existential true} b0(x:int, y:int, i:int %Decl:i%, ATTM$x_MOD_y:int): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  havoc y;

  assume(!(y <= 1));
  assume(%M:i%);

  while (x >= y)
  invariant b0(x,y,i %Inv:i%, x mod y);
  {
    assert(i > 0);
    if (x mod y == 1) { x := x + 1; }
      else { x := x - 2; }
    i := i - 1;
  }
}

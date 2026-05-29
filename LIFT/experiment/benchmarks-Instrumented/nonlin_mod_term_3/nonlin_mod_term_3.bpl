function {:existential true} b0(x:int, y:int, i:int %Decl:i%, ATTM$x_MOD_y:int): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  havoc y;

  assume(!(x <= 0));
  assume(!(y <= 0));
  assume(!(x mod y != 0));
  assume(%M:i%);

  while (x != 0)
  invariant b0(x,y,i %Inv:i%, x mod y);
  {
    assert(i > 0);
    x := x - y;
    i := i - 1;
  }
}

function {:existential true} b0(x:int, y:int, i:int %Decl:i%, ATTM$x_DIV_y:int): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  havoc y;

  assume(!(x < y));
  assume(!(y <= 1));
  assume(%M:i%);

  while (x > 0)
  invariant b0(x,y,i %Inv:i%, x div y);
  {
    assert(i > 0);
    x := x div y;
    i := i - 1;
  }
}

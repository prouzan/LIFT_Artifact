function {:existential true} b0(x:int, y:int, z:int, i:int %Decl:i%, ATTM$x_DIV_50:int): bool;

procedure main()
{
  var x,y,z,i: int;
  havoc x;
  havoc y;

  assume(%M:i%);

  while (x div 50 == y)
  invariant b0(x,y,z,i %Inv:i%, x div 50);
  {
    assert(i > 0);
    havoc z;
    x := x + 1 + 50*z;
    y := y + z;
    i := i - 1;
  }
}

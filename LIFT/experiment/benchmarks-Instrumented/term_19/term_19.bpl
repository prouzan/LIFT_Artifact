function {:existential true} b0(x:int, y:int, i:int %Decl:i%, ATTM$x_MOD_5:int): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  y := 5;

  assume(!(x <= 10));
  assume(%M:i%);

  while (x != 2*y)
  invariant b0(x,y,i %Inv:i%, x mod 5);
  {
    assert(i > 0);
    if (x mod 5 == 1) { x := x + 1; }
      else { x := x - 2; }
    i := i - 1;
  }
}

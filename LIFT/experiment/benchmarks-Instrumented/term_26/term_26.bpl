function {:existential true} b0(x:int, y:int, c1:int, c2:int, i:int %Decl:i%, ATTM$c1_MOD_2:int, ATTM$c2_MOD_3:int): bool;

procedure main()
{
  var x,y,c1,c2,i: int;
  havoc x;
  havoc y;
  c1 := 0;
  c2 := 0;

  assume(%M:i%);

  while (x == y)
  invariant b0(x,y,c1,c2,i %Inv:i%, c1 mod 2, c2 mod 3);
  {
    assert(i > 0);
    x := x + c1 mod 2;
    y := y + c2 mod 3;
    c1 := c1 + 1; c2 := c2 + 1;
    i := i - 1;
  }
}

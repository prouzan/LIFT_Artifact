function {:existential true} b0(x:int, y:int, z:int, i:int %Decl:i%, ATTM$y_MOD_50:int, ATTM$z_MOD_50:int): bool;

procedure main()
{
  var x,y,z,i: int;
  x := 0;
  y := 0;
  z := 0;

  assume(%M:i%);

  while (x <= 97)
  invariant b0(x,y,z,i %Inv:i%, y mod 50, z mod 50);
  {
    assert(i > 0);
    x := y mod 50 + z mod 50;
    y := y + 1;
    z := z + 1;
    i := i - 1;
  }
}

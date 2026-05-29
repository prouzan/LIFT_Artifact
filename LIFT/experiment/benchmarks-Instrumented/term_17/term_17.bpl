function {:existential true} b0(x:int, y:int, i:int %Decl:i%, ATTM$y_MOD_50:int): bool;

procedure main()
{
  var x,y,i: int;
  x := 0;
  y := 0;

  assume(%M:i%);

  while (x < 49)
  invariant b0(x,y,i %Inv:i%, y mod 50);
  {
    assert(i > 0);
    x := y mod 50;
    y := y + 1;
    i := i - 1;
  }
}

function {:existential true} b0(x:int, y:int, z:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,z,i: int;
  havoc x;
  havoc y;
  havoc z;

  if (*) {
    x := 1;
  } else {
    x := -1;
  }

  assume(%M:i%);

  while (y < 100 && z < 100)
  invariant b0(x,y,z,i %Inv:i%);
  {
    assert(i > 0);
    y := y + x;
    z := z - x;
    i := i - 1;
  }
}

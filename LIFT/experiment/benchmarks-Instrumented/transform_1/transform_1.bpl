function {:existential true} b0(x:int, y:int, z:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,z,i: int;
  havoc x;
  havoc y;
  assume(!(y <= 1));
  z := 0;

  assume(%M:i%);

  while (x > 0)
  invariant b0(x,y,z,i %Inv:i%);
  {
    assert(i > 0);
    x := x - y;
    y := y - z;
    if (z == 0) { z := 13; }
      else if (z == 13) { z := -20; }
        else if (z == -20) { z := 7; }
          else { z := 0; }
    i := i - 1;
  }
}

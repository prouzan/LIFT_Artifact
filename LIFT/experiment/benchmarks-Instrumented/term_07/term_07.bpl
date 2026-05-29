function {:existential true} b0(x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,i: int;
  havoc x;
  y := 0;

  assume(%M:i%);

  while (x > 0)
  invariant b0(x,y,i %Inv:i%);
  {
    assert(i > 0);
    if (y == 2) { x := x - 3; } else { x := x + 1; }
    if (y == 2) { y := 0; } else { y := y + 1; }
    i := i - 1;
  }
}

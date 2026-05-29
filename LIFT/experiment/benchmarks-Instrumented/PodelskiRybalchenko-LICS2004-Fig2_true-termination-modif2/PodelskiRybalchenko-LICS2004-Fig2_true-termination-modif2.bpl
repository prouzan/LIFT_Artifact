function {:existential true} b0(x:int, y:int, old_x:int, old_y:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,old_x,old_y,i: int;
  havoc x;
  havoc y;

  assume(%M:i%);

  while (x > 0 && y > 0)
  invariant b0(x,y,old_x,old_y,i %Inv:i%);
  {
    assert(i > 0);
    old_x := x;
    old_y := y;
    if (*) {
      x := old_x - 1;
      y := old_x;
    } else {
      x := old_y - 3;
      y := old_x + 2;
    }
    i := i - 1;
  }
}

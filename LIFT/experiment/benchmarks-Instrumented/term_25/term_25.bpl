function {:existential true} b0(x:int, y:int, z:int, w:int, c:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,z,w,c,i: int;
  havoc x;
  havoc y;
  havoc z;
  w := x + y + z;
  c := 0;

  assume(%M:i%);

  while (w == x + y + z)
  invariant b0(x,y,z,w,c,i %Inv:i%);
  {
    assert(i > 0);
    if (c < 100) { y := y - 1; }
    c := c + 1;
    x := x + y + c;
    z := z - y;
    i := i - 1;
  }
}

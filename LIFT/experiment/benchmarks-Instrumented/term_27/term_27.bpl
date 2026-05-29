function {:existential true} b0(x:int, y:int, c1:int, c2:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,c1,c2,i: int;

  havoc x;
  havoc y;

  c1 := 0;
  c2 := 0;
  assume(%M:i%);

  while (x > y)
  invariant b0(x,y,c1,c2,i %Inv:i%);
  {
    assert(i > 0);
    x := x + c1 div 3;
    y := y + c2 div 2;
    c1 := c1 + 2;
    c2 := c2 + 3;

    i := i - 1;
  }
}

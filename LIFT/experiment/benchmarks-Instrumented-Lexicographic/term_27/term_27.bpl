function {:existential true} b0(x:int, y:int, c1:int, c2:int %FD%): bool;

procedure main()
{
  var x,y,c1,c2 %VD%: int;

  havoc x;
  havoc y;

  c1 := 0;
  c2 := 0;
  %BE%

  while (x > y)
  invariant b0(x,y,c1,c2 %IC%);
  {
    %BT%
    x := x + c1 div 3;
    y := y + c2 div 2;
    c1 := c1 + 2;
    c2 := c2 + 3;

    %IT%
  }
}

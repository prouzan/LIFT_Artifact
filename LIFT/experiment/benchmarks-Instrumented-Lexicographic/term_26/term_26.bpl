function {:existential true} b0(x:int, y:int, c1:int, c2:int %FD%, ATTM$c1_MOD_2:int, ATTM$c2_MOD_3:int): bool;

procedure main()
{
  var x,y,c1,c2 %VD%: int;
  havoc x;
  havoc y;
  c1 := 0;
  c2 := 0;

  %BE%

  while (x == y)
  invariant b0(x,y,c1,c2 %IC%, c1 mod 2, c2 mod 3);
  {
    %BT%
    x := x + c1 mod 2;
    y := y + c2 mod 3;
    c1 := c1 + 1; c2 := c2 + 1;
    %IT%
  }
}

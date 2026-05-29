function {:existential true} b0(x:int, y:int %FD%, ATTM$y_MOD_50:int): bool;

procedure main()
{
  var x,y %VD%: int;
  x := 0;
  y := 0;

  %BE%

  while (x < 49)
  invariant b0(x,y %IC%, y mod 50);
  {
    %BT%
    x := y mod 50;
    y := y + 1;
    %IT%
  }
}

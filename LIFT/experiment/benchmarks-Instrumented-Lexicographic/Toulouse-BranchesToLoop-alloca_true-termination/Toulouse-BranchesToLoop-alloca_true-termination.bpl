function {:existential true} b0(x:int, y:int, z:int %FD%): bool;

procedure main()
{
  var x,y,z %VD%: int;
  havoc x;
  havoc y;
  havoc z;

  if (*) {
    x := 1;
  } else {
    x := -1;
  }

  %BE%

  while (y < 100 && z < 100)
  invariant b0(x,y,z %IC%);
  {
    %BT%
    y := y + x;
    z := z - x;
    %IT%
  }
}

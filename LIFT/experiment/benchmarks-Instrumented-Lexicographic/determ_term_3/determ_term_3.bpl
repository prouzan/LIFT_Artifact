function {:existential true} b0(x:int, y:int, z:int %FD%): bool;

procedure main()
{
  var x,y,z %VD%: int;
  x := 5;
  y := 1;
  z := 17;
  
  %BE%
  	
  while (! (x == y && y == z))
  invariant b0(x,y,z %IC%);
  {
    %BT%
    x := x + 1;
    y := y * 2;
    z := z - 3;

    %IT%
  }
}

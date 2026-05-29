function {:existential true} b0(x:int, y:int, z:int %FD%): bool;

procedure main()
{
  var x,y,z,oldx %VD%: int;
  x := 8;
  y := 9;
  z := -2;
  
  %BE%
  	
  while (x + y + z != 0)
  invariant b0(x,y,z %IC%);
  {
    %BT%
    oldx := x;
    x := -y + 1;
    y := 2 * oldx + z;
    z := z * 3;

    %IT%
  }
}

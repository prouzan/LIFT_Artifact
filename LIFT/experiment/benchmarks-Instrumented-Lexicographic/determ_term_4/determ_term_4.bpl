function {:existential true} b0(x:int, y:int, z:int %FD%): bool;

procedure main()
{
  var x,y,z %VD%: int;
  x := 4;
  y := -5;
  z := 1;
  
  %BE%
  	
  while (x + y != z)
  invariant b0(x,y,z %IC%);
  {
    %BT%
    x := x * -3;
    y := y + 2;
    z := z - 36;

    %IT%
  }
}

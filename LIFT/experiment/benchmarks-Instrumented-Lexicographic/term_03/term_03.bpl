function {:existential true} b0(x:int, y:int, z:int %FD%): bool;

procedure main()
{
  var x,y,z %VD%: int;

  havoc x;
  havoc y;
  havoc z;

  %BE%
  	
  while (x > y || y > z)
  invariant b0(x,y,z %IC%);
  {
    %BT%
    x := x - 3;
    y := y - 2;
    z := z - 1;
    
    %IT%
  }
}

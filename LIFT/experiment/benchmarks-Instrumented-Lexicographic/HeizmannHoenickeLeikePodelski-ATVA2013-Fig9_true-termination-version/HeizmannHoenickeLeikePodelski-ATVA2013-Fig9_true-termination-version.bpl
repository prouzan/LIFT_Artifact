function {:existential true} b0(x:int, y:int, z:int %FD%): bool;

procedure main()
{
  var x,y,z %VD%: int;

  havoc x;
  havoc y;
  havoc z;
  
  assume(10 * y > z && z < 10);
  %BE%
  	
  while (x >= 0)
  invariant b0(x,y,z %IC%);
  {
    %BT%
    x := x - 10 * y + z;

    %IT%
  }
}

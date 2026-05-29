function {:existential true} b0(x:int, y:int, z:int %FD%): bool;

procedure main()
{
  var x,y,z %VD%: int;

  havoc x;
  havoc y;
  havoc z;
  
  assume(2*y >= z);
  %BE%
  	
  while (x >= 0 && z == 1)
  invariant b0(x,y,z %IC%);
  {
    %BT%
    x := x - 2 * y + 1;

    %IT%
  }
}

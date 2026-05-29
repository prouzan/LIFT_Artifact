function {:existential true} b0(x:int, y:int, z:int %FD%): bool;

procedure main()
{
  var x,y,z %VD%: int;

  havoc x;
  havoc y;
  havoc z;

  assume(x > 1);
  assume(y > 1);
  assume(z > 1);
  %BE%
  	
  while (x < 1000000)
  invariant b0(x,y,z %IC%);
  {
    %BT%
    x := x * y * z;
    
    %IT%
  }
}

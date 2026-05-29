function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y %VD%: int;

  havoc x;
  havoc y;

  assume(x > y);
  assume(y > 1);
  %BE%
  	
  while (x > y)
  invariant b0(x,y %IC%);
  {
    %BT%
    x := x mod y;
    
    %IT%
  }
}

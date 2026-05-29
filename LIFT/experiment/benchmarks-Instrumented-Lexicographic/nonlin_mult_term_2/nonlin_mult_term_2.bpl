function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y %VD%: int;

  havoc x;
  havoc y;

  assume(x > 1);
  assume(y > 1);
  %BE%
  	
  while (x < 10000)
  invariant b0(x,y %IC%);
  {
    %BT%
    x := x * y;
    
    %IT%
  }
}

function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y %VD%: int;

  havoc x;
  havoc y;

  assume(x div y > 1);
  assume(y > 0);
  %BE%
  	
  while (x != y)
  invariant b0(x,y %IC%);
  {
    %BT%
    x := x - 1;
    
    %IT%
  }
}

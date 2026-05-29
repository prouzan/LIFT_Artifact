function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y %VD%: int;

  havoc x;
  havoc y;
  
  assume(x > y);
  %BE%
  	
  while (x >= 0)
  invariant b0(x,y %IC%);
  {
    %BT%
    y := 2 * y - x;
    x := (y + x + 1) div 2;

    %IT%
  }
}

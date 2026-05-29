function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y %VD%: int;
  havoc x;
  havoc y;
  
  %BE%
  	
  while (x < 0 && y > 0)
  invariant b0(x,y %IC%);
  {
    %BT%
    x := -3 * x - 17;
    y := -4 * y + 8;
    
    %IT%
  }
}

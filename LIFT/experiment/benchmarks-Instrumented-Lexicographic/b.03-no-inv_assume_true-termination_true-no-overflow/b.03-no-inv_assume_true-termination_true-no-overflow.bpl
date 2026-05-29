function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y %VD%: int;
  havoc x;
  havoc y;
  
  assume(x > 0);
  %BE%
  
  while (x > y && y <= 2147483647 - x)
  invariant b0(x,y %IC%);
  {
    %BT%
    
    y := y + x;
    %IT%
  }
}

function {:existential true} b0(x:int, oldx:int %FD%): bool;

procedure main()
{
  var x,oldx %VD%: int;
  havoc x;
  
  %BE%
  	
  while (x > 0 && x < 100 && x >= 2 * oldx + 10)
  invariant b0(x,oldx %IC%);
  {
    %BT%
    oldx := x;
    havoc x;
    
    %IT%
  }
}

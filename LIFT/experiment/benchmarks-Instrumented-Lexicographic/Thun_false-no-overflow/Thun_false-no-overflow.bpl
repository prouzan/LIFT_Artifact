function {:existential true} b0(x:int, y:int %FD%, ATTM$2$MUL$x$ADD$y:int): bool;

procedure main()
{
  var x,y %VD%: int;

  havoc x;
  havoc y;

  %BE%
  	
  while (x >= 0)
  invariant b0(x,y %IC%, 2*x + y);
  {
    %BT%
    x := x + y;
    y := (-2) * y - 1;
    
    %IT%
  }
}

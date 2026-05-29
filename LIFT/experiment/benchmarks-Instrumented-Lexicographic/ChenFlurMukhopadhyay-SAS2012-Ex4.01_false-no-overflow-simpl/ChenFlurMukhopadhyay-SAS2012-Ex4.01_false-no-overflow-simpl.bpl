function {:existential true} b0(x:int, y:int, n:int %FD%): bool;

procedure main()
{
  var x,y,n %VD%: int;
  havoc x;
  havoc y;
  havoc n;
  
  %BE%
  	
  while (x + y >= 0 && x <= n)
  invariant b0(x,y,n %IC%);
  {
    %BT%
    x := 2 * x + y;
    y := y + 1;
    
    %IT%
  }
}

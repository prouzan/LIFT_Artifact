function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y %VD%,r: int;
  havoc x;
  havoc y;

  r := 1;
  
  %BE%
  	
  while (y > 0)
  invariant b0(x,y %IC%);
  {
    %BT%
    r := r * x;
    y := y - 1;

    %IT%
  }
}

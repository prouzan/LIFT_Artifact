function {:existential true} b0(d:int, b:int %FD%): bool;

procedure main()
{
  var d,b %VD%: int;

  havoc d;
  havoc b;

  %BE%
  	
  while (d * b > 0)
  invariant b0(d,b %IC%);
  {
    %BT%
    b := -b;
    
    %IT%
  }
}

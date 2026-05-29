function {:existential true} b0(x:int %FD%): bool;

procedure main()
{
  var x %VD%: int;
  havoc x;
  
  assume(x > 0);
  %BE%
  
  while (x != 0)
  invariant b0(x %IC%);
  {
    %BT%
    x := x - 1;
    %IT%
  }
}

function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y %VD%: int;

  havoc x;
  havoc y;

  assume(x > y);
  %BE%
  	
  while (x != y)
  invariant b0(x,y %IC%);
  {
    %BT%
    x := x - 2;
    y := y - 1;

    %IT%
  }
}

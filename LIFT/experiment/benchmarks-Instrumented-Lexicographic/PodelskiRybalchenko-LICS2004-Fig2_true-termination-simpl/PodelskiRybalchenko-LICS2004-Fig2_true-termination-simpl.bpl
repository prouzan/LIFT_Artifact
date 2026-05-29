function {:existential true} b0(x:int, y:int, old_x:int, old_y:int %FD%): bool;

procedure main()
{
  var x,y,old_x,old_y %VD%: int;

  havoc x;
  havoc y;

  %BE%
  	
  while (x > 0 && y > 0)
  invariant b0(x,y,old_x,old_y %IC%);
  {
    %BT%
    old_x := x;
    old_y := y;
    x := old_y - 2;
    y := old_x + 1;

    %IT%
  }
}

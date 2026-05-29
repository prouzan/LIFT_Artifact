function {:existential true} b0(x:int, y:int %FD%): bool;

procedure main()
{
  var x,y,oldx %VD%: int;
  havoc x;
  havoc y;
  
  assume(-1073741823 <= x && x <= 1073741823);
  assume(-1073741823 <= y && y <= 1073741823);
  %BE%
  	
  while (x >= 0 || y >= 0)
  invariant b0(x,y %IC%);
  {
    %BT%
    oldx := x;
    x := y - 1;
    y := oldx - 1;

    %IT%
  }
}

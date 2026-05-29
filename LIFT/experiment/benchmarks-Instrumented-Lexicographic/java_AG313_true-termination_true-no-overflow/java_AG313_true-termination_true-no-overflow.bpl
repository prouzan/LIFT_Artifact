function {:existential true} b0(_i:int, x:int, y:int %FD%): bool;

procedure main()
{
  var _i,x,y %VD%: int;

  _i := 0;
  havoc x;
  havoc y;
  
  assume(x != 0);
  %BE%
  	
  while (x > 0 && y > 0)
  invariant b0(_i,x,y %IC%);
  {
    %BT%
    _i := _i + 1;
    x := (x - 1) - (y - 1);

    %IT%
  }
}

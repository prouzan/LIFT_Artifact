function {:existential true} b0(n:int %FD%, ATTM$n$SUB$_i:int): bool;

procedure main()
{
  var _i,x,y,n %VD%: int;
  _i := 0;
  x := 0;
  y := 0;
  havoc n;
  
  %BE%
  
  while (_i < n)
  invariant b0(n %IC%, n - _i);
  {
    %BT%
    x := x - y;
    havoc y;
    x := x + y;
    _i := _i + 1;

    %IT%
  }
}

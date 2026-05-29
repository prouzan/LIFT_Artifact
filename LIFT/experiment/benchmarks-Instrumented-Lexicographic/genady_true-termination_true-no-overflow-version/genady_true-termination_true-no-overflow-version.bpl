function {:existential true} b0(_i:int, j:int %FD%, ATTM$_i$SUB$2$MUL$i:int, ATTM$j$ADD$3$MUL$i:int): bool;

procedure main()
{
  var _i,j %VD%: int;
  j := 1;
  _i := 10000;

  %BE%

  while (_i-j >= 1)
  invariant b0(_i,j %IC%, _i-2*i, j+3*i);
  {
    %BT%
    j := j + 3;
    _i := _i - 2;
    %IT%
  }
}

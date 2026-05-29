function {:existential true} b0(_i:int, j:int, k:int %FD%): bool;

procedure main()
{
  var _i,j,k %VD%: int;
  _i := 100;
  j := -1;
  k := 1;

  %BE%

  while (_i + j + k >= 1)
  invariant b0(_i,j,k %IC%);
  {
    %BT%
    _i := _i - 1;
    j := j - 1;
    k := k + 1;
    %IT%
  }
}

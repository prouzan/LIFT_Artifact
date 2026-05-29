function {:existential true} b0(d:int, b:int, _i:int, j:int %FD%): bool;

procedure main()
{
  var _i,j,d,b %VD%: int;

  _i := 1;
  j := 1;
  havoc d;
  havoc b;

  assume(b > 1);
  assume(b > d);

  %BE%
  	
  while (_i >= j)
  invariant b0(d,b,_i,j %IC%);
  {
    %BT%
    _i := _i * d;
    j := j * b;
    
    %IT%
  }
}

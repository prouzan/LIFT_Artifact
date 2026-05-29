function {:existential true} b0(d:int, b:int, _i:int, j:int, i:int %Decl:i%): bool;

procedure main()
{
  var _i,j,d,b,i: int;

  _i := 1;
  j := 1;
  havoc d;
  havoc b;

  assume(b > 1);
  assume(b > d);

  assume(%M:i%);
  	
  while (_i >= j)
  invariant b0(d,b,_i,j,i %Inv:i%);
  {
    assert(i > 0);
    _i := _i * d;
    j := j * b;
    
    i := i - 1;
  }
}

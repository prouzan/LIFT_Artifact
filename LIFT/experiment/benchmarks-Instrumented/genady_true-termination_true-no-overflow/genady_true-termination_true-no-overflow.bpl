function {:existential true} b0(_i:int, j:int, i:int %Decl:i%, ATTM$_i$SUB$i:int, ATTM$j$ADD$i:int): bool;

procedure main()
{
  var _i, j, i: int;
  j := 1;
  _i := 10000;
  
  assume(%M:i%);
  	
  while (_i - j >= 1)
  invariant b0(_i, j, i %Inv:i%, _i-i, j+i);
  {
    assert(i > 0);
    j := j + 1;
    _i := _i - 1;

    i := i - 1;
  }
}

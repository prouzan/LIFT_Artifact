function {:existential true} b0(_i:int, j:int, a:int, b:int, i:int %Decl:i%, ATTM$_i$ADD$j$ADD$a$ADD$b: int): bool;

procedure main()
{
  var _i,j,a,b,i: int;

  havoc _i;
  havoc j;
  havoc a;
  havoc b;

  assume(%M:i%);
  	
  while (_i + j + a + b == 0)
  invariant b0(_i,j,a,b,i %Inv:i%, _i + j + a + b);
  {
    assert(i > 0);

    if(*)
    {
      _i := _i - 1;
    }
    else
    {
      j := j + 1;
    }
    if(*)
    {
      a := a - 2;
    }
    else
    {
      b := b + 2;
    }

    i := i - 1;
  }
}

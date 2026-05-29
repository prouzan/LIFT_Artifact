function {:existential true} b0(_i:int,j:int,k:int,tmp:int, i:int %Decl:i%): bool;

procedure main()
{
  var c,_i,j,k,tmp,i: int;
  havoc _i;
  havoc j;
  havoc k;
  havoc tmp;
  
  assume(%M:i%);
  
  while (_i <= 100)
  invariant b0(_i,j,k,tmp,i %Inv:i%);
  {
    assert(i > 0);
    
    tmp := _i;
    _i := j;
    j := tmp + 1;
    i := i - 1;
  }
}

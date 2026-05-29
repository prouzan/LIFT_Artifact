function {:existential true} b0(_i:int,j:int,k:int,tmp:int, i:int %Decl:i%, ATTM$k$SUB$j:int,ATTM$k$SUB$_i:int): bool;

procedure main()
{
  var c,_i,j,k,tmp,i: int;
  havoc _i;
  havoc j;
  havoc k;
  havoc tmp;
  
  c := 0;
  assume(%M:i%);
  
  while ((_i <= 100) && (j <= k) && (k > -2147483648))
  invariant b0(_i,j,k,tmp,i %Inv:i%,k-j,k-_i);
  {
    assert(i > 0);
    
    tmp := _i;
    _i := j;
    j := tmp + 1;
    k := k - 1;
    i := i - 1;
  }
}

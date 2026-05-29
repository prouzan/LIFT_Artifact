function {:existential true} b0(_i:int,j:int,k:int,tmp:int %FD%, ATTM$k$SUB$j:int,ATTM$k$SUB$_i:int): bool;

procedure main()
{
  var c,_i,j,k,tmp %VD%: int;
  havoc _i;
  havoc j;
  havoc k;
  havoc tmp;
  
  c := 0;
  %BE%
  
  while ((_i <= 100) && (j <= k) && (k > -2147483648))
  invariant b0(_i,j,k,tmp %IC%,k-j,k-_i);
  {
    %BT%
    
    tmp := _i;
    _i := j;
    j := tmp + 1;
    k := k - 1;
    %IT%
  }
}

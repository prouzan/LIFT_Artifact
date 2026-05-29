function {:existential true} b0(_i:int,j:int,k:int,tmp:int %FD%): bool;

procedure main()
{
  var c,_i,j,k,tmp %VD%: int;
  havoc _i;
  havoc j;
  havoc k;
  havoc tmp;
  
  %BE%
  
  while (_i <= 100)
  invariant b0(_i,j,k,tmp %IC%);
  {
    %BT%
    
    tmp := _i;
    _i := j;
    j := tmp + 1;
    %IT%
  }
}

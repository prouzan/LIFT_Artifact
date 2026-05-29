function {:existential true} b0(j:int, d:int, i:int %Decl:i%): bool;

procedure main()
{
  var j,d,i: int;

  havoc j;
  havoc d;

  assume(%M:i%);
  	
  while (j > 0 && d > 0)
  invariant b0(j,d,i %Inv:i%);
  {
    assert(i > 0);
    if(*)
    {
      j := j - 1;
    }
    else
    {
      d := d - 1;
    }
    
    i := i - 1;
  }
}

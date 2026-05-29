function {:existential true} b0(j:int, d:int, i:int %Decl:i%): bool;

procedure main()
{
  var j,d,i: int;

  havoc j;
  havoc d;

  assume(j > d);
  assume(d > 1);

  assume(%M:i%);
  	
  while (j > d)
  invariant b0(j,d,i %Inv:i%);
  {
    assert(i > 0);
    j := j mod 2;

    i := i - 1;
  }
}

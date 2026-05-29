function {:existential true} b0(j:int, b:int, i:int %Decl:i%): bool;

procedure main()
{
  var j,b,i: int;

  havoc j;
  havoc b;

  assume(b > 1);
  assume(j >= 1);
  assume(%M:i%);
  	
  while (j < 10)
  invariant b0(j,b,i %Inv:i%);
  {
    assert(i > 0);
    j := -2 * j * b;

    i := i - 1;
  }
}

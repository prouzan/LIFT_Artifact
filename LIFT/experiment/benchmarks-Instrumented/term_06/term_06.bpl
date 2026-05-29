function {:existential true} b0(x:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,i: int;

  x := 0;

  assume(%M:i%);

  while (x < 1000)
  invariant b0(x,i %Inv:i%);
  {
    assert(i > 0);
    if (x != 7777) { x := x + 1; }
    i := i - 1;
  }
}

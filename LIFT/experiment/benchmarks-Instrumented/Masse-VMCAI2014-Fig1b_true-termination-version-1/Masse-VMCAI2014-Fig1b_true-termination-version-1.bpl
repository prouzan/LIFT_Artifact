function {:existential true} b0(x:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,i: int;
  havoc x;

  assume(%M:i%);

  while (x <= 100)
  invariant b0(x,i %Inv:i%);
  {
    assert(i > 0);
    if (*) {
        x := - 2 * x + 2;
    } else if (*) {
        x := - 3 * x - 2;
    } else {
        x := - 4 * x + 2;
    }
    i := i - 1;
  }
}

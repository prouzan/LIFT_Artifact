function {:existential true} b0(x:int, c:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,c,i: int;
  havoc x;
  c := 1;

  assume(%M:i%);

  while (c > 0)
  invariant b0(x,c,i %Inv:i%);
  {
    assert(i > 0);
    if (x > 100) {
        x := x-10;
        c := c-1;
    } else {
        x := x+11;
        c := c+1;
    }
    i := i - 1;
  }
}

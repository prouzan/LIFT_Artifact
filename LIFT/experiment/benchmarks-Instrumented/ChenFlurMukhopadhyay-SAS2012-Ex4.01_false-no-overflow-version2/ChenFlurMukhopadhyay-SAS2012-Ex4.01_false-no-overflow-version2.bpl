function {:existential true} b0(x:int, y:int, z:int, n:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,z,n,i: int;
  havoc x;
  havoc y;
  havoc z;
  havoc n;

  assume(!(z == 0));
  assume(%M:i%);

  while (x + y >= 0 && x <= n)
  invariant b0(x,y,z,n,i %Inv:i%);
  {
    assert(i > 0);
    x := 2*x - y;
    y := z;
    z := -2*z;
    i := i - 1;
  }
}

function {:existential true} b0(K:int, x:int, y:int, i:int %Decl:i%): bool;

procedure main()
{
  var K,x,y,i: int;
  havoc K;
  havoc x;
  havoc y;

  assume(x < y);
  assume(%M:i%);

  while (y != K)
  invariant b0(K,x,y,i %Inv:i%);
  {
    assert(i > 0);
    if (x == y) {
      if (x > K) {
        x := x - 1;
      } else {
        x := x + 1;
      }
      y := x;
    } else {
      y := y - 1;
    }
    i := i - 1;
  }
}

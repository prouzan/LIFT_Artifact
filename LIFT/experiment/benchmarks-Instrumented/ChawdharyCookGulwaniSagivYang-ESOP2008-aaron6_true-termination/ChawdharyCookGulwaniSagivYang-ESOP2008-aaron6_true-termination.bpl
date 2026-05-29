function {:existential true} b0(x:int, tx:int, y:int, ty:int, n:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,tx,y,ty,n,i: int;
  havoc x;
  havoc tx;
  havoc y;
  havoc ty;
  havoc n;

  assume(x + y >= 0);
  assume(%M:i%);

  while (x <= n && x >= 2 * tx + y && y >= ty + 1 && x >= tx + 1)
  invariant b0(x,tx,y,ty,n,i %Inv:i%);
  {
    assert(i > 0);
    if (*) {
      tx := x;
      ty := y;
      havoc x;
      havoc y;
    } else {
      tx := x;
      havoc x;
    }
    i := i - 1;
  }
}

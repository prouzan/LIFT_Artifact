function {:existential true} b0(x:int, y:int, n:int, b:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,y,n,b,i: int;
  havoc n;
  havoc b;
  havoc x;
  havoc y;

  assume(%M:i%);

  while (x >= 0 && 0 <= y && y <= n)
  invariant b0(x,y,n,b,i %Inv:i%);
  {
	assert(i > 0);
	if (b == 0) {
			y := y + 1;
			if (*) {
				b := 1;
      }
		} else {
			y := y - 1;
			if (*) {
				x := x - 1;
				b := 0;
			}
		}
	i := i - 1;
  }
}

function {:existential true} b0(x:int, y:int, z:int, n:int %FD%): bool;

procedure main()
{
  var x,y,z,n %VD%: int;
  havoc x;
  havoc y;
  havoc z;
  havoc n;

  assume(!(z == 0));
  %BE%

  while (x + y >= 0 && x <= n)
  invariant b0(x,y,z,n %IC%);
  {
    %BT%
    x := 2*x - y;
    y := z;
    z := -2*z;
    %IT%
  }
}

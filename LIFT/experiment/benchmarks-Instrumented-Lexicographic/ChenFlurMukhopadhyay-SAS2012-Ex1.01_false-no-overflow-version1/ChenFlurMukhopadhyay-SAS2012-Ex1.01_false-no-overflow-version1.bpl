function {:existential true} b0(x:int %FD%): bool;

procedure main()
{
  var x %VD%: int;
  havoc x;

  %BE%

  while (x > 0)
  invariant b0(x %IC%);
  {
    %BT%
    x := -5*x + 50;
    %IT%
  }
}

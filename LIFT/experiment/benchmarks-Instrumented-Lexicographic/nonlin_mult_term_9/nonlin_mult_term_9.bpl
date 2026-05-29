function {:existential true} b0(j:int, b:int %FD%): bool;

procedure main()
{
  var j,b %VD%: int;

  havoc j;
  havoc b;

  assume(b > 1);
  assume(j >= 1);
  %BE%
  	
  while (j < 10)
  invariant b0(j,b %IC%);
  {
    %BT%
    j := -2 * j * b;

    %IT%
  }
}

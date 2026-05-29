function {:existential true} b0(j:int, d:int %FD%): bool;

procedure main()
{
  var j,d %VD%: int;

  havoc j;
  havoc d;

  assume(j > d);
  assume(d > 1);

  %BE%
  	
  while (j > d)
  invariant b0(j,d %IC%);
  {
    %BT%
    j := j mod 2;

    %IT%
  }
}

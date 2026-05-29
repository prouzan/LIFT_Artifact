function {:existential true} b0(a:int, b:int, olda:int %FD% ): bool;

procedure main()
{
  var a,b,olda %VD%: int;
  havoc a;
  havoc b;

  %BE%
  	
  while (a > 0)
  invariant b0(a,b,olda %IC%);
  {
    %BT%
    olda := a;
    a := 3*olda - 4*b;
    b := 4*olda + 3*b;
    %IT%
  }
}

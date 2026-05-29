function {:existential true} b0(a:int, b:int, q:int, olda:int %FD% ): bool;

procedure main()
{
  var a,b,q,olda %VD%: int;
  havoc q;
  havoc a;
  havoc b;

  %BE%
  	
  while (q > 0)
  invariant b0(a,b,q,olda %IC%);
  {
    %BT%
    q := q + a - 1;
    olda := a;
    a := 3*olda - 4*b;
    b := 4*olda + 3*b;
    %IT%
  }
}

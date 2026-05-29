function {:existential true} b0(a:int, b:int, q:int, olda:int, i:int %Decl:i% ): bool;

procedure main()
{
  var a,b,q,olda,i: int;
  havoc q;
  havoc a;
  havoc b;

  assume(%M:i%);
  	
  while (q > 0)
  invariant b0(a,b,q,olda,i %Inv:i%);
  {
    assert(i > 0);
    q := q + a - 1;
    olda := a;
    a := 3*olda - 4*b;
    b := 4*olda + 3*b;
    i := i - 1;
  }
}

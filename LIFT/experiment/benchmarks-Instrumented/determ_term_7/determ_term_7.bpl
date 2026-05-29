function {:existential true} b0(a:int, b:int, c:int, d:int, _e:int, i:int %Decl:i%): bool;

procedure main()
{
  var a, b, c, d, _e, i: int;
  a := 0;
  b := 0;
  c := 0;
  d := 0;
  _e := 0;
  
  assume(%M:i%);
  	
  while (a == 0)
  invariant b0(a, b, c, d, _e, i %Inv:i%);
  {
    assert(i > 0);
    a := a + b;
    b := b + c;
    c := c + d;
    d := d + _e;
    _e := _e + 1;

    i := i - 1;
  }
}

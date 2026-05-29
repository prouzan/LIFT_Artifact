function {:existential true} b0(a:int, b:int, c:int, d:int, _e:int, f:int %FD%): bool;

procedure main()
{
  var a, b, c, d, _e, f %VD%: int;
  a := 0;
  b := 0;
  c := 0;
  d := 0;
  _e := 0;
  f := 0;
  
  %BE%
  	
  while (a == 0)
  invariant b0(a, b, c, d, _e, f %IC%);
  {
    %BT%
    a := a + b;
    b := b + c;
    c := c + d;
    d := d + _e;
    _e := _e + f;
    f := f + 1;

    %IT%
  }
}

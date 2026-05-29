function {:existential true} b0(a:int, b:int, x:int, y:int %FD%): bool;

procedure main()
{
  var a,b,x,y,tmp %VD%: int;
  havoc a;
  havoc b;
  havoc x;
  havoc y;
  
  assume(a == b);
  %BE%
  	
  while (x >= 0 || y >= 0)
  invariant b0(a,b,x,y %IC%);
  {
    %BT%
    x := x + a - b - 1;
    y := y + b - a - 1;
    tmp := a;
    a := b;
    b := tmp;

    %IT%
  }
}

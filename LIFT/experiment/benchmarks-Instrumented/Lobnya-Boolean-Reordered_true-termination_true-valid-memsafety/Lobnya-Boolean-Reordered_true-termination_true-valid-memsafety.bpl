function {:existential true} b0(x:int, b:int, i:int %Decl:i%): bool;

procedure main()
{
  var x,b,i: int;

  havoc x;
  havoc b;
  
  assume(x >= -2147483647);
  assume(%M:i%);
  	
  while (b != 0)
  invariant b0(x,b,i %Inv:i%);
  {
    assert(i > 0);
    havoc b;
    x := x - 1;
    if (x >= 0){
        b := 1;
    }
    else{
        b := 0;
    }
    i := i - 1;
  }
}

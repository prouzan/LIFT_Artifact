function {:existential true} b0(a:int, i:int %Decl:i%, ATTM$a_MOD_10:int): bool;

procedure main()
{
  var a,i: int;
  havoc a;
  
  assume(%M:i%);
  	
  while (a > 1)
  invariant b0(a,i %Inv:i%, a mod 10);
  {
    assert(i > 0);
    
    if(a mod 10 == 0){
      a := a div 10;
    }
    else {
      a := a - 1;
    }
    i := i - 1;
  }
}

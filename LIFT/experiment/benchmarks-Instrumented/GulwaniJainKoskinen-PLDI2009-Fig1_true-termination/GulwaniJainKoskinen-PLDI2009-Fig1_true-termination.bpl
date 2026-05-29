function {:existential true} b0(id:int, maxId:int, tmp:int, i:int %Decl:i%, ATTM$i$ADD$tmp:int): bool;

procedure main()
{
  var id, maxId, tmp, i: int;
  havoc id;
  havoc maxId;

  assume(0 <= id && id < maxId);
  tmp := id + 1;
  assume(%M:i%);

  while (tmp != id)
  invariant b0(id, maxId, tmp, i %Inv:i%, i + tmp);
  {
    assert(i > 0);
    if (tmp <= maxId)
    {
        tmp := tmp + 1;
    }
    else
    {
        tmp := 0;
    }
    i := i - 1;
  }
}

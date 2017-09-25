#encoding "utf-8"

PersonName -> Word<kwtype="имя"> | Word<kwtype="имя_без_фамилии">;

Person -> PersonName interp (Person.Name);

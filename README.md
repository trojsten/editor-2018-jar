# editor-2017-jesen
Editor na jesenne KSP sustredko 2017.

## Django

To copy CKEditor run: `python manage.py collectstatic`.

First run: (optimalne mat virtualenv s python3 a djangom)

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


## Apt-gets
`fp-compiler`: free pascal
`g++`: C++ compiler
`python3`: pytohn compiler


## Jazyk

Každý riadok kódu je v inomm jazyku. Vo všetkých jazykoch máte prístup k niekoľkým
dopreedu definovaným premenným. Riadky sa vykonávajú pekne jeden za druhým.

Okrem beždých programovacích konštrukcí tento jazyk ešte obsahuje príkaz `IF <premenna> IS NOT ZERO GOTO <cislo_riadka>`. Pri vyhodnotení tohoto príkazu sa pozrieme na
  hodnotu premnnej `<var>` a ak nie je nulová, pokračujeme na riadku `<cislo_riadka>`.

Inak pokračujeme na ďalšom riadku.

Technicky detajl na zaver. Specialne znaky v stringoch pouziajte len na vlastne riziko.

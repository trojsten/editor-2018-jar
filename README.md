# editor-2018-jar
Editor na jarne KSP sustredko 2018.

## Django

See README in `editor` directory.

Odporúčam si nainštalovať všetky requirements z `editor` priečinku, a potom pustiť `./hard_reset.sh`, ktorý robí všetko potrebné, a ešte aj sa opýta na nastavenie super usera. Toho treba vytvoriť, aby ste sa mohli prihlásiť do appky.

## Apt-gets
 - `fp-compiler`: free pascal
 - `g++`: C++ compiler
 - `python3`: Python interpreter
 - `golang-go`: Go compiler & toolchain
 - `php7.0-cli`: Php?  nie som si ale uplne isty verziou
 - `rustc` : Rust
 - `perl` : Perl5
 - `r-base` : R-ko
 - `sudo apt install fp-compiler g++ python3 golang-go php7.0-cli rustc perl r-base`


## Jazyk

Každý riadok kódu je v inomm jazyku. Vo všetkých jazykoch máte prístup k niekoľkým
dopreedu definovaným premenným. Riadky sa vykonávajú pekne jeden za druhým.

Okrem beždých programovacích konštrukcí tento jazyk ešte obsahuje príkaz `IF <premenna> IS NOT ZERO GOTO <cislo_riadka>`. Pri vyhodnotení tohoto príkazu sa pozrieme na
  hodnotu premnnej `<var>` a ak nie je nulová, pokračujeme na riadku `<cislo_riadka>`.

Inak pokračujeme na ďalšom riadku.

Technicky detajl na zaver. Specialne znaky v stringoch pouziajte len na vlastne riziko.

## Ako sa pridava jazyk?

Chod na https://github.com/Zajozor/editor-2017-jesen/issues/1 a vyber si jazyk ktory mas rad este nie je urobeny.

Bud do issue napiste, ze chcete robit dany jazyk, alebo ho rovno zaskrtnite.

Nasledne mas dve moznosti:

### 1) napisat vlastny runner

Staci si pozriet runners/runner.py, a v novom subore subclassnut classu Runner a overridnut vsetky metody ktore maju v komentari override.
Meno a popis by mali byt zjavne. Ak nie, tak som (vlejd) nieco pokaslal a treba mi to napisat.
Pridajte aj if __name__ == '__main__': v ktorom sa vas kod vyskusa.
Inspirujte sa runner_cpp.py.
Testuje sa to tak, ze pridete do adresara judge a z neho pustite `python3 -m runners.runner_cpp` respektive `python3 -m runners.runner_<moj_jazyk>`.

Ak by to pindalo ze nema subor `tmp/volac`, teba vytvorit adresar `tmp` v priecinku judge.

### 2) napisem konkretny kod v danom jazyku a poslem to vlejdovi

Funkcionalita je nasledovna:
Ako commandline argument dostane dva subory.
Z jedneho nacita vektor intov, vektor stringov a vektor floatov.
V prvom riadku je vzdy dlzka vektora, v dalsich su samotne hodnoty (jedna hodnota na riadok).
Nasledne dane vektory zapise do druheho suboru.
Floaty sa vypisuju na 6 desatinnych miest.
Tento kod aj s instrukciami na kompilaciu a pustanie staci potom poslat vlejdovi a on z toho spravi runnera.

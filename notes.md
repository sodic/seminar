## Uvod

Nanoporeov base caller na koji se Nanopolish oslanja radi tako da:
1. Nekako je empirijski izgradena tablica normalnih distribucija u kojima se krece struja za svaku mogucu k-torku. U nasem je slucaju k-torka duljine 6. Prema tome, tablica ima 4096 redaka. Ova tablica naziva se *modelom*. Tablica po kojoj radi basecaller koristena u ovom procesu dostupna je ovdje: https://github.com/jts/nanopolish/blob/b9dc627e73816a415e4b96b14e8a8bf53622a6c9/etc/r9-models/r9.4_450bps.nucleotide.6mer.template.model (model koji tombo koristi: https://github.com/nanoporetech/tombo/blob/master/tombo/tombo_models/tombo.DNA.model)
2. Uzrokuje se struja i racunaju parametri normalne distribucije
3. U tablici iz koraka 1. pronalazi se normalna distribucija koja najbolje odgovara onoj izracunatoj iz uzorka i zakljucuje se da je rijec o odgovarajućoj k-torci.

## Sto se tice Nanopolisha:

1. `contig` - Ime contiga koji je dio reference.
2. `position` - Pozicija u contigu (position ime contiga zajedno jednoznacno odreduju poziciju u referenci). Ako koja pozicija nedostaje, znaci da taj dio reference nije uspjesno poravnat ni s jednim dijelom signala.
3. `reference_kmer` - K-torka koja se nalazi na doticnoj poziciji.
4. `read_index` - Indeks contiga cije je ime u prvom stupcu. Cini se da si Nanopolish odabere svoje indekse, nema previse veze s redoslijedom u datoteci.  Mislim da nam je ovo polje nevazno. Sve informacije koje nam trebaju sadrzane su u imenu contiga (1) i poziciji (2).
5. `strand` - Trebao bi oznacavati strand, ali uvijek je `t`. Ipak, cini se da mozemo utvrditi radi li se o komplementu usporedujuci `reference_kmer` i `model kmer`.
6. `event` - Indeks eventa (event je niza uzoraka u signalu), ide po redu.
7. `event_level_mean` - Ocekivanje izracunato iz uzoraka koji pripadaju tome eventu.
8. `event_stdv` - Standardna devijacija izracunata iz uzoraka koji pripadaju tome eventu.
9. `event_length` - vremenski interval u kojem su skupljeni svi uzorci za taj event.
10. `model_kmer` - K-torka modela, ona za koju je basecaller callao na temelju slicnosti distribucija (ona iz gore spomenute tablice).
11. `model_mean` - Ocekivanje distribucije za taj model (opet iz tablice).
12. `standardized_level` - racuna se po formuli koju je Dario napisao na slack.
13. `start_index` - indeks prvog uzorka sadrzanog u eventu
14. `end_index` - indeks za jedan veci od poslijednjeg uzorka sadrzanog u
eventu
15. `samples` - svi uzorci eventa

## Sto se tice Tomba:
  - Podaci o eventu za jednu bazu koje Tombo vraća:
 	1. `norm_mean` - normalizirana srednja vrijednost signala
	2. `norm_stdev` - standardna devijacija signala
	3. `start` - index početka baze u signalu
	4. `length` - trajanje baze u signalu (`stdev` i `mean` se računaj s obzirom na signale između start i start + length)
	5. `base` - string koji predstavlja bazu
	6. `digitisation`, `offset`, `range` su parametri koje Tombo koristi za pretvorbu signala iz pA
	7. `sampling_rate` - broj baza u sekundi
	8. `mapped_chrom` - ime kontiga
  
## Sto se tice protobufa:
Fokusirali smo se na pretvorbu jednog formata outputa u drugi (vise o tome kasnije), Zelimo li mozda imati i datoteku koja izgleda ovako:
```
{
	nanopolish data: ...
	tombo data: ...
}
```
Zajednicki event bi onda bio:
```
{
	unit32 start_index    		//pocetna pozicija u sekvenci
	uint 32 end_index		//krajnja pozicija u sekvenci
	double mean 			// u pA
	double stdev		
	string base/kmer			//base ili kmer 
	repeated double samples
}
```

## Sto se tice usporedbe Nanopolisha i Tomba:
  - nakon što smo otkrili koja su značenja polja unutar nanopolisha, mogli smo zakljuciti par stvari:
  	1. `position` možemo poravnati s tombovim indexom baze
	2. `contig` je identičan
	3. `event_level_mean`, `event_stdv`, `model_mean` nemožemo usporedivati jer nanopolish dobiva brojeve koji nigdje nisu objašnjeni [nasao sam neku transformaciju nasih norm_mean i norm_stdev vrijednosti iz tomba ali to moramo napisat prvo da bih mogao reci dal je ista vrijednost struja; nanopolish dobiva pA, tj. ono sta bi mi iz tomba trebali dobri]
	4. `reference_kmer` i `model_kmer` možemo donekle jednostavno dobiti konkatenirajući baze tombo evenata, uz problem reverznog komplementa, tombo nam ne daje tu informaciju, odnosno kod nanopolish/a nije potpuno jasno kada radi switch izmedu reverznog komplementa i obicnog (možda se ovo može izvući iz imena contige, ako pozicije baza na kraju imena idu od većeg prema manjem)	
	5. `length` donekle se poklapa, ali poklananje nije 100% točno, dolazi ponekad i do većih odstupanja
	6. `standardized_level` mislim da nemamo informacije
	7. `read_index` je za tombo uvijek 0 jer ne podržava multiread fast5 datoteke
  - start index i end index ne mozemo usporedit jer tombo gleda samo za kratko ocitanje (signal)
  - moguce da tombo gleda samo centralni, a nanopolish to interpretira kao dolazak novog kmera (koji je isti i zapravo nije novi) dok tombo misli da je novi (drugi je u centru, ali je i dalje isti kmer unutra)
  - nakon prvog nanopolishovog lazno detektirano novog kmer usporedbe više nemaju smisla za taj kmer jer ni se svi podaci razlikuju
  ### Zaključak usporedbe
Cini nam se da ovo nije smislen posao. Jedan je napravljen da radi jedno, a drugi drugo. Usporedba ce puno vise reci o nasem algoritmu preslikavanja no sto ce reci o alatima. Cim preslikavanje nije trivijalno, ne vjerujem da se iz konacnih rezultata mogu izvuci ikakvi relevantni zakljucci. Kako cemo odvojiti posljedice algoritama Tomba/Nanopolisha od posljedica naseg algoritma pretvorbe?

Pokusali smo brojne strategije preslikavanja baza u k-torke:
    - to je sve isto
    - kotinuirani output za evente
    - diskretni output za evente
    - trajanja evenata, poceci evenata, svakakve kombinacije

Ako je basecallanje radeno s k-torkama, Tombo dobiva baze algoritmom pretvorbe nad k-torkama (koji je sigurno ireverzibilan i uzrokuje greske) [kak znamo za ireverzibilnost?] . Mi bismo trebali svojim algoritmom (koji takoder neizbjezno uzrokuje greske) vratiti podatke u oblik u kojem su bili prije no sto je Tombo primjenjen. Cini nam se da je to analogno sa sljedecim postupkom:
1. Imamo dvije slike u .bmp formatu, ali ne mozemo ga otvoriti na racunalu.  Mozemo otvarati samo .png
2. Jednu sliku konvertiramo u .png bez gubitaka, a drugu maksimalnim postavkama kompresije konvertiramo u .jpg (s gubitkom kvalitete), zatim izmislimo algoritam kojim cemo je pretvoriti u .png te ga primjenimo.
3. Usporedimo dvije dobivene slike.

.bmp slike su ulazi u Tombo i Nanopolish, direktna konverzija u .png je Nanopolish, a konverzija bmp->jpg->png je Tombo.

Sve gore temelji se na pretpostavci da je nama u interesu dobiti k-torke poravnate sa signalima. U slucaju da nisam u pravu i da nam trebaju baze, imamo alat koji radi tocno to - Tombo. I Nanopolish i Tombo napravila je ista firma, oba su repozitorija priblizno jednako popularna i slicno aktivna. U svakom nam se slucaju slucaju citi logicnije tada uzeti onaj koji radi tocno ono sto zelimo, nego uzeti onaj koji radi nesto slicno i sami ga dovesti do kraja.

**Ukratko, vjerujemo da trebamo odustati od pitanja "Koji je bolji?" i koristiti onaj koji nam je potreban. Trebaju li nam poravnanja s bazama ili poravnanja s k-torkama?**

**Sto se tice projekta:**

Smatramo da nam fali sira slika o cijelom projektu. Ne vidimo poveznicu izmedu ovoga sad i detekcije modificiranih nukleotida.  Vjerujemo da je ovo dosta velik problem ta da bismo bili puno ucinkovitiji da smo svi 'na istoj stranici'. Bili bismo jako zahvalni kada bi netko tko je bolje informiran probao jednostavno objasniti planirani tijek rada. Recimo, kroz odgovore na sljedeca pitanja.
1. Sto tocno je nama cilj dobiti koristenjem Nanopolisha ili Tomba, odnosno, zelimo li poravnavati baze ili k-torke? Kao sto smo vec napomenuli, vjerujemo da bi ovo trebao biti najvazniji faktor u odluci o tome koji se alat koristi.
2. Cijelo vrijeme se govori o 'ekstrakciji podataka'. Koje podatke (format, njihov sadrzaj...) mi zelimo imati nakon uspjesne ekstrakcije i je li on drugaciji od trentuno definiranih?
3. Kako to sto cemo dobiti pomaze u konacnom cilju, detekciji modificiranih nukleotida?
4. Zasto je protobuf usao u racunicu. Argumenti su bili 'lakse koristenje iz raznih jezika'. Tko ce to koristiti osim nas i za sto tocno? Bez ovoga tesko mozemo odluciti sto treba izmijeniti u toj protobuf datoteci.


**Generalno:**
 - Zasto su reference nekad slozene u vise contiga i zasto su neki indeksi poslozeni. Ne implicira li pojam 'referenca' nesto potpuno i slozeno?
 - Koji je način na koji nanopolish dobiva brojeve između 80 i 100 ako su veličine zapisane u fast5 fileovima reda veličine 400 - 600? Ova konverzija nigdje nije objašnjena.


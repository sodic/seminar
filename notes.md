## Uvod

Nanoporeov base caller na koji se Nanopolish oslanja radi tako da:
1. Nekako je empirijski izgrađena tablica normalnih distribucija u kojima se kreće struja za svaku moguću k-torku. U našem je slučaju k-torka duljine 6. Prema tome, tablica ima 4096 redaka. Ova tablica naziva se *modelom*. Tablica po kojoj radi basecaller korištena u ovom procesu dostupna je ovdje: https://github.com/jts/nanopolish/blob/b9dc627e73816a415e4b96b14e8a8bf53622a6c9/etc/r9-models/r9.4_450bps.nucleotide.6mer.template.model (model koji tombo koristi: https://github.com/nanoporetech/tombo/blob/master/tombo/tombo_models/tombo.DNA.model)
2. Uzrokuje se struja i računaju parametri normalne distribucije
3. U tablici iz koraka 1. pronalazi se normalna distribucija koja najbolje odgovara onoj izračunatoj iz uzorka i zaključuje se da je riječ o odgovarajućoj k-torci.

### Zašto Nanopolish više puta očita istu k-torku?

Nanopolish "odluči" da je došlo do promjene k-torke unutar pore kada dođe do velikog skoka u signalu. Nekad su ti skokovi uzrokovani šumom, a ne stvarnom pojavom sljedeće k-torke. Nakon jednog takvog slučajnog skoka, signal se nastavi kretati u običajenim vrijednostima. Na taj se način više puta dobivaju vrlo slični podaci za istu k-torku.

## Nanopolish:

1. `contig` - Ime contiga koji je dio reference.
2. `position` - Pozicija u contigu (position i ime contiga zajedno jednoznačno određuju poziciju u referenci). Ako koja pozicija nedostaje, znači da taj dio reference nije uspješno poravnat niti s jednim dijelom signala.
3. `reference_kmer` - K-torka koja se nalazi na dotičnoj poziciji.
4. `read_index` - Indeks contiga čije je ime u prvom stupcu. Čini se da si Nanopolish odabere svoje indekse, nema previše veze s redoslijedom u datoteci.  Mislim da nam je ovo polje nevažno. Sve informacije koje nam trebaju sadržane su u imenu contiga (1) i poziciji (2).
5. `strand` - Trebao bi označavati strand, ali uvijek je `t`. Ipak, čini se da možemo utvrditi radi li se o komplementu uspoređujući `reference_kmer` i `model kmer`.
6. `event` - Indeks eventa (event je niza uzoraka u signalu), ide po redu.
7. `event_level_mean` - Očekivanje izračunato iz uzoraka koji pripadaju tome eventu.
8. `event_stdv` - Standardna devijacija izračunata iz uzoraka koji pripadaju tome eventu.
9. `event_length` - Vremenski interval u kojem su skupljeni svi uzorci za taj event.
10. `model_kmer` - K-torka modela, ona koju je basecaller callao na temelju sličnosti distribucija (ona iz gore spomenute tablice).
11. `model_mean` - Očekivanje distribucije za taj model (opet iz tablice).
12. `model_stdv` - Standardna devijacija distribucije za taj model (takoder iz tablice).
12. `standardized_level` - Računa se po formuli koju je Dario napisao na slack.
13. `start_index` - Indeks prvog uzorka sadržanog u eventu.
14. `end_index` - Indeks za jedan veći od posljednjeg uzorka sadržanog u eventu.
15. `samples` - Svi uzorci eventa.

## Tombo:
  - Podaci o eventu za jednu bazu koje Tombo vraća:
 	1. `norm_mean` - Normalizirana srednja vrijednost signala.
	2. `norm_stdev` - Normalizirana standardna devijacija signala.
	3. `start` - Index početka baze u signalu.
	4. `length` - Trajanje baze u signalu (`stdev` i `mean` se računaj s obzirom na signale između start i start + length).
	5. `base` - String koji predstavlja bazu.
	6. `digitisation`, `offset`, `range`- Parametri koje Tombo koristi za pretvorbu signala iz diskretnih u raw (veličine pA).
	7. `sampling_rate` - Broj baza u sekundi.
	8. `mapped_chrom` - Ime kontiga.
  
## Protobuff:
Fokusirali smo se na pretvorbu jednog formata outputa u drugi (više o tome kasnije), ali za sada nam se čini da bi zajednički event ovako izgledao:
```
{
	unit32 start_index    		//početna pozicija u sekvenci
	uint 32 end_index		//krajnja pozicija u sekvenci
	double mean 			// u pA
	double stdev		
	string base/kmer		//base ili kmer 
	repeated double samples
}
```
Uz to, Želimo li možda imati i datoteku koja izgleda ovako:
```
{
	nanopolish data: ...
	tombo data: ...
}
```


## Usporedba Nanopolisha i Tomba:
  - nakon što smo otkrili koja su značenja polja unutar nanopolisha, mogli smo zaključiti par stvari:
  	1. Nanopolishov `position` možemo poravnati s tombovim indexom baze
	2. `contig` je jednak kod oba alata.
	3. `event_level_mean`, `event_stdv`, `model_mean` - s ovim je bilo puno problema jer rade u potpuno različitim domenama. Na kraju smo uspjeli pronaći naćin da sve vrijednosti prebacimo u domenu pikoampera, ali podatke je još potrebno denormalizirati (to planiramo napraviti danas).
	4. `reference_kmer` i `model_kmer` možemo donekle jednostavno dobiti konkatenirajući baze tombo evenata, uz problem reverznog komplementa jer nam Tombo o njemu ne daje informaciju, odnosno, kod Nanopolisha nije potpuno jasno kada radi zamjenu između reverznog komplementa i običnog (možda se ovo može izvući iz imena contiga, ako pozicije baza na kraju imena idu od većeg prema manjem)
	5. `length` - donekle se poklapa, ali poklapnanje nije 100% točno, dolazi ponekad i do većih odstupanja.
	6. `standardized_level` - u Nanopolishu se racuna po formulama na Slacku, Tombo ga ne bilježi. Trebamo još razjasniti značenje te formule i njenu važnost.
	7. `read_index` je za Tombo uvijek 0 jer on ne podržava multiread fast5 datoteke
  - start index i end index ne mozemo usporediti jer Tombo gleda samo za kratko očitanje (signal)
  - moguće da Tombo gleda samo centralni nukelotid, a nanopolish to interpretira kao dolazak novog kmera (koji je isti i zapravo nije novi) dok tombo misli da je novi (drugi je u centru, ali je i dalje isti kmer unutra)
  - nakon prvog Nanopolishove lažne detekcije promjene k-torke, usporedbe za tu k-torku više nemaju smisla jer se svi podaci razlikuju.
  ### Zaključak usporedbe
Smatramo da je usporedba rezultata ova dva alata nije nesto sto nam može pomoci. Drugim riječima, možda je vrijeme da ponovno promislimo cijelu ideju. S obzirom ma to da je jedan napravljen da radi jedno, a drugi drugo, usporedba ce puno više reći o našem algoritmu preslikavanja, no što će reći o alatima. Čim preslikavanje nije trivijalno, ne vjerujem da se iz konačnih rezultata mogu izvući ikakvi relevantni zaključci. Kako ćemo odvojiti posljedice algoritama Tomba/Nanopolisha od posljedica našeg algoritma pretvorbe?

Pokušali smo brojne strategije preslikavanja baza u k-torke:
    - za event uzmemo u obzir samo prvu bazu kmera
    - kontinuirani output za evente
    - diskretni output za evente
    - trajanja evenata, počeci evenata, svakakve kombinacije

Ako je basecallanje rađeno s k-torkama, Tombo dobiva baze algoritmom pretvorbe nad k-torkama (koji je ireverzibilan i uzrokuje greške). Znamo da postupak mora početi od k-torki jer se u tablici modela za interpretaciju signala koriste k-torke, a ne baze. Mi bismo trebali svojim algoritmom (koji također neizbježno uzrokuje greške) vratiti podatke u oblik u kojem su bili prije no što je Tombo primijenjen. Čini nam se da je to analogno sa sljedećim postupkom:
1. Imamo dvije slike u .bmp formatu, ali ne možemo ga otvoriti na računalu.  Možemo otvarati samo .png
2. Jednu sliku konvertiramo u .png bez gubitaka, a drugu maksimalnim postavkama kompresije konvertiramo u .jpg (s gubitkom kvalitete), zatim izmislimo algoritam kojim ćemo je pretvoriti u .png te ga primijenimo.
3. Usporedimo dvije dobivene slike.

.bmp slike su ulazi u Tombo i Nanopolish, direktna konverzija u .png je Nanopolish, a konverzija bmp->jpg->png je Tombo.

Sve gore temelji se na pretpostavci da je nama u interesu dobiti k-torke poravnate sa signalima. U slučaju da nisam u pravu i da nam trebaju baze, imamo alat koji radi točno to - Tombo. I Nanopolish i Tombo napravila je ista firma, oba su repozitorija približno jednako popularna i slične aktivnosti. U svakom nam se slučaju čini logičnije tada uzeti onaj koji radi točno ono što želimo, nego uzeti onaj koji radi nešto slično i sami ga dovesti do kraja.

Ukratko, smatramo da nam usporedba alata neće puno koristiti. U svakom ćemo slučaju morati jedan format u drugi pretvarati s greškama (ktorke u nukleotide/nukleotide u ktorke) i zbog toga nećemo dobiti adekvatnu usporedbu.

**Bismo li možda trebali razmotriti mogućnost odustanka od pitanja "Koji je bolji?" i koristiti onaj koji nam je potreban. Trebaju li nam za naš krajnji cilj poravnanja signala s bazama ili poravnanja s k-torkama?**


**Što se tiče projekta:**

Smatramo da nam nedostaje šira slika o cijelom projektu. Ne vidimodovoljno jasnu poveznicu između ovoga što radimo sada i detekcije modificiranih nukleotida.  Vjerujemo da je nedostatak spomenutog konteskta velik problem te da bismo bili puno učinkovitiji da smo svi 'na istoj stranici'. Bili bismo jako zahvalni kada biste nam probali jednostavno objasniti planirani tijek rada. Recimo, kroz odgovore na sljedeća pitanja.
1. Sto točno je nama cilj dobiti korištenjem Nanopolisha ili Tomba, odnosno, želimo li sa signalima poravnavati baze ili k-torke? Kao što smo već napomenuli, vjerujemo da bi ovo trebao biti najvažniji faktor u odluci o tome koji se alat koristi.
2. Cijelo vrijeme se govori o 'ekstrakciji podataka'. Koje podatke (format, njihov sadržaj...) mi želimo imati nakon uspješne ekstrakcije?
3. Kako to što ćemo dobiti pomaže u konačnom cilju, detekciji modificiranih nukleotida?
4. Zašto je protobuf ušao u računicu. Argumenti su bili 'lakše korištenje iz raznih jezika'. Tko će to koristiti osim nas i za što točno? Bez definiranih zahtjeva teško možemo odlučiti što treba izmijeniti u toj protobuf datoteci, ako nam je ona uistinu potrebna (pod definirane zahtjeve ne ubrajamo tipove i ime svakog parametra, nego onaj kasniji viši cilj, na konceptualnoj razini).


**Generalno:**
 - Zašto su reference nekad složene u vise contiga i zašto su neki indeksi preskočeni. Ne implicira li pojam 'referenca' nešto potpuno i složeno?


# SAF-T-analyseverktøy for offline bruk
Denne web-applikasjonen (progressive web app, pwa) lar brukeren installere applikasjonen lokalt, og bruke den på lokale SAF-T-filer. På den måten får brukeren tilgang på Python og Python-bibliotek som pandas og matplotlib for analyse, av SAF-T-filer. Denne løsningen gir flere fordeler:

- Du kan analysere bokføringsdata i en SAF-T-fil, uten å dele dataene med noen andre
- Du kan utnytte Python-verktøy uten å måtte installere Python lokalt, noe du kanskje ikke heller har tillatelse til på datamaskinen du bruker
- Du får relativt sett raskere oppstart ved at alle filene som brukes for å kjøre Python i nettleseren, er lagret lokalt
- Du får tilgang til ferdige spørringer som kan være nyttige, f.eks. for ulike former for rapporteringskrav fra SSB
- Det er mulig å interagere mot andre nettsteder (http GET, http POST) fra applikasjonen, noe som kan åpne for å forenkle prosess med å hente SAF-T-fil fra regnskapssystem, og rapportere opplysninger

Koden er basert på John Hanleys artikler som viser [hvordan man kan bruke PyScript til å lage en Progressive Web App som kan installeres lokalt](https://www.jhanley.com/blog/pyscript-creating-installable-offline-applications/), og [hvordan man får tilgang til lokale filer](https://www.jhanley.com/blog/pyscript-files-and-file-systems-part-1/).
Øvrig kode er basert på eksempler fra Pyscript.net, bl.a. [Getting started with PyScript](https://docs.pyscript.net/latest/tutorials/getting-started.html).

## Todo
- DONE (delvis): Oppsett av webapplikasjonen for lokal installasjon (manifest.json m.m.). Status: Har på plass et minimum, men kan bruke Google Dev Tools Ligthouse til å forbedre det.
- DONE! Sørge for at alle filene som aksesseres er tilgjengelige lokalt, istedenfor å hentes over nettet fra pyscript.net
- DONE! Mulighet for å åpne lokal fil. MEN: det ser ut som ikke hele innholdet leses ... Noe som hindrer at hele fila blir lest? Ser ut som den er komplett, inneholder avslutningstag osv, men delen av fila med transaksjoner er mye kortere enn den opprinnelige filen. Merkelig. Har jeg samme fil ... ???? DUST!! Du har brukt to ulike filer ... det har virket hele tiden ... :)
- DONE! Lese lokal SAF-T-fil (eksempelfil fra Skattetatens github) inn i en pandas dataframe (basert på saft2dataframe)
- Legge til noen eksempler på spørringer som kan kjøres
- Strukturere koden mer hensiktsmessig
- Legge til en visualisering
- DONE! Mer ryddig og pen side (påbegynt)
- DONE! Publisere koden på Github
- DONE! Publisere webapplikasjonen, f.eks. via github pages
- gjøre saft2dataframe til en pakke som kan gjenbrukes i ulike prosjekter
- bruke Google Lighthouse til å forbedre web-applikasjonen, inkludert sikre at den fungerer på andre typer enheter som nettbrett og mobil
- flere eksempler på analyse
- DONE (delvis): finne måte å sende resultatet til en mottaker med ett klikk, f.eks. med et api-kall
- Tester!
- DONE! Endre til å be brukeren velge en fil som default, men ha Skatteetatens testfil som backup
- DONE! Endre slik at koden for å lese lokal fil kjøres automatisk, istedenfor at den må kjøres manuelt. MEN: Krever en uelegant global variabel. Kan vurdere å flytte filbehandlingskoden til main, kanskje?

## Kommunisere med andre nettsteder?
Det er mulig å gjøre API-kall, både GET, POST, PUT osv fra PyScript. Den vanligste pakken for dette i Python, requests, er ikke tilgjengelige, men det er [en egen oppskrift på PyScripts nettsider](https://docs.pyscript.net/latest/guides/http-requests.html) og fila ```request.py``` er kopiert fra den oppskriften.

Det åpner for å legge inn python-kode som både finner de relevante tallene fra SAF-T-fila, og deretter lar brukeren "POST"-e disse tallene til en rapporteringstjeneste, f.eks. Altinn. Litt usikker på hvordan det isåfall vil fungere med autentisering/autorisasjon, men antar at det vil være mulig å ha et API som tar imot verdiene, og deretter autoriserer brukeren, viser verdiene i et (delvis) forhåndsutfylt skjema, som brukeren til slutt sender inn.

Det kan kanskje også være mulig å ha python-kode som henter SAF-T-fila fra regnskapssystemet, avhengig av hva slags grensesnitt regnskapssystemene tilbyr. Det som trolig ikke vil være mulig er å gi mottakeren av rapporten noen form for sikkerhet for at de rapporterte tallene er hentet fra en SAF-T-fil, som ikke er endret på, eller med en spørring som ikke er endret på. Men for alle de tjenestene der en idag rapporterer manuelt, bør dette være mer enn godt nok som en start.

I nettsiden er det en liten demodel basert på PyScripts egen dokumentasjon, som viser ulike API-kall (GET, POST, PUT og DELETE) mot demo-API-et [https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com").

Ulike aktører kan kanskje lage sin versjon av web-applikasjonen, som krever innlogging, og da med mulighet til å sikre at det kan brukes API-nøkler eller andre mekanismer. F.eks. en versjon som lastes fra Altinn, kan ha noen signerte data om hvilken organisasjon det gjelder for. Det er antageligvis ikke nok til å erstatte autentiseringen, men til gjengjelde slipper API-ene være helt åpne. (Dette er egentlig rene gjetninger ...)

## Utviklingsmiljø
For å være sikker på at endringer blir reflektert i applikasjonen har jeg brukt en http-server som har no-cache-direktiver for alle filene. Koden for denne (NoCacheHTTPServer.py) [fant jeg på Stack Overflow](https://stackoverflow.com/a/62482117).

## Læringspunkter
Det er litt vanskelig å forutsi hvor resultatet av koden som kjører, blir vist. Hvis det brukes "print()" kommer resultatet til terminal-elementet (py-terimnal), men ellers kommer det rett etter der koden står, eller eventuelt i elementet jeg spesifiserer at det skal. Det er forsåvidt ryddig så lenge jeg bestemmer selv om jeg skal bruke print() eller ei. Men noen andre funksjoner, som f.eks. df.info() bruker også print (tydeligvis ...), mens df.describe() ikke gjør det.
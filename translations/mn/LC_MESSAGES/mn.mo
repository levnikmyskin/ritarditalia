��    !      $  /   ,      �  !   �       L   #  t   p  ,   �  F     3  Y     �  �   �    ,  �   >     +     J  6   W     �     �     �  6   �       �   /     �  L   �  a   "  9   �  :   �  <   �  >   6     u     �  ,  �  L   �       @  %  ^   f  :   �  @      q   A  �   �  d   8  �  �     G  �   T  )    2  B  ]   u     �  *   �  D      0   P   #   �   �   �      (!  �   C!     �!  k   �!  k   \"  L   �"  C   #  @   Y#  >   �#     �#  *   �#  e  $  j   s'     �'                               	                        
                              !                                                                          Aggiunto il treno, informazioni:
 C'è stato un errore :( C'è stato un errore e non è stato possibile aggiungere il treno dal pdf :( C'è stato un errore e non è stato possibile aggiungere il treno, controlla che il comando sia scritto corettamente C'è stato un errore nell'eliminare il treno Ci sono più treni per questo codice, indicami la stazione di partenza Ciao! Questo bot è in grado di tenerti informato/a sullo stato dei treni che scegli di monitorare. Puoi monitorare uno o più treni, per un solo giorno (oggi, domani ecc.) o tutti i giorni. Il bot controllerà fino a 4 ore prima della tua partenza se il treno presenta ritardo e, in caso,  ti avviserà :). Elimina treno Funzionamento:

		`/delete`

Questo comando ti permette di eliminare i treni che hai aggiunto. Puoi cliccare/toccare su un treno per eliminarlo. Funzionamento:

		`/monitora {codice_treno} {data|sempre|intervallo} {ora} (carrozza) (posto)`

Questo comando ti permette di aggiungere un treno e monitorare il suo ritardo fino a 4 ore prima della tua partenza.
Se usato da solo (senza aggiungere nulla) offre una procedura guidata.
Al momento, non è possibile cercare un treno, dovrai quindi averne il codice. Puoi usare il trattino `-` per specificare un intervallo di giorni, la virgola `,` per specificare i giorni singoli (es. mar-gio,sab,dom) Carrozza e posto sono opzionali!
Infine, ricorda che se hai un biglietto in PDF, puoi inviarlo al bot e verranno aggiunti i treni contenuti nel biglietto.
Per cominciare a monitorare un treno scrivi un messaggio come questo al bot:

		`/monitora 8626 03/03/2019 16:57`

Con questo aggiungi il treno 8626, specificando che parti il 3 marzo 2019 alle 16:57

		`/monitora 8626 sempre 16:57`

Con questo aggiungi il treno 8626, specificando che parti tutti i giorni alle 16:57

		`/monitora 8626 lun-mer,ven 16:57`

Con questo aggiungi il treno 8626, specificando che parti solo lunedì, martedì, mercoledì e venerdì alle 16:57

		`/monitora 8626 gio,ven,sab 16:57 4 11D`

Con questo aggiungi il treno 8626, specificando che parti solo giovedì, venerdì e sabato alle 16:57, carrozza 4, posto 11D Funzionamento:

		`/status`

Questo comando ti permette di vedere i treni che hai aggiunto. Puoi cliccare/toccare su un treno per vederne i ritardi (ammesso che il treno sia già partito). Se vuoi invece eliminare un treno,usa `/delete` Grazie per il tuo feedback! :) I tuoi treni Il formato della data inviata non è corretto, riprova Il treno è in orario! Il treno è in ritardo di {}! Il treno è in ritardo! Il treno è nel passato, non è possibile aggiungerlo! Il treno è stato eliminato! Inviami una data (es. 23/03/2019) o un intervallo di giorni.
Usa /ok per confermare l'intervallo, /stop per terminare la conversazione Lingua cambiata in italiano :D Lo stato del treno non sembra essere disponibile, forse deve ancora partire? Lo stato del tuo treno non è disponibile. Probabilmente c'è un errore nei servizi Trenitalia :( Non ho capito :/
Usa /stop per terminare la conversazione Non è stato possibile ottenere lo status del tuo treno :( Ok, dimmi cosa pensi del bot o se hai consigli a riguardo :) Ok, inviami il codice del treno oppure usa /stop per terminare Ok, mi fermo :D Ok, ora inviami l'orario Questo bot contiene diversi comandi possibili, puoi visualizzarli scrivendo `/`. Te ne mostro alcuni:
	1. /monitora {codice_treno} {sempre hh:mm OPPURE dd/mm/yyyy hh:mm OPPURE lun-mer,gio,ven}, puoi usarlo 	per monitorare un treno. Puoi inviare /monitora da solo per avere una procedura guidata.
Es. scrivi `/monitora 12855 sempre 3:06`.
	Altro es. /monitora 511 09/10/2019 3:06;
	O ancora /monitora 511 lun-mer,ven 16:20;
	2. Invia un biglietto in pdf al bot per aggiungerlo!	3. /english change the language to english;
	4. /italian cambia la lingua in italiano;
	5. /monello cambia lingua in una cazzona, è n po' volgare calcola;
	6. /help {comando} ottieni aiuto su un comando, es. /help monitora.
Se sei uno sviluppatore e vuoi contribuire, trovi il progetto qui https://github.com/levnikmyskin/ritarditalia Sembra esserci stato un errore da parte di Trenitalia : / riprova più tardi Status treno Project-Id-Version: PACKAGE VERSION
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-03-24 15:31+0100
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language-Team: LANGUAGE <LL@li.org>
Language: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 E sbim, aggiunto. Qualche dettaglio di cui non te frega un cazzo ma potresti almeno fa finta:
 Madonna non so che cazzo è successo, ma è morto tutto :( No zì che m'hai mandato? Non so riuscito a aggiunge il treno :( È andato tutto a puttane zì, hai sbagliato a scrive il comando eh? Madonna du comandi devi scrive, manco quello Eh niente, er treno non s'è eliminato. Quando c'è da sopprime sopprimono sempre, quando me tocca eliminà a me mai che funziona oh LOL calcola ce stanno più treni legati a sto codice (che monelli). Indicami la stazione di partenza Bella! Sto bot vuole tenerti aggiornato sullo stato dei treni che scegli de tenè sott'occhio. Ne puoi monitorà uno,duecento, quanti te pare calcola (nnèvvero a na certa me dovrai dà i soldi mortacci tua). Comunque, er bot spizza fino a 4 ore prima de quando credi che partirai pe capì ndo cazzo sta er treno tuo, che de sicuro se non sta in ritardo l'hanno soppresso; insomma in caso te avverte comunque, n te preoccupà Sbraga treno Funzionamento:

		`/delete`

Oh, sto comando è er mio preferito, sbraghi i treni che hai aggiunto co na goduria immensa, secondo me ogni tanto è bello aggiunge un treno solo per eliminarlo dopo Funzionamento:

		`/monitora {codice_treno} {data|sempre|intervallo} {ora} (carrozza) (posto)`

Co sto comando aggiungi un treno così che er bot t'avverte prima se sta in ritardo (er treno, no il bot). Alla fine a smadonnà smadonnerai comunque, ma per lo meno cominci a farlo 4 ore prima. Se te pesa er culo de invià tutti i parametri, usa /monitora da solo per una procedura guidata.
Puoi usare il trattino `-` per specificare un intervallo di giorni, la virgola `,` per specificare i giorni singoli (es. mar-gio,sab,dom) Carrozza e posto so opzionali!
Poi comunque se te pesa er culo puoi inviare il biglietto in PDF e i treni verranno aggiunti da soli.
Per partire verso questo viaggio incredibile, scrivi na cosa del genere:

		`/monitora 8626 03/03/2019 16:57`

Co questo aggiungi il treno 8626, specificando che te piacerebbe partì il 3 marzo 2019 alle 16:57 (e invece...)

		`/monitora 8626 sempre 16:57`

Co questo aggiungi il treno 8626, specificando che parti tutti i giorni alle 16:57

		`/monitora 8626 lun-mer,ven 16:57`

Co questo aggiungi il treno 8626, specificando che parti solo lunedì, martedì, mercoledì e venerdì alle 16:57

		`/monitora 8626 gio,ven,sab 16:57 4 11D`

Co questo aggiungi il treno 8626, specificando che parti solo giovedì, venerdì e sabato alle 16:57, carrozza 4, posto 11D Funzionamento:

		`/status`

Co sto comando vedi i treni che hai aggiunto, nel caso te fossi un po' rincojonito e non te ricordi più. Non solo, se ce clicchi o ce tocchi ;) vedi pure ando sta e se c'ha ritardo, a meno che er treno non è ancora partito e me sa che a quel punto non è lui che c'ha ritardo Daje grande! (tranne nel caso in cui m'hai mandato parolacce, in quel caso te reporto subito) Li treni tua A zì ma che data hai scritto? Dai riprova Oh zì er treno è in orario, potrebbe esse pure in anticipo calcola Mannaggia la troia, il treno è in ritardo di {} Oh indovina? Il treno è in ritardo Oh ma il treno è nel passato, la macchina del tempo ancora non ce l'avemo (quella pe i salti temporali non arriva così indietro) Sbragato er treno, sbimme! Le cose so due: o me mandi una data (23/03/2019) o clicchi sui pulsantini, vedi un po' te.
Usa /ok per confermare l'intervallo, /stop per terminare la conversazione Eddaje! Eh vbb, lo stato del treno non è disponibile, nnè che deve ancora partì? Ma che ansia c'hai cristo santo E niente, lo stato del treno non è disponibile. Me sa che pure oggi i servizi Trenitalia funzionano domani Non c'ho capito un cazzo calcola :/
Usa /stop per terminare la conversazione No zì calcola lo status del treno non c'è. Se famo na briscolata? Vai, dimme tutto. Oh se me scrivi le parolacce chiamo la polizia Vai, mandame il codice treno oppure usa /stop per fermà tutto M'aresto Vai, inviami l'orario che sto carichissimo Er bot contiene na cifra de comandi (manco troppi, ma comunque fa figo dillo). Se scrivi `/` li vedi, ma intanto beccate questi zì:
	1. /monitora {codice_treno} {sempre hh:mm OPPURE dd/mm/yyyy hh:mm}, co questo tieni sott'occhio er treno. Invia /monitora da solo per avere una procedura guidata.
Es. scrivi `/monitora 12855 sempre 3:06`.
	Altro es. /monitora 511 09/10/2019 3:06. Oh calcola che 3 e 06 è l'ora in cui devi partì te eh;
	O ancora /monitora 511 lun-mer,ven 16:20;
	2. /english change the language to english;
	3. /italian cambia la lingua in italiano;
	4. /monello cambia lingua in una cazzona, è n po' volgare calcola;
	5. /help {comando} te do na mano a capì i comandi;
Se te piace programmà e hai deciso che è ora de smette de vedè i campionati koreani de beer pong, puoi contribuire al progetto qui https://github.com/levnikmyskin/ritarditalia Eh calcola non se sa che è successo dalle parti di Trenitalia, qualcosa non è andato. Riprova più tardi A che punto sta er treno 
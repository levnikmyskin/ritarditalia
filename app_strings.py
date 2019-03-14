# -*- coding: utf-8 -*-

# Dummy functions which we need to allow
# xgettext to recognize the strings
def N_(string): return string


start_message = N_("Ciao! Questo bot è in grado di tenerti informato/a sullo stato dei treni che scegli di monitorare."
                   " Puoi monitorare uno o più treni, per un solo giorno (oggi, domani ecc.) o tutti i giorni."
                   " Il bot controllerà fino a 4 ore prima della tua partenza se il treno presenta ritardo e, in caso, "
                   " ti avviserà :).")
command_message = N_("Questo bot contiene diversi comandi possibili, puoi visualizzarli scrivendo "
                     "`/`. Te ne mostro alcuni:\n"
                     "\t1. /monitora {codice_treno} {sempre hh:mm OPPURE dd/mm/yyyy hh:mm}, puoi usarlo "
                     "\tper monitorare un treno.Es. scrivi `/monitora 12855 sempre 3:06`.\n"
                     "\tAltro es. /monitora 511 09/10/2019 3:06;\n"
                     "\t2. /english change the language to english;\n"
                     "\t3. /italian cambia la lingua in italiano;\n"
                     "\t4. /monello cambia lingua in una cazzona, è n po' volgare calcola;\n"
                     "\t5. /help {comando} ottieni aiuto su un comando, es. /help monitora.\n"
                     "Se sei uno sviluppatore e vuoi contribuire, trovi il progetto qui "
                     "https://github.com/levnikmyskin/ritarditalia")


language_switched = N_("Lingua cambiata in italiano :D")

added_train = N_("Aggiunto il treno, informazioni:\n")

error_adding_train = N_("C'è stato un errore e non è stato possibile aggiungere il treno, controlla che il comando"
                        " sia scritto corettamente")
error_deleting_train = N_("C'è stato un errore nell'eliminare il treno")

error_status_train = N_("Non è stato possibile ottenere lo status del tuo treno :(")

train = N_("Treno")
your_trains_status = N_("Status treno")
your_trains_deleting = N_("Elimina treno")
train_status_not_available = N_("Lo stato del treno non sembra essere disponibile, forse deve ancora partire?")
train_deleted = N_("Il treno è stato eliminato!")

train_delayed = N_("Il treno è in ritardo di {} minuti!")
train_on_time = N_("Il treno è in orario!")

monitor_help = N_("Funzionamento:\n\n\t\t`/monitora {codice_treno} {data|sempre} {ora}`\n"
                  "Questo comando ti permette di aggiungere un treno e monitorare il suo ritardo fino a 4 ore prima "
                  "della tua partenza.\nAl momento, non è possibile cercare un treno, dovrai quindi averne il codice. "
                  "Per cominciare a monitorare un treno scrivi un messaggio come questo al bot:\n\n"
                  "\t\t`/monitora 8626 03/03/2019 16:57`\n\n"
                  "Con questo aggiungi il treno 8626, specificando che parti il 3 marzo 2019 alle 16:57\n\n"
                  "\t\t`/monitora 8626 sempre 16:57\n\n"
                  "Con questo aggiungi il treno 8626, specificando che parti tutti i giorni alle 16:57")

status_help = N_("Funzionamento:\n\n\t\t`/status`\n"
                 "Questo comando ti permette di vedere i treni che hai aggiunto. Puoi cliccare/toccare su un treno "
                 "per vederne i ritardi (ammesso che il treno sia già partito). Se vuoi invece eliminare un treno,"
                 "usa `/delete`")

delete_help = N_("Funzionamento:\n\n\t\t`/delete`\n"
                 "Questo comando ti permette di eliminare i treni che hai aggiunto. Puoi cliccare/toccare su un treno "
                 "per eliminarlo.")

italian_help = N_("Funzionamento:\n\n\t\t`/italian`\n"
                  "Cambia la lingua in italiano")

monello_help = N_("Funzionamento:\n\n\t\t`/monello`\n"
                  ";) Per viaggi mai banali, per treni che non devono chiedere mai, per ritardi oltre ogni aspettativa")

english_help = N_("The english language is not available yet :(")
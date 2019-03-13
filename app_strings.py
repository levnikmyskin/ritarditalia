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
"1. /monitora {codice_treno} {sempre hh:mm OPPURE dd/mm/yyyy hh:mm}, puoi usarlo "
"per monitorare un treno.Es. scrivi `/monitora 12855 sempre 3:06`.\n"
"Altro es. /monitora 511 09/10/2019 3:06;\n"
"2. /english change the language to english;\n"
"2. /italian cambia la lingua in italiano;\n"
"3. /monello cambia lingua in una cazzona, è n po' volgare calcola;\n")


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

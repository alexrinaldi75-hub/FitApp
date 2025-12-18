Si intende sviluppare un prototipo di software gestionale per centri fitness che consenta di amministrare utenti, schede di allenamento e monitoraggio delle performance.
L'obiettivo è costruire un'applicazione Python a riga di comando (CLI) basata sul paradigma della programmazione a oggetti (OOP), supportata da un database documentale MongoDB.

Il sistema deve simulare il flusso operativo di una palestra: i trainer creano le schede, gli atleti registrano le sessioni di allenamento e il sistema storicizza i dati. Successivamente, i dati raccolti vengono elaborati in un ambiente separato per analisi di Data Science.
Architettura Logica

- Livello Applicativo – Python CLI & OOP
        È il cuore del sistema operativo. Un'applicazione Python stand-alone che gestisce la logica di business, l'autenticazione degli utenti e l'interazione tramite terminale. Il codice è strutturato secondo il paradigma OOP per rappresentare le entità del dominio (Utenti, Esercizi, Schede, Sessioni).
- Livello di Persistenza – Database documentale MongoDB
      Memorizzazione centrale di tutte le informazioni. Funge da "Single Source of Truth" per l'applicazione CLI e garantisce la persistenza dei log di allenamento e delle configurazioni utente. I dati sono organizzati in collezioni flessibili.
- Livello Analitico – Jupyter Notebook
      Ambiente disaccoppiato dall'applicazione principale. Si connette al database MongoDB in sola lettura per estrarre i dati storicizzati, effettuare analisi statistiche e generare visualizzazioni grafiche (Pandas, Matplotlib/Seaborn).

Obiettivi Principali

    - Importare un catalogo iniziale di dati tramite fixture (file JSON).
    - Gestire l'accesso sicuro tramite autenticazione con password hashata.
    - Offrire un'interfaccia a riga di comando (CLI) navigabile per diverse tipologie di utente (Trainer e Atleti).
    - Permettere la creazione e l'assegnazione di schede di allenamento.
    - Registrare i risultati delle sessioni di allenamento (logbook).
    - Produrre un report analitico su Jupyter Notebook basato sui dati raccolti.


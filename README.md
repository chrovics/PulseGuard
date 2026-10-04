🛡️️ PulseGuard: Uptime & SSL Monitor

Un micro-serviciu complet pentru monitorizarea disponibilității web și a validității certificatelor SSL. Construit cu o arhitectură decuplată, proiectul rulează într-un mediu complet izolat prin containere și este expus printr-un reverse proxy securizat pe un server Linux.
⚙️ Arhitectură & Tehnologii

    Backend: Python, FastAPI, SQLAlchemy (operare asincronă cu asyncpg).

    Bază de date: PostgreSQL (containerizat cu persistență pe volume locale).

    Frontend: Interfață web responsivă cu Tailwind CSS și vizualizare de date prin Chart.js.

    Infrastructură: Docker & Docker Compose pentru orchestrarea serviciilor.

    Rețelistică & Securitate: Nginx configurat ca Reverse Proxy, UFW (Uncomplicated Firewall) pentru restricționarea traficului strict pe porturile esențiale (22, 80, 443).

🚀 Funcționalități Cheie

    Monitorizare activă (ping) a endpoint-urilor la intervale configurabile de utilizator.

    Verificare automată a datei de expirare pentru certificatele SSL.

    Alerte în timp real via Telegram Bot la detectarea downtime-ului sau a expirării SSL.

    Dashboard vizual pentru urmărirea latenței și a istoricului de uptime.

🧠 Provocări Tehnice Rezolvate

    Izolare și Rețelistică: Am gestionat comunicarea internă între containere în rețeaua Docker și am rutat traficul extern către serviciul intern folosind Nginx, remediind blocajele CORS la nivel de client prin implementarea rutelor relative.

    Securizarea Sistemului: Am aplicat reguli stricte de firewall (UFW) pe serverul gazdă pentru a bloca expunerea accidentală a porturilor interne ale bazei de date către exterior.

    Gestionarea Bazelor de Date în Producție: Am inițializat schema bazei de date injectând direct scripturi SQL via CLI în containerul PostgreSQL activ, fără a deschide conexiuni externe vulnerabile.

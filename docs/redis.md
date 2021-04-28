# Redis

Redis ist eine NoSQL Datenbank. Das bedeutet, dass keine komplexe Verknüpfung der Daten möglich ist, wie in
MySQL oder PostgreSQL. Redis läuft im Arbeitsspeicher des Servers und wird vor allem wegen der Geschwindigkeit
beim Schreiben und Lesen genutzt. Im Grunde werden nur zwei Spalten der gleichen, sehr "langen" Datentabelle genutzt,
`key` und `value` (key-value store).

In Schiller-Online wird Redis benutzt, um die Daten der User-Sessions zu verwalten. Der User identifiziert sich mit
einem Cookie (Flask, `session['token']`), der serverseitig die Session zuordenbar macht.

## Links
[Redis Linksammlung](https://www.fullstackpython.com/redis.html)
[Redis auf Uberspace installieren](https://lab.uberspace.de/guide_redis.html)
[Redis Security](https://redis.io/topics/security)

## Modelle
Schiller-Online nutzt die Datentypen HASH (entspricht `dict`) für "session" und "raster" sowie SET (entspricht `set`)
für den Abgleich der möglichen Prüfungsfächer.

### Server Session (HASH)
Serverseitige Speicherung der User-Session. Der Name des `HASH field` setzt sich zusammen aus `'session:' + token`:

```
session:0azRqv = {
                    "vorname":          "Andi",
                    "nachname":         "Gewehre",
                    "jahrgang":         "20",
                    "klasse":           "a",
                    "profilbuchstabe":  "A",
                    "freierlk":         "eng",
                    "msa":              "True",
                    "pflichstundenzahl": "124",
                 }
```

### Raster (HASH)
Das sog. Raster ergibt sich aus dem gewünschten Output, der Ü-Plan Tabelle. Da Redis kein verschachteltes `dict`
zulässt, wird jedes Oberstufenhalbjahr von E-Phase 1.1 (e11) bis Q-Phase 2.2 (q22) als eigener HASH abgelegt, mit
`'halbjahr:token'` zur Zuordnung. Eine Zusammenführung einzelnen HASHes erfolgt erst am Ende zur Generierung
der PDF/Excel-Datei.

```
 not in redis |    hash field   |  hash key  |  hash value
--------------|-----------------|------------|--------------
              |                 |            |               
  raster = {  |                 |            | 
              | "e11:0azRqv": { |            |
              |                 |   "deu":   |      4, 
              |                 |   "eng":   |      4,
              |                 |   "mat":   |      4, ...
              |               },|            |
              | "e12:0azRqv": { |    ...     |     ... },
              | "q11:0azRqv": { |    ...     |     ... },
              | "q12:0azRqv": { |    ...     |     ... },
              | "q21:0azRqv": { |    ...     |     ... },
              | "q22:0azRqv": { |    ...     |     ... },
           }  |                 |            |
              |                 |            |
```


### Prüfungsfächer (SET)
Die Prüfungsfächer ergeben sich für jeden User aus Profil- und freiem LK:
```
pruefungsfaecher:0azRqv = {"deu", "eng"}
```
Zum Abgleich wird noch zweites SET mit allen möglichen Prüfungsfächern für jeden User angelegt:
```
possiblepruefung:0azRqv = {"eng", "kun", "mat", "ges", "deu"}
```

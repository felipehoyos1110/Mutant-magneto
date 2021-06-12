# MAGNETO - Reclutación Mutantes

### Ejecución API REST

Para detectar si un humano es mutante se debe consumir el servicio `POST /mutant/`
enviando el siguiente JSON con la cadena de dna: 
```
{
"dna":["ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"]
}
```

Para consultar las estadisticas de las verificaciones de ADN se debe consumir el servicio `GET /stats/` 
se recibe el siguiente JSON
```
{
    "count_mutant_dna": 7,
    "count_human_dna": 8,
    "ratio": "0.88"
}
```

### Explicación cadena ADN

El API `POST /mutant/` recibira como parámetro un array de Strings que representan cada fila de una tabla
de (NxN) con la secuencia del ADN. Las letras de los Strings solo pueden ser: (A,T,C,G), las
cuales representa cada base nitrogenada del ADN.
```
String[] dna = {"ATGCGA","CAGTGC","TTATGT","AGAAGG","CCCCTA","TCACTG"};
```
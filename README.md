# formula-info

néhány információ egy logikai formuláról.

## célok

- [x] sztringről megállapítani, hogy formula-e
- [x] szerkezeti fa tárolása (bináris fában):
    - [x] később visszaadni inorder alakban
    - [x] visszadni TeXben
- [x] logikai összetettség (nem a mélység!)
- [x] összes részformulája (C++: set `.insert(...)`)
- [x] zárójelek elhagyása

## használat

```
./formula.py < in
```

vagy

```
./formula.py --tex < in
```

(szebb kimenetért)

## példa kimenet

[👉 out.pdf](./out.pdf)

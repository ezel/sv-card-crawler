# sv-card-crawler
a simple crawler for [shadowverse-portal](https://shadowverse-portal.com/)

## Quick start:
recommend in virtualenv
```bash
> pip install -r requirement.txt
> python main.py 1 en
```
this will generate a cards.db file for sqlite3

## Usage
```bash
> python main.py -h
```

```cmd
usage: main.py [-h] [-w MAXWORKERS] [-f] {1,3} {en,ja,zh-tw}

positional arguments:
  {1,3}                 game mode of the card: 1=Rotation, 3=Unlimit
  {en,ja,zh-tw}         card language: en=english, ja=janpanse, zh-tw=traditional chinese

optional arguments:
  -h, --help            show this help message and exit
  -w MAXWORKERS, --maxWorkers MAXWORKERS
                        the max concurrent workers when downling images
  -f, --forceFetch      wheather fetch from web or use local temp file

```

## Generated card schema
```sql
CREATE TABLE IF NOT EXISTS "card" ("id" INTEGER NOT NULL PRIMARY KEY, "cid" VARCHAR(255) NOT NULL, "language" VARCHAR(255) NOT NULL, "title" VARCHAR(255) NOT NULL, "imageURL1" VARCHAR(255) NOT NULL, "imageURL2" VARCHAR(255), "imageLink1" VARCHAR(255), "imageLink2" VARCHAR(255), "Atk1" INTEGER, "HP1" INTEGER, "Atk2" INTEGER, "HP2" INTEGER, "minCost" INTEGER, "skill1" TEXT NOT NULL, "skill2" TEXT, "desp1" TEXT NOT NULL, "desp2" TEXT, "traitInfo" VARCHAR(255) NOT NULL, "classInfo" VARCHAR(255) NOT NULL, "rarityInfo" VARCHAR(255) NOT NULL, "createInfo" INTEGER NOT NULL, "liquefyInfo" VARCHAR(255) NOT NULL, "cardPackInfo" VARCHAR(255) NOT NULL, "mainCard_id" INTEGER, FOREIGN KEY ("mainCard_id") REFERENCES "card" ("id"));
```


## TODO

* ~~a gui to view card [maybe in a new project]~~
* a better UX usage
* compress/resize images
* store images in database
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
usage: main.py [-h] [-w MAXWORKERS] [-f] [-s {1,2}] {1,3} {en,ja,zh-tw}

positional arguments:
  {1,3}                 game mode: 1=Rotation, 3=Unlimit, default=1
  {en,ja,zh-tw}         card language: default=zh-tw

optional arguments:
  -h, --help            show this help message and exit
  -w MAXWORKERS, --maxWorkers MAXWORKERS
                        the max concurrent workers when downling images, default=20
  -f, --forceFetch      if set, always fetch the whole list from web
  -s {1,2}, --save {1,2}
                        save images in: 1=database, 2=file in a directory, default=1
```




## TODO

* ~~a gui to view card~~ [will in a new project]
* ~~compress/resize images~~ [abandon]
* ~~store images in database~~
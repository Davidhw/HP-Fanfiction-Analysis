#!/bin/sh
scrapy startproject hpfanfic;
mv items.py $PWD/test/hpfanfic/spiders;
mv spider1.py $PWD/hpfanfic/hpfanfic/spiders;

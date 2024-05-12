# python-dlshogi2

This is a fork of https://github.com/TadaoYamaoka/python-dlshogi2.

## Environmental setup

```
pip install -r requirements.txt
```

## Data download

- Download 7z files from http://wdoor.c.u-tokyo.ac.jp/shogi/x/
- Extract them

## Preprocessing

- Convert csa files to train and test hcpe files

```
python3 scripts/csa_to_hcpe.py --csa-dir /path/to/csa/files/dir --hcpe-train /path/to/save/hcpe/train/file.hcpe --hcpe-test /path/to/save/hcpe/test/file.hcpe
```

## Training

```
python3 scripts/train.py --train-data /path/to/train.hcpe --test-data /path/to/test.hcpe
```

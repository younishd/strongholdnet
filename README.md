# StrongholdNet

1. Download raw stronghold data from [here](https://drive.google.com/file/d/1N3TjOB29kHpysWrq7yHVjB-v2g5IMgdV/view?usp=sharing).

2. Clone this repository:

```
git clone https://github.com/younishd/strongholdnet.git
```

3. Install dependencies etc.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Generate the sequential dataset:

```
python dataset_rnn.py 100k_strongholds.txt > 100k_dataset_rnn.csv
```

5. Run JupyterLab and open the notebook: `stronghold_rnn.ipynb`

```
jupyter lab
```

6. ???

7. Debug

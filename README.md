# StrongholdNet

## Usage

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

## Models

| model | brief | "evaluation" |
| :------------- | :------------- | - |
| `rnn_2` | LSTM trained on portal path data | - kinda good<br>- better than simple classifier<br>- has not learned being wrong is a thing |
| `rnn_4` | LSTM trained on portal and library path data | - overall worse than `rnn_2`<br>- somewhat more aware of backtracking
| `rnn_7` | LSTM trained on portal path data + `entry` feature | - a better `rnn_2` |
| `rnn_8` | LSTM based on `rnn_7` and briefly trained on its own navigation | - a promising failure |
| `rnn_9` | LSTM (2 layers) trained on the same data as `rnn_7` | - will be used as a base model for further training |
| `rnn_10` | LSTM (2 layers) based on `rnn_9` | - trained on its own navigation<br>- approx. 18k strongholds |

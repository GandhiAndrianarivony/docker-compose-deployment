from utils.data_validation import validate
from models.schema import EisaModel
from utils.pnud_preprocessing import age, job, election
import pandas as pd


def column_tfsm(df):
    if 'anarana_fanilo' in df.columns:
        df['anarana_fanilo'] = df['anarana_fanilo'].map(
            lambda x: [v for l in x for _, v in l.items()])

    df = pd.DataFrame(validate(df.to_dict('records'), EisaModel))
    df['nisoratra_anaty_lisitra'] = df['nisoratra_anaty_lisitra'].map(
        lambda x: "Eny" if x == "1" else "Tsia")
    df['efa_nifidy'] = df['efa_nifidy'].map(lambda x: election(x))
    df['taona'] = df['taona'].map(lambda x: age(x))
    df['asa'] = df['asa'].map(lambda x: job(x))
    return df

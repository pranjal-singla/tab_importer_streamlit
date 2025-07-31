import pandas as pd
from .utils import normalize_gender

def process_file(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df['You are filling this form as'] = df['You are filling this form as'].str.strip().str.lower()

    # Institutions
    institutions_1 = df['Institution'].dropna().astype(str)
    institutions_2 = df['Team Institution'].dropna().astype(str)
    all_institutions = pd.Series(list(set(institutions_1).union(set(institutions_2))))
    institutions_df = pd.DataFrame({'Long': all_institutions, 'Short': all_institutions})

    # Judges
    judges_df = df[df['You are filling this form as'] == 'judge'].copy()
    judges_output = pd.DataFrame({
        'Institution': judges_df['Institution'].astype(str),
        'Short': judges_df['Institution'].astype(str),
        'Name': judges_df['Name'].astype(str),
        'Score': 0,
        'Email': judges_df['Email ID'].astype(str),
        'Number': judges_df['Contact Details'].astype(str),
        'Gender': judges_df["Gender"].apply(normalize_gender)
    })

    # Teams
    teams_df = df[df['You are filling this form as'] == 'team'].copy()
    teams_df['Is Speaker 1 novice?'] = teams_df['Is Speaker 1 novice?'].fillna('').astype(str).str.lower()
    teams_df['Is Speaker 2 novice?'] = teams_df['Is Speaker 2 novice?'].fillna('').astype(str).str.lower()

    teams_df['C1'] = teams_df['Is Speaker 1 novice?'].apply(lambda x: 'open, novice' if x == 'yes' else 'open')
    teams_df['C2'] = teams_df['Is Speaker 2 novice?'].apply(lambda x: 'open, novice' if x == 'yes' else 'open')
    teams_df['break_category'] = teams_df.apply(
        lambda row: 'open, novice' if row['Is Speaker 1 novice?'] == 'yes' and row['Is Speaker 2 novice?'] == 'yes' else 'open',
        axis=1
    )

    teams_output = pd.DataFrame({
        'Code': teams_df['Team Institution'].astype(str),
        'Team': teams_df['Team Name'].astype(str),
        'S1': teams_df['Name of Speaker 1'].astype(str),
        'E1': teams_df['Email ID of Speaker 1'].astype(str),
        'P1': teams_df['Contact Details of Speaker 1'].astype(str),
        'G1': teams_df['Gender of Speaker 1'].apply(normalize_gender),
        'S2': teams_df['Name of Speaker 2'].astype(str),
        'E2': teams_df['Email ID of Speaker 2'].astype(str),
        'P2': teams_df['Contact Details of Speaker 2'].astype(str),
        'G2': teams_df['Gender of Speaker 2'].apply(normalize_gender),
        'C1': teams_df['C1'],
        'C2': teams_df['C2'],
        'break_category': teams_df['break_category']
    })

    return institutions_df, judges_output, teams_output

import requests
import streamlit as st

def post_to_api(institutions, judges, teams, token, site, slug):
    errors = []
    headers = {'Authorization': f'token {token}'}

    inst_map = {
        inst['code']: inst['url']
        for inst in requests.get(f'{site}api/v1/institutions', headers=headers).json()
    }

    st.write("Posting institutions...")
    for _, row in institutions.iterrows():
        if row['Short'] in inst_map:
            continue
        r = requests.post(
            f'{site}api/v1/institutions',
            json={"name": row['Long'], "code": row['Short']},
            headers=headers
        )
        if r.status_code == 201:
            inst_map[row['Short']] = r.json()['url']
        else:
            errors.append(f"Institution error: {row['Long']} — {r.text}")
    st.success("Institutions processed!")

    judge_emails = {
        j['email'].lower()
        for j in requests.get(f'{site}api/v1/tournaments/{slug}/adjudicators', headers=headers).json()
        if j.get('email')
    }

    st.write("Posting judges...")
    for _, row in judges.iterrows():
        if row['Email'].lower() in judge_emails:
            continue
        inst_url = inst_map.get(row['Short'])
        r = requests.post(
            f'{site}api/v1/tournaments/{slug}/adjudicators',
            json={
                "name": row['Name'],
                "email": row['Email'],
                "anonymous": False,
                "institution": inst_url,
                "base_score": float(row['Score']),
                "breaking": False,
                "trainee": False,
                "independent": False,
                "adj_core": False,
                "institution_conflicts": [],
                "team_conflicts": [],
                "adjudicator_conflicts": [],
                "gender": row['Gender']
            },
            headers=headers
        )
        if r.status_code != 201:
            errors.append(f"Judge error: {row['Name']} — {r.text}")
    st.success("Judges processed!")

    team_refs = {
        t['reference'].lower()
        for t in requests.get(f'{site}api/v1/tournaments/{slug}/teams', headers=headers).json()
    }

    st.write("Posting teams...")
    for _, row in teams.iterrows():
        if row['Team'].lower() in team_refs:
            continue
        inst_url = inst_map.get(row['Code'])
        team_json = {
            "reference": row['Team'],
            "short_reference": row['Team'],
            "institution": inst_url,
            "speakers": [
                {"name": row["S1"], "email": row["E1"], "phone": row["P1"], "gender": row["G1"],
                 "anonymous": False, "pronoun": "", "categories": [], "url_key": ""},
                {"name": row["S2"], "email": row["E2"], "phone": row["P2"], "gender": row["G2"],
                 "anonymous": False, "pronoun": "", "categories": [], "url_key": ""}
            ],
            "use_institution_prefix": False,
            "break_categories": [],
            "institution_conflicts": []
        }
        r = requests.post(f'{site}api/v1/tournaments/{slug}/teams', json=team_json, headers=headers)
        if r.status_code != 201:
            errors.append(f"Team error: {row['Team']} — {r.text}")
    st.success("Teams processed!")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("✅ All data posted successfully!")

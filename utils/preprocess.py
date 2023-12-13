import pandas as pd
from pathlib import Path
from anonymizedf.anonymizedf import anonymize


def load_data(df):
    data = pd.read_csv(df, sep=";")
    mask = data["hôtel"].notna()
    data = data[mask]
    data["date_debut"] = data.apply(lambda x: x["date"].split(" →")[0], axis=1)
    data["date_debut"] = data["date_debut"].apply(lambda x: x.split(" (")[0])
    # data["date_debut"] = data["date_debut"].apply(lambda x: x.replace(" (UTC)", ""))
    data["date_debut"] = pd.to_datetime(data["date_debut"], format="%d/%m/%Y %H:%M")
    data["time_delta"] = data["nbre d'heures"].apply(lambda x: pd.to_timedelta(x))
    data["date_fin"] = data.apply(lambda x: x["date_debut"] + x["time_delta"], axis=1)
    data["Propriété"] = data["hôtel"].apply(lambda x: x.split(" (")[0])
    data["extra_clean"] = data["extra"].apply(lambda x: x.split(" (")[0])
    data["Année"] = data["date_fin"].dt.year.astype(str)
    data["Mois"] = data["date_fin"].dt.to_period("M").astype(str)
    data["Semaine"] = data["date_fin"].dt.to_period("W-Mon").astype(str)
    data["marge"] = data.apply(lambda x: x["total HT"] - x["montant HT"], axis=1)
    data["Jour"] = data["date_fin"].dt.to_period("D").astype(str)
    data["statuts"] = data["statuts"].fillna("standard")
    data["date_fin"] = pd.to_datetime(data["date_fin"])
    data["mois"] = data["date_fin"].dt.strftime("%B")
    data["mois"] = pd.Categorical(
        data["mois"],
        categories=[
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ],
        ordered=True,
    )

    # ## Commenter les lignes ci dessous pour ne pas anonymiser
    # an = anonymize(data)
    # an.fake_names("extra_clean")
    # an.fake_categories("Propriété")
    # an.fake_whole_numbers("total HT")
    # an.fake_whole_numbers("montant HT")
    # data["total HT"] = data["Fake_total HT"]
    # data["montant HT"] = data["Fake_montant HT"]
    # data["Propriété"] = data["Fake_Propriété"]
    # data["extra_clean"] = data["Fake_extra_clean"]
    # data.drop(
    #     ["Fake_Propriété", "Fake_extra_clean", "Fake_total HT", "Fake_montant HT"],
    #     axis=1,
    # )
    # data_sample = data.sample(1500)
    # data = pd.concat([data, data_sample])

    ## Write csv
    my_file = Path("./missions_processed.csv")

    data.to_csv("missions_processed.csv")

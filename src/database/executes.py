from utils.consts import cursor, db

from .exists import (
    deputy_exists,
    party_exists,
    sitting_exists,
    vote_exists,
    voting_exists,
)
from .inserts import (
    insert_deputy,
    insert_parties,
    insert_sittings,
    insert_vote,
    insert_voting,
)


def execute_parties(parties):
    print("Importing parties to the database...")
    for party in parties:
        if party_exists(cursor, party):
            pass
        else:
            insert_parties(cursor, party)
    print("Parties added to the database")
    db.commit()


def execute_deputies(deputies_dataframe):
    print("Importing deputies to the database...")
    for index, row in deputies_dataframe.iterrows():
        if deputy_exists(cursor, row["id"]):
            pass
        else:
            insert_deputy(cursor, row["id"], row["imie"], row["nazwisko"])
    print("Deputies added to the database")
    db.commit()


def execute_sittings(sitting_dataframe):
    print("Importing sittings to the database...")
    for index, row in sitting_dataframe.iterrows():
        if sitting_exists(cursor, row["id"]):
            pass
        else:
            insert_sittings(cursor, row["id"], row["nr_posiedzenia"], row["data"])
    db.commit()
    print("Sittings added to the database")


def execute_votings(glosowania_dataframe):
    print("Importing votings to the database...")
    for index, row in glosowania_dataframe.iterrows():
        if voting_exists(cursor, row["nr_glosowania"], row["opis"]):
            pass
        else:
            insert_voting(
                cursor, row["id_posiedzenia"], row["nr_glosowania"], row["opis"]
            )
    print("Votings added to the database")
    db.commit()


def execute_votes(votes_dataframe):
    print("Importing votes to the database")
    for index, row in votes_dataframe.iterrows():
        if vote_exists(cursor, row["id_posel"], row["id_glosowania"]):
            pass
        else:
            insert_vote(
                cursor,
                row["id_partia"],
                row["id_posel"],
                row["id_glosowania"],
                row["glos"],
                row["data_glosu"],
            )
    print("Votes added to the database")
    db.commit()

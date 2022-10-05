def insert_parties(cursor, party):
    insert_into_parties = ('''INSERT INTO partie (nazwa) VALUES (%s)''')
    cursor.execute(insert_into_parties, (party,))


def insert_deputy(cursor, id_deputy, first_name, surname):
    insert_into_deputies = ('''INSERT INTO poslowie (id, imie, nazwisko) VALUES (%s,%s,%s)''')
    row_to_insert = (id_deputy, first_name, surname)
    cursor.execute(insert_into_deputies, row_to_insert)


def insert_sittings(cursor, id_sitting, nr_sitting, date):
    insert_into_sittings = ('''INSERT INTO posiedzenia (id, nr_posiedzenia, data) VALUES (%s,%s,%s)''')
    row_to_insert = (id_sitting, nr_sitting, date)
    cursor.execute(insert_into_sittings, row_to_insert)


def insert_voting(cursor, id_sitting, nr_sitting, description):
    insert_into_votings = ('''INSERT INTO glosowania SET
                                id_posiedzenia = (SELECT id FROM posiedzenia WHERE id = %s),
                                nr_glosowania = %s, opis = %s''')
    row_to_insert = (id_sitting, nr_sitting, description)
    cursor.execute(insert_into_votings, row_to_insert)


def insert_vote(cursor, id_party, id_deputy, id_voting, vote, vote_date):
    insert_into_votes = ('''INSERT INTO glosy SET id_partia = (SELECT id FROM partie WHERE id = %s),
                        id_posel = (SELECT id FROM poslowie WHERE id = %s),
                        id_glosowania = (SELECT id FROM glosowania WHERE id = %s),
                        glos = %s,
                        data_glosu = %s''')
    row_to_insert = (id_party, id_deputy, id_voting, vote, vote_date)
    cursor.execute(insert_into_votes, row_to_insert)

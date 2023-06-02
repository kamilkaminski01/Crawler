def party_exists(cursor, name):
    query = """SELECT nazwa FROM partie WHERE nazwa = %s"""
    cursor.execute(query, (name,))
    return cursor.fetchone() is not None


def deputy_exists(cursor, id_deputy):
    query = """SELECT id FROM poslowie WHERE id = %s"""
    cursor.execute(query, (id_deputy,))
    return cursor.fetchone() is not None


def sitting_exists(cursor, id_sitting):
    query = """SELECT id FROM posiedzenia WHERE id = %s"""
    cursor.execute(query, (id_sitting,))
    return cursor.fetchone() is not None


def voting_exists(cursor, nr_voting, description):
    query = (
        "SELECT nr_glosowania, opis FROM glosowania WHERE "
        "nr_glosowania = %s AND opis = %s"
    )
    row_to_insert = (nr_voting, description)
    cursor.execute(query, row_to_insert)
    return cursor.fetchone() is not None


def vote_exists(cursor, id_deputy, id_voting):
    query = (
        "SELECT id_posel, id_glosowania FROM glosy WHERE "
        "id_posel = %s and id_glosowania = %s"
    )
    row_to_insert = (id_deputy, id_voting)
    cursor.execute(query, row_to_insert)
    return cursor.fetchone() is not None

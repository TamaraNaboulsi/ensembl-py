from ensembl.database.dbconnection import DBConnection
from ensembl.api.dbsql import TranscriptAdaptor
from ensembl.api.fileio import GFFAdaptor

url = 'mysql://ensro@mysql-ens-core-prod-1.ebi.ac.uk:4524/panthera_leo_core_110_1'
dbc = DBConnection(url)

ta = TranscriptAdaptor(dbc)
tr = ta.fetch_by_stable_id("ENSPLOT00000000003")

ga = GFFAdaptor("example.gff3")
ga.print_transcript(tr)

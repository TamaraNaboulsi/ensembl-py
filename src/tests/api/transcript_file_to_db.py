from ensembl.database.dbconnection import DBConnection
from ensembl.api.dbsql import TranscriptAdaptor
from ensembl.api.fileio import GFFAdaptor

ga = GFFAdaptor("Panthera_leo.PanLeo1.0.109.gff3")
tr = ga.fetch_transcript_by_stable_id("ENSPLOT00000000003")

tr.description = "this is a new description"

url = 'mysql://ensro@mysql-ens-core-prod-1.ebi.ac.uk:4524/panthera_leo_core_110_1'
dbc = DBConnection(url)

ta = TranscriptAdaptor(dbc)
ta.update(tr)

from ensembl.database.dbconnection import DBConnection

from ensembl.api.core import Transcript
from ensembl.core.models import Transcript as TranscriptDB
from ensembl.core.models import Xref as XrefDB
from ensembl.core.models import ExternalDb as ExternalDbDB
from ensembl.core.models import SeqRegion as SeqRegionDB

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from typing import List

class TranscriptAdaptor(object):
  def __init__(self, dbc: DBConnection) -> None:
    self._dbc = dbc
    self._columns = {
      TranscriptDB: ['transcript_id', 'stable_id', 'version', 'source', 'created_date', 'modified_date', 'description', 'display_xref_id', 'is_current', {'seq_region_start': 'start'}, {'seq_region_end': 'end'}, {'seq_region_strand': 'strand'}],
      XrefDB: [{'display_label': 'external_name'}],
      ExternalDbDB: [{'db_name': 'external_db'}, {'status': 'external_status'}],
      SeqRegionDB: [{'name': 'seq_region_name'}]
    }
    self._left_joins = {
      XrefDB: XrefDB.xref_id==TranscriptDB.display_xref_id,
      ExternalDbDB: ExternalDbDB.external_db_id==XrefDB.external_db_id,
      SeqRegionDB: SeqRegionDB.seq_region_id==TranscriptDB.seq_region_id
    }

  def _construct_query(self):
    query = select()

    for db, columns in self._columns.items():
      for col in columns:
        if type(col) is dict:
          for name, alias in col.items():
            query = query.add_columns(getattr(db, name).label(alias))
        else:
          query = query.add_columns(getattr(db, col))

    for db, condition in self._left_joins.items():
      query = query.join(db, condition, isouter=True)

    return query

  def fetch_by_stable_id(self, stable_id: str) -> Transcript:
    if "." in stable_id:
      (stable_id, version) = stable_id.split(".")
      return self.fetch_by_stable_id_version(stable_id, version)

    query = self._construct_query().where(TranscriptDB.stable_id==stable_id, TranscriptDB.is_current==1)
    result = self._dbc.execute(query).mappings().first()

    if not result:
      raise NoResultFound(f'No current Transcript exists for stable_id {stable_id}')

    transcript = Transcript(result)
    return transcript

  def fetch_by_stable_id_version(self, stable_id: str, version: int) -> Transcript:
    if "." in stable_id:
      (stable_id, new_version) = stable_id.split(".")
      if version is None:
        version = new_version
    
    if version is None:
      return self.fetch_by_stable_id(stable_id)

    query = self._construct_query().where(TranscriptDB.stable_id==stable_id, TranscriptDB.is_current==1, TranscriptDB.version==version)
    result = self._dbc.execute(query).mappings().first()

    if not result:
      raise NoResultFound(f'No current Transcript exists for stable_id {stable_id} and version {version}')

    transcript = Transcript(result)
    return transcript

  def fetch_by_display_label(self, label: str) -> Transcript:
    query = self._construct_query().where(XrefDB.display_label==label, TranscriptDB.is_current==1)
    result = self._dbc.execute(query).mappings().first()

    if not result:
      raise NoResultFound(f'No current Transcript exists for display_label {label}')

    transcript = Transcript(result)
    return transcript

  def list_dbIDs(self, ordered: bool=0) -> List[int]:
    query = select(TranscriptDB.transcript_id)
    if ordered:
      query = select(TranscriptDB.transcript_id).order_by(TranscriptDB.seq_region_id, TranscriptDB.seq_region_start)

    result = self._dbc.execute(query).fetchall()

    dbIDs = []
    for row in result:
      dbIDs.append(row[0])

    return dbIDs

  def list_stable_ids(self, ordered: bool=0) -> List[str]:
    query = select(TranscriptDB.stable_id)
    if ordered:
      query = select(TranscriptDB.stable_id).order_by(TranscriptDB.seq_region_id, TranscriptDB.seq_region_start)

    result = self._dbc.execute(query).fetchall()

    stable_ids = []
    for row in result:
      stable_ids.append(row[0])

    return stable_ids

  def update(self, transcript: Transcript) -> None:
    if Transcript is None:
      raise AttributeError(f'Must provide a Transcript object')

    query = update(TranscriptDB).where(TranscriptDB.stable_id==transcript.stable_id).values(stable_id=transcript.stable_id, display_xref_id=transcript.display_xref_id, description=transcript.description, source=transcript.source, is_current=transcript.is_current, version=transcript.version)
    result = self._dbc.execute(query)


from ensembl.api.core import Transcript

import re
from os.path import exists

class GFFAdaptor(object):
  def __init__(self, gff_file: str) -> None:
    self._gff_file = gff_file
    self._feature_types = {
      'gene' : 'gene', 'ncRNA_gene' : 'gene', 'pseudogene' : 'gene',
      'mRNA' : 'transcript', 'lnc_RNA' : 'transcript', 'snRNA' : 'transcript', 'snoRNA' : 'transcript', 'pseudogenic_transcript' : 'transcript', 'miRNA' : 'transcript',
      'Y_RNA' : 'transcript', 'rRNA' : 'transcript', 'scRNA' : 'transcript',
      'exon' : 'exon'
    }
    self._features = self._load_features()

  def fetch_transcript_by_stable_id(self, stable_id: str) -> Transcript:
    transcript_attributes = self._features['transcript'].get(stable_id)

    if transcript_attributes is None:
      raise NoResultFound(f'No current Transcript exists for stable_id {stable_id}')

    transcript = Transcript(transcript_attributes)
    return transcript

  def _load_features(self):
    all_features = {'gene' : {}, 'transcript' : {}, 'exon' : {}}

    if not exists(self._gff_file):
      return None

    read_fh = open(self._gff_file)
    lines = read_fh.readlines()

    for line in lines:
      # Disregard commented out lines
      if re.search(r'^#', line):
        continue

      line = line.rstrip()
      fields = re.split(r'\t+', line)
      (seqname, source, feature, start, end, score, strand, phase, attributes) = fields

      # Only consider genes. transcripts, and exons
      feature_type = self._feature_types.get(feature)
      if feature_type is None:
        continue

      attributes = self._parse_attributes(attributes)
      feature_id_key = feature_type + "_id"
      feature_id = attributes.get(feature_id_key)

      if feature_id is not None:
        all_features[feature_type][feature_id] = {
          'stable_id' : feature_id, 'version' : attributes.get('version'), 'external_name' : attributes.get('Name'),
          'seq_region_name' : seqname, 'start' : start, 'end' : end, 'strand' : strand, 'source' : source, 'is_current' : 1
        }
        # all_features[feature_type][feature_id].update(attributes)

    return all_features

  def _parse_attributes(self, unparsed_attributes: str) -> dict:
    parsed_attributes = {}

    split_attributes = re.split(r';', unparsed_attributes)
    for attribute in split_attributes:
      attribute_pair = re.split(r'=', attribute)
      parsed_attributes[attribute_pair[0]] = attribute_pair[1]

    return parsed_attributes


  def print_transcript(self, transcript: Transcript) -> None:
    summary = transcript.summary_as_hash()
    line = ""

    # Column 1: seqname - the name of the sequence/chromosome the transcript is on
    line += summary["seq_region_name"]+"\t"
    del summary["seq_region_name"]

    # Column 2: source - the originator of the data
    line += summary["source"]+"\t"
    del summary["source"]

    # Column 3: feature - the ontology term for the kind of transcript this is
    # TO DO: use biotype
    line += "transcript\t"

    # Column 4: start - the start coordinate of the transcript
    # TO DO: check start and end order
    line += str(summary["start"])+"\t"
    del summary["start"]

    # Column 5: end - the end coordinate (absolute) of the transcript
    line += str(summary["end"])+"\t"
    del summary["end"]

    # Column 6: score - for variations only
    line += ".\t"

    # Column 7: strand - up or down
    strand_conversion = {'1': '+', '0': '.', '-1': '-'};
    strand = strand_conversion[str(summary["strand"])] or "?"
    line += strand+"\t"
    del summary["strand"]

    # Column 8: phase - only for Exons
    line += ".\t"

    # Column 9: attributes
    for key in ['ID', 'Name', 'Alias', 'Parent', 'Target', 'Gap', 'Derives_from', 'Note', 'Dbxref', 'Ontology_term', 'Is_circular']:
      if key in summary.keys():
        value = summary[key]
        del summary[key]

        if value is not None:
          if key == 'ID':
            value = "transcript:"+value
          elif key == 'Parent':
            value = "gene:"+value

          line += key+"="+str(value)+";"

    for key, value in summary.items():
      if value is not None:
        line += key+"="+str(value)+";"

    # Remove last ; and add new line
    line = line[:-1]
    line += "\n"

    write_fh = open(self._gff_file, "a")
    write_fh.write(line)
    write_fh.close()

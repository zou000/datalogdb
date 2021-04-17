# Modified from colab_logica.py

from logica.common import color

from logica.compiler import rule_translate
from logica.compiler import universe

import IPython

from IPython.core.magic import register_cell_magic
from IPython.display import display

import pandas

from logica.parser_py import parse

PROJECT = None

DB_CONNECTION = None

def SetProject(project):
  global PROJECT
  PROJECT = project

def SetDbConnection(connection):
  global DB_CONNECTION
  DB_CONNECTION = connection

@register_cell_magic
def logica(line, cell):
  Logica(line, cell, run_query=True)


def ParseList(line):
  line = line.strip()
  if not line:
    predicates = []
  else:
    predicates = [p.strip() for p in line.split(',')]
  return predicates


def RunSQL(sql, engine):
  if engine == 'psql':
    return pandas.read_sql(sql, DB_CONNECTION)
  elif engine == 'sqlite':
    statements = parse.SplitRaw(sql, ';')
    for s in statements[:-2]:
      cursor = DB_CONNECTION.execute(s)
    return pandas.read_sql(statements[-2], DB_CONNECTION)
  else:
    raise Exception('Logica only supports BigQuery, PostgreSQL and SQLite '
                    'for now.')


def Logica(line, cell, run_query):
  """Running Logica predicates and storing results."""
  predicates = ParseList(line)
  try:
    parsed_rules = parse.ParseFile(cell)['rule']
  except parse.ParsingException as e:
    e.ShowMessage()
    return
  program = universe.LogicaProgram(parsed_rules)
  engine = program.annotations.Engine()

  logs_idx = len(predicates)

  ip = IPython.get_ipython()
  for idx, predicate in enumerate(predicates):
    print('Running %s' % predicate)
    try:
      sql = program.FormattedPredicateSql(predicate)
      ip.push({predicate + '_sql': sql})
    except rule_translate.RuleCompileException as e:
      e.ShowMessage()
      return

    # Publish output to Colab cell.
    print(
        color.Format(
            'The following query is stored at {warning}%s{end} '
            'variable.' % (
                predicate + '_sql')))
    print(sql)

    if run_query:
      t = RunSQL(sql, engine)
      ip.push({predicate: t})

    if run_query:
      print(
          color.Format(
              'The following table is stored at {warning}%s{end} '
              'variable.' %
              predicate))
      display(t)
    else:
      print('The query was not run.')

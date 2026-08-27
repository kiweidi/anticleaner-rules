#!/usr/bin/env python3
import json,re,sys
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; CATALOG=ROOT/'docs/data/reported-candidates.v1.json'
EXPECTED={'PhoneSeep - Junk Remover','Keep PDF','Clean Master Kit','CleanPro','ProCleaner','CleanSwift','Reiniger & Schutz','AI FileCleaner','AntivirusPure','AuraClean','CCleaner','Cool File Cleaner','Easy Cleaner','Gründliche Speicherreinigung','Jiffy Clean','Security Phone Cleaner','Ultra File Cleaner','PDF Reader Lite - PDF Viewer'}
MISSING={'exact_package_name','signer_sha256','tested_version_range','reproducible_public_evidence'}
def fail(message): print('ERROR:',message,file=sys.stderr); raise SystemExit(1)
def keys(value,expected,label):
 if set(value)!=set(expected): fail(f'{label} fields differ: {sorted(set(value)^set(expected))}')
def iso(value,label):
 try: date.fromisoformat(value)
 except (TypeError,ValueError): fail(f'{label} is not an ISO date')
def main():
 data=json.loads(CATALOG.read_text(encoding='utf-8')); keys(data,{'schemaVersion','catalogVersion','publishedDate','titleDe','titleEn','scopeDe','scopeEn','notAMalwareVerdict','entries'},'catalog')
 if data['schemaVersion']!=1 or data['catalogVersion']!=1 or data['notAMalwareVerdict'] is not True: fail('unexpected version or missing non-verdict boundary')
 iso(data['publishedDate'],'publishedDate'); entries=data['entries']; names=[e.get('displayName') for e in entries]
 if len(entries)!=18 or set(names)!=EXPECTED or len(names)!=len(set(names)): fail('catalog must exactly match 18 deduplicated names')
 ids=set(); folded=set()
 for i,e in enumerate(entries):
  label=f'entry[{i}]'; keys(e,{'id','displayName','status','reportCount','observation','identityBinding'},label)
  if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',e['id']) or e['id'] in ids: fail(f'{label} invalid/duplicate id')
  ids.add(e['id']); fold=e['displayName'].casefold()
  if fold in folded:
   fail(f'{label} duplicate name')
  folded.add(fold)
  if e['status']!='reported_candidate' or e['reportCount']!=1: fail(f'{label} overstates report status')
  o=e['observation']; keys(o,{'category','observedDate','sourceType','evidenceLevel','summaryDe','summaryEn'},label+'.observation'); iso(o['observedDate'],label+'.observedDate')
  if (o['category'],o['sourceType'],o['evidenceLevel'])!=('frequent_unwanted_advertising','user_field_report','name_only_report'): fail(f'{label} overstates evidence')
  b=e['identityBinding']; keys(b,{'packageName','signerSha256','minVersionCode','maxVersionCode','ruleEligible','missingFields'},label+'.identityBinding')
  if b['packageName'] is not None or b['signerSha256']!=[] or b['minVersionCode'] is not None or b['maxVersionCode'] is not None or b['ruleEligible'] is not False or set(b['missingFields'])!=MISSING: fail(f'{label} crossed trust boundary')
 if list((ROOT/'rules').glob('*.json')): fail('rule JSON blocked until repository verifies production signatures')
 if 'data/reported-candidates.v1.json' not in (ROOT/'docs/app.js').read_text(encoding='utf-8') or 'Kein Malwareurteil' not in (ROOT/'docs/index.html').read_text(encoding='utf-8'): fail('site boundary missing')
 print('OK: 18 unique name-only reports; no active rule package; trust boundary intact')
if __name__=='__main__': main()

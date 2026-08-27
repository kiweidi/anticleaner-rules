# AntiCleaner Rules & Observations

Public, transparent data repository for AntiCleaner.

## What is published here?

- **Reported candidates:** name-based field reports that require technical verification.
- **Signed rules:** a separate, currently empty channel reserved for exact package, signer and version-bound rules.
- **GitHub Pages:** a human-readable view of the reported-candidate catalog.

**A reported name is not a malware verdict, risk rating, removal recommendation or app-enforced rule.** App names are not stable identities and may be shared by unrelated software.

## Public catalog

- Website: <https://kiweidi.github.io/anticleaner-rules/>
- Canonical JSON: <https://kiweidi.github.io/anticleaner-rules/data/reported-candidates.v1.json>
- JSON Schema: [`schema/reported-candidates.schema.json`](schema/reported-candidates.schema.json)

The initial catalog contains 18 unique names from one field report. The observation was frequent unwanted advertising appearing every few seconds. Two duplicate names in the original 20-line report were deduplicated.

## Trust boundary

AntiCleaner must never consume `reported-candidates.v1.json` as a detection or removal rule set. An app-enforced rule requires, at minimum:

1. exact Android package name;
2. SHA-256 signing-certificate binding;
3. tested minimum and maximum version codes;
4. reproducible evidence and review;
5. an offline-produced cryptographic signature;
6. monotonic versioning and expiry.

The private signing key must never be stored in this repository, GitHub Actions or the serving environment. See [`rules/README.md`](rules/README.md).

## Corrections and new reports

Use the issue forms. Do not upload APKs, personal data, screenshots containing account details, credentials or secrets.

## Validation

```bash
python3 scripts/validate_catalog.py
```

The validation workflow checks the catalog structure, exact count, unique names/IDs, name-only trust boundary and the absence of unsigned app-consumable rules.

## License

Catalog and documentation: [Creative Commons Attribution 4.0 International](LICENSE).

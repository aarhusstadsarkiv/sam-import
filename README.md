# Converter

Et script der genererer metadata ud fra en webfomular. 

## Funktionalitet

- Læser `submission.json` fra mapper
- Genererer `_regnote.txt` med kontaktinformation
- Opretter `metadata.csv` med filmetadata
- Genererer `ophavsret.pdf` baseret på Jinja2-skabelon
- Omdøber mapper med `_DONE` suffix efter behandling

## Installation

```bash
uv run src/sam_import/main.py <sti-til-mappe>
```

Programmet behandler alle undermapper rekursivt.

## Output

- `_regnote.txt` - Registreringsnote
- `metadata.csv` - Filmetadata
- `ophavsret.pdf` - Ophavsretserklæring
import csv
from collections import Counter
from pathlib import Path


def normalize_email(email: str) -> str:
    return email.strip().lower()


def load_emails(path: Path) -> set[str]:
    if not path.is_file():
        raise FileNotFoundError(f"Archivo no encontrado: {path}")

    emails: set[str] = set()
    with path.open('r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            raw_email = row[0].strip()
            if not raw_email:
                continue
            if raw_email.lower() == 'email':
                continue
            normalized = normalize_email(raw_email)
            if '@' in normalized:
                emails.add(normalized)
    return emails


def write_email_list(path: Path, emails: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Email'])
        for email in sorted(emails):
            writer.writerow([email])


def write_domain_counts(path: Path, emails: set[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    domain_counts = Counter(email.split('@', 1)[1] for email in emails)
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Dominio', 'Cantidad'])
        for domain, count in domain_counts.most_common():
            writer.writerow([domain, count])


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent

    source_files = [
        root_dir / 'Log_Files' / 'Results' / 'email_list.csv',
        root_dir / 'Database_Extraction' / 'Results' / 'emails_list.csv',
        root_dir / 'Log_Files' / 'Results' / 'telecom_email_list.csv',
    ]

    all_emails: set[str] = set()
    for source_file in source_files:
        source_emails = load_emails(source_file)
        print(f"Cargando {len(source_emails)} emails desde {source_file}")
        all_emails.update(source_emails)

    print(f"Total de emails únicos después de fusionar: {len(all_emails)}")

    output_dir = script_dir / 'Results'
    output_emails = output_dir / 'merged_emails.csv'
    output_domains = output_dir / 'merged_emails_per_domain.csv'

    write_email_list(output_emails, all_emails)
    write_domain_counts(output_domains, all_emails)

    print(f"Guardado CSV de emails: {output_emails}")
    print(f"Guardado CSV de dominios: {output_domains}")


if __name__ == '__main__':
    main()

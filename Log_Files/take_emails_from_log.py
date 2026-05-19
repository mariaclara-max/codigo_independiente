import csv
import re
from pathlib import Path

EMAIL_RE = re.compile(r'[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}')
ENCODING_RE = re.compile(r'^Content-Transfer-Encoding:\s*(7bit|8bit)\b', re.IGNORECASE)
RECORD_START_RE = re.compile(r'^From\s.+$', re.MULTILINE)
SENDER_LOCAL_PARTS = {'marketing', 'noreply'}
RECEIVER_PATTERNS = [
    re.compile(r'^To:\s*(.+)$', re.IGNORECASE),
    re.compile(r'^Cc:\s*(.+)$', re.IGNORECASE),
    re.compile(r'^Delivered-To:\s*(.+)$', re.IGNORECASE),
    re.compile(r'^X-CP-For:\s*(.+)$', re.IGNORECASE),
    re.compile(r'^Final-Recipient:\s*[^;]+;\s*(.+)$', re.IGNORECASE),
    re.compile(r'^Original-Recipient:\s*[^;]+;\s*(.+)$', re.IGNORECASE),
]


def normalize_email(raw_email: str) -> str:
    email = raw_email.strip().strip('"\'"')
    if email.startswith('<') and email.endswith('>'):
        email = email[1:-1].strip()
    if ',' in email:
        email = email.split(',')[0].strip()
    return email


def is_receiver_email(email: str) -> bool:
    if '@' not in email:
        return False
    local_part = email.split('@', 1)[0].lower()
    return local_part not in SENDER_LOCAL_PARTS


def extract_receivers_from_text(text: str) -> set[str]:
    receivers = set()

    for line in text.splitlines():
        for pattern in RECEIVER_PATTERNS:
            match = pattern.match(line)
            if match:
                candidate_text = match.group(1)
                for raw_email in EMAIL_RE.findall(candidate_text):
                    email = normalize_email(raw_email).lower()
                    if is_receiver_email(email):
                        receivers.add(email)
                break

    if not receivers:
        for raw_email in EMAIL_RE.findall(text):
            email = normalize_email(raw_email).lower()
            if is_receiver_email(email):
                receivers.add(email)

    return receivers


def extract_encoding_from_text(text: str) -> str:
    for line in text.splitlines():
        match = ENCODING_RE.match(line)
        if match:
            value = match.group(1).lower()
            return '7-bit' if value == '7bit' else '8-bit' if value == '8bit' else value
    return 'unknown'


def split_log_records(text: str) -> list[str]:
    parts = RECORD_START_RE.split(text)
    if len(parts) <= 1:
        return [text]
    records = []
    starts = RECORD_START_RE.findall(text)
    for i, body in enumerate(parts[1:], start=0):
        header = starts[i]
        records.append(header + '\n' + body)
    return records


def load_domain_list(path: Path) -> set[str]:
    domains = set()
    if not path.is_file():
        return domains
    with path.open('r', encoding='utf-8', errors='replace') as f:
        for line in f:
            domain = line.strip().lower()
            if domain and not domain.startswith('#'):
                domains.add(domain)
    return domains


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    source_dir = script_dir / 'Source'
    results_dir = script_dir / 'Results'
    config_dir = script_dir / 'Config Files'
    source_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    forbidden_domains = load_domain_list(config_dir / 'forbidden_domains.log')
    telecom_domains = load_domain_list(config_dir / 'telecom_domains.log')

    log_files = sorted(source_dir.glob('*.log'))
    if not log_files:
        raise SystemExit(f'No se encontraron archivos .log en {source_dir}.')

    normal_rows: set[tuple[str, str]] = set()
    telecom_rows: set[tuple[str, str]] = set()
    total_records = 0

    for log_file in log_files:
        file_normal_rows: set[tuple[str, str]] = set()
        file_telecom_rows: set[tuple[str, str]] = set()
        file_forbidden_emails: set[str] = set()

        with log_file.open('r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        records = split_log_records(content)
        total_records += len(records)

        for record in records:
            receivers = extract_receivers_from_text(record)
            if not receivers:
                continue
            encoding = extract_encoding_from_text(record)
            for receiver in sorted(receivers):
                domain = receiver.split('@', 1)[1].lower()
                if domain in forbidden_domains:
                    file_forbidden_emails.add(receiver)
                    continue
                row = (receiver, encoding)
                if domain in telecom_domains:
                    file_telecom_rows.add(row)
                else:
                    file_normal_rows.add(row)

        normal_rows.update(file_normal_rows)
        telecom_rows.update(file_telecom_rows)

        print(f'Archivo: {log_file.name}')
        print(f'  Standard emails: {len(file_normal_rows)}')
        print(f'  Telecom emails: {len(file_telecom_rows)}')
        print(f'  Forbidden emails descartados: {len(file_forbidden_emails)}')
        print('')

    normal_csv = results_dir / 'email_list.csv'
    telecom_csv = results_dir / 'telecom_email_list.csv'

    with normal_csv.open('w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Email', 'Codificacion'])
        for email, encoding in sorted(normal_rows):
            writer.writerow([email, encoding])

    with telecom_csv.open('w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Email', 'Codificacion'])
        for email, encoding in sorted(telecom_rows):
            writer.writerow([email, encoding])

    print(f'Procesados {len(log_files)} archivos .log desde {source_dir}')
    print(f'Total de registros encontrados: {total_records}')
    print(f'Total de filas únicas escritas en {normal_csv}: {len(normal_rows)}')
    print(f'Total de filas únicas escritas en {telecom_csv}: {len(telecom_rows)}')
    print(f'CSV guardado en: {normal_csv}')
    print(f'CSV guardado en: {telecom_csv}')


if __name__ == '__main__':
    main()

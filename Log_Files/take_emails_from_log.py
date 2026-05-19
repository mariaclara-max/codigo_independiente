import argparse
import os
import re
import sys
import subprocess
from pathlib import Path
from typing import Optional

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


def load_telecom_domains(path: str = 'Config Files/telecom_domains.log') -> set[str]:
    """Carga dominios telecom desde el archivo Config Files/telecom_domains.log."""
    domains = set()
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            domain = line.strip().lower()
            if domain and not domain.startswith('#'):
                domains.add(domain)
    return domains


def load_forbidden_mails(path: str = 'Config Files/forbidden_domains.log') -> set[str]:
    if not os.path.exists(path):
        return set()

    domains = set()
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            domain = line.strip().lower()
            if domain and not domain.startswith('#'):
                domains.add(domain)
    return domains


def split_log_records(text: str) -> list[str]:
    parts = RECORD_START_RE.split(text)
    if len(parts) <= 1:
        return [text]
    # RECORD_START_RE.split drops the separators; keep them attached to each record
    records = []
    starts = RECORD_START_RE.findall(text)
    for i, body in enumerate(parts[1:], start=0):
        header = starts[i]
        records.append(header + '\n' + body)
    return records


def find_available_logs(pattern: str = 'textlog_part*.log') -> list[int]:
    """Encuentra todos los archivos que coinciden con el patrón y retorna sus números ordenados."""
    script_dir = Path(__file__).resolve().parent
    files = sorted(script_dir.glob(pattern))
    numbers = []
    for f in files:
        # Extrae el número de 'textlog_part{N}.log'
        try:
            num = int(f.stem.replace('textlog_part', ''))
            numbers.append(num)
        except ValueError:
            pass
    return sorted(numbers)


def build_output_filename(log_id: str, explicit_output: Optional[str]) -> str:
    if explicit_output:
        return explicit_output
    return 'extracted_mails.log'


def parse_args() -> tuple[argparse.Namespace, list[int], int]:
    parser = argparse.ArgumentParser(
        description='Extrae direcciones de correo receptoras de archivos .log y guarda el resultado en un archivo de salida.'
    )
    
    # Detectar archivos disponibles
    available_nums = find_available_logs()
    max_num = max(available_nums) if available_nums else 0
    
    parser.add_argument(
        'part_number',
        nargs='?',
        type=int,
        help=f'Número de archivo a procesar (1-{max_num}). Usa {max_num + 1} para procesar todos recursivamente.',
    )
    parser.add_argument(
        '--output-file',
        '-o',
        default=None,
        help='Archivo de salida donde se guardan los correos extraídos. Si no se indica, usa extracted_mails.log y se agrega al final.',
    )
    parser.add_argument(
        '--telecom-output-file',
        default='extracted_telecom_mails.log',
        help='Archivo de salida para correos de dominios telecom. Default: extracted_telecom_mails.log.',
    )
    parser.add_argument(
        '--telecom-domains-file',
        default='Config Files/telecom_domains.log',
        help='Lista de dominios telecom. Si no existe, se usan defaults internos.',
    )
    parser.add_argument(
        '--forbidden-mails-file',
        default='Config Files/forbidden_domains.log',
        help='Lista de dominios vetados que no deben aparecer en ningún archivo.',
    )
    parser.add_argument(
        '--log-id',
        '-i',
        default=None,
        help='Identificador usado para construir el nombre del archivo de salida cuando no se especifica --output-file.',
    )
    parser.add_argument(
        '--no-dedupe',
        action='store_true',
        help='No omitir duplicados en el archivo de salida.',
    )
    return parser.parse_args(), available_nums, max_num


def main() -> None:
    args, available_nums, max_num = parse_args()
    
    # Si no se proporciona número, preguntar o procesarlos todos
    if args.part_number is None:
        print(f'Archivos disponibles: 1-{max_num}')
        print(f'Para procesar todos, introduce: {max_num + 1}')
        try:
            part_num = int(input('Introduce el número del archivo a procesar: ').strip())
        except ValueError:
            raise SystemExit('Debes introducir un número válido.')
    else:
        part_num = args.part_number
    
    # Validar número
    if part_num < 1 or part_num > max_num + 1:
        raise SystemExit(f'Número inválido. Debe estar entre 1 y {max_num + 1}.')
    
    # Si pasa max_num + 1, procesar todos recursivamente
    if part_num == max_num + 1:
        print(f'Procesando todos los archivos (1-{max_num}) recursivamente...\\n')
        script_path = Path(__file__).resolve()

        def count_file_lines(path: Path) -> int:
            if not path.is_file():
                return 0
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                return sum(1 for line in f if line.strip())

        for num in range(1, max_num + 1):
            print(f'--- Procesando archivo {num}/{max_num} ---')
            subprocess.run(
                [sys.executable, str(script_path), str(num)] + sys.argv[2:],
                check=False
            )

        output_file = script_path.parent / build_output_filename('', args.output_file)
        telecom_output_file = script_path.parent / args.telecom_output_file
        print(f'\\n✓ Todos los archivos han sido procesados.')
        print('Resumen final de archivos generados:')
        print(f'  {output_file}: {count_file_lines(output_file)} líneas')
        print(f'  {telecom_output_file}: {count_file_lines(telecom_output_file)} líneas')
        return
    
    # Procesar archivo específico
    script_dir = Path(__file__).resolve().parent
    log_file_path = script_dir / f'textlog_part{part_num}.log'
    args.log_files = [str(log_file_path)]

    log_entries: list[tuple[str, str]] = []

    for log_file in args.log_files:
        if not os.path.isfile(log_file):
            raise FileNotFoundError(f'No se encontró el archivo: {log_file}')

        with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        records = split_log_records(content)

        for record in records:
            receivers = extract_receivers_from_text(record)
            if not receivers:
                continue
            encoding = extract_encoding_from_text(record)
            for receiver in sorted(receivers):
                log_entries.append((receiver, encoding))

    script_dir = Path(__file__).resolve().parent
    output_file = script_dir / build_output_filename('', args.output_file)
    telecom_output_file = script_dir / args.telecom_output_file
    telecom_domains_path = script_dir / args.telecom_domains_file
    forbidden_mails_path = script_dir / args.forbidden_mails_file
    telecom_domains = load_telecom_domains(str(telecom_domains_path))
    forbidden_mail_domains = load_forbidden_mails(str(forbidden_mails_path))

    def read_existing_lines(path: Path) -> set[str]:
        if not path.is_file():
            return set()
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return {line.rstrip('\n') for line in f if line.strip()}

    normal_lines = read_existing_lines(output_file) if not args.no_dedupe else set()
    telecom_lines = read_existing_lines(telecom_output_file) if not args.no_dedupe else set()
    added_normal = 0
    added_telecom = 0
    skipped_forbidden = 0

    with open(str(output_file), 'a', encoding='utf-8') as out_normal, open(
        str(telecom_output_file), 'a', encoding='utf-8'
    ) as out_telecom:
        for email, encoding in log_entries:
            domain = email.split('@', 1)[1].lower()
            line = f'{email}|{encoding}'
            if domain in forbidden_mail_domains:
                skipped_forbidden += 1
                continue
            if domain in telecom_domains:
                if not args.no_dedupe and line in telecom_lines:
                    continue
                out_telecom.write(line + '\n')
                telecom_lines.add(line)
                added_telecom += 1
            else:
                if not args.no_dedupe and line in normal_lines:
                    continue
                out_normal.write(line + '\n')
                normal_lines.add(line)
                added_normal += 1

    print(f'Entradas procesadas: {len(log_entries)}')
    print(f'Entradas nuevas escritas (otros dominios): {added_normal}')
    print(f'Entradas nuevas escritas (telecom): {added_telecom}')
    print(f'Entradas descartadas por forbidden_mails: {skipped_forbidden}')


if __name__ == '__main__':
    main()

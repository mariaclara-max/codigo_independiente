# SAAS ↔ Promozione CSV 

Automated CSV transformation pipeline for transferring
frozen and blacklisted email records between platforms.

## Features
- CSV normalization
- Email extraction
- Reason column generation
- Daily archive folders
- Duplicate removal
- UTF-8 export compatibility
- Automated output structure

/tu_proyecto
│
├── FROZEN_SAAS.csv
├── FROZEN_PROMO.csv
│
├── /processed_csv
│
│   ├── /processed_csv_2026-05-07
│   │      ├── FROZEN_SAAS_TO_PROMO_TC.csv
│   │      └── FROZEN_PROMO_TO_SAAS_TC.csv
│   │
│   ├── /processed_csv_2026-05-08
│   │      ├── FROZEN_SAAS_TO_PROMO_TC.csv
│   │      └── FROZEN_PROMO_TO_SAAS_TC.csv

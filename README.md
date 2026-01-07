# mukey

## POPCATUSDT Trading Data Analysis

This repository contains cryptocurrency trading data for the POPCATUSDT futures pair and comprehensive analysis tools.

### Data Overview

- **File**: `POPCATUSDT_merged_full.csv`
- **Size**: ~17 MB
- **Records**: 92,261 trades
- **Time Period**: 2026-01-01 to 2026-01-02 (48 hours)
- **Trading Pair**: POPCATUSDT (Popcat token futures on Binance)

### Data Fields

The CSV file contains the following columns:

- `agg_trade_id`: Aggregated trade ID
- `price`: Trade price
- `quantity`: Trade quantity
- `first_trade_id`, `last_trade_id`: Trade ID range for aggregated trades
- `transact_time`: Transaction timestamp
- `is_buyer_maker`: Boolean indicating if buyer was maker
- `bucket_time`: Time bucket for aggregation
- `create_time`: Record creation time
- `symbol`: Trading symbol (POPCATUSDT)
- `sum_open_interest`: Sum of open interest
- `sum_open_interest_value`: Value of open interest
- `count_toptrader_long_short_ratio`: Top trader ratio count
- `sum_toptrader_long_short_ratio`: Top trader ratio sum
- `count_long_short_ratio`: Long/short ratio count
- `sum_taker_long_short_vol_ratio`: Taker volume ratio

### Analysis Tools

#### Running the Analysis

```bash
# Install dependencies
pip install pandas numpy

# Run the analysis script
python3 analyze_data.py
```

#### Output Files

1. **ANALYSIS_SUMMARY.md** - Human-readable markdown summary with key statistics
2. **analysis_report.json** - Detailed JSON report with all analysis data

### Key Findings

- **Total Trading Volume**: 632.1M tokens
- **Price Range**: $0.073 - $0.0965
- **VWAP**: $0.089430
- **Average Trade Size**: 6,851 tokens
- **Median Trade Size**: 635 tokens
- **Trading Activity**: Peak hours 8-14 UTC
- **Data Quality**: 99.95% complete (minimal missing values)

### Analysis Features

The `analyze_data.py` script performs:

1. **Basic Dataset Information**
   - Record counts, memory usage
   - Date range analysis
   - Column overview

2. **Data Quality Checks**
   - Missing value analysis
   - Data type validation
   - Duplicate detection

3. **Trading Statistics**
   - Price statistics (min, max, mean, median, volatility)
   - Volume analysis
   - Buy/sell distribution
   - Open interest metrics

4. **Temporal Analysis**
   - Time gaps between trades
   - Trading patterns by hour
   - Activity distribution

5. **Market Insights**
   - Volume-Weighted Average Price (VWAP)
   - Large trade identification (>95th percentile)
   - Price volatility metrics
   - Return analysis

### License

Data and code provided as-is for analysis purposes.
#!/usr/bin/env python3
"""
POPCATUSDT Trading Data Analysis Script

This script performs comprehensive analysis of the POPCATUSDT_merged_full.csv file,
including data quality checks, statistical summaries, and insights generation.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json


def load_data(filepath):
    """Load the CSV data file."""
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    print(f"Data loaded successfully: {len(df)} rows, {len(df.columns)} columns")
    return df


def basic_info(df):
    """Generate basic information about the dataset."""
    print("\n" + "="*80)
    print("BASIC DATASET INFORMATION")
    print("="*80)
    
    info = {
        "total_records": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / (1024**2),
        "date_range": {},
    }
    
    # Parse transact_time if available
    if 'transact_time' in df.columns:
        df['transact_time_parsed'] = pd.to_datetime(df['transact_time'], errors='coerce')
        valid_times = df['transact_time_parsed'].dropna()
        if len(valid_times) > 0:
            info["date_range"] = {
                "start": str(valid_times.min()),
                "end": str(valid_times.max()),
                "duration_hours": (valid_times.max() - valid_times.min()).total_seconds() / 3600
            }
    
    print(f"\nTotal Records: {info['total_records']:,}")
    print(f"Total Columns: {info['total_columns']}")
    print(f"Memory Usage: {info['memory_usage_mb']:.2f} MB")
    
    if info["date_range"]:
        print(f"\nDate Range:")
        print(f"  Start: {info['date_range']['start']}")
        print(f"  End: {info['date_range']['end']}")
        print(f"  Duration: {info['date_range']['duration_hours']:.2f} hours")
    
    return info


def data_quality_check(df):
    """Check data quality and missing values."""
    print("\n" + "="*80)
    print("DATA QUALITY ANALYSIS")
    print("="*80)
    
    quality_report = {
        "missing_values": {},
        "data_types": {},
        "duplicate_records": 0
    }
    
    # Missing values analysis
    print("\nMissing Values by Column:")
    for col in df.columns:
        missing_count = df[col].isna().sum()
        missing_pct = (missing_count / len(df)) * 100
        quality_report["missing_values"][col] = {
            "count": int(missing_count),
            "percentage": float(missing_pct)
        }
        if missing_count > 0:
            print(f"  {col}: {missing_count:,} ({missing_pct:.2f}%)")
    
    # Data types
    print("\nData Types:")
    for col in df.columns:
        dtype = str(df[col].dtype)
        quality_report["data_types"][col] = dtype
        print(f"  {col}: {dtype}")
    
    # Check for duplicates
    duplicate_count = df.duplicated().sum()
    quality_report["duplicate_records"] = int(duplicate_count)
    print(f"\nDuplicate Records: {duplicate_count:,}")
    
    # Check for duplicate agg_trade_ids
    if 'agg_trade_id' in df.columns:
        dup_trade_ids = df['agg_trade_id'].duplicated().sum()
        print(f"Duplicate Trade IDs: {dup_trade_ids:,}")
    
    return quality_report


def trading_statistics(df):
    """Calculate trading-related statistics."""
    print("\n" + "="*80)
    print("TRADING STATISTICS")
    print("="*80)
    
    stats = {}
    
    # Price statistics
    if 'price' in df.columns:
        price_stats = df['price'].describe()
        stats["price"] = {
            "min": float(df['price'].min()),
            "max": float(df['price'].max()),
            "mean": float(df['price'].mean()),
            "median": float(df['price'].median()),
            "std": float(df['price'].std()),
            "range": float(df['price'].max() - df['price'].min())
        }
        print("\nPrice Statistics:")
        print(f"  Min Price: {stats['price']['min']:.6f}")
        print(f"  Max Price: {stats['price']['max']:.6f}")
        print(f"  Mean Price: {stats['price']['mean']:.6f}")
        print(f"  Median Price: {stats['price']['median']:.6f}")
        print(f"  Std Dev: {stats['price']['std']:.6f}")
        print(f"  Price Range: {stats['price']['range']:.6f}")
    
    # Quantity statistics
    if 'quantity' in df.columns:
        quantity_stats = df['quantity'].describe()
        stats["quantity"] = {
            "min": float(df['quantity'].min()),
            "max": float(df['quantity'].max()),
            "mean": float(df['quantity'].mean()),
            "median": float(df['quantity'].median()),
            "total": float(df['quantity'].sum()),
            "std": float(df['quantity'].std())
        }
        print("\nQuantity Statistics:")
        print(f"  Min Quantity: {stats['quantity']['min']:.2f}")
        print(f"  Max Quantity: {stats['quantity']['max']:.2f}")
        print(f"  Mean Quantity: {stats['quantity']['mean']:.2f}")
        print(f"  Median Quantity: {stats['quantity']['median']:.2f}")
        print(f"  Total Volume: {stats['quantity']['total']:,.2f}")
    
    # Buyer/Seller analysis
    if 'is_buyer_maker' in df.columns:
        buyer_maker_counts = df['is_buyer_maker'].value_counts()
        stats["buyer_maker_distribution"] = {
            str(k): int(v) for k, v in buyer_maker_counts.items()
        }
        print("\nBuyer/Maker Distribution:")
        for key, value in buyer_maker_counts.items():
            pct = (value / len(df)) * 100
            print(f"  {key}: {value:,} ({pct:.2f}%)")
    
    # Open Interest statistics (if available and not all null)
    if 'sum_open_interest' in df.columns:
        oi_data = df['sum_open_interest'].dropna()
        if len(oi_data) > 0:
            stats["open_interest"] = {
                "min": float(oi_data.min()),
                "max": float(oi_data.max()),
                "mean": float(oi_data.mean()),
                "records_with_data": int(len(oi_data))
            }
            print("\nOpen Interest Statistics:")
            print(f"  Records with OI data: {len(oi_data):,}")
            print(f"  Min OI: {stats['open_interest']['min']:,.2f}")
            print(f"  Max OI: {stats['open_interest']['max']:,.2f}")
            print(f"  Mean OI: {stats['open_interest']['mean']:,.2f}")
    
    return stats


def temporal_analysis(df):
    """Analyze temporal patterns in the data."""
    print("\n" + "="*80)
    print("TEMPORAL ANALYSIS")
    print("="*80)
    
    temporal_stats = {}
    
    if 'transact_time' in df.columns:
        df['transact_time_parsed'] = pd.to_datetime(df['transact_time'], errors='coerce')
        valid_times = df[df['transact_time_parsed'].notna()].copy()
        
        if len(valid_times) > 0:
            # Calculate time gaps between trades
            valid_times = valid_times.sort_values('transact_time_parsed')
            time_diffs = valid_times['transact_time_parsed'].diff()
            
            temporal_stats["time_gaps"] = {
                "mean_seconds": float(time_diffs.dt.total_seconds().mean()),
                "median_seconds": float(time_diffs.dt.total_seconds().median()),
                "max_seconds": float(time_diffs.dt.total_seconds().max())
            }
            
            print("\nTime Gaps Between Trades:")
            print(f"  Mean Gap: {temporal_stats['time_gaps']['mean_seconds']:.2f} seconds")
            print(f"  Median Gap: {temporal_stats['time_gaps']['median_seconds']:.2f} seconds")
            print(f"  Max Gap: {temporal_stats['time_gaps']['max_seconds']:.2f} seconds")
            
            # Trades per hour
            valid_times['hour'] = valid_times['transact_time_parsed'].dt.hour
            trades_per_hour = valid_times.groupby('hour').size()
            temporal_stats["trades_per_hour"] = {int(k): int(v) for k, v in trades_per_hour.items()}
            
            print("\nTrades by Hour of Day:")
            for hour, count in trades_per_hour.items():
                print(f"  Hour {hour:02d}: {count:,} trades")
    
    return temporal_stats


def market_insights(df):
    """Generate market insights from the data."""
    print("\n" + "="*80)
    print("MARKET INSIGHTS")
    print("="*80)
    
    insights = {}
    
    # Calculate volume-weighted average price if possible
    if 'price' in df.columns and 'quantity' in df.columns:
        total_value = (df['price'] * df['quantity']).sum()
        total_quantity = df['quantity'].sum()
        vwap = total_value / total_quantity if total_quantity > 0 else 0
        insights["vwap"] = float(vwap)
        print(f"\nVolume-Weighted Average Price (VWAP): {vwap:.6f}")
    
    # Large trades analysis
    if 'quantity' in df.columns:
        q75 = df['quantity'].quantile(0.75)
        q95 = df['quantity'].quantile(0.95)
        large_trades = df[df['quantity'] > q95]
        
        insights["large_trades"] = {
            "threshold_95_percentile": float(q95),
            "count": int(len(large_trades)),
            "percentage": float((len(large_trades) / len(df)) * 100)
        }
        
        print(f"\nLarge Trades (>95th percentile = {q95:.2f}):")
        print(f"  Count: {len(large_trades):,}")
        print(f"  Percentage: {(len(large_trades)/len(df)*100):.2f}%")
    
    # Price volatility
    if 'price' in df.columns:
        price_returns = df['price'].pct_change().dropna()
        insights["volatility"] = {
            "std_returns": float(price_returns.std()),
            "max_increase": float(price_returns.max()),
            "max_decrease": float(price_returns.min())
        }
        print(f"\nPrice Volatility:")
        print(f"  Std Dev of Returns: {price_returns.std():.6f}")
        print(f"  Max Price Increase: {price_returns.max():.4%}")
        print(f"  Max Price Decrease: {price_returns.min():.4%}")
    
    return insights


def generate_summary_report(all_stats):
    """Generate a summary report and save to JSON."""
    print("\n" + "="*80)
    print("GENERATING SUMMARY REPORT")
    print("="*80)
    
    timestamp = datetime.now().isoformat()
    report = {
        "analysis_timestamp": timestamp,
        "data_file": "POPCATUSDT_merged_full.csv",
        "analysis": all_stats
    }
    
    # Save to JSON file
    output_file = "analysis_report.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed analysis report saved to: {output_file}")
    
    # Create a markdown summary
    md_file = "ANALYSIS_SUMMARY.md"
    with open(md_file, 'w') as f:
        f.write("# POPCATUSDT Trading Data Analysis Summary\n\n")
        f.write(f"**Analysis Date:** {timestamp}\n\n")
        f.write(f"**Data File:** POPCATUSDT_merged_full.csv\n\n")
        
        if "basic_info" in all_stats:
            f.write("## Dataset Overview\n\n")
            f.write(f"- **Total Records:** {all_stats['basic_info']['total_records']:,}\n")
            f.write(f"- **Total Columns:** {all_stats['basic_info']['total_columns']}\n")
            f.write(f"- **Memory Usage:** {all_stats['basic_info']['memory_usage_mb']:.2f} MB\n\n")
            
            if all_stats['basic_info'].get('date_range'):
                dr = all_stats['basic_info']['date_range']
                f.write("### Time Period\n\n")
                f.write(f"- **Start:** {dr['start']}\n")
                f.write(f"- **End:** {dr['end']}\n")
                f.write(f"- **Duration:** {dr['duration_hours']:.2f} hours\n\n")
        
        if "trading_stats" in all_stats and "price" in all_stats["trading_stats"]:
            f.write("## Price Statistics\n\n")
            ps = all_stats["trading_stats"]["price"]
            f.write(f"- **Min:** {ps['min']:.6f}\n")
            f.write(f"- **Max:** {ps['max']:.6f}\n")
            f.write(f"- **Mean:** {ps['mean']:.6f}\n")
            f.write(f"- **Median:** {ps['median']:.6f}\n")
            f.write(f"- **Range:** {ps['range']:.6f}\n\n")
        
        if "trading_stats" in all_stats and "quantity" in all_stats["trading_stats"]:
            f.write("## Volume Statistics\n\n")
            qs = all_stats["trading_stats"]["quantity"]
            f.write(f"- **Total Volume:** {qs['total']:,.2f}\n")
            f.write(f"- **Mean Trade Size:** {qs['mean']:.2f}\n")
            f.write(f"- **Median Trade Size:** {qs['median']:.2f}\n\n")
        
        if "insights" in all_stats:
            f.write("## Key Insights\n\n")
            if "vwap" in all_stats["insights"]:
                f.write(f"- **VWAP:** {all_stats['insights']['vwap']:.6f}\n")
            if "large_trades" in all_stats["insights"]:
                lt = all_stats["insights"]["large_trades"]
                f.write(f"- **Large Trades (>95th percentile):** {lt['count']:,} ({lt['percentage']:.2f}%)\n")
        
        f.write("\n## Data Quality\n\n")
        if "quality" in all_stats:
            f.write("See detailed quality report in `analysis_report.json`\n\n")
        
        f.write("\n---\n\n")
        f.write("*This analysis was generated automatically by analyze_data.py*\n")
    
    print(f"Markdown summary saved to: {md_file}")
    
    return report


def main():
    """Main analysis function."""
    print("="*80)
    print("POPCATUSDT TRADING DATA ANALYSIS")
    print("="*80)
    
    # Load data
    filepath = "POPCATUSDT_merged_full.csv"
    df = load_data(filepath)
    
    # Collect all statistics
    all_stats = {}
    
    # Run analysis modules
    all_stats["basic_info"] = basic_info(df)
    all_stats["quality"] = data_quality_check(df)
    all_stats["trading_stats"] = trading_statistics(df)
    all_stats["temporal"] = temporal_analysis(df)
    all_stats["insights"] = market_insights(df)
    
    # Generate summary report
    report = generate_summary_report(all_stats)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\nOutputs generated:")
    print("  - analysis_report.json (detailed JSON report)")
    print("  - ANALYSIS_SUMMARY.md (markdown summary)")
    

if __name__ == "__main__":
    main()

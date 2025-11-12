#!/usr/bin/env python3
"""
Data Exporter
Exports all analysis results to various formats (CSV, JSON, etc.)
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timezone

class DataExporter:
    """Export portfolio analysis data to multiple formats"""

    def __init__(self):
        self.data_dir = Path('data')
        self.export_dir = Path('exports')
        self.export_dir.mkdir(exist_ok=True)

    def load_analysis_data(self):
        """Load completed analysis data"""
        with open('data/portfolio_analysis_complete.json', 'r') as f:
            return json.load(f)

    def export_portfolio_features(self):
        """Export detailed portfolio features to CSV"""
        data = self.load_analysis_data()
        portfolio_data = data['portfolio_metrics']['current_portfolio']

        features = []
        for ticker, metrics in portfolio_data.items():
            features.append({
                'ticker': ticker,
                'weight': metrics['weight'],
                'value': metrics['value'],
                'price': metrics['price'],
                'expected_return': metrics['expected_return'],
                'volatility': metrics['volatility'],
                'dividend_yield': metrics['dividend_yield'],
                'dividend_income': metrics['dividend_income'],
                'asset_type': metrics['asset_type']
            })

        df = pd.DataFrame(features)
        df.to_csv(self.export_dir / 'features.csv', index=False)
        return self.export_dir / 'features.csv'

    def export_covariance_matrix(self):
        """Export correlation and covariance matrices"""
        data = self.load_analysis_data()
        corr_matrix = np.array(data['portfolio_metrics']['risk_metrics']['correlation_matrix'])
        tickers = list(data['portfolio_metrics']['current_portfolio'].keys())

        # Correlation matrix
        corr_df = pd.DataFrame(corr_matrix, index=tickers, columns=tickers)
        corr_df.to_csv(self.export_dir / 'correlation.csv')

        # Create covariance matrix (simplified)
        volatilities = [data['portfolio_metrics']['current_portfolio'][t]['volatility'] for t in tickers]
        cov_matrix = np.outer(volatilities, volatilities) * corr_matrix
        cov_df = pd.DataFrame(cov_matrix, index=tickers, columns=tickers)
        cov_df.to_csv(self.export_dir / 'covariance.csv')

        return self.export_dir / 'covariance.csv', self.export_dir / 'correlation.csv'

    def export_weights_comparison(self):
        """Export before/after weights comparison"""
        data = self.load_analysis_data()
        current = data['portfolio_metrics']['current_portfolio']
        plan_a = data['optimization_proposals']['plan_a_conservative']['new_weights']
        plan_b = data['optimization_proposals']['plan_b_aggressive']['new_weights']

        comparison = []
        for ticker in current.keys():
            comparison.append({
                'ticker': ticker,
                'current_weight': current[ticker]['weight'],
                'plan_a_weight': plan_a.get(ticker, 0),
                'plan_b_weight': plan_b.get(ticker, 0),
                'plan_a_change': plan_a.get(ticker, 0) - current[ticker]['weight'],
                'plan_b_change': plan_b.get(ticker, 0) - current[ticker]['weight']
            })

        df = pd.DataFrame(comparison)
        df.to_csv(self.export_dir / 'weights_before_after.csv', index=False)
        return self.export_dir / 'weights_before_after.csv'

    def export_sector_exposure(self):
        """Export sector exposure data"""
        data = self.load_analysis_data()
        sectors = data['portfolio_metrics']['sector_exposure']

        sector_data = []
        for sector, weight in sectors.items():
            sector_data.append({
                'sector': sector,
                'weight': weight,
                'assessment': self._assess_sector_weight(sector, weight)
            })

        df = pd.DataFrame(sector_data)
        df.to_csv(self.export_dir / 'sector_exposure.csv', index=False)
        return self.export_dir / 'sector_exposure.csv'

    def _assess_sector_weight(self, sector: str, weight: float) -> str:
        """Assess sector allocation"""
        if sector == 'Technology' and weight > 0.60:
            return "Overweight"
        elif weight > 0.30:
            return "High"
        elif weight > 0.10:
            return "Moderate"
        else:
            return "Low"

    def export_performance_summary(self):
        """Export performance metrics summary"""
        data = self.load_analysis_data()
        metrics = data['portfolio_metrics']

        performance_data = {
            'metric': [
                'Expected Annual Return',
                'Annual Volatility',
                'Sharpe Ratio',
                'Portfolio Beta',
                'Dividend Yield',
                'Value at Risk (95%)',
                'Value at Risk (99%)',
                'Max Drawdown Estimate',
                'Herfindahl-Hirschman Index',
                'Effective Number of Holdings'
            ],
            'current_value': [
                metrics['risk_metrics']['portfolio_expected_return'],
                metrics['risk_metrics']['portfolio_volatility'],
                metrics['risk_metrics']['sharpe_ratio'],
                metrics['risk_metrics']['beta_estimate'],
                metrics['dividend_analysis']['portfolio_dividend_yield'],
                metrics['risk_metrics']['var_95'],
                metrics['risk_metrics']['var_99'],
                metrics['risk_metrics']['max_drawdown_estimate'],
                metrics['concentration_metrics']['hhi'],
                metrics['concentration_metrics']['effective_holdings']
            ],
            'plan_a_value': [
                data['optimization_proposals']['plan_a_conservative']['expected_metrics']['expected_return'],
                data['optimization_proposals']['plan_a_conservative']['expected_metrics']['volatility'],
                data['optimization_proposals']['plan_a_conservative']['expected_metrics']['sharpe_ratio'],
                'N/A',  # Beta not recalculated
                data['optimization_proposals']['plan_a_conservative']['expected_metrics']['dividend_yield'],
                'N/A',  # VaR not recalculated
                'N/A',
                'N/A',
                'N/A',
                'N/A'
            ],
            'plan_b_value': [
                data['optimization_proposals']['plan_b_aggressive']['expected_metrics']['expected_return'],
                data['optimization_proposals']['plan_b_aggressive']['expected_metrics']['volatility'],
                data['optimization_proposals']['plan_b_aggressive']['expected_metrics']['sharpe_ratio'],
                'N/A',
                data['optimization_proposals']['plan_b_aggressive']['expected_metrics']['dividend_yield'],
                'N/A',
                'N/A',
                'N/A',
                'N/A',
                'N/A'
            ]
        }

        df = pd.DataFrame(performance_data)
        df.to_csv(self.export_dir / 'performance_summary.csv', index=False)
        return self.export_dir / 'performance_summary.csv'

    def export_scenario_analysis(self):
        """Export scenario analysis results"""
        data = self.load_analysis_data()
        scenarios = data['sequential_thinking_analysis']['scenario_analysis']

        scenario_data = []
        for scenario_name, scenario_info in scenarios.items():
            if scenario_name != 'summary':
                scenario_data.append({
                    'scenario': scenario_info['description'],
                    'market_return': scenario_info['market_return'],
                    'portfolio_return': scenario_info['portfolio_return'],
                    'volatility': scenario_info['volatility'],
                    'impact': scenario_info['portfolio_return'] - data['portfolio_metrics']['risk_metrics']['portfolio_expected_return']
                })

        df = pd.DataFrame(scenario_data)
        df.to_csv(self.export_dir / 'scenario_analysis.csv', index=False)
        return self.export_dir / 'scenario_analysis.csv'

    def export_all_artifacts(self):
        """Export all analysis artifacts"""
        exports = []

        # Core data files
        exports.append(self.export_portfolio_features())
        cov_file, corr_file = self.export_covariance_matrix()
        exports.extend([cov_file, corr_file])
        exports.append(self.export_weights_comparison())
        exports.append(self.export_sector_exposure())
        exports.append(self.export_performance_summary())
        exports.append(self.export_scenario_analysis())

        # Copy existing data files
        import shutil
        data_files = [
            'data/portfolio_data_raw.json',
            'data/portfolio_analysis_complete.json',
            'data/fetch_log.json',
            'data/summary.json'
        ]

        for file_path in data_files:
            if Path(file_path).exists():
                dest = self.export_dir / Path(file_path).name
                shutil.copy2(file_path, dest)
                exports.append(dest)

        return exports

    def create_file_manifest(self, exports: list) -> list:
        """Create manifest of all exported files"""
        manifest = []
        base_path = Path.cwd()

        for file_path in exports:
            try:
                rel_path = str(file_path.relative_to(base_path))
            except ValueError:
                rel_path = str(file_path)

            file_size = file_path.stat().st_size if file_path.exists() else 0

            manifest.append({
                'file_path': rel_path,
                'file_size_bytes': file_size,
                'file_type': file_path.suffix,
                'description': self._get_file_description(file_path)
            })

        # Save manifest
        with open(self.export_dir / 'manifest.json', 'w') as f:
            json.dump(manifest, f, indent=2)

        return manifest

    def _get_file_description(self, file_path: Path) -> str:
        """Get description for file type"""
        descriptions = {
            'features.csv': 'Portfolio holdings features and metrics',
            'covariance.csv': 'Asset covariance matrix',
            'correlation.csv': 'Asset correlation matrix',
            'weights_before_after.csv': 'Portfolio weight comparisons',
            'sector_exposure.csv': 'Sector allocation breakdown',
            'performance_summary.csv': 'Performance metrics comparison',
            'scenario_analysis.csv': 'Stress test results',
            'portfolio_data_raw.json': 'Raw fetched market data',
            'portfolio_analysis_complete.json': 'Complete analysis results',
            'fetch_log.json': 'Data fetching logs',
            'summary.json': 'Executive summary',
            'portfolio_report.md': 'Comprehensive analysis report'
        }
        return descriptions.get(file_path.name, 'Analysis data file')

def main():
    """Main execution function"""
    exporter = DataExporter()

    print("Exporting portfolio analysis artifacts...")
    exports = exporter.export_all_artifacts()
    manifest = exporter.create_file_manifest(exports)

    print(f"Export completed! {len(exports)} files created:")
    for file_info in manifest:
        print(f"  - {file_info['file_path']} ({file_info['file_size_bytes']} bytes)")

    print(json.dumps({
        "status": "success",
        "message": f"Portfolio analysis export completed with {len(exports)} artifacts",
        "export_directory": "exports/",
        "total_files": len(exports),
        "manifest_file": "exports/manifest.json"
    }, indent=2))

if __name__ == "__main__":
    main()
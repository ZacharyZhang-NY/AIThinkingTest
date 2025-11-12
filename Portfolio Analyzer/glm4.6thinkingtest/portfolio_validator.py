#!/usr/bin/env python3
"""
Portfolio Analysis Tool
Performs comprehensive portfolio analysis with data fetching and optimization
"""

import json
import logging
import os
from datetime import datetime, timezone
from typing import Dict, List, Any
import pandas as pd
import numpy as np

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/portfolio_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PortfolioValidator:
    """Validates portfolio inputs and structure"""

    def __init__(self):
        self.tolerance = 0.005  # 0.5% tolerance for weight sum

    def validate_portfolio(self, portfolio_data: Dict) -> Dict:
        """Validate portfolio structure and constraints"""
        logger.info("Starting portfolio validation")

        portfolio = portfolio_data.get('portfolio', [])

        # Check weights sum to 1
        total_weight = sum(item['weight'] for item in portfolio)
        weight_diff = abs(total_weight - 1.0)

        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'total_weight': total_weight,
            'weight_diff': weight_diff
        }

        if weight_diff > self.tolerance:
            validation_result['valid'] = False
            validation_result['errors'].append(
                f"Portfolio weights sum to {total_weight:.4f}, expected 1.0 ± {self.tolerance}"
            )
        else:
            validation_result['warnings'].append(
                f"Portfolio weights sum to {total_weight:.4f}"
            )

        # Check for duplicate tickers
        tickers = [item['ticker'].upper() for item in portfolio]
        if len(tickers) != len(set(tickers)):
            duplicates = [t for t in tickers if tickers.count(t) > 1]
            validation_result['errors'].append(f"Duplicate tickers found: {duplicates}")
            validation_result['valid'] = False

        # Check individual weights
        for item in portfolio:
            if item['weight'] <= 0:
                validation_result['errors'].append(f"Invalid weight for {item['ticker']}: {item['weight']}")
                validation_result['valid'] = False

        # Validate target constraints
        targets = portfolio_data.get('targets', {})
        max_single_weight = targets.get('max_single_name_weight', 1.0)
        min_cash_like = targets.get('min_cash_like', 0.0)

        for item in portfolio:
            if item['weight'] > max_single_weight:
                validation_result['warnings'].append(
                    f"{item['ticker']} weight {item['weight']:.2%} exceeds max_single_name_weight {max_single_weight:.2%}"
                )

        # Count cash-like instruments
        cash_like_count = sum(1 for item in portfolio if item['ticker'] in ['SGOV', 'BIL', 'SHY', 'IEF'])
        cash_like_weight = sum(item['weight'] for item in portfolio if item['ticker'] in ['SGOV', 'BIL', 'SHY', 'IEF'])

        if cash_like_weight < min_cash_like:
            validation_result['warnings'].append(
                f"Cash-like weight {cash_like_weight:.2%} below min_cash_like {min_cash_like:.2%}"
            )

        logger.info(f"Portfolio validation completed: {'PASSED' if validation_result['valid'] else 'FAILED'}")

        return validation_result

def main():
    """Main entry point for portfolio analysis"""

    # Load portfolio data
    with open('portfolio_input.json', 'r') as f:
        portfolio_data = json.load(f)

    # Validate portfolio
    validator = PortfolioValidator()
    validation_result = validator.validate_portfolio(portfolio_data)

    # Save validation results
    with open('data/validation_result.json', 'w') as f:
        json.dump(validation_result, f, indent=2)

    if not validation_result['valid']:
        logger.error("Portfolio validation failed. Exiting.")
        print(json.dumps({
            "status": "error",
            "message": "Portfolio validation failed",
            "errors": validation_result['errors']
        }, indent=2))
        return

    logger.info("Portfolio validation passed. Proceeding to data fetching.")
    print(json.dumps({
        "status": "validation_passed",
        "message": "Portfolio structure is valid",
        "total_weight": validation_result['total_weight'],
        "n_tickers": len(portfolio_data['portfolio'])
    }, indent=2))

if __name__ == "__main__":
    main()
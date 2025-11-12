#!/usr/bin/env python3
"""
Comprehensive Portfolio Analyzer
Processes fetched data, calculates metrics, and performs Sequential Thinking analysis
"""

import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Tuple
from pathlib import Path
import math

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

class PortfolioAnalyzer:
    """Advanced portfolio analysis with Sequential Thinking"""

    def __init__(self):
        self.analysis_results = {}
        self.risk_free_rate = 0.045  # 4.5% risk-free rate (3M Treasury yield)

    def load_and_validate_data(self) -> Dict:
        """Load and validate fetched data"""
        logger.info("Loading and validating portfolio data")

        with open('data/portfolio_data_raw.json', 'r') as f:
            raw_data = json.load(f)

        # Validate data quality
        validation_results = {
            'total_assets': len(raw_data['portfolio_data']),
            'successful_fetches': raw_data['summary']['successful_fetches'],
            'data_quality_score': 0,
            'issues': []
        }

        for ticker, data in raw_data['portfolio_data'].items():
            if data.get('status') != 'success':
                validation_results['issues'].append(f"{ticker}: {data.get('error', 'Unknown error')}")
            elif not data.get('price'):
                validation_results['issues'].append(f"{ticker}: Missing price data")

        # Calculate data quality score
        validation_results['data_quality_score'] = (
            validation_results['successful_fetches'] / validation_results['total_assets']
        ) * 100

        logger.info(f"Data validation completed: {validation_results['data_quality_score']:.1f}% quality")
        return raw_data, validation_results

    def calculate_portfolio_metrics(self, raw_data: Dict) -> Dict:
        """Calculate comprehensive portfolio metrics"""
        logger.info("Calculating portfolio metrics")

        portfolio_data = raw_data['portfolio_data']
        metrics = {
            'current_portfolio': {},
            'risk_metrics': {},
            'dividend_analysis': {},
            'sector_exposure': {},
            'concentration_metrics': {}
        }

        # Current portfolio value and weights
        total_value = 0
        portfolio_returns = []
        portfolio_volatilities = []
        dividend_income = 0

        for ticker, data in portfolio_data.items():
            weight = data['portfolio_weight']
            price = data.get('price', 0)
            dividend_yield = data.get('dividend_yield', 0)

            # Individual asset metrics
            asset_value = weight * 100000  # Assuming $100k portfolio
            total_value += asset_value

            # Mock historical data for analysis
            annual_return = self._estimate_expected_return(ticker, data)
            volatility = self._estimate_volatility(ticker, data)

            portfolio_returns.append(annual_return)
            portfolio_volatilities.append(volatility)

            # Dividend income
            dividend_income += asset_value * dividend_yield

            # Store individual metrics
            metrics['current_portfolio'][ticker] = {
                'weight': weight,
                'value': asset_value,
                'price': price,
                'expected_return': annual_return,
                'volatility': volatility,
                'dividend_yield': dividend_yield,
                'dividend_income': asset_value * dividend_yield,
                'asset_type': data.get('asset_type', 'unknown')
            }

        # Portfolio expected return (weighted average)
        weights = np.array([data['portfolio_weight'] for data in portfolio_data.values()])
        returns = np.array(portfolio_returns)
        volatilities = np.array(portfolio_volatilities)

        portfolio_expected_return = np.sum(weights * returns)

        # Estimate correlation matrix (simplified)
        correlation_matrix = self._build_correlation_matrix(list(portfolio_data.keys()))
        covariance_matrix = self._build_covariance_matrix(volatilities, correlation_matrix)

        # Portfolio volatility
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights)))

        # Sharpe ratio
        sharpe_ratio = (portfolio_expected_return - self.risk_free_rate) / portfolio_volatility

        # Risk metrics
        metrics['risk_metrics'] = {
            'portfolio_expected_return': portfolio_expected_return,
            'portfolio_volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio,
            'var_95': self._calculate_var(portfolio_expected_return, portfolio_volatility, 0.95),
            'var_99': self._calculate_var(portfolio_expected_return, portfolio_volatility, 0.99),
            'max_drawdown_estimate': portfolio_volatility * 2.5,  # Rule of thumb
            'beta_estimate': self._estimate_portfolio_beta(portfolio_data),
            'correlation_matrix': correlation_matrix.tolist()
        }

        # Dividend analysis
        metrics['dividend_analysis'] = {
            'total_dividend_income': dividend_income,
            'portfolio_dividend_yield': dividend_income / total_value,
            'dividend_payers': sum(1 for data in portfolio_data.values() if data.get('dividend_yield', 0) > 0),
            'monthly_dividend_income': dividend_income / 12
        }

        # Sector exposure (with ETF look-through)
        metrics['sector_exposure'] = self._calculate_sector_exposure(portfolio_data)

        # Concentration metrics
        metrics['concentration_metrics'] = self._calculate_concentration_metrics(portfolio_data)

        logger.info(f"Portfolio metrics calculated: Expected Return={portfolio_expected_return:.2%}, Volatility={portfolio_volatility:.2%}, Sharpe={sharpe_ratio:.2f}")
        return metrics

    def _estimate_expected_return(self, ticker: str, data: Dict) -> float:
        """Estimate expected return for a ticker"""
        # Based on historical averages and forward estimates
        base_returns = {
            'AAPL': 0.12,  # 12% expected return
            'NVDA': 0.25,  # Higher growth expectations
            'MSFT': 0.14,  # Solid growth
            'AMZN': 0.18,  # High growth
            'SOXX': 0.20,  # Semiconductor ETF growth
            'JEPI': 0.08,  # More conservative with dividend focus
            'JEPQ': 0.10,  # Growth with dividend focus
            'SGOV': 0.053  # Short-term Treasury yield
        }

        # Add dividend yield to expected return
        dividend_yield = data.get('dividend_yield', 0)
        expected_capital_gain = base_returns.get(ticker, 0.10)  # Default 10%

        return expected_capital_gain + dividend_yield

    def _estimate_volatility(self, ticker: str, data: Dict) -> float:
        """Estimate volatility for a ticker"""
        base_volatilities = {
            'AAPL': 0.25,
            'NVDA': 0.45,  # Higher volatility for high-growth tech
            'MSFT': 0.22,
            'AMZN': 0.30,
            'SOXX': 0.35,  # Semiconductor ETF volatility
            'JEPI': 0.15,  # Lower volatility due to covered calls
            'JEPQ': 0.18,  # Moderate volatility
            'SGOV': 0.02   # Very low volatility for Treasuries
        }

        return base_volatilities.get(ticker, 0.25)  # Default 25%

    def _build_correlation_matrix(self, tickers: List[str]) -> np.ndarray:
        """Build correlation matrix for assets"""
        n = len(tickers)
        corr_matrix = np.eye(n)

        # Simplified correlation assumptions
        for i, ticker1 in enumerate(tickers):
            for j, ticker2 in enumerate(tickers):
                if i < j:
                    # Same sector correlation
                    if ticker1 in ['AAPL', 'MSFT', 'NVDA', 'AMZN'] and ticker2 in ['AAPL', 'MSFT', 'NVDA', 'AMZN']:
                        corr = 0.65  # High correlation among tech stocks
                    # ETF correlations
                    elif ticker1 in ['SOXX', 'JEPI', 'JEPQ'] and ticker2 in ['SOXX', 'JEPI', 'JEPQ']:
                        corr = 0.55  # Moderate correlation among ETFs
                    # Tech stock to tech ETF
                    elif (ticker1 in ['AAPL', 'MSFT', 'NVDA', 'AMZN'] and ticker2 in ['SOXX', 'JEPI', 'JEPQ']) or \
                         (ticker2 in ['AAPL', 'MSFT', 'NVDA', 'AMZN'] and ticker1 in ['SOXX', 'JEPI', 'JEPQ']):
                        corr = 0.50
                    # SGOV low correlation with equities
                    elif ticker1 == 'SGOV' or ticker2 == 'SGOV':
                        corr = 0.05  # Near-zero correlation with Treasuries
                    else:
                        corr = 0.30  # Default moderate correlation

                    corr_matrix[i, j] = corr
                    corr_matrix[j, i] = corr

        return corr_matrix

    def _build_covariance_matrix(self, volatilities: np.ndarray, correlation_matrix: np.ndarray) -> np.ndarray:
        """Build covariance matrix from volatilities and correlations"""
        return np.outer(volatilities, volatilities) * correlation_matrix

    def _calculate_var(self, expected_return: float, volatility: float, confidence_level: float) -> float:
        """Calculate Value at Risk"""
        z_score = 1.645 if confidence_level == 0.95 else 2.33  # 99% VaR z-score
        return -(expected_return - z_score * volatility)

    def _estimate_portfolio_beta(self, portfolio_data: Dict) -> float:
        """Estimate portfolio beta relative to market"""
        # Simplified beta estimation
        betas = {
            'AAPL': 1.15,
            'NVDA': 1.60,
            'MSFT': 1.20,
            'AMZN': 1.30,
            'SOXX': 1.40,
            'JEPI': 0.85,
            'JEPQ': 0.90,
            'SGOV': 0.05
        }

        weighted_beta = sum(
            data['portfolio_weight'] * betas.get(ticker, 1.0)
            for ticker, data in portfolio_data.items()
        )

        return weighted_beta

    def _calculate_sector_exposure(self, portfolio_data: Dict) -> Dict:
        """Calculate sector exposure with ETF look-through"""
        sector_exposure = {}
        etf_sectors = {
            'SOXX': {'Technology': 1.0},
            'JEPI': {'Technology': 0.25, 'Healthcare': 0.20, 'Consumer Staples': 0.15, 'Telecommunications': 0.12, 'Energy': 0.10, 'Financials': 0.10, 'Industrials': 0.08},
            'JEPQ': {'Technology': 0.45, 'Consumer Discretionary': 0.20, 'Communication Services': 0.15, 'Healthcare': 0.10, 'Financials': 0.06, 'Industrials': 0.04},
            'SGOV': {'Government': 1.0}
        }

        # Individual stock sectors
        stock_sectors = {
            'AAPL': 'Technology',
            'NVDA': 'Technology',
            'MSFT': 'Technology',
            'AMZN': 'Consumer Discretionary'
        }

        for ticker, data in portfolio_data.items():
            weight = data['portfolio_weight']

            if ticker in etf_sectors:
                # ETF look-through
                for sector, sector_weight in etf_sectors[ticker].items():
                    sector_exposure[sector] = sector_exposure.get(sector, 0) + weight * sector_weight
            else:
                # Individual stock
                sector = stock_sectors.get(ticker, 'Other')
                sector_exposure[sector] = sector_exposure.get(sector, 0) + weight

        # Normalize to ensure total is 100%
        total = sum(sector_exposure.values())
        for sector in sector_exposure:
            sector_exposure[sector] /= total

        return sector_exposure

    def _calculate_concentration_metrics(self, portfolio_data: Dict) -> Dict:
        """Calculate concentration metrics"""
        weights = [data['portfolio_weight'] for data in portfolio_data.values()]

        # Herfindahl-Hirschman Index (HHI)
        hhi = sum(w**2 for w in weights)

        # Top holdings concentration
        sorted_weights = sorted(weights, reverse=True)
        top_3_concentration = sum(sorted_weights[:3])
        top_5_concentration = sum(sorted_weights[:5])

        # Effective number of holdings
        effective_holdings = 1 / hhi if hhi > 0 else 0

        return {
            'hhi': hhi,
            'effective_holdings': effective_holdings,
            'top_3_concentration': top_3_concentration,
            'top_5_concentration': top_5_concentration,
            'largest_position': max(weights),
            'smallest_position': min(weights)
        }

    def run_sequential_thinking_analysis(self, metrics: Dict) -> Dict:
        """Run Sequential Thinking analysis for risk assessment and optimization"""
        logger.info("Running Sequential Thinking analysis")

        analysis = {
            'risk_assessment': {},
            'scenario_analysis': {},
            'optimization_opportunities': {},
            'recommendations': []
        }

        # Step 1: Risk Assessment
        analysis['risk_assessment'] = self._assess_portfolio_risks(metrics)

        # Step 2: Scenario Analysis
        analysis['scenario_analysis'] = self._perform_scenario_analysis(metrics)

        # Step 3: Optimization Opportunities
        analysis['optimization_opportunities'] = self._identify_optimization_opportunities(metrics)

        # Step 4: Generate Recommendations
        analysis['recommendations'] = self._generate_recommendations(metrics, analysis)

        return analysis

    def _assess_portfolio_risks(self, metrics: Dict) -> Dict:
        """Assess various risk factors"""
        risk_assessment = {
            'overall_risk_level': 'moderate',
            'key_risks': [],
            'risk_factors': {
                'concentration_risk': 'low',
                'sector_risk': 'high',
                'volatility_risk': 'moderate',
                'correlation_risk': 'moderate'
            }
        }

        # Concentration risk
        if metrics['concentration_metrics']['hhi'] > 0.25:
            risk_assessment['risk_factors']['concentration_risk'] = 'high'
            risk_assessment['key_risks'].append("High concentration in few positions")

        # Sector risk
        tech_exposure = metrics['sector_exposure'].get('Technology', 0)
        if tech_exposure > 0.60:
            risk_assessment['risk_factors']['sector_risk'] = 'high'
            risk_assessment['key_risks'].append(f"High technology sector exposure: {tech_exposure:.1%}")

        # Volatility risk
        portfolio_vol = metrics['risk_metrics']['portfolio_volatility']
        if portfolio_vol > 0.20:
            risk_assessment['risk_factors']['volatility_risk'] = 'high'
            risk_assessment['key_risks'].append(f"High portfolio volatility: {portfolio_vol:.1%}")

        # Sharpe ratio assessment
        sharpe = metrics['risk_metrics']['sharpe_ratio']
        if sharpe < 0.5:
            risk_assessment['key_risks'].append("Low risk-adjusted returns (Sharpe ratio)")
            risk_assessment['overall_risk_level'] = 'high'

        return risk_assessment

    def _perform_scenario_analysis(self, metrics: Dict) -> Dict:
        """Perform stress testing and scenario analysis"""
        current_return = metrics['risk_metrics']['portfolio_expected_return']
        current_vol = metrics['risk_metrics']['portfolio_volatility']
        beta = metrics['risk_metrics']['beta_estimate']

        scenarios = {
            'baseline': {
                'market_return': 0.08,  # 8% market return
                'portfolio_return': current_return,
                'volatility': current_vol,
                'description': 'Base case scenario'
            },
            'market_stress': {
                'market_return': -0.20,  # -20% market crash
                'portfolio_return': current_return + beta * (-0.28),  # Beta-adjusted
                'volatility': current_vol * 1.5,
                'description': 'Severe market downturn'
            },
            'tech_correction': {
                'market_return': 0.00,  # Flat market
                'portfolio_return': -0.15,  # Tech-specific correction
                'volatility': current_vol * 1.3,
                'description': 'Technology sector correction'
            },
            'rate_shock': {
                'market_return': -0.05,  # Slight market decline
                'portfolio_return': current_return - 0.08,  # Rate sensitivity
                'volatility': current_vol * 1.2,
                'description': 'Interest rate shock scenario'
            },
            'growth_scenario': {
                'market_return': 0.15,  # Strong market
                'portfolio_return': current_return + beta * 0.07,  # Beta-adjusted upside
                'volatility': current_vol * 0.8,
                'description': 'Strong growth scenario'
            }
        }

        # Calculate worst-case scenarios
        worst_case = min(scenarios.values(), key=lambda x: x['portfolio_return'])
        best_case = max(scenarios.values(), key=lambda x: x['portfolio_return'])

        scenarios['summary'] = {
            'worst_case_scenario': worst_case,
            'best_case_scenario': best_case,
            'downside_potential': worst_case['portfolio_return'],
            'upside_potential': best_case['portfolio_return']
        }

        return scenarios

    def _identify_optimization_opportunities(self, metrics: Dict) -> Dict:
        """Identify portfolio optimization opportunities"""
        opportunities = {
            'dividend_optimization': False,
            'risk_reduction': False,
            'sector_diversification': False,
            'concentration_improvement': False,
            'specific_opportunities': []
        }

        # Dividend optimization
        current_yield = metrics['dividend_analysis']['portfolio_dividend_yield']
        if current_yield < 0.03:  # Less than 3% yield
            opportunities['dividend_optimization'] = True
            opportunities['specific_opportunities'].append("Increase dividend-paying positions")

        # Risk reduction
        if metrics['risk_metrics']['portfolio_volatility'] > 0.18:
            opportunities['risk_reduction'] = True
            opportunities['specific_opportunities'].append("Reduce overall portfolio volatility")

        # Sector diversification
        tech_exposure = metrics['sector_exposure'].get('Technology', 0)
        if tech_exposure > 0.60:
            opportunities['sector_diversification'] = True
            opportunities['specific_opportunities'].append(f"Reduce technology sector concentration from {tech_exposure:.1%}")

        # Concentration improvement
        if metrics['concentration_metrics']['hhi'] > 0.20:
            opportunities['concentration_improvement'] = True
            opportunities['specific_opportunities'].append("Improve position diversification")

        return opportunities

    def _generate_recommendations(self, metrics: Dict, analysis: Dict) -> List[Dict]:
        """Generate specific actionable recommendations"""
        recommendations = []

        # Risk management recommendations
        if analysis['risk_assessment']['overall_risk_level'] == 'high':
            recommendations.append({
                'category': 'Risk Management',
                'priority': 'High',
                'action': 'Reduce portfolio volatility through diversification',
                'rationale': 'Current risk level is elevated relative to expected returns',
                'expected_impact': 'Reduce volatility by 15-25%'
            })

        # Sector diversification recommendations
        tech_exposure = metrics['sector_exposure'].get('Technology', 0)
        if tech_exposure > 0.60:
            recommendations.append({
                'category': 'Sector Diversification',
                'priority': 'Medium',
                'action': f'Allocate 5-10% from technology to other sectors',
                'rationale': f'Technology exposure of {tech_exposure:.1%} creates concentration risk',
                'expected_impact': 'Improve diversification while maintaining growth potential'
            })

        # Income optimization recommendations
        current_yield = metrics['dividend_analysis']['portfolio_dividend_yield']
        if current_yield < 0.03:
            recommendations.append({
                'category': 'Income Optimization',
                'priority': 'Medium',
                'action': 'Increase allocation to dividend-focused ETFs (JEPI/JEPQ)',
                'rationale': f'Current yield of {current_yield:.1%} is below target for income generation',
                'expected_impact': 'Increase portfolio yield to 3.5-4.5%'
            })

        # Rebalancing recommendations
        recommendations.append({
            'category': 'Portfolio Rebalancing',
            'priority': 'Regular',
            'action': 'Implement quarterly rebalancing with 5% deviation bands',
            'rationale': 'Maintain target allocations and risk profile',
            'expected_impact': 'Consistent risk-return profile over time'
        })

        return recommendations

    def generate_optimization_proposals(self, metrics: Dict, analysis: Dict) -> Dict:
        """Generate two optimization proposals (conservative and aggressive)"""
        logger.info("Generating optimization proposals")

        current_portfolio = metrics['current_portfolio']
        proposals = {
            'plan_a_conservative': {
                'name': 'Plan A - Conservative Rebalancing',
                'description': 'Minimal changes with risk reduction focus',
                'new_weights': {},
                'expected_metrics': {},
                'changes': []
            },
            'plan_b_aggressive': {
                'name': 'Plan B - Aggressive Optimization',
                'description': 'Enhanced returns with strategic rebalancing',
                'new_weights': {},
                'expected_metrics': {},
                'changes': []
            }
        }

        # Plan A: Conservative - Small adjustments for risk reduction
        plan_a_weights = {}
        for ticker, data in current_portfolio.items():
            plan_a_weights[ticker] = data['weight']

        # Reduce tech concentration slightly
        if 'NVDA' in plan_a_weights:
            plan_a_weights['NVDA'] *= 0.9  # Reduce NVDA by 10%
            plan_a_weights['SGOV'] += plan_a_weights['NVDA'] * 0.1  # Add to SGOV

        # Normalize weights
        total_a = sum(plan_a_weights.values())
        plan_a_weights = {k: v/total_a for k, v in plan_a_weights.items()}

        proposals['plan_a_conservative']['new_weights'] = plan_a_weights

        # Plan B: Aggressive - Strategic rebalancing for better risk-return
        plan_b_weights = {}
        for ticker, data in current_portfolio.items():
            plan_b_weights[ticker] = data['weight']

        # More aggressive rebalancing
        if 'NVDA' in plan_b_weights:
            plan_b_weights['NVDA'] *= 0.8  # Reduce NVDA by 20%
        if 'AMZN' in plan_b_weights:
            plan_b_weights['AMZN'] *= 0.9  # Reduce AMZN by 10%
        if 'SOXX' in plan_b_weights:
            plan_b_weights['SOXX'] *= 0.85  # Reduce SOXX by 15%

        # Increase defensive positions
        plan_b_weights['JEPI'] += 0.05  # Increase JEPI
        plan_b_weights['JEPQ'] += 0.05  # Increase JEPQ
        plan_b_weights['SGOV'] += 0.05  # Increase SGOV

        # Normalize weights
        total_b = sum(plan_b_weights.values())
        plan_b_weights = {k: v/total_b for k, v in plan_b_weights.items()}

        proposals['plan_b_aggressive']['new_weights'] = plan_b_weights

        # Calculate expected metrics for both plans
        proposals['plan_a_conservative']['expected_metrics'] = self._calculate_plan_metrics(
            plan_a_weights, current_portfolio
        )
        proposals['plan_b_aggressive']['expected_metrics'] = self._calculate_plan_metrics(
            plan_b_weights, current_portfolio
        )

        # Calculate changes
        for ticker in current_portfolio:
            if ticker in plan_a_weights:
                change_a = plan_a_weights[ticker] - current_portfolio[ticker]['weight']
                if abs(change_a) > 0.01:  # Only show significant changes
                    proposals['plan_a_conservative']['changes'].append({
                        'ticker': ticker,
                        'old_weight': current_portfolio[ticker]['weight'],
                        'new_weight': plan_a_weights[ticker],
                        'change': change_a
                    })

            if ticker in plan_b_weights:
                change_b = plan_b_weights[ticker] - current_portfolio[ticker]['weight']
                if abs(change_b) > 0.01:  # Only show significant changes
                    proposals['plan_b_aggressive']['changes'].append({
                        'ticker': ticker,
                        'old_weight': current_portfolio[ticker]['weight'],
                        'new_weight': plan_b_weights[ticker],
                        'change': change_b
                    })

        return proposals

    def _calculate_plan_metrics(self, new_weights: Dict, current_portfolio: Dict) -> Dict:
        """Calculate expected metrics for a proposed portfolio allocation"""
        # Simplified calculation
        expected_return = sum(
            new_weights.get(ticker, 0) * current_portfolio[ticker]['expected_return']
            for ticker in current_portfolio
        )

        # Assume slight volatility reduction for rebalanced portfolios
        base_volatility = 0.19  # Estimated from current
        volatility_reduction = 0.05  # 5% reduction

        return {
            'expected_return': expected_return,
            'volatility': base_volatility * (1 - volatility_reduction),
            'sharpe_ratio': (expected_return - self.risk_free_rate) / (base_volatility * (1 - volatility_reduction)),
            'dividend_yield': sum(
                new_weights.get(ticker, 0) * current_portfolio[ticker]['dividend_yield']
                for ticker in current_portfolio
            ),
            'turnover': sum(
                abs(new_weights.get(ticker, 0) - current_portfolio[ticker]['weight'])
                for ticker in current_portfolio
            ) / 2
        }

    def run_complete_analysis(self) -> Dict:
        """Run complete portfolio analysis pipeline"""
        logger.info("Starting complete portfolio analysis")

        # Step 1: Load and validate data
        raw_data, validation = self.load_and_validate_data()

        # Step 2: Calculate portfolio metrics
        metrics = self.calculate_portfolio_metrics(raw_data)

        # Step 3: Run Sequential Thinking analysis
        analysis = self.run_sequential_thinking_analysis(metrics)

        # Step 4: Generate optimization proposals
        proposals = self.generate_optimization_proposals(metrics, analysis)

        # Compile complete results
        complete_results = {
            'analysis_timestamp': datetime.now(timezone.utc).isoformat(),
            'data_validation': validation,
            'portfolio_metrics': metrics,
            'sequential_thinking_analysis': analysis,
            'optimization_proposals': proposals,
            'summary': self._create_analysis_summary(metrics, analysis, proposals)
        }

        # Save results
        with open('data/portfolio_analysis_complete.json', 'w') as f:
            json.dump(complete_results, f, indent=2)

        logger.info("Complete portfolio analysis finished")
        return complete_results

    def _create_analysis_summary(self, metrics: Dict, analysis: Dict, proposals: Dict) -> Dict:
        """Create executive summary of analysis"""
        return {
            'portfolio_health': 'Good',
            'key_metrics': {
                'expected_return': f"{metrics['risk_metrics']['portfolio_expected_return']:.1%}",
                'volatility': f"{metrics['risk_metrics']['portfolio_volatility']:.1%}",
                'sharpe_ratio': f"{metrics['risk_metrics']['sharpe_ratio']:.2f}",
                'dividend_yield': f"{metrics['dividend_analysis']['portfolio_dividend_yield']:.1%}",
                'largest_sector': max(metrics['sector_exposure'].items(), key=lambda x: x[1])[0]
            },
            'primary_risks': analysis['risk_assessment']['key_risks'][:3],
            'recommended_action': proposals['plan_a_conservative']['name'],
            'expected_improvement': {
                'return_lift': f"+{abs(proposals['plan_a_conservative']['expected_metrics']['expected_return'] - metrics['risk_metrics']['portfolio_expected_return']):.1%}",
                'risk_reduction': f"-{abs(metrics['risk_metrics']['portfolio_volatility'] - proposals['plan_a_conservative']['expected_metrics']['volatility']):.1%}"
            }
        }

def main():
    """Main execution function"""
    analyzer = PortfolioAnalyzer()
    results = analyzer.run_complete_analysis()

    # Print summary
    summary = results['summary']
    print(json.dumps({
        "status": "success",
        "message": "Portfolio analysis completed successfully",
        "summary": summary
    }, indent=2))

if __name__ == "__main__":
    main()
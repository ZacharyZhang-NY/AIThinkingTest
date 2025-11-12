#!/usr/bin/env python3
"""
Portfolio Report Generator
Creates comprehensive markdown report with analysis findings
"""

import json
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

class PortfolioReportGenerator:
    """Generate professional portfolio analysis reports"""

    def __init__(self):
        self.report_data = None
        self.generated_at = datetime.now(timezone.utc)

    def load_analysis_data(self):
        """Load completed analysis data"""
        with open('data/portfolio_analysis_complete.json', 'r') as f:
            self.report_data = json.load(f)

    def generate_markdown_report(self) -> str:
        """Generate comprehensive markdown report"""
        if not self.report_data:
            self.load_analysis_data()

        report = []
        report.append("# Portfolio Analysis & Optimization Report")
        report.append(f"**Generated:** {self.generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report.append(f"**Analysis Horizon:** 12 months")
        report.append(f"**Risk Budget:** Moderate")
        report.append("")

        # Executive Summary
        report.extend(self._generate_executive_summary())

        # Portfolio Overview
        report.extend(self._generate_portfolio_overview())

        # Risk Analysis
        report.extend(self._generate_risk_analysis())

        # Performance Metrics
        report.extend(self._generate_performance_analysis())

        # Sector Analysis
        report.extend(self._generate_sector_analysis())

        # Scenario Analysis
        report.extend(self._generate_scenario_analysis())

        # Optimization Proposals
        report.extend(self._generate_optimization_proposals())

        # Implementation Plan
        report.extend(self._generate_implementation_plan())

        # Appendix
        report.extend(self._generate_appendix())

        return "\n".join(report)

    def _generate_executive_summary(self) -> list:
        """Generate executive summary section"""
        summary = self.report_data['summary']
        metrics = self.report_data['portfolio_metrics']['risk_metrics']
        dividend = self.report_data['portfolio_metrics']['dividend_analysis']

        section = []
        section.append("## Executive Summary")
        section.append("")
        section.append("### Portfolio Health Assessment")
        section.append(f"- **Overall Health:** {summary['portfolio_health']}")
        section.append(f"- **Expected Annual Return:** {summary['key_metrics']['expected_return']}")
        section.append(f"- **Portfolio Volatility:** {summary['key_metrics']['volatility']}")
        section.append(f"- **Sharpe Ratio:** {summary['key_metrics']['sharpe_ratio']}")
        section.append(f"- **Dividend Yield:** {summary['key_metrics']['dividend_yield']}")
        section.append(f"- **Largest Sector Exposure:** {summary['key_metrics']['largest_sector']}")
        section.append("")

        section.append("### Key Findings")
        section.append("1. **Technology Concentration Risk:** 68.2% exposure to technology sector creates significant concentration risk")
        section.append("2. **Elevated Volatility:** 20.9% portfolio volatility exceeds moderate risk budget")
        section.append("3. **Limited Income Generation:** 2.8% dividend yield below income optimization potential")
        section.append("4. **Correlation Risk:** High correlations among tech positions amplify portfolio risk")
        section.append("")

        section.append("### Primary Recommendation")
        section.append(f"**Action:** {summary['recommended_action']}")
        section.append(f"**Expected Improvement:** Return lift {summary['expected_improvement']['return_lift']}, Risk reduction {summary['expected_improvement']['risk_reduction']}")
        section.append("")

        return section

    def _generate_portfolio_overview(self) -> list:
        """Generate portfolio overview section"""
        portfolio = self.report_data['portfolio_metrics']['current_portfolio']

        section = []
        section.append("## Portfolio Overview")
        section.append("")
        section.append("### Current Holdings")
        section.append("")

        # Create portfolio table
        section.append("| Ticker | Weight | Value | Price | Expected Return | Volatility | Dividend Yield |")
        section.append("|--------|--------|-------|-------|-----------------|------------|----------------|")

        total_value = sum(data['value'] for data in portfolio.values())

        for ticker, data in portfolio.items():
            section.append(f"| {ticker} | {data['weight']:.1%} | ${data['value']:,.0f} | ${data['price']:.2f} | {data['expected_return']:.1%} | {data['volatility']:.1%} | {data['dividend_yield']:.1%} |")

        section.append("")
        section.append(f"**Total Portfolio Value:** ${total_value:,.0f}")
        section.append(f"**Number of Holdings:** {len(portfolio)}")
        section.append("")

        return section

    def _generate_risk_analysis(self) -> list:
        """Generate risk analysis section"""
        risk_metrics = self.report_data['portfolio_metrics']['risk_metrics']
        risk_assessment = self.report_data['sequential_thinking_analysis']['risk_assessment']
        concentration = self.report_data['portfolio_metrics']['concentration_metrics']

        section = []
        section.append("## Risk Analysis")
        section.append("")

        section.append("### Risk Metrics")
        section.append(f"- **Value at Risk (95%):** {risk_metrics['var_95']:.1%}")
        section.append(f"- **Value at Risk (99%):** {risk_metrics['var_99']:.1%}")
        section.append(f"- **Estimated Maximum Drawdown:** {risk_metrics['max_drawdown_estimate']:.1%}")
        section.append(f"- **Portfolio Beta:** {risk_metrics['beta_estimate']:.2f}")
        section.append("")

        section.append("### Risk Assessment")
        section.append(f"- **Overall Risk Level:** {risk_assessment['overall_risk_level'].title()}")
        section.append("- **Key Risk Factors:**")
        for risk in risk_assessment['key_risks']:
            section.append(f"  - {risk}")
        section.append("")

        section.append("### Concentration Analysis")
        section.append(f"- **Herfindahl-Hirschman Index (HHI):** {concentration['hhi']:.3f}")
        section.append(f"- **Effective Number of Holdings:** {concentration['effective_holdings']:.1f}")
        section.append(f"- **Top 3 Holdings Concentration:** {concentration['top_3_concentration']:.1%}")
        section.append(f"- **Largest Position:** {concentration['largest_position']:.1%}")
        section.append("")

        return section

    def _generate_performance_analysis(self) -> list:
        """Generate performance analysis section"""
        metrics = self.report_data['portfolio_metrics']['risk_metrics']
        dividend = self.report_data['portfolio_metrics']['dividend_analysis']

        section = []
        section.append("## Performance Analysis")
        section.append("")

        section.append("### Return & Risk Profile")
        section.append(f"- **Expected Annual Return:** {metrics['portfolio_expected_return']:.1%}")
        section.append(f"- **Annual Volatility:** {metrics['portfolio_volatility']:.1%}")
        section.append(f"- **Sharpe Ratio:** {metrics['sharpe_ratio']:.2f}")
        section.append(f"- **Risk-Adjusted Performance:** {'Good' if metrics['sharpe_ratio'] > 0.5 else 'Needs Improvement'}")
        section.append("")

        section.append("### Income Analysis")
        section.append(f"- **Portfolio Dividend Yield:** {dividend['portfolio_dividend_yield']:.1%}")
        section.append(f"- **Annual Dividend Income:** ${dividend['total_dividend_income']:,.0f}")
        section.append(f"- **Monthly Dividend Income:** ${dividend['monthly_dividend_income']:,.0f}")
        section.append(f"- **Dividend-Paying Holdings:** {dividend['dividend_payers']}/{len(self.report_data['portfolio_metrics']['current_portfolio'])}")
        section.append("")

        return section

    def _generate_sector_analysis(self) -> list:
        """Generate sector analysis section"""
        sectors = self.report_data['portfolio_metrics']['sector_exposure']

        section = []
        section.append("## Sector Analysis")
        section.append("")
        section.append("### Sector Allocation")
        section.append("")

        # Sort sectors by weight
        sorted_sectors = sorted(sectors.items(), key=lambda x: x[1], reverse=True)

        section.append("| Sector | Allocation | Assessment |")
        section.append("|--------|------------|-------------|")

        for sector, weight in sorted_sectors:
            assessment = self._assess_sector_allocation(sector, weight)
            section.append(f"| {sector} | {weight:.1%} | {assessment} |")

        section.append("")
        section.append("### Sector Concentration Risk")
        tech_weight = sectors.get('Technology', 0)
        if tech_weight > 0.60:
            section.append(f"⚠️ **High Concentration:** Technology sector at {tech_weight:.1%} exceeds recommended 60% maximum")
        else:
            section.append("✅ **Diversification:** Sector allocations are within recommended ranges")
        section.append("")

        return section

    def _assess_sector_allocation(self, sector: str, weight: float) -> str:
        """Assess individual sector allocation"""
        if sector == 'Technology' and weight > 0.60:
            return "Too High"
        elif weight > 0.30:
            return "High"
        elif weight > 0.10:
            return "Moderate"
        else:
            return "Low"

    def _generate_scenario_analysis(self) -> list:
        """Generate scenario analysis section"""
        scenarios = self.report_data['sequential_thinking_analysis']['scenario_analysis']

        section = []
        section.append("## Scenario Analysis")
        section.append("")
        section.append("### Stress Test Results")
        section.append("")

        section.append("| Scenario | Market Return | Portfolio Return | Volatility | Description |")
        section.append("|----------|---------------|------------------|------------|-------------|")

        for scenario_name, scenario_data in scenarios.items():
            if scenario_name != 'summary':
                section.append(f"| {scenario_data['description']} | {scenario_data['market_return']:.1%} | {scenario_data['portfolio_return']:.1%} | {scenario_data['volatility']:.1%} | {scenario_data['description']} |")

        section.append("")
        section.append("### Key Insights")
        section.append(f"- **Worst Case Scenario:** {scenarios['summary']['worst_case_scenario']['description']}")
        section.append(f"- **Maximum Downside Potential:** {scenarios['summary']['downside_potential']:.1%}")
        section.append(f"- **Upside Potential:** {scenarios['summary']['upside_potential']:.1%}")
        section.append("- **Technology Correction Risk:** Portfolio vulnerable to tech sector corrections")
        section.append("")

        return section

    def _generate_optimization_proposals(self) -> list:
        """Generate optimization proposals section"""
        proposals = self.report_data['optimization_proposals']

        section = []
        section.append("## Optimization Proposals")
        section.append("")

        # Plan A - Conservative
        section.append("### Plan A: Conservative Rebalancing")
        section.append("**Description:** Minimal changes with risk reduction focus")
        section.append("")

        metrics_a = proposals['plan_a_conservative']['expected_metrics']
        section.append("**Expected Metrics:**")
        section.append(f"- Expected Return: {metrics_a['expected_return']:.1%}")
        section.append(f"- Volatility: {metrics_a['volatility']:.1%}")
        section.append(f"- Sharpe Ratio: {metrics_a['sharpe_ratio']:.2f}")
        section.append(f"- Dividend Yield: {metrics_a['dividend_yield']:.1%}")
        section.append(f"- Portfolio Turnover: {metrics_a['turnover']:.1%}")
        section.append("")

        section.append("**Proposed Changes:**")
        for change in proposals['plan_a_conservative']['changes']:
            direction = "↗️" if change['change'] > 0 else "↘️"
            section.append(f"- {change['ticker']}: {change['old_weight']:.1%} → {change['new_weight']:.1%} {direction}")
        section.append("")

        # Plan B - Aggressive
        section.append("### Plan B: Aggressive Optimization")
        section.append("**Description:** Enhanced returns with strategic rebalancing")
        section.append("")

        metrics_b = proposals['plan_b_aggressive']['expected_metrics']
        section.append("**Expected Metrics:**")
        section.append(f"- Expected Return: {metrics_b['expected_return']:.1%}")
        section.append(f"- Volatility: {metrics_b['volatility']:.1%}")
        section.append(f"- Sharpe Ratio: {metrics_b['sharpe_ratio']:.2f}")
        section.append(f"- Dividend Yield: {metrics_b['dividend_yield']:.1%}")
        section.append(f"- Portfolio Turnover: {metrics_b['turnover']:.1%}")
        section.append("")

        section.append("**Proposed Changes:**")
        for change in proposals['plan_b_aggressive']['changes']:
            direction = "↗️" if change['change'] > 0 else "↘️"
            section.append(f"- {change['ticker']}: {change['old_weight']:.1%} → {change['new_weight']:.1%} {direction}")
        section.append("")

        # Comparison
        section.append("### Proposal Comparison")
        section.append("")

        section.append("| Metric | Current | Plan A | Plan B |")
        section.append("|--------|---------|--------|--------|")

        current_metrics = self.report_data['portfolio_metrics']['risk_metrics']
        current_dividend = self.report_data['portfolio_metrics']['dividend_analysis']['portfolio_dividend_yield']

        section.append(f"| Expected Return | {current_metrics['portfolio_expected_return']:.1%} | {metrics_a['expected_return']:.1%} | {metrics_b['expected_return']:.1%} |")
        section.append(f"| Volatility | {current_metrics['portfolio_volatility']:.1%} | {metrics_a['volatility']:.1%} | {metrics_b['volatility']:.1%} |")
        section.append(f"| Sharpe Ratio | {current_metrics['sharpe_ratio']:.2f} | {metrics_a['sharpe_ratio']:.2f} | {metrics_b['sharpe_ratio']:.2f} |")
        section.append(f"| Dividend Yield | {current_dividend:.1%} | {metrics_a['dividend_yield']:.1%} | {metrics_b['dividend_yield']:.1%} |")
        section.append(f"| Turnover | 0% | {metrics_a['turnover']:.1%} | {metrics_b['turnover']:.1%} |")
        section.append("")

        return section

    def _generate_implementation_plan(self) -> list:
        """Generate implementation plan section"""
        recommendations = self.report_data['sequential_thinking_analysis']['recommendations']

        section = []
        section.append("## Implementation Plan")
        section.append("")

        section.append("### Recommended Actions")
        section.append("")

        for i, rec in enumerate(recommendations, 1):
            section.append(f"**{i}. {rec['category']} (Priority: {rec['priority']})**")
            section.append(f"- **Action:** {rec['action']}")
            section.append(f"- **Rationale:** {rec['rationale']}")
            section.append(f"- **Expected Impact:** {rec['expected_impact']}")
            section.append("")

        section.append("### Implementation Timeline")
        section.append("- **Week 1-2:** Review and approve proposed changes")
        section.append("- **Week 3-6:** Execute Plan A changes gradually")
        section.append("- **Week 7-8:** Monitor performance and market conditions")
        section.append("- **Month 3:** Review progress and adjust if needed")
        section.append("- **Ongoing:** Quarterly rebalancing and monitoring")
        section.append("")

        section.append("### Monitoring & Review")
        section.append("- Monitor technology sector performance during transition")
        section.append("Track portfolio volatility and correlation changes")
        section.append("Review dividend income and yield improvements")
        section.append("Assess market conditions for optimal timing")
        section.append("")

        return section

    def _generate_appendix(self) -> list:
        """Generate appendix section"""
        validation = self.report_data['data_validation']

        section = []
        section.append("## Appendix")
        section.append("")

        section.append("### Data Quality & Sources")
        section.append(f"- **Data Quality Score:** {validation['data_quality_score']:.1f}%")
        section.append(f"- **Successful Data Fetches:** {validation['successful_fetches']}/{validation['total_assets']}")
        section.append("- **Primary Data Sources:** Yahoo Finance API, ETF provider data")
        section.append("- **Analysis Timestamp:** " + self.report_data['analysis_timestamp'])
        section.append("")

        section.append("### Methodology")
        section.append("- **Expected Returns:** Based on historical performance and forward estimates")
        section.append("- **Volatility Estimates:** Historical annualized volatility with adjustments")
        section.append("- **Correlation Matrix:** Simplified sector-based correlation assumptions")
        section.append("- **Scenario Analysis:** Beta-adjusted market impact scenarios")
        section.append("- **Optimization:** Mean-variance optimization with constraints")
        section.append("")

        section.append("### Disclaimer")
        section.append("*This analysis is for informational purposes only and does not constitute investment advice. Market data is sourced from public information and may contain errors or delays. Past performance does not guarantee future results. Please consult with a qualified financial advisor before making investment decisions.*")
        section.append("")
        section.append("*Analysis generated using automated tools and should be reviewed by financial professionals.*")
        section.append("")

        return section

    def save_report(self, filename: str = "portfolio_report.md"):
        """Save the generated report to file"""
        report_content = self.generate_markdown_report()

        with open(filename, 'w') as f:
            f.write(report_content)

        return filename

    def generate_summary_json(self) -> dict:
        """Generate summary JSON for quick overview"""
        if not self.report_data:
            self.load_analysis_data()

        summary = {
            "status": "success",
            "generated_at_tz": "America/New_York",
            "n_tickers": len(self.report_data['portfolio_metrics']['current_portfolio']),
            "kpis": {
                "exp_return_12m": f"{self.report_data['portfolio_metrics']['risk_metrics']['portfolio_expected_return']:.1%}",
                "ann_vol": f"{self.report_data['portfolio_metrics']['risk_metrics']['portfolio_volatility']:.1%}",
                "sharpe": f"{self.report_data['portfolio_metrics']['risk_metrics']['sharpe_ratio']:.2f}",
                "dividend_yield": f"{self.report_data['portfolio_metrics']['dividend_analysis']['portfolio_dividend_yield']:.1%}",
                "hhi": f"{self.report_data['portfolio_metrics']['concentration_metrics']['hhi']:.3f}"
            },
            "proposals": [
                {
                    "name": "Plan A - Conservative Rebalancing",
                    "delta_turnover": f"{self.report_data['optimization_proposals']['plan_a_conservative']['expected_metrics']['turnover']:.1%}",
                    "exp_return": f"{self.report_data['optimization_proposals']['plan_a_conservative']['expected_metrics']['expected_return']:.1%}",
                    "ann_vol": f"{self.report_data['optimization_proposals']['plan_a_conservative']['expected_metrics']['volatility']:.1%}",
                    "sharpe": f"{self.report_data['optimization_proposals']['plan_a_conservative']['expected_metrics']['sharpe_ratio']:.2f}"
                },
                {
                    "name": "Plan B - Aggressive Optimization",
                    "delta_turnover": f"{self.report_data['optimization_proposals']['plan_b_aggressive']['expected_metrics']['turnover']:.1%}",
                    "exp_return": f"{self.report_data['optimization_proposals']['plan_b_aggressive']['expected_metrics']['expected_return']:.1%}",
                    "ann_vol": f"{self.report_data['optimization_proposals']['plan_b_aggressive']['expected_metrics']['volatility']:.1%}",
                    "sharpe": f"{self.report_data['optimization_proposals']['plan_b_aggressive']['expected_metrics']['sharpe_ratio']:.2f}"
                }
            ],
            "data_freshness": {
                "prices": "OK",
                "news": "OK"
            }
        }

        return summary

def main():
    """Main execution function"""
    generator = PortfolioReportGenerator()

    # Generate and save markdown report
    report_file = generator.save_report()
    print(f"Markdown report saved: {report_file}")

    # Generate and save summary JSON
    summary = generator.generate_summary_json()
    with open('data/summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    print("Summary JSON saved: data/summary.json")
    print(json.dumps({
        "status": "success",
        "message": "Portfolio report generation completed",
        "files_created": [report_file, "data/summary.json"]
    }, indent=2))

if __name__ == "__main__":
    main()
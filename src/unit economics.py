"""Unit Economics Calculator - CAC, LTV, Payback Period"""

class UnitEconomicsCalculator:
    def __init__(self):
        self.segments = {
            'SMB': {
                'cac': 3500,
                'monthly_revenue': 2999,
                'monthly_churn': 0.02,
                'gross_margin': 0.85,
                'upsell_rate': 0.15,
                'cross_sell_rate': 0.20,
            },
            'Enterprise': {
                'cac': 20000,
                'monthly_revenue': 49999,
                'monthly_churn': 0.005,
                'gross_margin': 0.75,
                'upsell_rate': 0.30,
                'cross_sell_rate': 0.35,
            }
        }
        
        self.reliance_advantage = {
            'brand_lower_churn': 0.20,
            'network_cac_reduction': 0.35,
            'ecoystem_ltv_boost': 1.30
        }
    
    def calculate_ltv(self, segment, with_reliance=True):
        data = self.segments[segment]
        effective_churn = data['monthly_churn']
        if with_reliance:
            effective_churn = data['monthly_churn'] * (1 - self.reliance_advantage['brand_lower_churn'])
        
        lifetime_months = 1 / effective_churn
        monthly_profit = data['monthly_revenue'] * data['gross_margin']
        base_ltv = monthly_profit * lifetime_months
        
        if with_reliance:
            upsell_value = base_ltv * data['upsell_rate']
            cross_sell_value = base_ltv * data['cross_sell_rate']
            total_ltv = (base_ltv + upsell_value + cross_sell_value) * self.reliance_advantage['ecoystem_ltv_boost']
        else:
            total_ltv = base_ltv
        
        return total_ltv
    
    def calculate_payback_period(self, segment, with_reliance=True):
        data = self.segments[segment]
        effective_cac = data['cac']
        if with_reliance:
            effective_cac = data['cac'] * (1 - self.reliance_advantage['network_cac_reduction'])
        
        monthly_contribution = data['monthly_revenue'] * data['gross_margin']
        payback_months = effective_cac / monthly_contribution
        return payback_months
    
    def calculate_ltv_cac_ratio(self, segment, with_reliance=True):
        ltv = self.calculate_ltv(segment, with_reliance)
        effective_cac = self.segments[segment]['cac']
        if with_reliance:
            effective_cac = self.segments[segment]['cac'] * (1 - self.reliance_advantage['network_cac_reduction'])
        return ltv / effective_cac
    
    def get_all_metrics(self):
        metrics = {}
        for segment in ['SMB', 'Enterprise']:
            metrics[segment] = {
                'CAC': self.segments[segment]['cac'] * (1 - self.reliance_advantage['network_cac_reduction']),
                'LTV': self.calculate_ltv(segment, with_reliance=True),
                'LTV_CAC_Ratio': self.calculate_ltv_cac_ratio(segment, with_reliance=True),
                'Payback_Months': self.calculate_payback_period(segment, with_reliance=True),
                'Monthly_Revenue': self.segments[segment]['monthly_revenue'],
                'Gross_Margin': self.segments[segment]['gross_margin']
            }
        return metrics

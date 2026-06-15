"""Market Sizing Analysis - TAM/SAM/SOM"""

class MarketSizingAnalysis:
    def __init__(self):
        self.market_data = {
            'total_smb_india': 63_000_000,
            'total_enterprises': 1_500_000,
            'saas_market_india': 250_000_000_000,  # ₹25,000 Cr
        }
        
        self.addressable = {
            'digital_transformation_pct': 0.25,
            'reliance_reachable_pct': 0.40,
        }
    
    def calculate_tam(self):
        tam_smb = (self.market_data['total_smb_india'] * 
                  self.addressable['digital_transformation_pct'] * 50000)
        tam_enterprise = (self.market_data['total_enterprises'] * 
                         self.addressable['digital_transformation_pct'] * 500000)
        return tam_smb + tam_enterprise
    
    def calculate_sam(self):
        return self.calculate_tam() * self.addressable['reliance_reachable_pct']
    
    def calculate_som(self):
        sam = self.calculate_sam()
        return {
            'Year1': sam * 0.001,
            'Year2': sam * 0.0025,
            'Year3': sam * 0.005,
        }
    
    def get_market_metrics(self):
        tam = self.calculate_tam()
        sam = self.calculate_sam()
        som = self.calculate_som()
        
        return {
            'TAM_Cr': tam / 1e7,
            'SAM_Cr': sam / 1e7,
            'SOM_Year1_Cr': som['Year1'] / 1e7,
            'SOM_Year2_Cr': som['Year2'] / 1e7,
            'SOM_Year3_Cr': som['Year3'] / 1e7,
      }

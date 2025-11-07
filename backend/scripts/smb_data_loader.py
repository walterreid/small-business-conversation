"""
SMB Data Loader

Loads insights from Excel file about small business marketing.
Gracefully falls back to hardcoded defaults if file not found.
"""

import os
from typing import Dict, Optional


def load_smb_insights(excel_path: Optional[str] = None) -> Dict:
    """
    Load insights from Excel file about small business marketing.
    
    Args:
        excel_path: Optional path to Excel file. If None, tries default location.
        
    Returns:
        Dict with budget ranges, pain points, effective channels, etc.
    """
    # Default hardcoded insights (used if Excel file not found)
    default_insights = {
        "budget_ranges": [
            "Under $500",
            "$500-1000",
            "$1000-2500",
            "$2500-5000",
            "$5000+"
        ],
        "pain_points": [
            "Limited time for marketing",
            "Don't know where to start",
            "Wasted money on ineffective ads",
            "Can't track ROI",
            "Competing with bigger businesses"
        ],
        "effective_channels": [
            "Google Business Profile (free)",
            "Instagram organic",
            "Local SEO",
            "Email marketing",
            "Facebook ads (if budget allows)",
            "Word of mouth referrals"
        ],
        "budget_allocations": {
            "Under $500": {
                "focus": "Free and low-cost channels",
                "channels": ["Google Business Profile", "Social media organic", "Email marketing"]
            },
            "$500-1000": {
                "focus": "Mix of free and paid",
                "channels": ["Google Ads (limited)", "Social media ads", "Email marketing"]
            },
            "$1000-2500": {
                "focus": "Balanced paid and organic",
                "channels": ["Google Ads", "Social media ads", "Email marketing", "Content marketing"]
            },
            "$2500+": {
                "focus": "Multi-channel strategy",
                "channels": ["Google Ads", "Social media ads", "Email marketing", "Content marketing", "Retargeting"]
            }
        }
    }
    
    # Try to load from Excel if pandas is available
    try:
        import pandas as pd
        
        # Default path if not provided
        if excel_path is None:
            # Look for Excel file in common locations
            possible_paths = [
                os.path.join(os.path.dirname(__file__), '..', '..', 'SMB_stats_to_use_on_website.xlsx'),
                os.path.join(os.path.dirname(__file__), '..', 'data', 'SMB_stats_to_use_on_website.xlsx'),
                'SMB_stats_to_use_on_website.xlsx'
            ]
            
            excel_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    excel_path = path
                    break
        
        if excel_path and os.path.exists(excel_path):
            # Load Excel file
            df = pd.read_excel(excel_path)
            
            # Extract insights (this is a placeholder - actual extraction depends on Excel structure)
            # For now, return defaults with a note that Excel was found
            insights = default_insights.copy()
            insights['source'] = 'excel'
            insights['excel_path'] = excel_path
            
            return insights
        else:
            # Excel file not found, use defaults
            insights = default_insights.copy()
            insights['source'] = 'defaults'
            return insights
            
    except ImportError:
        # pandas not installed, use defaults
        insights = default_insights.copy()
        insights['source'] = 'defaults'
        insights['note'] = 'pandas not installed, using hardcoded defaults'
        return insights
    except Exception as e:
        # Error loading Excel, use defaults
        insights = default_insights.copy()
        insights['source'] = 'defaults'
        insights['error'] = str(e)
        return insights


def enhance_template_with_data(template: Dict, smb_insights: Dict) -> Dict:
    """
    Add SMB insights to template for better recommendations.
    
    Args:
        template: Template dictionary
        smb_insights: Insights from load_smb_insights()
        
    Returns:
        Template with smb_insights added
    """
    template['smb_insights'] = smb_insights
    return template


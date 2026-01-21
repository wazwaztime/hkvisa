"""
Base class for visa appointment checkers
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional
from datetime import datetime


class VisaChecker(ABC):
    """Abstract base class for visa appointment checkers"""
    
    def __init__(self, country_name: str):
        self.country_name = country_name
        self.last_check_time = None
        self.last_result = None
    
    @abstractmethod
    def check_appointments(self) -> Dict:
        """
        Check for available visa appointments
        
        Returns:
            Dict with appointment information:
            {
                'country': str,
                'status': str,  # 'available', 'unavailable', 'error'
                'earliest_date': Optional[datetime],
                'message': str,
                'check_time': datetime
            }
        """
        pass
    
    def format_result(self, result: Dict) -> str:
        """Format the result into a readable string"""
        status = result.get('status', 'unknown')
        message = result.get('message', 'No information available')
        
        output = f"\n{'='*60}\n"
        output += f"Country: {result.get('country', 'Unknown')}\n"
        output += f"Status: {status.upper()}\n"
        
        if result.get('earliest_date'):
            output += f"Earliest Date: {result['earliest_date'].strftime('%Y-%m-%d')}\n"
        
        output += f"Message: {message}\n"
        output += f"Checked at: {result.get('check_time', datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}\n"
        output += f"{'='*60}\n"
        
        return output

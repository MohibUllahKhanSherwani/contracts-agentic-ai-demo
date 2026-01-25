"""
CSV Output Handler
Saves evaluation results to CSV file for tracking and reporting
"""
import csv
import os
from pathlib import Path
from typing import Dict
from datetime import datetime


class CSVOutputHandler:
    """Handles writing evaluation results to CSV"""
    
    def __init__(self, csv_path: str = "data/evaluations.csv"):
        """
        Initialize CSV handler
        
        Args:
            csv_path: Path to CSV file
        """
        self.csv_path = Path(csv_path)
        self.fieldnames = [
            "timestamp",
            "contract_id",
            "vendor_name",
            "performance_score",
            "grade",
            "risk_level",
            "recommendation",
            "status"
        ]
        
        # Ensure directory exists
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    def save_result(self, result: Dict) -> None:
        """
        Save evaluation result to CSV
        
        Args:
            result: Evaluation result dictionary
        """
        # Check if file exists to determine if we need headers
        file_exists = self.csv_path.exists()
        
        # Prepare row data
        row = {
            "timestamp": result.get("timestamp", datetime.utcnow().isoformat() + "Z"),
            "contract_id": result.get("contract_id", ""),
            "vendor_name": result.get("vendor_name", ""),
            "performance_score": result.get("performance_score", 0),
            "grade": self._get_grade(result),
            "risk_level": result.get("risk_level", ""),
            "recommendation": result.get("recommendation", ""),
            "status": result.get("status", "")
        }
        
        # Write to CSV
        with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            
            # Write header if new file
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(row)
    
    def _get_grade(self, result: Dict) -> str:
        """Extract grade from result steps"""
        for step in result.get("steps", []):
            if step.get("agent") == "performance_analysis":
                return step.get("output", {}).get("grade", "")
        return ""
    
    def read_results(self) -> list:
        """
        Read all results from CSV
        
        Returns:
            List of result dictionaries
        """
        if not self.csv_path.exists():
            return []
        
        results = []
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append(dict(row))
        
        return results
    
    def get_by_contract_id(self, contract_id: str) -> Dict:
        """
        Get result by contract ID
        
        Args:
            contract_id: Contract ID to search for
            
        Returns:
            Result dictionary or None
        """
        results = self.read_results()
        for result in results:
            if result.get("contract_id") == contract_id:
                return result
        return None

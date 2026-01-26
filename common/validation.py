"""Validation Framework for Microprocessor Performance Models.

This module provides validation utilities to verify that performance models
produce accurate predictions within documented ranges.
"""

from dataclasses import dataclass
from typing import List, Optional, Callable, Any, Dict, Tuple


@dataclass
class ValidationResult:
    """Result of a single validation test."""
    name: str
    passed: bool
    expected: Any
    actual: Any
    tolerance: float
    message: str


class ValidationSuite:
    """Collection of validation tests for a processor model."""
    
    def __init__(self, processor_name: str):
        """Initialize validation suite.
        
        Args:
            processor_name: Name of processor being validated
        """
        self.processor_name = processor_name
        self.tests: List[Callable[[], ValidationResult]] = []
        self.results: List[ValidationResult] = []
    
    def add_test(self, test_func: Callable[[], ValidationResult]):
        """Add a validation test function."""
        self.tests.append(test_func)
    
    def add_ips_test(
        self,
        actual_ips: float,
        min_ips: float,
        max_ips: float,
        tolerance: float = 0.05,
        workload: str = "typical"
    ):
        """Add IPS range validation test.
        
        Args:
            actual_ips: Predicted IPS from model
            min_ips: Minimum documented IPS
            max_ips: Maximum documented IPS
            tolerance: Allowed tolerance (default 5%)
            workload: Workload name for reporting
        """
        def test():
            min_allowed = min_ips * (1 - tolerance)
            max_allowed = max_ips * (1 + tolerance)
            passed = min_allowed <= actual_ips <= max_allowed
            
            return ValidationResult(
                name=f"IPS range ({workload})",
                passed=passed,
                expected=f"{min_ips:,.0f} - {max_ips:,.0f}",
                actual=f"{actual_ips:,.0f}",
                tolerance=tolerance,
                message=f"IPS={actual_ips:,.0f}, expected {min_ips:,.0f}-{max_ips:,.0f}"
            )
        
        self.tests.append(test)
    
    def add_cpi_test(
        self,
        actual_cpi: float,
        min_cpi: float,
        max_cpi: float,
        tolerance: float = 0.10,
        workload: str = "typical"
    ):
        """Add CPI range validation test.
        
        Args:
            actual_cpi: Predicted CPI from model
            min_cpi: Minimum expected CPI
            max_cpi: Maximum expected CPI
            tolerance: Allowed tolerance (default 10%)
            workload: Workload name for reporting
        """
        def test():
            min_allowed = min_cpi * (1 - tolerance)
            max_allowed = max_cpi * (1 + tolerance)
            passed = min_allowed <= actual_cpi <= max_allowed
            
            return ValidationResult(
                name=f"CPI range ({workload})",
                passed=passed,
                expected=f"{min_cpi:.1f} - {max_cpi:.1f}",
                actual=f"{actual_cpi:.2f}",
                tolerance=tolerance,
                message=f"CPI={actual_cpi:.2f}, expected {min_cpi:.1f}-{max_cpi:.1f}"
            )
        
        self.tests.append(test)
    
    def add_weights_test(self, timing_categories: Dict[str, Dict]):
        """Add test to verify workload weights sum to ~1.0.
        
        Args:
            timing_categories: Dict of timing categories with weights
        """
        def test():
            total = sum(cat.get('weight', 0) for cat in timing_categories.values())
            passed = 0.95 <= total <= 1.05
            
            return ValidationResult(
                name="Weights sum",
                passed=passed,
                expected="0.95 - 1.05",
                actual=f"{total:.3f}",
                tolerance=0.05,
                message=f"Weights sum to {total:.3f}"
            )
        
        self.tests.append(test)
    
    def add_category_count_test(self, timing_categories: Dict[str, Dict]):
        """Add test to verify 5-15 timing categories.
        
        Args:
            timing_categories: Dict of timing categories
        """
        def test():
            count = len(timing_categories)
            passed = 5 <= count <= 15
            
            return ValidationResult(
                name="Category count",
                passed=passed,
                expected="5 - 15",
                actual=str(count),
                tolerance=0.0,
                message=f"{count} categories (expected 5-15)"
            )
        
        self.tests.append(test)
    
    def add_bottleneck_test(
        self,
        actual_bottleneck: str,
        expected_bottlenecks: List[str]
    ):
        """Add bottleneck identification test.
        
        Args:
            actual_bottleneck: Identified bottleneck from model
            expected_bottlenecks: List of acceptable bottleneck identifications
        """
        def test():
            # Normalize for comparison
            actual_lower = actual_bottleneck.lower().replace('_', ' ').replace('-', ' ')
            passed = any(
                exp.lower() in actual_lower or actual_lower in exp.lower()
                for exp in expected_bottlenecks
            )
            
            return ValidationResult(
                name="Bottleneck identification",
                passed=passed,
                expected=", ".join(expected_bottlenecks),
                actual=actual_bottleneck,
                tolerance=0.0,
                message=f"Bottleneck: {actual_bottleneck}"
            )
        
        self.tests.append(test)
    
    def add_sources_test(self, sources: List[str]):
        """Add test to verify timing sources are documented.
        
        Args:
            sources: List of documentation sources
        """
        def test():
            passed = len(sources) >= 1 and all(len(s) > 5 for s in sources)
            
            return ValidationResult(
                name="Source documentation",
                passed=passed,
                expected="At least 1 source",
                actual=f"{len(sources)} sources",
                tolerance=0.0,
                message=f"Sources: {', '.join(sources[:3])}"
            )
        
        self.tests.append(test)
    
    def add_cycles_documented_test(self, timing_categories: Dict[str, Dict]):
        """Verify all categories have cycle counts."""
        def test():
            missing = [cat for cat, data in timing_categories.items() 
                      if 'cycles' not in data]
            passed = len(missing) == 0
            
            return ValidationResult(
                name="Cycles documented",
                passed=passed,
                expected="All categories have cycles",
                actual=f"{len(timing_categories) - len(missing)}/{len(timing_categories)}",
                tolerance=0.0,
                message=f"Missing cycles: {missing}" if missing else "All documented"
            )
        
        self.tests.append(test)
    
    def run(self) -> Tuple[List[ValidationResult], bool]:
        """Run all validation tests.
        
        Returns:
            Tuple of (results list, all_passed boolean)
        """
        self.results = []
        
        for test in self.tests:
            try:
                result = test()
                self.results.append(result)
            except Exception as e:
                self.results.append(ValidationResult(
                    name="Test execution",
                    passed=False,
                    expected="No error",
                    actual=str(e),
                    tolerance=0.0,
                    message=f"Test failed with error: {e}"
                ))
        
        all_passed = all(r.passed for r in self.results)
        return self.results, all_passed
    
    def summary(self) -> str:
        """Generate summary of validation results.
        
        Returns:
            Formatted summary string
        """
        if not self.results:
            self.run()
        
        lines = [f"Validation Results: {self.processor_name}", "=" * 50]
        
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        
        for result in self.results:
            status = "✓ PASS" if result.passed else "✗ FAIL"
            lines.append(f"{status}: {result.name}")
            lines.append(f"       Expected: {result.expected}")
            lines.append(f"       Actual:   {result.actual}")
        
        lines.append("=" * 50)
        lines.append(f"Total: {passed}/{total} tests passed")
        
        return "\n".join(lines)


def validate_ips_range(
    actual: float,
    min_ips: float,
    max_ips: float,
    tolerance: float = 0.05
) -> bool:
    """Check if IPS is within expected range.
    
    Args:
        actual: Predicted IPS
        min_ips: Minimum documented IPS
        max_ips: Maximum documented IPS
        tolerance: Allowed tolerance
        
    Returns:
        True if within range
    """
    return min_ips * (1 - tolerance) <= actual <= max_ips * (1 + tolerance)


def validate_cpi_range(
    actual: float,
    min_cpi: float,
    max_cpi: float,
    tolerance: float = 0.10
) -> bool:
    """Check if CPI is within expected range.
    
    Args:
        actual: Predicted CPI
        min_cpi: Minimum expected CPI
        max_cpi: Maximum expected CPI
        tolerance: Allowed tolerance
        
    Returns:
        True if within range
    """
    return min_cpi * (1 - tolerance) <= actual <= max_cpi * (1 + tolerance)


def validate_weights_sum(timing_categories: Dict[str, Dict]) -> bool:
    """Check if weights sum to approximately 1.0.
    
    Args:
        timing_categories: Dict of timing categories
        
    Returns:
        True if weights sum to 0.95-1.05
    """
    total = sum(cat.get('weight', 0) for cat in timing_categories.values())
    return 0.95 <= total <= 1.05


def validate_category_count(timing_categories: Dict[str, Dict]) -> bool:
    """Check if category count is 5-15.
    
    Args:
        timing_categories: Dict of timing categories
        
    Returns:
        True if count is 5-15
    """
    return 5 <= len(timing_categories) <= 15


def validate_bottleneck(actual: str, expected: List[str]) -> bool:
    """Check if identified bottleneck matches expected.
    
    Args:
        actual: Identified bottleneck
        expected: List of acceptable bottlenecks
        
    Returns:
        True if match found
    """
    actual_lower = actual.lower().replace('_', ' ').replace('-', ' ')
    return any(
        exp.lower() in actual_lower or actual_lower in exp.lower()
        for exp in expected
    )


def create_standard_suite(
    processor_name: str,
    ips_range: Tuple[float, float],
    cpi_range: Tuple[float, float],
    expected_bottlenecks: List[str],
    timing_categories: Dict[str, Dict],
    sources: List[str],
    actual_ips: float,
    actual_cpi: float,
    actual_bottleneck: str
) -> ValidationSuite:
    """Create a standard validation suite for a processor.
    
    Args:
        processor_name: Name of processor
        ips_range: (min_ips, max_ips)
        cpi_range: (min_cpi, max_cpi)
        expected_bottlenecks: List of acceptable bottlenecks
        timing_categories: Dict of timing categories
        sources: List of documentation sources
        actual_ips: Predicted IPS
        actual_cpi: Predicted CPI
        actual_bottleneck: Identified bottleneck
        
    Returns:
        Configured ValidationSuite
    """
    suite = ValidationSuite(processor_name)
    
    suite.add_ips_test(actual_ips, ips_range[0], ips_range[1])
    suite.add_cpi_test(actual_cpi, cpi_range[0], cpi_range[1])
    suite.add_bottleneck_test(actual_bottleneck, expected_bottlenecks)
    suite.add_weights_test(timing_categories)
    suite.add_category_count_test(timing_categories)
    suite.add_cycles_documented_test(timing_categories)
    suite.add_sources_test(sources)
    
    return suite

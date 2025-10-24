"""Classifiers for various PM tasks.

This module provides pre-built classifiers for common product management tasks.

Available Classifiers:
    - SignalClassifier: Classify customer signals (feature requests, bugs, churn risk, etc.)

Example:
    >>> from pm_prompt_toolkit.classifiers import SignalClassifier
    >>> classifier = SignalClassifier()
    >>> result = classifier.classify("We need SSO integration")
    >>> print(result.category)
    feature_request
"""

from pm_prompt_toolkit.classifiers.signal_classifier import SignalClassifier

__all__ = ["SignalClassifier"]

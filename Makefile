clean:
	@echo "Cleaning up cache and generated files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.py[codz]" -delete 2>/dev/null || true
	@find . -type f -name "*\$$py.class" -delete 2>/dev/null || true
	@rm -rf build/ dist/ .eggs/ 2>/dev/null || true
	@rm -rf .pytest_cache/ .cache/ .coverage htmlcov/ coverage.xml 2>/dev/null || true
	@rm -rf .mypy_cache/ .dmypy.json dmypy.json .pytype/ 2>/dev/null || true
	@rm -rf .ruff_cache/ 2>/dev/null || true
	@echo "Clean complete!"

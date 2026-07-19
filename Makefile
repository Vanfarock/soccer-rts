style:
	uv run ruff format src/
	uv run ruff check src/ --fix
	uv run ty check src/

run:
	uv run python src/main.py
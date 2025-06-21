# Garmin-Grafana OpenCode Guidelines

## Build/Run Commands
- Run container: `docker compose up -d`
- Check logs: `docker compose logs --follow`
- Fetch historical data: `docker compose run --rm -e MANUAL_START_DATE=YYYY-MM-DD -e MANUAL_END_DATE=YYYY-MM-DD garmin-fetch-data`
- Export data to CSV: `docker exec garmin-fetch-data uv run /app/garmin_grafana/influxdb_exporter.py --last-n-days=30`
- Backup database: `docker exec influxdb influxd backup -portable -db GarminStats /tmp/influxdb_backup`

## Code Style Guidelines
- **Imports**: Group standard library, third-party, and local imports in separate blocks
- **Formatting**: Use 4-space indentation, no trailing whitespace
- **Types**: Use type hints where appropriate, especially for function parameters and returns
- **Naming**: Use snake_case for variables/functions, UPPER_CASE for constants
- **Error Handling**: Use try/except blocks with specific exceptions, log errors with appropriate level
- **Environment Variables**: Use os.getenv() with default values, validate inputs
- **Logging**: Use appropriate log levels (INFO, WARNING, ERROR) with descriptive messages
- **Documentation**: Add docstrings for functions explaining purpose, parameters, and return values

## Project Structure
- Python code in src/garmin_grafana/
- Docker configuration in compose files
- Dashboard templates in Grafana_Dashboard/
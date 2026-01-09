# Changelog

## [1.0.2] - 2026-01-10
### Fixed
- Fixed horizontal and vertical swing mode when parsing returned raw data
- Removed duplicate mode definitions, simplified HORIZONTAL enum to use only ON/OFF values
- Fix status response when Vert. swing mode set to SWING

### Added
- Improved error handling
- Support for climate.turn_on and climate.turn_off

## [1.0.1] - 2026-01-06
### Fixed
- Fixed ambient temps > 32

### Added
- Factions of degrees to ambient temp
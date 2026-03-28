# Changelog

## [1.0.3] - 2026-03-28
### Fixed
- Added missing `device_info` property to climate entity so the AC is correctly
  registered in the Home Assistant device registry. Without this, the entity
  appeared as a floating entity with no parent device, preventing it from being
  selectable in integrations such as Variables+History.
- Added `mdi:air-conditioner` icon to fix broken image shown in device and
  entity search results
- Added brand png files for local logo display

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
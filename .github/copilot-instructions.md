# Broadlink AC Home Assistant Integration - AI Agent Guidelines

## Architecture Overview
This is a Home Assistant custom integration for Broadlink AC devices, implementing direct local control without MQTT dependency. The integration consists of:

- **Device Protocol Layer** (`ac_db.py`): Low-level Broadlink AC communication protocol with encryption/decryption, device discovery, and status control
- **Home Assistant Integration** (`__init__.py`): Sets up config entries and forwards to climate platform
- **Climate Entity** (`climate.py`): Maps Home Assistant climate features to AC device capabilities
- **Configuration Flow** (`config_flow.py`): User setup via IP address and MAC address

## Key Patterns & Conventions

### Device Communication
- Use `ac_db` class from `ac_db.py` for all device interactions
- Always call `get_ac_status(force_update=True)` to fetch current state
- Set device state via specific methods like `set_temperature()`, `set_homeassistant_mode()`, `set_fanspeed()`, `set_fixation_v()`, `set_fixation_h()`
- Handle status responses as dictionaries with keys like `"power"`, `"temp"`, `"mode"`, `"fanspeed"`, `"ambient_temp"`, `"fixation_v"`, `"fixation_h"`

### Home Assistant Integration
- Store `ac_db` instance in both `entry.runtime_data` and `hass.data[DOMAIN][entry.entry_id]`
- Climate entity initialization: `BroadlinkACClimate(ac_instance, entry)`
- Map HVAC modes using `_map_mode_to_hvac()` and `_map_hvac_to_mode()` methods
- Supported modes: `HVACMode.OFF/COOL/HEAT/DRY/FAN_ONLY/AUTO`
- Supported fan modes: `FAN_AUTO/LOW/MEDIUM/HIGH`
- Supported swing modes: `AUTO/TOP/MIDDLE1/MIDDLE2/MIDDLE3/BOTTOM/SWING` (vertical fixation positions)
- Supported horizontal swing modes: `LEFT_FIX/LEFT_FLAP/LEFT_RIGHT_FIX/LEFT_RIGHT_FLAP/RIGHT_FIX/RIGHT_FLAP` (horizontal flap positions)

### Configuration
- Requires user input: `host` (IP address) and `mac` (MAC address)
- MAC address formatted via `format_mac()` and stored without colons as hex bytes
- Unique ID based on formatted MAC address

### Error Handling
- Wrap all device communication calls in try-except blocks catching `ConnectTimeout` and `ConnectError`
- Log timeouts as warnings (device temporarily unavailable), other errors as errors
- Don't crash the entity on network failures - gracefully degrade state
- All control methods (`async_set_temperature()`, `async_set_hvac_mode()`, etc.) must catch connection errors

### Code Style
- Follow Home Assistant patterns: async methods, ConfigEntry usage, proper entity features
- Use static constants from `ac_db.STATIC` for AC-specific values (fan speeds, modes, etc.)
- Import from `homeassistant.components.climate` for climate features

## Development Workflow
- No automated tests currently - manual testing required
- Integration installed via HACS or manual copy to `custom_components/broadlink_ac`
- Restart Home Assistant after code changes
- Configure via HA UI: Configuration > Integrations > Add Integration > Broadlink AC

## Common Tasks
- **Adding new AC features**: Extend `ac_db` methods, update `ClimateEntityFeature` flags, add mapping in climate entity
- **Device discovery**: Use `discover()` function from `ac_db.py` for network scanning
- **Status polling**: Implement in `async_update()` method with error handling
- **Mode/fan control**: Add new mappings in `_map_*` methods and call appropriate `set_*` methods
- **Swing control**: Map `fixation_v` to HA swing modes, use `set_fixation_v()` for control
- **Horizontal swing control**: Map `fixation_h` to HA horizontal swing modes, use `set_fixation_h()` for control</content>
<parameter name="filePath">d:\broadlink-ac\.github\copilot-instructions.md
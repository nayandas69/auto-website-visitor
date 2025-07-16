# Change Log

## [Release 3.0.0] - 2025-16-07

### Major Improvements

#### **Fixed CLI Argument Processing**
- **FIXED**: `--count` argument now properly maps to `visit_count` setting
- **FIXED**: Hyphenated CLI arguments (`--auto-scroll`, `--random-delay`, `--user-agent`, `--log-level`) now work correctly
- **FIXED**: `awv create-config --config-path config.yaml` command now works without requiring URL validation 
- **FIXED**: `awv update` command now works without requiring URL validation 
- **IMPROVED**: Better argument validation and error handling

#### **Enhanced Visual Feedback**
- **NEW**: Colored output for success (GREEN ✓) and failure (RED ✗) messages
- **NEW**: Added colorama support for cross-platform color compatibility
- **IMPROVED**: Better status messages with visual icons (✓, ✗, 🔍, 🗑️)

#### **Smart Browser & Driver Management**
- **NEW**: Automatic browser detection before starting visits
- **NEW**: Intelligent WebDriver caching system - checks cache first, downloads only when needed
- **NEW**: Auto-update mechanism for outdated drivers
- **NEW**: Cache clearing and retry logic for failed driver setups
- **IMPROVED**: Clear error messages with download links when browsers are missing
- **IMPROVED**: Better WebDriver installation feedback with progress indicators

#### **Configuration Improvements**
- **UPDATED**: Configuration templates (`config.yaml` and `config.json`) with version 2025.01.16
- **IMPROVED**: Better documentation and examples in templates
- **FIXED**: Template validation and functionality testing

#### **Code Quality & Maintenance**
- **REMOVED**: Debug print statements from CLI processing
- **IMPROVED**: Error handling throughout the application
- **IMPROVED**: Code comments and documentation
- **FIXED**: setuptools_scm version detection issues
- **UPDATED**: All version references to 2025.01.16

### **New Features**

#### Browser Detection System
```bash
✓ Chrome browser found at: C:\Program Files\Google\Chrome\Application\chrome.exe
🔍 Checking chrome WebDriver cache...
✓ Chrome WebDriver ready: /path/to/chromedriver
```

#### Colored Success/Failure Output
```bash
✓ Visit 1/10 completed successfully  (GREEN)
✗ Visit 2/10 failed                  (RED)
```

#### Smart Error Messages
```bash
✗ Chrome browser not found!
Please install Chrome browser:
  Download from: https://www.google.com/chrome/
```

### **Bug Fixes**
- Fixed CLI argument mapping issues that caused `--count` to be ignored
- Fixed hyphenated argument processing (`--auto-scroll`, `--user-agent`, etc.)
- Fixed setuptools_scm version detection in development installations
- Fixed template configuration loading and validation
- Fixed WebDriver cache management and update logic

### **Technical Improvements**
- Enhanced logger with colored output methods (`success()`, `failure()`)
- Improved browser manager with intelligent caching
- Better error handling and user feedback throughout
- Optimized WebDriver installation and update process
- Improved configuration validation and error messages

### **Dependencies**
- Added `colorama>=0.4.6` for cross-platform colored output
- Updated all existing dependencies to latest compatible versions
- Improved dependency management in setup files

### **Testing & Validation**
- All CLI arguments now properly tested and validated
- Configuration templates tested for functionality
- Browser detection and driver management tested across platforms
- Color output tested on Windows, macOS, and Linux

### **Documentation**
- Updated README.md with new features and examples
- Improved code comments throughout the codebase
- Enhanced configuration template documentation
- Added troubleshooting guide for common issues

---

## [Release 2025.01.07] - 2025-01-07

### Release
- Basic website visiting functionality
- Multi-browser support (Chrome, Firefox, Edge)
- Scheduling capabilities
- Configuration file support
- CLI interface
- Logging system

---

## [Older Version]

## Adeed
- Release

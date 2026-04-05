# ==========================================
# FIVEM TOOLS CONFIGURATION FILE
# ==========================================

# --- EXECUTION MODES ---
# FAST_MODE: Skips all menus and instantly runs the DEFAULT_MODULE.
FAST_MODE = False
DEFAULT_MODULE = 1

# --- DEVELOPER AUTO-TESTING ---
# AUTO_TEST: Creates a timestamped folder and runs a batch test of specified modules.
AUTO_TEST = True
# Which modules to test? (1=Spawn Codes, 2=SQL, 3=Duplicates, 4=vMenu)
TEST_MODULES = [1, 2, 3, 4]

# --- PATH SETTINGS ---
# Use "" (empty string) to default to 1 folder up from the script.
TARGET_DIRECTORY = "" 
# Use "" to default to saving files in the same folder as these scripts.
OUTPUT_DIRECTORY = ""

# --- MODULE SETTINGS ---
# Output format for Spawn Codes (".lua" or ".txt")
OUTPUT_FORMAT = ".lua"

# Include Top Speed/Mass handling profile in Spawn Codes? (True/False)
INCLUDE_HANDLING = True

# Use dynamic economy pricing for SQL generation? (True/False)
SMART_PRICING = True
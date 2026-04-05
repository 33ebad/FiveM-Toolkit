import os
import sys
import datetime
import config 
from modules import core_scanner
from modules import mod_spawn_codes
from modules import mod_sql
from modules import mod_duplicates
from modules import mod_vmenu

def setup_paths():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    target_dir = config.TARGET_DIRECTORY if config.TARGET_DIRECTORY else os.path.dirname(script_dir)
    output_dir = config.OUTPUT_DIRECTORY if config.OUTPUT_DIRECTORY else script_dir
    folder_name = os.path.basename(os.path.normpath(target_dir))
    
    return target_dir, output_dir, folder_name

def run_module(choice, target_dir, output_dir, folder_name, spawn_codes, duplicates, is_headless=False):
    if choice == 1:
        ext = config.OUTPUT_FORMAT
        out_file = os.path.join(output_dir, f"spawn_codes_{folder_name}{ext}")
        if config.INCLUDE_HANDLING:
            print(f"\n[1] Extracting handling data for Spawn Codes...")
            detailed_data = core_scanner.parse_handling_data(target_dir, spawn_codes)
            mod_spawn_codes.execute(spawn_codes, out_file, ext, True, detailed_data)
        else:
            print(f"\n[1] Generating Spawn Codes...")
            mod_spawn_codes.execute(spawn_codes, out_file, ext)
            
    elif choice == 2:
        out_file = os.path.join(output_dir, f"vehicles_{folder_name}.sql")
        
        if is_headless:
            use_smart = config.SMART_PRICING
        else:
            default_txt = 'Y' if config.SMART_PRICING else 'N'
            pricing_choice = input(f"\nUse Smart Pricing? (Y/N) [Default: {default_txt}]: ").strip().lower()
            if pricing_choice == 'y': use_smart = True
            elif pricing_choice == 'n': use_smart = False
            else: use_smart = config.SMART_PRICING

        if use_smart:
            print(f"\n[2] Calculating dynamic economies for SQL...")
            detailed_data = core_scanner.parse_handling_data(target_dir, spawn_codes)
            mod_sql.execute(spawn_codes, out_file, use_smart_pricing=True, handling_data=detailed_data)
        else:
            print(f"\n[2] Generating SQL Database...")
            mod_sql.execute(spawn_codes, out_file)
        
    elif choice == 3:
        print(f"\n[3] Scanning for Duplicates...")
        # Passing target_dir and is_headless for the intelligent auto-fixer
        mod_duplicates.execute(duplicates, target_dir, is_headless)
        
    elif choice == 4:
        print(f"\n[4] Generating vMenu Addons...")
        out_file = os.path.join(output_dir, f"vmenu_addons_{folder_name}.json")
        mod_vmenu.execute(spawn_codes, out_file)
        
    else:
        print(f"\n❌ Invalid module choice: {choice}")

if __name__ == "__main__":
    target_dir, output_dir, folder_name = setup_paths()

    # --- DEVELOPER AUTO-TEST EXECUTION ---
    if config.AUTO_TEST:
        # Changed Date Format to: 1-Dec-2000_1-05-40PM
        timestamp = datetime.datetime.now().strftime("%d-%b-%Y_%I-%M-%S%p")
        test_folder_name = f"AutoTest_{timestamp}"
        test_dir = os.path.join(output_dir, test_folder_name)
        os.makedirs(test_dir, exist_ok=True)

        print("\n" + "="*50)
        print("🧪 DEVELOPER AUTO-TEST MODE INITIATED")
        print("="*50)
        print(f"Scanning : {target_dir}")
        print(f"Output   : {test_dir}\n")
        
        spawn_codes, duplicates = core_scanner.get_base_data(target_dir)
        if not spawn_codes:
            print("❌ No vehicles.meta found. Auto-Test aborted.")
            sys.exit()

        for mod_num in config.TEST_MODULES:
            run_module(mod_num, target_dir, test_dir, folder_name, spawn_codes, duplicates, is_headless=True)
            
        print(f"\n✅ Auto-Test Complete! Review results in the '{test_folder_name}' folder.")
        sys.exit()

    # --- FAST MODE EXECUTION ---
    if config.FAST_MODE:
        print(f"⚡ FAST MODE ENABLED | Scanning: {target_dir}")
        spawn_codes, duplicates = core_scanner.get_base_data(target_dir)
        if not spawn_codes:
            sys.exit()
        run_module(config.DEFAULT_MODULE, target_dir, output_dir, folder_name, spawn_codes, duplicates, is_headless=True)
        sys.exit()

    # --- INTERACTIVE MENU EXECUTION ---
    while True:
        folder_name = os.path.basename(os.path.normpath(target_dir))
        
        print("\n" + "="*45)
        print("🔍 DIRECTORY PRE-SCAN")
        print("="*45)
        print(f"Scanning: {target_dir}")
        
        if not os.path.exists(target_dir):
            print("❌ Target directory does not exist! Please change the path.")
            total_folders, total_meta_files = 0, 0
        else:
            total_folders, total_meta_files = core_scanner.get_directory_overview(target_dir)
            print(f"Total Subfolders : {total_folders}")
            print(f"Meta Files Found : {total_meta_files}")
        
        print("="*45)
        print(f"Current Output Path: {output_dir}")
        print("="*45)

        choice = input("\nProceed with these paths? (Y = Yes, N = Change Paths, Q = Quit) [Default: Y]: ").strip().lower()

        if choice == 'y' or choice == '':
            if total_meta_files == 0:
                print("\n❌ No vehicles.meta files found. Cannot proceed. Exiting.")
                sys.exit()
            break 
            
        elif choice == 'q':
            sys.exit()
            
        elif choice == 'n':
            print("\n--- CHANGE PATHS ---")
            new_target = input(f"New Source Directory\n[Current: {target_dir}]\n(Press Enter to keep): ").strip().strip('"').strip("'")
            if new_target and os.path.exists(new_target): target_dir = new_target

            new_output = input(f"\nNew Output Directory\n[Current: {output_dir}]\n(Press Enter to keep): ").strip().strip('"').strip("'")
            if new_output and os.path.exists(new_output): output_dir = new_output

    print("\n⏳ Performing deep scan and extracting meta data...")
    spawn_codes, duplicates = core_scanner.get_base_data(target_dir)

    while True:
        print("\n" + "="*35)
        print("🚗 FIVEM TOOLKIT 🚗")
        print("="*35)
        print("1. Generate Spawn Codes")
        print("2. Generate SQL Database")
        print("3. Check Duplicates & Auto-Fix")
        print("4. Generate vMenu Addons (JSON)")
        print("5. Exit")
        print("="*35)
        
        try:
            menu_choice = input("Select option (1-5): ").strip()
            if not menu_choice: continue
                
            menu_choice = int(menu_choice)
            if menu_choice == 5: sys.exit()
                
            if menu_choice == 1:
                default_handling = 'Y' if config.INCLUDE_HANDLING else 'N'
                handling_choice = input(f"\nExtract Handling Data? (Y/N) [Default: {default_handling}]: ").strip().lower()
                if handling_choice == 'y': config.INCLUDE_HANDLING = True
                elif handling_choice == 'n': config.INCLUDE_HANDLING = False
                    
            run_module(menu_choice, target_dir, output_dir, folder_name, spawn_codes, duplicates, is_headless=False)
            
        except ValueError:
            print("❌ Please enter a valid number.")
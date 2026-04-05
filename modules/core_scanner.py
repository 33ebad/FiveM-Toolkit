import os
import re

def get_directory_overview(root_folder):
    total_folders, total_meta_files = 0, 0
    for root, dirs, files in os.walk(root_folder):
        total_folders += len(dirs)
        for filename in files:
            if filename.lower() == "vehicles.meta":
                total_meta_files += 1
    return total_folders, total_meta_files

def get_base_data(root_folder):
    spawn_codes = {}
    duplicates = {} 
    
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            if filename.lower() == "vehicles.meta":
                # Get the actual relative path from the target directory so users know exactly where it is
                rel_path = os.path.relpath(root, root_folder)
                
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        content = file.read()
                        model_names = re.findall(r"<modelName>(.*?)</modelName>", content, re.IGNORECASE)
                        
                        for model in model_names:
                            if model in spawn_codes:
                                if model not in duplicates:
                                    duplicates[model] = [spawn_codes[model]]
                                duplicates[model].append(rel_path)
                            else:
                                spawn_codes[model] = rel_path
                except Exception:
                    pass
                    
    return spawn_codes, duplicates

def parse_handling_data(root_folder, spawn_codes):
    handling_data = {}
    for root, dirs, files in os.walk(root_folder):
        for filename in files:
            if filename.lower() == "handling.meta":
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        content = file.read()
                        items = re.split(r'<Item type="CHandlingData">', content)[1:]
                        for item in items:
                            name_match = re.search(r'<handlingName>(.*?)</handlingName>', item, re.IGNORECASE)
                            if not name_match: continue
                                
                            h_name = name_match.group(1).strip().lower()
                            
                            speed_match = re.search(r'<fInitialDriveMaxFlatVel value="(.*?)"', item, re.IGNORECASE)
                            mass_match = re.search(r'<fMass value="(.*?)"', item, re.IGNORECASE)
                            bias_match = re.search(r'<fDriveBiasFront value="(.*?)"', item, re.IGNORECASE)
                            gears_match = re.search(r'<nInitialDriveGears value="(.*?)"', item, re.IGNORECASE)
                            
                            speed = f"{int(float(speed_match.group(1).strip()) * 1.32)} KM/H" if speed_match else "N/A"
                            mass = f"{int(float(mass_match.group(1).strip()))}kg" if mass_match else "N/A"
                            gears = f"{gears_match.group(1).strip()}G" if gears_match else "N/A"
                            
                            drive_type = "UNK"
                            if bias_match:
                                bias_val = float(bias_match.group(1).strip())
                                if bias_val == 0.0: drive_type = "RWD"
                                elif bias_val == 1.0: drive_type = "FWD"
                                else: drive_type = "AWD"

                            handling_data[h_name] = f"[ {drive_type:^10} | {gears:^5} | {mass:>6} | {speed:>9} ]"
                            
                except Exception:
                    pass

    detailed_codes = {}
    for code, category in spawn_codes.items():
        # Clean up the category name if it's trapped inside a data folder
        clean_category = category.replace("\\data", "").replace("/data", "")
        profile = handling_data.get(code.lower(), "[ No Handling Data Found                      ]")
        detailed_codes[code] = {"category": clean_category, "profile": profile}
        
    return detailed_codes
import json

def execute(spawn_codes, output_file):
    # Extract just the spawn codes and sort them alphabetically
    vehicle_list = sorted(list(spawn_codes.keys()))
    
    # Structure required by vMenu's addons.json
    vmenu_format = {
        "vehicles": vehicle_list,
        "pedmodels": [],
        "weapons": []
    }
    
    # Write the data to a JSON file with proper indentation
    with open(output_file, "w", encoding="utf-8") as out_file:
        json.dump(vmenu_format, out_file, indent=4)
        
    print(f"\n✅ vMenu Addons file generated: {output_file}")
    print("💡 Tip: Open this file and copy the 'vehicles' list into your server's main vMenu/config/addons.json file.")
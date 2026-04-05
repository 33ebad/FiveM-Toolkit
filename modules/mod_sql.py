import re

def calculate_price(profile_string):
    """Calculates a dynamic vehicle price based on top speed and drive type."""
    base_price = 50000

    if "No Handling Data" in profile_string or profile_string == "UNK":
        return base_price

    try:
        # The profile looks like: [ AWD | 6G | 1740kg | 315 KM/H ]
        parts = profile_string.strip("[] ").split("|")
        if len(parts) == 4:
            drive_type = parts[0].strip()
            speed_str = parts[3].strip()
            
            # Extract just the number from "315 KM/H"
            speed_match = re.search(r'(\d+)', speed_str)
            if speed_match:
                speed = int(speed_match.group(1))
                
                # --- 1. Speed Tiering Economy ---
                if speed < 150:
                    base_price = 25000      # Slow/Utility
                elif speed < 200:
                    base_price = 45000      # Daily Traffic
                elif speed < 250:
                    base_price = 85000      # Sports Cars
                elif speed < 290:
                    base_price = 180000     # Supercars
                elif speed < 330:
                    base_price = 650000     # High-End Supercars
                else:
                    base_price = 1500000    # Hypercars

                # --- 2. Drive Type Multipliers ---
                if "AWD" in drive_type:
                    base_price = int(base_price * 1.15) # AWD is 15% more expensive
                elif "RWD" in drive_type:
                    base_price = int(base_price * 1.05) # RWD is 5% more expensive
                    
                # --- 3. Clean Rounding ---
                # Rounds to the nearest $1,000 for a clean vehicle shop display
                base_price = int(round(base_price, -3))
                
    except Exception:
        pass

    return base_price

def execute(spawn_codes, output_file, use_smart_pricing=False, handling_data=None):
    with open(output_file, "w", encoding="utf-8") as out_file:
        
        # --- Write Instructions ---
        out_file.write("-- ========================================================\n")
        out_file.write("-- 🛠️ HOW TO IMPORT THIS FILE INTO YOUR FIVEM DATABASE 🛠️\n")
        out_file.write("-- 1. Open your Database Manager (e.g., HeidiSQL, phpMyAdmin).\n")
        out_file.write("-- 2. Select your FiveM server's database.\n")
        out_file.write("-- 3. Navigate to the 'Query' or 'SQL' tab.\n")
        out_file.write("-- 4. Copy all the text below and paste it into the query box.\n")
        out_file.write("-- 5. Click Run / Execute.\n")
        out_file.write("-- ========================================================\n\n")
        
        if use_smart_pricing:
            out_file.write("-- ========================================================\n")
            out_file.write("-- 💰 SMART PRICING ENABLED\n")
            out_file.write("-- Prices are calculated dynamically based on handling.meta\n")
            out_file.write("-- \n")
            out_file.write("-- --- Pricing Calculation Formula ---\n")
            out_file.write("-- 1. Base Price by Top Speed:\n")
            out_file.write("--    < 150 KM/H : $25,000    (Utility / Slow)\n")
            out_file.write("--    < 200 KM/H : $45,000    (Daily Traffic)\n")
            out_file.write("--    < 250 KM/H : $85,000    (Sports Cars)\n")
            out_file.write("--    < 290 KM/H : $180,000   (Supercars)\n")
            out_file.write("--    < 330 KM/H : $650,000   (High-End Supercars)\n")
            out_file.write("--    > 330 KM/H : $1,500,000 (Hypercars)\n")
            out_file.write("-- \n")
            out_file.write("-- 2. Drive Type Multiplier:\n")
            out_file.write("--    AWD = +15% Value\n")
            out_file.write("--    RWD = +5% Value\n")
            out_file.write("-- \n")
            out_file.write("-- 3. Final Polish:\n")
            out_file.write("--    All prices are rounded to the nearest $1,000.\n")
            out_file.write("-- ========================================================\n\n")
        else:
            out_file.write("-- ========================================================\n")
            out_file.write("-- 💰 DEFAULT PRICING\n")
            out_file.write("-- All cars set to flat $50,000.\n")
            out_file.write("-- Use CTRL+F or your database editor to mass-change prices.\n")
            out_file.write("-- ========================================================\n\n")

        # --- Write SQL Insert Query ---
        out_file.write("INSERT INTO `vehicles` (`name`, `model`, `price`, `category`) VALUES\n")
        
        items = list(spawn_codes.items())
        for i, (model, category) in enumerate(items):
            display_name = model.replace("_", " ").title()
            
            # Determine the price
            price = 50000
            if use_smart_pricing and handling_data:
                profile = handling_data.get(model, {}).get("profile", "UNK")
                price = calculate_price(profile)
            
            line = f"\t('{display_name}', '{model}', {price}, '{category}')"
            
            if i < len(items) - 1:
                out_file.write(line + ",\n")
            else:
                out_file.write(line + ";\n")
                
    print(f"✅ SQL database file generated: {output_file}")
    if use_smart_pricing:
        print("💡 Smart Pricing applied successfully! Vehicles have been priced based on their top speed.")
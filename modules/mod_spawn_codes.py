def execute(spawn_codes, output_file, format_ext, include_handling=False, handling_data=None):
    unique_categories = sorted(set(spawn_codes.values()))
    
    total_cars = len(spawn_codes)
    total_categories = len(unique_categories)
    
    drift_count = 0
    race_count = 0
    offroad_count = 0
    police_count = 0
    identified_cars = set()

    for code in spawn_codes.keys():
        lower_code = code.lower()
        is_identified = False
        
        if any(k in lower_code for k in ['drift', 'drft', 'slide']):
            drift_count += 1
            is_identified = True
        if any(k in lower_code for k in ['race', 'gt3', 'track', 'f1', 'rally']):
            race_count += 1
            is_identified = True
        if any(k in lower_code for k in ['offroad', '4x4', 'truck', 'jeep']):
            offroad_count += 1
            is_identified = True
        if any(k in lower_code for k in ['pol', 'cop', 'pd', 'sheriff']):
            police_count += 1
            is_identified = True

        if is_identified:
            identified_cars.add(code)

    unknown_count = total_cars - len(identified_cars)
    cmt = "--"
    
    max_code_len = max([len(code) for code in spawn_codes.keys()]) if spawn_codes else 20
    pad_length = max_code_len + 4 

    with open(output_file, "w", encoding="utf-8") as out_file:
        
        out_file.write(f"{cmt} " + "="*60 + "\n")
        out_file.write(f"{cmt} FIVEM CAR PACK SUMMARY\n")
        out_file.write(f"{cmt} " + "="*60 + "\n")
        out_file.write(f"{cmt} Total Cars             : {total_cars}\n")
        out_file.write(f"{cmt} Total Categories       : {total_categories}\n")
        out_file.write(f"{cmt} Approx. Drift Cars     : {drift_count}\n")
        out_file.write(f"{cmt} Approx. Race Cars      : {race_count}\n")
        out_file.write(f"{cmt} Approx. Offroad/4x4    : {offroad_count}\n")
        out_file.write(f"{cmt} Approx. Police/Rescue  : {police_count}\n")
        out_file.write(f"{cmt} Approx. Unknown/Other  : {unknown_count}\n")
        out_file.write(f"{cmt} " + "="*60 + "\n\n")

        if include_handling:
            out_file.write(f"{cmt} " + "="*60 + "\n")
            out_file.write(f"{cmt} HANDLING DATA EXTRACTION & MATH\n")
            out_file.write(f"{cmt} " + "="*60 + "\n")
            
            # Formatted legend to align perfectly with the data
            out_file.write(f"{cmt} Format  : [ Drive Type | Gears |   Mass | Top Speed ]\n")
            out_file.write(f"{cmt} Example : [    AWD     |  6G   | 1740kg |  315 KM/H ]\n")
            
            out_file.write(f"{cmt} \n")
            out_file.write(f"{cmt} --- Calculation Formula ---\n")
            out_file.write(f"{cmt} Drive Type : <fDriveBiasFront> (1.0 = FWD, 0.0 = RWD, Other = AWD)\n")
            out_file.write(f"{cmt} Gears      : <nInitialDriveGears> (e.g., value '6' = 6G)\n")
            out_file.write(f"{cmt} Mass       : <fMass> (e.g., value '1740.000' = 1740kg)\n")
            out_file.write(f"{cmt} Top Speed  : <fInitialDriveMaxFlatVel> * 1.32 = KM/H\n")
            out_file.write(f"{cmt}              (e.g., 238.636 * 1.32 = 315 KM/H)\n")
            out_file.write(f"{cmt} " + "="*60 + "\n\n")
        
        for category in unique_categories:
            out_file.write(f"{cmt} --- [ {category.upper()} ] ---\n")
            models_in_category = [m for m, c in spawn_codes.items() if c == category]
            models_in_category.sort()

            for model in models_in_category:
                if include_handling and handling_data:
                    padded_model = model.ljust(pad_length)
                    profile = handling_data[model]["profile"]
                    out_file.write(f"{padded_model} {cmt} {profile}\n")
                else:
                    out_file.write(f"{model}\n")
            out_file.write("\n")
            
    print(f"✅ Spawn code list generated: {output_file}")
import os
import re

def execute(duplicates, target_dir, is_headless=False):
    if not duplicates:
        print("\n✅ System clean. No duplicate spawn codes found.")
        return

    # Added a double space after the emoji to stop PowerShell from squishing it, plus the line break!
    print("\n⚠️  WARNING: Duplicate spawn codes found! These WILL cause server crashes:")
    for model, paths in duplicates.items():
        print(f" - '{model}' is conflicting! (Found inside: {' & '.join(paths)})")

    if is_headless:
        print("\n💡 Tip: Run Option 3 in Interactive Mode to use the Auto-Fix tool.")
        return

    choice = input("\n🛠️  Do you want to intelligently Auto-Rename the duplicates? \n(This will safely append '_fix' to conflicting files and meta entries) (Y/N): ").strip().lower()

    if choice == 'y':
        print("\n⏳ Auto-fixing duplicates...")
        for model, paths in duplicates.items():
            
            # Keep the FIRST instance original. Fix the 2nd, 3rd, etc.
            conflicting_paths = paths[1:]

            for rel_path in conflicting_paths:
                base_folder = os.path.join(target_dir, rel_path)
                
                # If path is inside 'data', step back to the root of the car folder
                search_dir = base_folder
                if os.path.basename(search_dir).lower() == "data":
                    search_dir = os.path.dirname(search_dir)

                new_model = f"{model}_fix"

                # 1. Safely rename inside ALL .meta files using exact tag boundaries
                for root, _, files in os.walk(search_dir):
                    for file in files:
                        if file.lower().endswith('.meta'):
                            filepath = os.path.join(root, file)
                            try:
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    content = f.read()

                                # Safely replaces >gtr< with >gtr_fix< inside tags like <modelName> or <txdName>
                                updated_content = re.sub(
                                    rf"(>)([ \t]*{re.escape(model)}[ \t]*)(<)", 
                                    rf"\g<1>{new_model}\g<3>", 
                                    content, 
                                    flags=re.IGNORECASE
                                )

                                if content != updated_content:
                                    with open(filepath, 'w', encoding='utf-8') as f:
                                        f.write(updated_content)
                                    print(f"  📝 Updated meta entries in: {rel_path}\\{file}")
                            except Exception as e:
                                print(f"  ❌ Failed to update {file}: {e}")

                # 2. Rename physical .YFT and .YTD files in stream folder
                for root, _, files in os.walk(search_dir):
                    for file in files:
                        if file.lower().startswith(model.lower()) and file.lower().endswith(('.yft', '.ytd')):
                            # This handles things like gtr_hi.yft safely -> gtr_fix_hi.yft
                            suffix = file[len(model):] 
                            new_filename = f"{new_model}{suffix}"

                            old_filepath = os.path.join(root, file)
                            new_filepath = os.path.join(root, new_filename)

                            try:
                                os.rename(old_filepath, new_filepath)
                                print(f"  🔄 Renamed model file to: {new_filename}")
                            except Exception as e:
                                print(f"  ❌ Failed to rename {file}: {e}")

        print("\n✅ Auto-Rename complete! \n🚨 IMPORTANT: Please re-run the Pre-Scan (Restart the script) to update your SQL/Lua files with the new fixed names!")
    else:
        print("\n💡 Fix this manually by deleting or renaming the conflicting vehicles.meta entries.")
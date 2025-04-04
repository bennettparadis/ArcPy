import arcpy
import random

#####################################################
##### WORKS 20x faster when workspace is local ######
#####################################################

# Set workspace
workspace = r"C:\Users\bparadis\Documents\ArcGIS\Projects\2025monitoring\Default.gdb"

# Set path to folder containing layers with specified symbologies
# layer names will match the nomenclature for material types defined in other scripts used for OS survey planning
symbology_folder = r"C:\Users\bparadis\Documents\ArcGIS\Projects\2025monitoring\symbology"

# Open ArcGIS Pro project
aprx = arcpy.mp.ArcGISProject(r"C:\Users\bparadis\Documents\ArcGIS\Projects\2025monitoring\2025monitoring.aprx")
m = aprx.listMaps("OS Network")[0]

# Get list of all feature classes
feature_classes = arcpy.ListFeatureClasses()

# Loop through feature classes
for fc in feature_classes:
    desc = arcpy.Describe(fc)

    # Apply symbology only if it's a point layer
    if desc.shapeType == "Point":
        print(f"Applying symbology to: {fc}")
        
        # Extract material type (everything after the second underscore)
        split_name = fc.split("_", 2)
        if len(split_name) > 2:
            mat_name = split_name[2]
        else:
            mat_name = fc  # Fallback in case of unexpected naming
        
        print(f"Extracted material: {mat_name}")  # Debugging output

        # Define the layer file path to the appropriate symbology layer 
        lyrx_path = os.path.join(symbology_folder, f"{mat_name}.lyrx")
        
        # make sure layer and symbology for material exists
        if os.path.exists(lyrx_path):
            arcpy.ApplySymbologyFromLayer_management(fc, lyrx_path)
            print(f"Applied symbology from {lyrx_path} to {fc}")
        else:
            print(f"Warning: No symbology file found for {mat_name}, skipping.")
               
# Save the project
aprx.save()
print("Symbology updated successfully.")
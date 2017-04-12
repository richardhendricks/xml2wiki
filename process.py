import sys
import xml.etree.ElementTree as ET

if not sys.version_info >= (3,5):
	print ("Please use Python 3.5 or greater")
	
Research = ET.parse('Research.xml')
ResearchRoot = Research.getroot()

ManufacturerRecipes = ET.parse('ManufacturerRecipes.xml')
ManufacturerRecipesRoot = ManufacturerRecipes.getroot()

Items = ET.parse('Items.xml')
ItemsRoot = Items.getroot()

TerrainData = ET.parse('TerrainData.xml')
TerrainDataRoot = TerrainData.getroot()

# Iterate across all manufacturer items, look for research requirements
for recipe in ManufacturerRecipesRoot:
	for craftdata in recipe:
		if (craftdata.tag == 'ResearchRequirements'):
			for researchrequirements in craftdata:
				print(recipe.find('Key').text, researchrequirements.text)
				
# Add unlock info into research XML
# Add research friendly name into recipe XML

# Iterate across all research options
    # Look up unlock item name in terrain data
# Print wiki output

# Iterate across all manufacturer items
    # Look up research name in research requirements
# Print wiki output
 
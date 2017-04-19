import sys
import xml.etree.ElementTree as ET

if not sys.version_info >= (3,4):
  raise Exception("Incorrect Python Version, please use Python 3.4 or greater")
	
Research = ET.parse('Research.xml')
ResearchRoot = Research.getroot()

ManufacturerRecipes = ET.parse('ManufacturerRecipes.xml')
ManufacturerRecipesRoot = ManufacturerRecipes.getroot()

Items = ET.parse('Items.xml')
ItemsRoot = Items.getroot()

TerrainData = ET.parse('TerrainData.xml')
TerrainDataRoot = TerrainData.getroot()

ResearchAssemblerRecipes = ET.parse('ResearchAssemblerRecipes.xml')
ResearchAssemblerRecipesRoot = ResearchAssemblerRecipes

# Iterate across all manufacturer items, look for research requirements
for recipe in ManufacturerRecipesRoot:
  for craftdata in recipe:
    if (craftdata.tag == 'ResearchRequirements'):
      for researchrequirements in craftdata:
        req = researchrequirements.text
        key = recipe.find('CraftedKey').text
        # print("Req", key, req)
        # Find name of the object
        name = None
        # TODO - Add research reqs back into terraindata
        Terrain = None
        for TerrainData in TerrainDataRoot:
          if TerrainData.find('Key').text.lower() == recipe.find('CraftedKey').text.lower():
            # print ("Ter", recipe.find('CraftedKey').text, TerrainData.find('Name').text)
            name = TerrainData.find('Name').text
          values = TerrainData.find('Values')
          if values == None:
            continue
          for valuesentry in values:
            if valuesentry.find('Key').text == recipe.find('CraftedKey').text:
              # print ("Val", recipe.find('CraftedKey').text, valuesentry.find('Name').text)
              name = valuesentry.find('Name').text
        # print("Nam", name, req)
        
        for ItemsData in ItemsRoot:
          if ItemsData.find('Key').text.lower() == recipe.find('CraftedKey').text.lower():
            name = ItemsData.find('Name').text
        
        if name == None:
          print('Could not find name of ' + recipe.find('CraftedKey').text + ' anywhere!')
          exit()
        #Locate research requirement and add name to it as unlock
        for researchdataentry in ResearchRoot:
          if researchdataentry.find('Key').text == req:
            # print("Unl", req, key, name)
            unlock = ET.Element('unlock')
            unlock.text = name
            researchdataentry.append(unlock)
            # TODO - Add research reqs name back into Terraindata

# Backannotate research with research it unlocks
for researchdataentry in ResearchRoot:
  # Crappy solution, breaks if more than 9 research unlocks. Fix!
  if researchdataentry.find('ResearchRequirements'):
    researchrequirements = researchdataentry.find('ResearchRequirements')
    for resreq in researchrequirements:
      # print('Res', resreq.text)
      for resreqdataentry in ResearchRoot:
        if resreqdataentry.find('Key').text.lower() == resreq.text.lower():
          # print( resreqdataentry.find('Name').text  + " --|> " + researchdataentry.find('Name').text )
          a = ET.Element('unlockres')
          a.text = researchdataentry.find('Name').text
          resreqdataentry.append(a)

plant = open("Research.uml","w")
plant.write("@startuml\n")
# Iterate across all research options
for researchdataentry in ResearchRoot:
  planttree = ""
  print("\n\n",researchdataentry.find('Name').text, "\n")
  print("{{Research" + '\n' +
        "|name = " + researchdataentry.find('Name').text + '\n' +
        "|image = " + researchdataentry.find('Name').text + ".png", 
        )
  plant.write( "class " + researchdataentry.find('Name').text.replace( " ", "_").replace("-","_") + " {\n")
  if researchdataentry.find('ScanRequirements'):
    plant.write("  -- Scan Requirements --\n" )
    scanrequirements = researchdataentry.find('ScanRequirements')
    count=1
    for scanreq in scanrequirements:
      # print('Sca', scanreq.text)
      scanname = "Unknown"
      for TerrainData in TerrainDataRoot:
        if TerrainData.find('Key').text == scanreq.text:
          scanname = TerrainData.find('Name').text
      for itementry in ItemsRoot:
        if itementry.find('Key').text == scanreq.text:
          scanname = itementry.find('Name').text
      print("|scan" + str(count) + " = [[" + scanname + "]]")
      plant.write("  -"+scanname+"\n")
      count = count + 1
  if researchdataentry.find('ResearchRequirements'):
    researchrequirements = researchdataentry.find('ResearchRequirements')
    count=1
    for resreq in researchrequirements:
      # print('Res', resreq.text)
      resname = "Unknown"
      for scanresearchdataentry in ResearchRoot:
        if scanresearchdataentry.find('Key').text.lower() == resreq.text.lower():
          resname = scanresearchdataentry.find('Name').text
      print("|research" + str(count) + " = [[" + resname + "]]")
      count = count + 1
  
  if researchdataentry.find('ProjectItemRequirements'):
    print("|research_station = [[Laboratory]]")
    plant.write("  -- Project Requirements --"+"\n")
    projectrequirements = researchdataentry.find('ProjectItemRequirements')
    count = 1
    for projreq in projectrequirements:
      # print('Pro',projreq.find('Key').text)
      projname = "Unknown"
      for TerrainData in TerrainDataRoot:
        if TerrainData.find('Key').text == projreq.find('Key').text:
          projname = TerrainData.find('Name').text
      for itementry in ItemsRoot:
        if itementry.find('Key').text == projreq.find('Key').text:
          projname = itementry.find('Name').text      
      print("|pod" + str(count) + " = " + projreq.find('Amount').text + " [[" + projname + "]]")
      plant.write("  #" + projreq.find('Amount').text + " " + projname +"\n")
      oount = count + 1
  else:
    print("|research_station = [[Research Station]]")
    print("|research_points = " + researchdataentry.find('ResearchCost').text )
    plant.write("  -- Research Cost --"+"\n")
    plant.write("  ~"+researchdataentry.find('ResearchCost').text+"\n")
  unlockrescount = 1
  unlockcount = 1
  for ul in researchdataentry:
    if ul.tag == 'unlockres':
      print("|unlockres%02d" % unlockrescount + " = [[" + ul.text + "]]")
      unlockrescount = unlockrescount + 1
      planttree = planttree + "  " + researchdataentry.find('Name').text.replace( " ", "_").replace("-","_") + " --|> " + ul.text.replace(" ", "_").replace("-","_") + "\n"
    if ul.tag == 'unlock':
      print("|unlock%02d" % unlockcount + " = [[" + ul.text + "]]")
      if unlockcount == 1:
        plant.write("  -- Unlocks --"+"\n")
      plant.write( "  +" + ul.text +"\n")
      unlockcount = unlockcount + 1
  print("|note = " + researchdataentry.find('PreDescription').text)
  print("}}")
  plant.write("}\n\n")
  plant.write(planttree + "\n")
  
plant.write("@enduml\n")
plant.close()

# TODO Iterate across all manufacturer items
# Print wiki output
 
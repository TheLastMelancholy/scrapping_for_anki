import genanki
import os
from pathlib import Path

def generateNamedImages(targetDir=os.path.join(os.getcwd(),"scrapped")):
    namedImagesList = []
    for _r, _d, _f in os.walk(targetDir):
        for f in _f:
            namedImagesList.append(os.path.join(_r,f))
    return namedImagesList

imageToNameModel = genanki.Model(
    1888923,
    'Plain text model',
    fields=[
        {'name': 'MyMedia'},
        {'name': 'Answer'}
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{MyMedia}}',
            'afmt': '{{MyMedia}}<hr id="answer">{{Answer}}',
        },
    ])


birdsDeck = genanki.Deck(123414525425, 'Birds of Belarus')

namedImages = generateNamedImages()
for namedImage in namedImages:
    name = Path(namedImage).stem
    fileBaseName = os.path.basename(namedImage)
    labeledImageNote = genanki.Note(model=imageToNameModel,
                                    fields=[f'<img src=\"{fileBaseName}\">',name])
    birdsDeck.add_note(labeledImageNote)

myPackage = genanki.Package(birdsDeck)
myPackage.media_files = generateNamedImages()
myPackage.write_to_file('birdsOfBelarus.apkg')

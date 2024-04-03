from dotenv import load_dotenv
from argilla import (
    init,
    list_datasets,
    delete,
    FeedbackDataset
)
import os

load_dotenv('D:\\gitFolders\\python_de_learners_data\\.env')

init(api_key="owner.apikey",
     api_url="https://kamaljp-argillatest.hf.space",
     extra_headers={"Authorization": f"Bearer {os.environ['HUGGING_FACE_KEY']}"})

gen1ds = list_datasets()
gen2ds = FeedbackDataset.list(workspace='hfgilla')

if len(gen1ds) > 0:
    for ds in gen1ds:
        print(ds.name, 'is deleted')
        delete(name=ds.name, workspace='hfgilla')
else:
    print('No gen1 dataset available to delete... Checking gen2 DS')

if len(gen2ds) > 0:
    for ds in gen2ds:
        print(ds.name, 'is deleted')
        FeedbackDataset.from_argilla(name=ds.name, workspace='hfgilla').delete()
else:
    print('No gen2 dataset available to delete... Exiting')
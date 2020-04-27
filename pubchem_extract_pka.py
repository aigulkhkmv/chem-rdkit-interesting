import json

import requests
from requests import Timeout
from loguru import logger

pka = {}
for i in range(1, 5000):
    logger.info("Structure number {}", i)
    retry = 0
    success = False
    while retry != 5 and success is False:
        logger.info("Structure number {}. Retry {}. Success {}", i, retry, success)
        try:
            r = requests.get(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{i}/JSON')
            success = True
            logger.info("Request is successful")
            pka.update({i: []})
            for section in r.json()['Record']['Section']:
                if section.get('TOCHeading') == 'Chemical and Physical Properties':
                    for subsection in section['Section']:
                        if subsection['TOCHeading'] == 'Experimental Properties':
                            for subsubsection in subsection['Section']:
                                if subsubsection['TOCHeading'] == 'Dissociation Constants':
                                    pka[i].append(subsubsection)
                                    logger.info("Pka info isn't absent")

        except Timeout:
            retry += 1
            logger.info("Timeout error. Retry {}", retry)

    if i % 1000 == 0:
        logger.info("Structures {}. Write to file pka_data_{}.json", i, i)
        with open(f'pka_data_{i}.json', 'w') as outfile:
            json.dump(pka, outfile)
        pka = {}


with open(f'pka_data_{i}.json', 'w') as outfile:
    logger.info("The last structures {}. Write to file pka_data_{}.json", i, i)
    json.dump(pka, outfile)

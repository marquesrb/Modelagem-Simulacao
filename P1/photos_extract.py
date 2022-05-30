import argparse
import json
import re

def get_photo_array_positions(txt):
    s = txt.index("\"photos\":[{")
    e = txt.index("}]", s + 1)
    return s, e + len("}]")

def clean_extracted(txt):
    txt = json.loads(txt)
    clean = []
    for index in range(0,7847):
        lat = txt['photos'][index]['lat']
        lng = txt['photos'][index]['lng']
        head = txt['photos'][index]['heading']
        date = txt['photos'][index]['shot_date']
        clean.append({'lat': lat, 'lng': lng, 'heading': head, 'shot_date': date})
    clean =  "{\"photos\":"+str(clean)+"}"
    return clean.replace("\'", "\"")
    
def make_extract_photos_JSON(output_file, json_msg):
    first_pos, last_pos = get_photo_array_positions(json_msg)
    extracted_str = "{" + json_msg[first_pos:last_pos] + "}"
    with open(output_file, "w") as ejf:
        ejf.write(extracted_str)
    return extracted_str

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extraí o campo 'photos' da resposta JSON da API do OpenStreetCam.")
    parser.add_argument(
        'jsonfile',
        type=str,
        help="O arquivo JSON com a resposta do OpenStreetCam."
    )

    args = parser.parse_args()
    jsonfile = args.jsonfile
    extracted_filename = "extracted_" + jsonfile
    cleaned_filename = "cleaned_" + jsonfile

    with open(jsonfile, "r") as jf:
        # Aqui o array 'photos' é extraído e colocado 
        # em outro arquivo (com o prefixo extracted_),
        # para facilitar o processamento do array.
        #
        # Em seguida usamos a função clean_extracted para
        # criar um terceiro arquivo (com prefixo _cleaned)
        # que contenha somente os campos de interesse para
        # a análise.
        txt = jf.read()
        extracted_str = make_extract_photos_JSON(extracted_filename, txt)

        with open(cleaned_filename, "w") as cjf:
            cjf.write(clean_extracted(extracted_str))




    pass
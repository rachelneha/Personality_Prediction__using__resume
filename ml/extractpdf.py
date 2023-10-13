import re
import PyPDF2
from typing import Dict


def personality_detection_from_reviews_submitted(model_input: str) -> Dict[str, float]:
    if len(model_input) < 20:
        ret = {
            "Extroversion": float(0),
            "Neuroticism": float(0),
            "Agreeableness": float(0),
            "Conscientiousness": float(0),
            "Openness": float(0),
        }
        return ret

    else:
        from transformers import BertForSequenceClassification, BertTokenizer

        model = BertForSequenceClassification.from_pretrained("./Personality_detection_Classification_Save/",
                                                              num_labels=5)  # =num_labels)
        tokenizer = BertTokenizer.from_pretrained('./Personality_detection_Classification_Save/', do_lower_case=True)
        print("Loaded...!")

        model.config.label2id = {
            "Extroversion": 0,
            "Neuroticism": 1,
            "Agreeableness": 2,
            "Conscientiousness": 3,
            "Openness": 4,
        }

        model.config.id2label = {
            "0": "Extroversion",
            "1": "Neuroticism",
            "2": "Agreeableness",
            "3": "Conscientiousness",
            "4": "Openness",
        }
        import torch

        # Encoding input data
        dict_custom = {}
        preprocess_part1 = model_input[:len(model_input)]
        preprocess_part2 = model_input[len(model_input):]
        dict1 = tokenizer.encode_plus(preprocess_part1, max_length=1024, padding=True, truncation=True)
        dict2 = tokenizer.encode_plus(preprocess_part2, max_length=1024, padding=True, truncation=True)
        dict_custom['input_ids'] = [dict1['input_ids'], dict1['input_ids']]
        dict_custom['token_type_ids'] = [dict1['token_type_ids'], dict1['token_type_ids']]
        dict_custom['attention_mask'] = [dict1['attention_mask'], dict1['attention_mask']]
        outs = model(torch.tensor(dict_custom['input_ids']), token_type_ids=None,
                     attention_mask=torch.tensor(dict_custom['attention_mask']))
        b_logit_pred = outs[0]
        pred_label = torch.sigmoid(b_logit_pred)
        ret = {
            "Extroversion": float(pred_label[0][0]),
            "Neuroticism": float(pred_label[0][1]),
            "Agreeableness": float(pred_label[0][2]),
            "Conscientiousness": float(pred_label[0][3]),
            "Openness": float(pred_label[0][4]), }
        return ret


class ResumeParser(object):

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def get_extracted_data(self):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{10}'
        # define the regular expression pattern for college names
        college_pattern = r'\b[A-Za-z\s\(\)\-\.,&\s]*?(College|University|Institute|Technology|Management|IIM)\b'
        import spacy

        # Load the PDF file
        with open(self.pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)

            # Extract the number of pages
            no_of_pages = len(pdf_reader.pages)

            # Extract the text from the PDF file
            text = ''
            for page_num in range(no_of_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            # Load the spaCy model
            nlp = spacy.load('en_core_web_sm')

            # Parse the text using the spaCy model
            doc = nlp(text)

            # Extract the information
            info = {
                'name': None,
                'email': None,
                'mobile_number': None,
                # 'skills': None,
                # 'college_name': None,
                # 'degree': None,
                # 'designation': None,
                # 'experience': None,
                # 'company_names': None,
                'no_of_pages': no_of_pages,
                # 'total_experience': None,
            }

            #         "skills": null,
            #         "college_name": "Aroor House  \nEvoor South",
            #         "degree": null,
            #         "designation": null,
            #         "company_names": "Kerala   \n      School                       ",
            #         "no_of_pages": 2,
            #         "total_experience": "0 years"

            for entity in doc.ents:
                if entity.label_ == 'PERSON' and not info['name']:
                    info['name'] = entity.text
                elif entity.label_ == 'EMAIL':
                    info['email'] = entity.text
                elif entity.label_ == 'PHONE':
                    info['mobile_number'] = entity.text
                 # elif entity.label_ == 'DEGREE' and not info['degree']:
                #     info['degree'] = entity.text
                # elif entity.label_ == 'TITLE' and not info['designation']:
                #     info['designation'] = entity.text
                # elif entity.label_ == 'DATE' and not info['experience']:
                #     info['experience'] = entity.text
                # elif entity.label_ == 'ORG' and not (info['company_names'] and len(info['company_names']) > 12):
                #     info['company_names'] = entity.text
                # elif entity.label_ == 'SKILL' and not info['skills']:
                #     info['skills'] = entity.text

            if not info['email']:
                info['email'] = re.findall(email_pattern, text)
            if not info['mobile_number']:
                info['mobile_number'] = re.findall(phone_pattern, text)
            # if not info['college_name']:
            #     info['college_name'] = re.findall(college_pattern, text)

            return info

    def get_traits(self):
        text = ''
        with open(self.pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)

            # Extract the number of pages
            no_of_pages = len(pdf_reader.pages)

            # Extract the text from the PDF file
            for page_num in range(no_of_pages):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        import spacy

        # Load the spaCy model
        nlp = spacy.load('en_core_web_sm')
        doc = nlp.make_doc(("".join([t.strip().replace('  ', ' ') for t in text.split('\n') if len(t.strip().replace('  ', '')) > 50])))
        out = personality_detection_from_reviews_submitted(str(doc))
        return out


if __name__ == "__main__":
    ResumeParser('../media/neharesume1i.pdf').get_extracted_data()


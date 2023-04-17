import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

obj_c_pattern1 = [{'LOWER': 'objective'},
                  {'IS_PUNCT': True, 'OP': '?'},
                  {'LOWER': 'c'}]

obj_c_pattern2 = [{'LOWER': 'objectivec'}]

golang_pattern1 = [{'LOWER': 'golang'}]
golang_pattern2 = [{'LOWER': 'go',
                    'POS': {'NOT_IN': ['VERB']}}]

python_pattern = [{'LOWER': 'python'}]
ruby_pattern   = [{'LOWER': 'ruby'}]
js_pattern     = [{'LOWER': {'IN': ['js', 'javascript']}}]

matcher = Matcher(nlp.vocab, validate=True)
matcher.add("OBJ_C_LANG", [obj_c_pattern1, obj_c_pattern2])
matcher.add("PYTHON_LANG", [python_pattern])
matcher.add("GO_LANG",  [golang_pattern1, golang_pattern2])
matcher.add("JS_LANG",  [js_pattern])
matcher.add("RUBY_LANG",  [ruby_pattern])


doc = nlp("I am an iOS dev who codes in both python, go/golang as well as objective-c")

print([(t, t.pos_) for t in doc])

for match_id, start, end in matcher(doc):
    print(doc[start: end])
    print(nlp.vocab.strings[match_id])
# md = matcher(doc)
# print(md)

text = """
Location - Jerusalem, Har Hahotzabim (full time)
An excellent opportunity to integrate into a technological, dynamic and fun work environment where you can influence and contribute, while learning and personal development in the field.
ResponsibilitiesProviding service and technical support (Help Desk) regarding computing, hardware, software and terminal equipment.Receiving calls for assistance and handling malfunctions, routing to professional care if necessary.Responsibility for handling complex and continuous faults in the computer systems.
Qualifications1-2 years of experience in technical assistance and support for users (help desk).Bachelor's degree in computer science / graduate of a higher course in computer systems / Computer Practical Engineer.Experience in providing telephone technical support.Experience in providing customer service in any field.Basic knowledge of computers: office applications, networks, printers, technical faults.
"""

doc2 = nlp(text)
print(doc2[0:48])
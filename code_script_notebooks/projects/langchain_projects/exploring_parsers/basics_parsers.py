"""
“Get format instructions”: A method which returns a string containing instructions for how the output of a language model should be formatted.
“Parse”: A method which takes in a string (assumed to be the response from a language model) and parses it into some structure.
"""
from langchain.output_parsers import (
    PydanticOutputParser,
    DatetimeOutputParser,
    CommaSeparatedListOutputParser,
    EnumOutputParser,
    OutputFixingParser,
    YamlOutputParser,
    StructuredOutputParser,
    XMLOutputParser,
    RetryOutputParser,
    RegexDictParser,
    RegexParser,
    PandasDataFrameOutputParser,
    JsonOutputToolsParser
)
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from enum import Enum
import os
import openai
from dotenv import load_dotenv
from langchain_community.utils.openai_functions import (
    convert_pydantic_to_openai_function,
    convert_pydantic_to_openai_tool
)

load_dotenv("D:\\gitFolders\\python_de_learners_data\\.env")

openai.api_key = os.environ['OPENAI_API_KEY']
# print(openai.api_key)  # checking the key is registered

model = OpenAI(model='gpt-3.5-turbo-instruct', temperature=0.0)


class Joke(BaseModel):
    setup: str = Field(description="Setup for the question of the joke")
    punchline: str = Field(description="Answer to resolve the joke")

    # applying custom validator to the pydantic
    @validator("setup")
    def question_ends_with_question_mark(cls, field):
        if field[-1] != "?":
            raise ValueError("Badly formed Question!")
        return field


class REProperty(BaseModel):
    prop_sale: str = Field(description="Property for sale")
    prop_rent: str = Field(description="Property for rent")
    look_buy: str = Field(description="Looking to buy")
    look_rent: str = Field(description="Looking to rent")

# pydantic_parser = PydanticOutputParser(pydantic_object=Joke)
pydantic_parser_property = PydanticOutputParser(pydantic_object=REProperty)

# print("Pydantic Parser output")
# print(pydantic_parser.get_format_instructions())
print(pydantic_parser_property.get_format_instructions())

# simple_json_parser = SimpleJsonOutputParser()

# csv_parser = CommaSeparatedListOutputParser()
# print("CSV Parser output")
# print(csv_parser.get_format_instructions())

# datetime_parser = DatetimeOutputParser()
# print("Datetime Parser output")
# print(datetime_parser.get_format_instructions())


# # Enum Parser will require Enum object
# class Colors(Enum):
    # RED = "red"
    # GREEN = "green"
    # BLUE = "blue"

class REProperty(Enum):
    RENT = "property for rent"
    SELL = "property for sale"
    TOBUY = "looking to buy"
    TORENT = "looking to rent"


# enum_parser = EnumOutputParser(enum=Colors)
# print("Enum Parser output")
# print(enum_parser.get_format_instructions())

# property_parser = EnumOutputParser(enum=REProperty)
# print(property_parser.get_format_instructions())

# json_opt_parser = JsonOutputToolsParser()
# print("Json Tools Parser Schema")
# print(json_opt_parser.get_output_schema())

# # openai_func = [convert_pydantic_to_openai_function(Joke)]

# print(openai_func[0])

# new_parser = OutputFixingParser.from_llm(parser=pydantic_parser, 
                                         # llm=model)

# def format_parser_output(parser_output: Dict[str, Any]) -> None:
    # for key in parser_output.keys():
        # parser_output[key] = parser_output[key].to_dict()
    # return pprint.PrettyPrinter(width=4,
                                # compact=True).pprint(parser_output)
# Pydantic output section
# prompt = PromptTemplate(
    # template="Answer the user query. \n{format_instruction}\n{query}",
    # input_variables=["query"],
    # partial_variables={"format_instruction": pydantic_parser.get_format_instructions()}
# )
prompt1 = PromptTemplate(
    template="Classify the given complete message based on below instructions. \n{format_instruction}\n{query}\n Keep the entire message intact",
    input_variables=["query"],
    partial_variables={"format_instruction": pydantic_parser_property.get_format_instructions()} 
)

# prompt_model = prompt | model
prompt_property_model = prompt1 | model

# output = prompt_model.invoke({"query": "Tell me a joke"})
# print(pydantic_parser.invoke(output))

query = """
*DLH DARPAN TOWER*\n2BHK FLAT SALE\n2.OPTINS\n2.CR TO 2.20.CR NEGOTIABLE \n\n*2BHK MITTAL COVE*\nNEW BUILDING\nPRICE 2.10.CR NEGOTIABLE \n\n*2BHK CAME SWEET 16*\nAZAD NAGAR\nASKING 1.90.CR NEGOTIABLE \n\n*2BHK PALASH TOWER*\n3.OPTINS\n2.25.CR TO 2.55.CR\n\n1BHK FLAT SALE\n*SANGAM APARTMENT*\nCARPET 500.SQFIT\nPRICE 1.40.CR\n\nVEER DESSAI ROAD ANDHERI WEST\n\n\n*2BHK RENTAL FLAT*\n*VAIDEHI APARTMENTS*\n*FURNISHED FLAT*\n*RENT 70.00* *NEGOTIABLE*\n*VEERA DESAI ROAD NEAR AZAD NAGAR METRO STATION ANDHERI WEST*\n\n2BHK RENTAL\nEXCLUSIVE FULLY FURNISHED\n*SHANTIVAN MHADA OSHIWARA*\nRENT 75.000\n \n3BHK RENTAL\n*MITTAL COVE*\nNEW BUILDING\nEMPTY FLAT\n3BHK 2BHATHROO\nRENT 75.000\n\n3bhk semi furnished flat \n*SHIV SHIVAM TOWER* \nonly working family client immediate possession \n*RENT 80K*\n\nANY INFORMATION\nCALL ME\nDHARMENDRA\n9987741783
"""

output_1 = prompt_property_model.invoke({"query": query})
print(pydantic_parser_property.invoke(output_1))

# Simple JSON Parser output section
# json_prompt = PromptTemplate.from_template(
    # "Return a JSON object with an `answer` key that answers following {question}"
# )
# json_chain = json_prompt | model | json_parser

# print(list(json_chain.stream({"question": "Where is Inca Temple?"})))

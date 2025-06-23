import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()
# Get the OpenAI API key from the environment
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)

RESPONSE_FORMAT_JSON = {
    "type": "json_schema",
    "json_schema": {
        "name": "proposition_info",
        "schema": {
            "type": "object",
            "properties": {
                "info": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "organization": {"type": "string"},
                            "prop": {"type": "string"},
                            "name": {"type": "string"},
                            "support": {"type": "string"},
                            "additionalProperties": False,
                        },
                    },
                },
            },
        },
    },
}

# Few-shot learning examples for the model
examples = """
Extract organizations making arguments for/against propositions.

Example 1:
Link: "https://voterguide.sos.ca.gov/propositions/2/arguments-rebuttals.htm"
Output:
{
  "info": [
    {"organization": "California Teachers Association", "name": "David Goldberg", "prop": "Proposition 2", "support": "Yes"},
    {"organization": "California School Nurses Organization", "name": "Sheri Coburn", "prop": "Proposition 2", "support": "Yes"},
    {"organization": "Community College League of California", "name": "Larry Galizio", "prop": "Proposition 2", "support": "Yes"},
    {"organization": "International Brotherhood of Electrical Workers Local Union 11", "name": "Diana Limon", "prop": "Proposition 2", "support": "Yes"},
    {"organization": "Assemblyman Bill Essayli", "name": null, "prop": "Proposition 2", "support": "No"},
    {"organization": "Howard Jarvis Taxpayers Association", "name": "Jon Coupal", "prop": "Proposition 2", "support": "No"},
  ]
}

Example 2:
Link: "https://voterguide.sos.ca.gov/propositions/3/arguments-rebuttals.htm"
Output:
{
  "info": [
    {"organization": "Assemblymember Evan Low", "name": null, "prop": "Proposition 3", "support": "Yes"},
    {"organization": "Equality California", "name": "Tony Hoang", "prop"":Proposition 3", "support": "Yes"},
    {"organization": "Planned Parenthood Affiliates of California", "name": "Jodi Hicks", "prop": "Proposition 3", "support": "Yes"},
    {"organization": "Senator Scott Wiener", "name": null, "prop": "Proposition 3", "support": "Yes"},
    {"organization": "Human Rights Campaign", "name": "Mia Kirby", "prop": "Proposition 3", "support": "Yes"},
    {"organization": "TransLatin@ Coalition", "name": "Maria Roman", "prop": "Proposition 3", "support": "Yes"},
    {"organization": "California Family Council", "name": "Jonathan Keller", "prop": "Proposition 3", "support": "No"},
    {"organization": "The American Council of Evangelicals", "name": "Rev. Tanner DiBella", "prop"":Proposition 3", "support": "No"},
  ]
}

Example 3:
Link: "https://voterguide.sos.ca.gov/propositions/4/arguments-rebuttals.htm"
Output:
{
  "info": [
    {"organization": "Clean Water Action", "name": "Jennifer Clary", "prop": "Proposition 4", "support": "Yes"},
    {"organization": CALFIRE Firefighters", "name": "Tim Edwards", "prop"":Proposition 4", "support": "Yes"},
    {"organization": "National Wildlife Federation", "name": "Beth Pratt", "prop": "Proposition 4", "support": "Yes"},
    {"organization": "Community Water Center", "name": "Susana De Anda ", "prop": "Proposition 4", "support": "Yes"},
    {"organization": "The Nature Conservancy", "name": "Sarah Gibson", "prop": "Proposition 4", "support": "Yes"},
    {"organization": "Coalition for Clean Air", "name": "Christopher Chavez", "prop": "Proposition 4", "support": "Yes"},
    {"organization": "Senate Minority Leader Brian W. Jones", "name": "", "prop": "Proposition 4", "support": "No"},
    {"organization": "Assemblyman Jim Patterson", "name": "", "prop"":Proposition 4", "support": "No"},
    {"organization": "Howard Jarvis Taxpayers Association", "name": "Jon Coupal", "prop"":Proposition 4", "support": "No"},
  ]
}
"""


def extract(link):
    prompt=f"""
  {examples}
  Example 4
  Link: "{link}"
  Output:
  """

    # Request from OpenAI using the few-shot prompt
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format=RESPONSE_FORMAT_JSON,
        temperature=0
    )

    # Extract and print the response
    content = completion.choices[0].message.content
    content = content.replace("json", "")

    # Convert the response text to a JSON object
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("Response is not valid JSON:", content)
        return None

if __name__ == "__main__":
    links = []
    results = []

    with open("compiled_propositions.json", "r") as file:
        props = json.load(file)

    for item in props:
        data_url = item["data_url"]
        propositions = item["propositions"]
        for prop in propositions:
            link = data_url.format(prop)
            links.append(link)

    for link in links:
        print(link)
        info = extract(link)
        results.append(info)

    # for info in results:
    #     print(json.dumps(info, indent=2))

    with open("compiled_prop_results.json", "w") as file:
        json.dump(results, file, indent=2)

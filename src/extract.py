import requests
from bs4 import BeautifulSoup
import re
import json
import sys
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app_args import Args

# Load environment variables from the .env file
load_dotenv()
# Get the OpenAI API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")
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
                            "name": {"type": "string"},
                            "prop": {"type": "string"},
                            "year": {"type": "number"},
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
Extract organizations making arguments for/against propositions. For the output, put the input argument year in the year field in json

Example 1:
text_block: "VOTE YES ON PROP. 2 TO HELP MORE CALIFORNIA STUDENTS LEARN IN SAFE, CLEAN, UPGRADED SCHOOLS!
Many public schools and community colleges throughout California are outdated and need repairs and upgrades to meet basic health and safety standards, prepare students for college and 21st Century careers, and retain and attract quality teachers. Prop. 2 will meet those needs and is guided by strict taxpayer accountability protections so funds are spent as promised with local control.
REPAIRING AND UPGRADING CALIFORNIA’S PUBLIC SCHOOLS
Many schools in California are old, deteriorating, unsafe and cannot support the basic needs of our children. Prop. 2 provides funding for urgent repairs to leaky roofs; deteriorating gas, electrical, and sewer lines; plumbing and restrooms; providing clean drinking water; removing hazardous mold, asbestos, and lead paint from our schools; and protecting students from extreme heat.
MAKING SCHOOLS SAFER
Too many of our local schools lack adequate safety and security protections. Prop. 2 will make students safer by funding door locks, emergency communications and security systems, fire alarms, smoke detectors, and more.
PREPARING STUDENTS FOR 21st CENTURY CAREERS
Prop. 2 will upgrade local schools and community colleges including science, engineering, career technical, and vocational education classrooms; labs; and learning technology. It will help more students get job training, technical knowledge, and specialized skills to compete for good–paying jobs in the competitive economy.
INCREASING ACCESS TO AN AFFORDABLE COLLEGE EDUCATION
Prop. 2 will increase access to quality, affordable higher education for all Californians—allowing more students to start their college education, earn college credits, and transfer to a four–year university without crushing debt.
HELPING RETURNING VETERANS
Prop. 2 helps local community colleges upgrade facilities to expand veteran services, job training, and support for the tens of thousands of California’s returning veterans who rely on their local community college for job training and to complete their education and enter the civilian workforce.
RESTORING SCHOOLS AFFECTED BY WILDFIRES, EARTHQUAKES, AND OTHER NATURAL DISASTERS
Prop. 2 provides immediate assistance to schools that are damaged or destroyed by wildfires, floods, earthquakes, and other natural disasters so they can quickly get up and running.
PROTECTING LOCAL CONTROL OVER EVERY PROJECT
Prop. 2 protects local control by requiring that its funding only be used for projects approved by local school and community college districts, with local community input. All of the money will be controlled and spent locally, where taxpayers have a voice in deciding how these funds are best used to improve their neighborhood schools, without increasing local property taxes.
FISCALLY RESPONSIBLE WITH TOUGH TAXPAYER ACCOUNTABILITY
Prop. 2 requires public disclosure of every dollar, tough independent financial audits, and strict limits on administrative and bureaucratic costs. These protections ensure that funding is spent directly on schools and used efficiently and as promised.
Our schools are in desperate need of upgrades and repairs to ensure our students are safe and ready to learn. Prop. 2 will help our students succeed.
PLEASE JOIN US IN VOTING YES ON PROP. 2.
David Goldberg, President
California Teachers Association
Sheri Coburn, Executive Director
California School Nurses Organization
Larry Galizio, Chief Executive Officer
Community College League of California"
Output:
{
  "info": [
    {"organization": "California Teachers Association", "name": "David Goldberg", "prop": "Proposition 2", "year": null, "support": "Yes"},
    {"organization": "California School Nurses Organization", "name": "Sheri Coburn", "prop": "Proposition 2", "year": null, "support": "Yes"},
    {"organization": "Community College League of California", "name": "Larry Galizio", "prop": "Proposition 2", "year": null, "support": "Yes"},
  ]
}

Example 2:
text_block: "NO ON PROPOSITION 2: Tell politicians to prioritize education funding over free healthcare for illegal immigrants in our state budget, rather than further burdening taxpayers to pay off Sacramento's ballooning bond debt.
Proposition 2 is yet another attempt to circumvent California's financial problems by asking taxpayers to approve a $10 billion bond for education financing that should have been included in this year's $288 billion budget package,
A budget is a reflection of priorities, and our State Legislature chose to prioritize over $5 billion for universal illegal immigrant healthcare rather than providing funds to support and repair our school infrastructure. Billions in new bond debt is not the answer.
Prop. 2 Saddles Future Generations with Debt that Our Kids Will Be Paying Off for Decades
The Howard Jarvis Taxpayers Association points out that bonds are borrowed money that must be paid back, plus interest, even if that means cutting vital programs to do it. Governor Newsom recently declared a budget emergency because California spends more than it takes in. Children in school today will be drowning in new debt for decades if Prop. 2 passes.
Politicians want to borrow $10 billion from Wall Street and make Californians pay it back with interest, forcing taxpayers to pay up to $10 billion for debt service payments.
California Is Out of Money, Californians Are Over-taxed, Prop. 2 Will Make Things Worse
California, with rampant infation and the highest gas and graduated income taxes in the nation, already has over $109 billion of outstanding and unissued bonds alongside almost $200 billion of unfunded pension liabilities and retiree medical benefits—over a quarter trillion dollars. Californians will have to shoulder a greater increase in their tax burden paying off our bonds and related interest payments. Our bond debt alone is already $2,460 per person.
Sacramento politicians overspend, issue bonds, and punish us with tax hikes on our cars, gasoline, and income. And those tax dollars rarely go where politicians say they will— our roads crumble while billions go to High-Speed Rail.
Prop. 2 Is the Latest in a Long List of Broken Promises
In 2012, California voters approved Proposition 30's “temporary” increases to income and sales taxes. Then, Proposition 55 in 2016 extended many of those “temporary” taxes to 2028. Both times, teachers' unions promised billions in funding for our schools.
Money pits in the vast education bureaucracy will suck up most Prop. 2 funds without one cent going toward direct instruction in school classrooms. Instead, this money will be spent on wasteful construction projects benefiting special interests.
California's schools are consistently ranked near the lowest in the country. Rather than throwing nearly $20 billion into school construction projects, our state needs a well thought out, long-term solution to achieve a high standard of excellence in reading, writing, and math. Prop. 2 does nothing to improve classroom instruction or help our children succeed.
Voters rejected Proposition 13, a $15 billion school bond, in 2020 for exactly these reasons.
VOTE NO ON PROP. 2.
Assemblyman Bill Essayli"
Output:
{
  "info": [
    {"organization": "Assemblyman Bill Essayli", "name": null, "prop": "Proposition 2", "year": null, "support": "No"},
    {"organization": "Howard Jarvis Taxpayers Association", "name": "Jon Coupal", "prop": "Proposition 2", "year": null, "support": "No"},
    ]
   }
"""


def extract_from_text_block(text_block, year):
    prompt = f"""
  {examples}
  Example 1
  text_block: "{text_block}"
  Output:
  """
    # Request from OpenAI using the few-shot prompt
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You extract structured data from text."},
            {"role": "user", "content": prompt}
        ],
        response_format=RESPONSE_FORMAT_JSON,
        temperature=0,
    )

    # Extract and print the response
    content = completion.choices[0].message.content

    # Try to parse the result as JSON
    try:
        import json
        data = json.loads(content)

        # Inject the year information about the proposition into each item
        for item in data["info"]:
            item["year"] = year

        return data
        # return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Could not parse response as JSON:")
        print(content)
        return []


def extract_prop_names_with_affiliations(url):
    response = requests.get(url)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text(separator="\n")

    sections = {
        "supporters": None,
        "opponents": None
    }

    lines = content.split('\n')
    current_section = None
    buffer = []

    section_map = {
        "argument in favor": "supporters",
        "argument against": "opponents",
        "rebuttal to argument in favor": "rebuttal_to_favor",
        "rebuttal to argument against": "rebuttal_to_against"
    }

    sections['supporters'] = ''
    sections['opponents'] = ''
    year = None

    for line in lines:
        line_lower = line.lower().strip()
        if year is None:
            # try to find year information
            match = re.search(r"\b(1[0-9]{3}|2[0-9]{3})\b", line)
            if match:
                year = match.group(0)

        if "back to the top" in line_lower:
            # we have reached the end, do not read anymore
            break

        if any(line_lower.startswith(header) for header in section_map):
            # find keywords
            if current_section and buffer:
                sections[current_section] = sections[current_section] + "\n".join(buffer).strip()
                buffer = []

            for k, v in section_map.items():
                if line_lower.startswith(k):
                    if k == 'rebuttal to argument in favor':
                        # lump 'rebuttal to argument in favor' with 'opponents'
                        current_section = 'opponents'
                    elif k == 'rebuttal to argument against':
                        # lump 'rebuttal to arguments aginst' with 'supporters'
                        current_section = 'supporters'
                    else:
                        current_section = v

                    break
        elif current_section:
            buffer.append(line)

    if current_section and buffer:
        sections[current_section] = sections[current_section] + "\n".join(buffer).strip()

    # print('supports:' + sections["supporters"])
    # print('opponents:' + sections["opponents"])

    # Now extract information from each text section
    return {
        "supporters": extract_from_text_block(sections["supporters"], year),
        "opponents": extract_from_text_block(sections["opponents"], year)
    }


# source .venv/bin/activate
# python src/extract.py -h
# python src/extract.py src/compiled_propositions.json -o data/extracted/v0.1/extracted_prop_results.json
if __name__ == "__main__":
    links = []
    results = []
    args = Args().parse()

    with open(args.propositions_json, "r") as file:
        props = json.load(file)

    for item in props:
        year = item["year"]
        data_url = item["data_url"]
        propositions = item["propositions"]
        for prop in propositions:
            link = data_url.format(prop)
            links.append((link, year))

    for link, year in links:
        try:
            result = extract_prop_names_with_affiliations(link)
            if result:
                results.append(result)
        except Exception as e:
            print(f"Failed to process {link}: {e}")

    output_file = args.output if args.output else "./out/compiled_prop_results.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as file:
        json.dump(results, file, indent=2)

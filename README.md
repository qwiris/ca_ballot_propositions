# California Ballot Propositions Datasets
California Ballot Proposition Data. Includes supporters and opponents with their affiliated organizations, 
per ballot proposition.

This dataset compiles endorsements for various California ballot propositions. 
Each record represents an organization or public figure's position on a specific proposition, 
including support or opposition.
---
## 📝 Instructions

---

## ⚠️ Known Issues
+ Depending on selected OpenAI model (ex. gpt-4o, gpt-4o-mini), accuracy varies
  + Currently, code mainly supports gpt-4o
  + Requires further extension to support more advanced, recent models
  
---

## 📁 Dataset Structure

The data is organized as a list of proposition blocks. Each block contains an `"info"` array with entries in the following format:

### ✅ Fields

| Field         | Type   | Description                                             |
|---------------|--------|---------------------------------------------------------|
| `prop`        | string | The proposition number (e.g. `"Proposition 3"`)         |
| `organization` | string | The endorsing organization or name of official          |
| `name`        | string | Individual associated with the endorsement (optional)   |
| `support`     | string | `"Yes"` if supporting, `"No"` if opposing the measure   |

---

## 📌 Example Entry

```json
{
  "organization": "California Teachers Association",
  "name": "David Goldberg",
  "prop": "Proposition 2",
  "support": "Yes"
}

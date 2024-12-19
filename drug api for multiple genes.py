#!/usr/bin/env python
# coding: utf-8

# In[13]:


import requests
import json
import pandas as pd

def get_drug_info(gene_names):
    
    # Convert the list of gene names to a JSON-formatted string
    gene_names_in_json = json.dumps(gene_names)
    
    # Define the GraphQL query to retrieve drug-gene interactions for multiple genes
    query = """
    {
      genes(names: %s) {
        nodes {
          name
          interactions {
            drug {
              name
            }
            interactionScore
            interactionTypes {
              type
              directionality
            }
            sources {
              sourceDbName
            }
          }
        }
      }
    }
    """ % gene_names_in_json

    # Define the API endpoint
    base_url = "https://dgidb.org/api/graphql"

    # Send a POST request to the API with the GraphQL query
    response = requests.post(base_url, json={'query': query})

    # Initialize an empty list to store drug information
    drug_info = []

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Extract drug interaction data from the response
        genes = data.get('data', {}).get('genes', {}).get('nodes', [])
        for gene in genes:
            gene_name = gene.get('name', '')
            interactions = gene.get('interactions', [])
            for interaction in interactions:
                drug_info.append({
                    "Gene Name": gene_name,
                    "Drug Name": interaction.get("drug", {}).get("name", ""),
                    "Interaction Score": interaction.get("interactionScore", ""),
                    "Interaction Types": ", ".join(
                        [f"{t['type']} ({t['directionality']})" for t in interaction.get("interactionTypes", [])]
                    ),
                    "Sources": ", ".join([source.get("sourceDbName", "") for source in interaction.get("sources", [])])
                })
    else:
        print(f"Failed to retrieve data. Error: {response.status_code} Server Error: {response.text}")

    # Convert the list of dictionaries to a DataFrame
    drug_info_df = pd.DataFrame(drug_info)

    return drug_info_df

# Example usage
gene_names = ["TP53", "BRCA1", "EGFR"]  # Replace with your list of genes
drug_df = get_drug_info(gene_names)

# Save the result to a CSV file
drug_df.to_csv("drug_gene_interactions.csv", index=False)

print("Data saved to 'drug_gene_interactions.csv'")


# In[ ]:





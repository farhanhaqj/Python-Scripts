#!/usr/bin/env python
# coding: utf-8

# In[19]:


import requests
import json
import pandas as pd

def get_drug_info(gene_name):
    
    query = f"""
    {{
      genes(names: ["{gene_name}"]) {{
        nodes {{
          name
          interactions {{
            drug {{
              name
            }}
            interactionScore
            interactionTypes {{
              type
              directionality
            }}
            sources {{
              sourceDbName
            }}
          }}
        }}
      }}
    }}
    """

    base_url = "https://dgidb.org/api/graphql"

    response = requests.post(base_url, json={'query': query})

    drug_info = []

    if response.status_code == 200:
        data = response.json()
#         print(data)
        gene = data.get('data', {}).get('genes', {}).get('nodes', [])[0]

        if gene:
            gene_name = gene.get('name', '')
            interactions = gene.get('interactions', [])

            for interaction in interactions:
                drug_info.append({
                    "Gene Name": gene_name,
                    "Drug Name": interaction.get("drug", {}).get("name", ""),
                    "Interaction Score": interaction.get("interactionScore", ""),
                    "Interaction Types": ", ".join([f"{t['type']}" for t in interaction.get("interactionTypes", [])]),
                    "Sources": ", ".join([source.get("sourceDbName", "") for source in interaction.get("sources", [])])
                })
    else:
        print(f"Failed to retrieve data.")
        
    drug_info_df = pd.DataFrame(drug_info)

    return drug_info_df

gene_name = "TP53"  
drug_data = get_drug_info(gene_name)
print(drug_data)


# In[ ]:





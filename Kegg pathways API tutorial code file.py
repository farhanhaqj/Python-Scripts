#!/usr/bin/env python
# coding: utf-8

# In[13]:


import requests

def get_pathways(gene_symbol):
    # Convert the gene symbol to the KEGG gene identifier
    gene_search_url = f"http://rest.kegg.jp/find/genes/{gene_symbol}"
    gene_response = requests.get(gene_search_url)
    print(gene_response)
    
    if gene_response.status_code != 200 or not gene_response.text.strip():
        print(f"No gene found for symbol: {gene_symbol}")
        return
    
    # Parse the first gene ID (if multiple are returned, pick the first one)
    gene_data = gene_response.text.split("\n")[0]
    kegg_gene_id = gene_data.split("\t")[0]
    print(f"KEGG Gene ID: {kegg_gene_id}")
    
    # Get pathways associated with the gene
    pathway_url = f"http://rest.kegg.jp/link/pathway/{kegg_gene_id}"
    pathway_response = requests.get(pathway_url)
    
    if pathway_response.status_code != 200 or not pathway_response.text.strip():
        print(f"No pathways found for gene: {gene_symbol}")
        return
    
    # Parse the pathway data
    pathway_data = pathway_response.text.strip().split("\n")
    pathway_ids = []
    for line in pathway_data:
        pathway_ids.append(line.split("\t")[1])
    
    # Retrieve pathway names
    pathway_names = []
    for pathway_id in pathway_ids:
        pathway_info_url = f"http://rest.kegg.jp/get/{pathway_id}"
        pathway_info_response = requests.get(pathway_info_url)
        if pathway_info_response.status_code == 200:
            pathway_name = pathway_info_response.text.split("\n")[1].split("NAME")[1].strip()
            pathway_names.append((pathway_id, pathway_name))
    
    # Print pathways
    print(f"Pathways for gene {gene_symbol}:")
    for pid, pname in pathway_names:
        print(f"ID: {pid}, Name: {pname}")
    
    return pathway_names

get_pathways('BRCA1')


# In[ ]:





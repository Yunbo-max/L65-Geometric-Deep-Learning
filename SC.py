# -*- coding: utf-8 -*-
# @Author: Yunbo
# @Date:   2024-02-27 12:00:07
# @Last Modified by:   Yunbo
# @Last Modified time: 2024-02-27 14:01:45
import pandas as pd
import numpy as np
import torch

# Load your CSV file into a DataFrame
def load_data(csv_file):
    return pd.read_excel(csv_file)

# Function to calculate eigenvalues and eigenvectors for each graph
def calculate_eigenvalues_eigenvectors(adjacency_matrices):
    eigenvalues = []
    eigenvectors = []
    for adj_matrix in adjacency_matrices:
        # Calculate Laplacian matrix
        degree_matrix = np.diag(np.sum(adj_matrix, axis=1))
        laplacian_matrix = degree_matrix - adj_matrix
        
        # Calculate eigenvalues and eigenvectors of the Laplacian matrix
        eigenvals, eigvecs = np.linalg.eigh(laplacian_matrix)
        eigenvalues.append(eigenvals)
        eigenvectors.append(eigvecs)
    return eigenvalues, eigenvectors

# Function to create adjacency matrices for each graph
def create_adjacency_matrices(df, num_graphs):
    adjacency_matrices_list = []
    # Drop rows with NaN values in 'CompanyName' or 'Suppliers' columns
    df = df.dropna(subset=['CompanyName', 'Suppliers'])
    unique_nodes = np.unique(df[['CompanyName', 'Suppliers']].values)
    nodes_per_graph = len(unique_nodes) // num_graphs
    graph_nodes = [unique_nodes[i:i+nodes_per_graph] for i in range(0, len(unique_nodes), nodes_per_graph)]

    graph_nodes = graph_nodes[:len(graph_nodes)-1]
    
    for nodes in graph_nodes:
        adj_matrix = np.zeros((len(nodes), len(nodes)))
        node_to_index = {node: idx for idx, node in enumerate(nodes)}
        for _, row in df.iterrows():
            if row['CompanyName'] in nodes and row['Suppliers'] in nodes:
                source_idx = node_to_index[row['CompanyName']]
                target_idx = node_to_index[row['Suppliers']]
                adj_matrix[source_idx, target_idx] = 1  # Assuming a binary relationship
        print(adj_matrix.sum())
        adjacency_matrices_list.append(adj_matrix)
    
    adjacency_matrices_list.pop()
    
    return adjacency_matrices_list


# Function to save data as a .pt file


def save_as_pt_file(adjacency_matrices, eigenvalues, eigenvectors, output_file):
    num_nodes_list = [len(adj_matrix) for adj_matrix in adjacency_matrices]
    
    torch.save((adjacency_matrices, eigenvalues, eigenvectors,num_nodes_list,max(max(ev) for ev in eigenvalues),min(min(ev) for ev in eigenvalues),False,max(len(adj_matrix) for adj_matrix in adjacency_matrices)), output_file)

# Main function to orchestrate the process
def main(csv_file, num_graphs, output_file):
    df = load_data(csv_file)
    adjacency_matrices = create_adjacency_matrices(df, num_graphs)
    eigenvalues, eigenvectors = calculate_eigenvalues_eigenvectors(adjacency_matrices)
    save_as_pt_file(adjacency_matrices, eigenvalues, eigenvectors, output_file)

# Example usage
if __name__ == "__main__":
    csv_file = 'company-customers.xlsx'
    num_graphs = 200
    output_file = 'data_clustering.pt'
    main(csv_file, num_graphs, output_file)

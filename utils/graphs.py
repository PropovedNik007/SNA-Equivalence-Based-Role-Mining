import networkx as nx
import pandas as pd


def graph_article_posting_votes(graph_data):
    G = nx.Graph()

    # Construct the graph
    for _, row in graph_data.iterrows():
        # Define node identifiers
        article_node = f"Article-{row['ID_Article']}"
        posting_node = f"Posting-{row['ID_Posting']}"
        vote_node = f"Vote-{row['ID_Posting']}"

        # Add nodes for ArticleChannel, ArticleRessortName, Article, Posting, and Votes
        G.add_node(row['ArticleChannel'], type='ArticleChannel')
        G.add_node(row['ArticleRessortName'], type='ArticleRessortName')
        G.add_node(article_node, type='Article')
        G.add_node(posting_node, type='Posting')
        G.add_node(vote_node, type='Vote', vote_positive=row['VotePositive'], vote_negative=row['VoteNegative'])

        # Add directed edges
        G.add_edge(row['ArticleChannel'], row['ArticleRessortName'], weight=1)
        G.add_edge(row['ArticleRessortName'], article_node, weight=1)
        G.add_edge(article_node, posting_node, weight=1)
        G.add_edge(posting_node, vote_node, weight=1)

        # Add reply relationship
        if not pd.isna(row['ID_Posting_Parent']):
            parent_posting_node = f"Posting-{row['ID_Posting_Parent']}"
            G.add_edge(parent_posting_node, posting_node, weight=1, label='reply')

    return G

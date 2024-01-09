import networkx as nx
import pandas as pd


def graph_article_posting_votes(graph_data):
    G = nx.DiGraph()

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


def graph_article_posting_weighted_votes(graph_data):
    G = nx.DiGraph()

    for _, row in graph_data.iterrows():
        # Add nodes for ArticleChannel, ArticleRessortName, Article, Posting, and Parent Posting (if exists)
        G.add_node(row['ArticleChannel'], type='ArticleChannel')
        G.add_node(row['ArticleRessortName'], type='ArticleRessortName')
        G.add_node(row['ID_Article'], type='Article')
        G.add_node(row['ID_Posting'], type='Posting')
        if not pd.isna(row['ID_Posting_Parent']):
            G.add_node(row['ID_Posting_Parent'], type='Parent Posting')

        # Add directed edges
        G.add_edge(row['ArticleChannel'], row['ArticleRessortName'], weight=1)
        G.add_edge(row['ArticleRessortName'], row['ID_Article'], weight=1)
        G.add_edge(row['ID_Article'], row['ID_Posting'], weight=1)
        if not pd.isna(row['ID_Posting_Parent']):
            G.add_edge(row['ID_Posting_Parent'], row['ID_Posting'], weight=1, label='reply')

    # Adding weights for votes to the Posting nodes
    for node in G.nodes(data=True):
        if node[1]['type'] == 'Posting':
            posting_row = graph_data[graph_data['ID_Posting'] == node[0]].iloc[0]
            vote_weight = posting_row['VotePositive'] - posting_row['VoteNegative']
            G.nodes[node[0]]['vote_weight'] = vote_weight
    return G


def graph_article_posting_votes_nodes(graph_data):
    G = nx.DiGraph()

    for _, row in graph_data.iterrows():
        # Define node identifiers
        article_node = f"Article-{row['ID_Article']}"
        posting_node = f"Posting-{row['ID_Posting']}"
        vote_node = f"Vote-{row['ID_Posting']}"
        article_channel_node = f"Channel-{row['ArticleChannel']}"
        article_ressort_node = f"Ressort-{row['ArticleRessortName']}"

        # Add nodes for ArticleChannel, ArticleRessortName, Article, Posting, and Votes
        G.add_node(article_channel_node, type='ArticleChannel', name=row['ArticleChannel'])
        G.add_node(article_ressort_node, type='ArticleRessortName', name=row['ArticleRessortName'])
        G.add_node(article_node, type='Article', title=row['ArticleID'])
        G.add_node(posting_node, type='Posting', comment=row.get('PostingComment', ''))
        G.add_node(vote_node, type='Vote', vote_positive=row['VotePositive'], vote_negative=row['VoteNegative'])

        # Add directed edges
        G.add_edge(article_channel_node, article_ressort_node, type='channel_to_ressort')
        G.add_edge(article_ressort_node, article_node, type='ressort_to_article')
        G.add_edge(article_node, posting_node, type='article_to_posting')
        G.add_edge(posting_node, vote_node, type='posting_to_vote')

        # Add reply relationship
        if not pd.isna(row['ID_Posting_Parent']):
            parent_posting_node = f"Posting-{row['ID_Posting_Parent']}"
            G.add_edge(parent_posting_node, posting_node, type='reply', label='reply')

    return G
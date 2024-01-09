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


def graph_posting_posting_weighted_replies(graph_data, directed=False):
    comment_user_mapping = graph_data[['ID_Posting',
                                       'ID_CommunityIdentity']].drop_duplicates().rename(
        columns={'ID_Posting': 'Id_posting',
                 'ID_CommunityIdentity': 'ID_ParentIdentity'})

    result_df = pd.merge(graph_data, comment_user_mapping, left_on='ID_Posting_Parent', right_on='Id_posting',
                         how='left')
    result_df = result_df[['ID_CommunityIdentity', 'ID_ParentIdentity']]
    reply_counts = result_df.groupby(['ID_CommunityIdentity', 'ID_ParentIdentity']).size().reset_index(name='counts')

    reply_counts = reply_counts[:500]

    if directed:
        G = nx.from_pandas_edgelist(reply_counts,
                                    source='ID_CommunityIdentity',
                                    target='ID_ParentIdentity',
                                    edge_attr='counts',
                                    create_using=nx.MultiDiGraph())
    else:
        G = nx.from_pandas_edgelist(reply_counts,
                                    source='ID_CommunityIdentity',
                                    target='ID_ParentIdentity',
                                    edge_attr='counts',
                                    create_using=nx.MultiGraph())

    return G


def graph_user_user_weighted_votes(votes, postings, slice=500, directed=False):
    merged_df = pd.merge(votes, postings[['ID_CommunityIdentity', 'ID_Posting']], on='ID_Posting', how='left')
    merged_df[["ID_CommunityIdentity_x", "VoteNegative", "VotePositive", "ID_CommunityIdentity_y"]].head()

    graph_data = merged_df.groupby(['ID_CommunityIdentity_x', 'ID_CommunityIdentity_y']).agg(
        {'VotePositive': 'sum', 'VoteNegative': 'sum'})
    graph_data = graph_data[:slice]

    if directed:
        G = nx.MultiDiGraph()
    else:
        G = nx.MultiGraph()

    for index, row in graph_data.iterrows():
        user_x = index[0]
        user_y = index[1]
        positive_votes = row['VotePositive']
        negative_votes = row['VoteNegative']

        vote_difference = positive_votes - negative_votes
        G.add_edge(user_x, user_y, weight=vote_difference)

    return G


def graph_user_user(graph_data, directed=False):
    # comment_user_mapping = graph_data[['ID_Posting',
    #                                    'ID_CommunityIdentity']].drop_duplicates().rename(
    #     columns={'ID_Posting': 'Id_posting',
    #              'ID_CommunityIdentity': 'ID_ParentIdentity'})
    #
    # result_df = pd.merge(graph_data, comment_user_mapping, left_on='ID_Posting_Parent', right_on='Id_posting',
    #                      how='left')
    result_df = graph_data[['ID_CommunityIdentity', 'ID_CommunityIdentity_y']]
    reply_counts = result_df.groupby(['ID_CommunityIdentity', 'ID_CommunityIdentity_y']).size().reset_index(
        name='counts')

    reply_counts = reply_counts[:500]

    if directed:
        G = nx.from_pandas_edgelist(reply_counts,
                                    source='ID_CommunityIdentity',
                                    target='ID_ParentIdentity',
                                    edge_attr='counts',
                                    create_using=nx.DiGraph())
    else:
        G = nx.from_pandas_edgelist(reply_counts,
                                    source='ID_CommunityIdentity',
                                    target='ID_CommunityIdentity_y',
                                    edge_attr='counts',
                                    create_using=nx.Graph())

    return G



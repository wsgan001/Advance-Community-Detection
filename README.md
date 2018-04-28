# Advance-Community-Detection
Implementation of novel ideal of "Advancing Community Detection Using Keyword Attribute Search"

Background:
This is an implementation of novel algorithm proposed by us known as, ‘Advancing Community Detection Using Keyword Attribute Search’ (IEEE Access under review), which finds online communities based on the user input query. This novel method finds personalized as well as generalized communities from an attributed graph based on the attribute similarity and connectivity of nodes. This project is an application of this novel algorithm, where we can find the content and extract the knowledge/influence of memes/contents posted by different users in a social network. The outline of this project is as follows:

Dataset:
1.	For this project attibuted social network is considered, where there are multiple attributes on each node of the network and each node is connected to different nodes in the network. 
2.	Since there are few attributed network datasets available, a social network dataset from ‘Stanford Network Analysis Project (SNAP)’ is used. A Facebook dataset which is categorized in different categories based on the Facebook pages is considered for demo of this project. 
3.	Since all these Facebook datasets are unattributed network structures, the random attributes collected for the memes/tweets by different users during the US 2016 election are assigned as attributes of each node in the social network. 
4.	These attributes contain the information about contents posted/shared by different users about Donald Trump and Hillary Clinton. The attributes include the information like Id, candidate, tweets, sentiments about the tweets, confidence value for the sentiment, retweet count, tweet id, and the time tweet created. 
5.	The attributes are assigned randomly so that there is not any bias on the distribution of attributes in the network structure. Also data cleaning like random shuffling of attribute rows, and replacing missing values is done on the attribute dataset. The datasets can be accessed at following links:

SNAP : https://snap.stanford.edu/data/gemsec_facebook_dataset.html
Attribute dataset (Memes): https://www.kaggle.com/SIZZLE/2016electionmemes/data

Project steps:
Following major steps highlight the novel ideal and unexplored facts about this project.

1.	There is no online community detection method available which finds a particular community of users based on the user input query, like, find me a group of people who likes ‘Star Wars’ and lives in Las Vegas. This novel method is able to provide the flexibility of personalized community detection based on such queries.
2.	There are few community detection methods which deals with the attributed social networks. Attributed community detection is not popular yet, but can be useful in many aspects of social network analysis. Hence, the attributed network dataset is synthetically created based on the real world network datasets and attributes. These type of datasets are not easily available on internet, but should be given importance for effective social network analysis. These attributed structures of social network datasets are explored in this project. 
3.	The major aspects of this project are already developed as an experimental analysis of the novel algorithm. The novel method is classifying the nodes and attributes based on the similarity of attributes and connectivity of nodes. The class information is stored in an index structure along with the required information like attributes, first node, and count of the nodes which belong to the same class. 
5.	The novel method is using keyword search technique on graph to derive the community of nodes having the same class label. 

